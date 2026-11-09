#!/usr/bin/env python3
"""Local fail-closed *structural* audit for source provenance and D/E closure.

Private case text is read in memory; no network operations and no storage of case text.
The script cannot verify a legal claim is correct or that a source was truly accessed.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

STANDARD_RE = re.compile(r'(?<![\w/])(?:GB\s*/\s*T|GB|ISO)\s*[0-9]{4,6}(?:\s*[-—–:]\s*[0-9]{2,5})?(?!\w)', re.I)
STRONG_CLAIM = re.compile(r'(?:违法|触犯|违反|严禁|明令禁止|必须|一律|直接(?:拒审|下架|否决)|强制(?:性)?要求|强标底线|完全规避|合规无硬伤|唯(?:一|有).*可行)')
UNVERIFIED_MARKER = re.compile(r'(?:待核实|未经核实|尚未核实|未完成核验|未查询|仅作为待核验条目|未进行外部核验)')
OFFICIAL = {'VERIFIED_OFFICIAL'}
USER_DOC = {'USER_DOCUMENT'}
UNVERIFIED = {'MODEL_KNOWLEDGE_UNVERIFIED','UNVERIFIED'}
ALLOWED = OFFICIAL | USER_DOC | UNVERIFIED


def norm_id(value: str) -> str:
    return re.sub(r'\s+', '', value).replace('—', '-').replace('–', '-').upper()


def load_sources(path: Path | None) -> dict[str, dict]:
    if path is None: return {}
    raw=json.loads(path.read_text(encoding='utf-8'))
    entries=raw.get('sources', [])
    if not isinstance(entries, list): raise ValueError('sources must be a list')
    out={}
    for x in entries:
        if not isinstance(x, dict) or not isinstance(x.get('id'),str):
            raise ValueError('each source must have an id')
        key=norm_id(x['id'])
        if key in out:raise ValueError('duplicate source id')
        out[key]=x
    return out


def inspect(text: str, sources: dict[str,dict], mode: str) -> list[str]:
    issues=[]
    lines=text.splitlines()
    for n,line in enumerate(lines,1):
        for match in STANDARD_RE.finditer(line):
            name=norm_id(match.group())
            entry=sources.get(name)
            if entry is None:
                issues.append(f'UNRECORDED_STANDARD line={n} id={name}')
                continue
            status=entry.get('status')
            if status not in ALLOWED:
                issues.append(f'BAD_SOURCE_STATUS line={n} id={name}')
                continue
            if status in OFFICIAL:
                if not str(entry.get('official_url','')).startswith('https://') or not entry.get('checked_on') or not entry.get('scope') or not entry.get('provision_locator'):
                    issues.append(f'INCOMPLETE_OFFICIAL_SOURCE line={n} id={name}')
            if status in USER_DOC:
                if not entry.get('document_anchor') or not entry.get('document_version'):
                    issues.append(f'INCOMPLETE_USER_DOCUMENT line={n} id={name}')
            if status in UNVERIFIED:
                if STRONG_CLAIM.search(line):
                    issues.append(f'UNVERIFIED_MANDATORY_CLAIM line={n} id={name}')
                elif not UNVERIFIED_MARKER.search(line):
                    issues.append(f'UNVERIFIED_UNMARKED line={n} id={name}')
    if mode in ('DE','D','E'):
        nonblank=next((line.strip().lstrip('#* ').strip() for line in lines if line.strip()),'')
        if not nonblank.startswith('业务推进图'):
            issues.append('MISSING_FIRST_SCREEN_MAP')
        req={
         'DECISION_STATE':re.compile(r'阶段性决策|当前决策|当前建议|决策状态|建议(?:暂缓|保留|比较|试点)'),
         'UX_MECHANISM':re.compile(r'用户体验|用户任务|感知|控制感|预期|可预测|中断|错误恢复|信任'),
         'NEXT_ACTION':re.compile(r'下一步|后续计划|下一轮|后续行动'),
         'OPTIONAL_USER_INPUT':re.compile(r'可补充|补充资料|可以提供|可提供|如有.*(?:VOC|资料|日志|数据)|待补信息'),
         'REVERSAL_TRIGGER':re.compile(r'逆转条件|改变(?:当前)?(?:判断|结论|选择|建议)|重新评估|会推翻'),
         'ACCOUNTABILITY':re.compile(r'责任|负责|交由|专业复核|业务确认|法务|合规|研发|产品团队'),
        }
        for k,rx in req.items():
            if not rx.search(text):issues.append('MISSING_'+k)
    return sorted(set(issues))


def main() -> int:
    ap=argparse.ArgumentParser(description='Structural checks only; no web calls')
    ap.add_argument('--response',type=Path,required=True)
    ap.add_argument('--evidence',type=Path,help='Local private source ledger JSON')
    ap.add_argument('--mode',choices=['D','E','DE','OTHER'],default='DE')
    ap.add_argument('--citation-ledger',type=Path,help='Optional private formal-claim and source ledger')
    ap.add_argument('--private-root',type=Path,help='Authorized private project folder')
    args=ap.parse_args()
    try:
        report_text=args.response.read_text(encoding='utf-8')
        issues=inspect(report_text,load_sources(args.evidence),args.mode)
        if args.citation_ledger:
            from citation_integrity import inspect as inspect_citations
            issues.extend(inspect_citations(report_text,json.loads(args.citation_ledger.read_text(encoding='utf-8')),private_root=args.private_root))
        elif '[SRC:' in report_text:
            issues.append('CITATIONS_PRESENT_BUT_PRIVATE_LEDGER_NOT_SUPPLIED')
        issues=sorted(set(issues))
        print(json.dumps({'ok':not bool(issues),'issues':issues,'note':'Only structural lint; cannot verify legal applicability, accessed provenance or true UX effects'},ensure_ascii=False,indent=2))
        return 1 if issues else 0
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as e:
        print(json.dumps({'ok':False,'issues':[f'INPUT_ERROR {type(e).__name__}'],'note':'Private case content not echoed'},ensure_ascii=False))
        return 2

if __name__=='__main__':raise SystemExit(main())
