#!/usr/bin/env python3
"""Advisory, offline-only structural O/E review. Does not determine truth or legality.

Never echoes private text, never reads public or private workspaces automatically.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

NUMERIC = re.compile(r'(?:\b\d+(?:\.\d+)?\s*%|\b\d+(?:\.\d+)?\s*(?:厘米|米|分钟|小时|kg|cm)\b)', re.I)
EVIDENCE_MARK = re.compile(r'已(?:实测|验证|核验)|来源|用户提供|参考|据[^，。；]*?数据|示例|假设|候选|待(?:验证|确认|核实)|未经核实|模拟|非实际|样例|\[[A-Za-z]\d+\]|<Cite',re.I)
TECH_PRIORITY = re.compile(r'\bP[012]\b.{0,10}(?:必做|优先|启动|排期|落地)|(?:必做项|开发优先级)[：:]',re.I)
DECISION_APPROVAL = re.compile(r'(?:顶层方案(?:路线)?决策|产品方案(?:路线)?决策|D[^\n]{0,15}决策)[^\n]{0,8}(?:已完成|已批准|已确认)',re.I)
O_E_OUT = re.compile(r'(?:##?\s*(?:O|E)\s*[｜|])|(?:机会|体验|人因|风险)',re.I)
END_RESEARCH = re.compile(r'可补充|可提供|现有资料|可选资料|补充资料|如有.*(?:数据|资料|VOC)|下一轮.*(?:资料|数据|用户输入)|下一步.*(?:资料|数据)')
DECISION_LINK = re.compile(r'决策|方案选择|判断|对后续.*(?:选择|方案)|影响.*(?:取舍|选择)')
CLOSING_RESEARCH = re.compile(r'可补充|可提供|用户(?:可以|可选择|明确选择)|继续\s*O(?:\+|/|与)E|选择.*(?:补充|继续|停止|不提供)|下轮.*(?:资料|验证|判断)|研究.*(?:结论|证据)|改变.*判断|逆转条件|现有资料')
REVERSAL = re.compile(r'逆转|推翻|反例|不成立|改变.*(?:判断|结论|选择)|若.*则|条件')


def audit(text: str, *, scope: str = 'OE', approval_evidence: bool = False) -> list[str]:
    issues=[]
    first=next((x.strip().lstrip('#* ').strip() for x in text.splitlines() if x.strip()),'')
    if not first.startswith('业务推进图'):
        issues.append('MISSING_FIRST_SCREEN_MAP')
    if '分析范围' not in text:
        issues.append('MISSING_CONFIRMED_SCOPE')
    if not O_E_OUT.search(text):
        issues.append('MISSING_RESEARCH_ASSESSMENT')
    if not DECISION_LINK.search(text):
        issues.append('MISSING_DECISION_LINK')
    if not END_RESEARCH.search(text):
        issues.append('MISSING_OPTIONAL_RESEARCH_OR_SOURCE_CONTINUATION')
    if not REVERSAL.search(text):
        issues.append('MISSING_COUNTERCASE_OR_REVERSAL')
    # Inspect the last substantive section, not an earlier optional-input mention.
    blocks=re.split(r'(?m)^#{2,3}\s+', text)
    tail=blocks[-1] if len(blocks)>1 else '\n'.join([t.strip() for t in text.splitlines() if t.strip()][-3:])
    if not CLOSING_RESEARCH.search(tail):
        issues.append('MISSING_RESEARCH_CLOSING_AT_END')
    for n,line in enumerate(text.splitlines(),1):
        if not approval_evidence and DECISION_APPROVAL.search(line):
            issues.append(f'PREMATURE_DECISION_APPROVAL line={n}')
        if scope.upper() in ('O','E','OE','EO') and TECH_PRIORITY.search(line):
            issues.append(f'UNAUTHORIZED_ROADMAP_PRIORITY line={n}')
        if NUMERIC.search(line) and not EVIDENCE_MARK.search(line):
            # This is an advisory: exact quantities may be provided elsewhere in a verified source ledger.
            issues.append(f'QUANTITATIVE_CLAIM_NEEDS_TRACE line={n}')
    return sorted(set(issues))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--response',required=True,type=Path)
    ap.add_argument('--scope',default='OE',choices=['O','E','OE','D','V'])
    ap.add_argument('--approved-by-user',action='store_true',help='Only if a recorded explicit business approval exists')
    a=ap.parse_args()
    try:
        problems=audit(a.response.read_text(encoding='utf-8'),scope=a.scope,approval_evidence=a.approved_by_user)
        print(json.dumps({'ok':not bool(problems),'issues':problems,'note':'Offline structural preflight only. Does not verify evidence, user approval or domain safety. No private content echoed.'},ensure_ascii=False,indent=2))
        return 1 if problems else 0
    except (OSError,UnicodeError) as e:
        print(json.dumps({'ok':False,'issues':[f'INPUT_ERROR {type(e).__name__}']},ensure_ascii=False))
        return 2
if __name__=='__main__': raise SystemExit(main())
