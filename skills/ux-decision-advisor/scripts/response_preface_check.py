#!/usr/bin/env python3
"""Heuristic presentation lint for a saved UXDA response. Does NOT certify UX correctness.

Default mode = business-first. Use --mode workflow when user explicitly requested a
workflow/route, or --mode legacy for comparison against pre-pilot reports.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

MAP = re.compile(r'业务推进图|业务推进路线|业务推进流程图')
STAGE = re.compile(r'→|-->|\bflowchart\b|\bgraph TD\b')
STATUS = re.compile(r'已知|待核实|待评估|进行中|当前|已确认|已完成|候选|建议|待推进|可选|规划中')
UX = re.compile(r'用户|使用者|受访者|研究|体验|交互|任务|可用性|人因|认知')
JUDGEMENT = re.compile(r'建议|判断|不宜|可以|优先|暂不|需要|适合|不能|风险|证据|假设|问题|结论')
NEXT = re.compile(r'下一步|先|再|核实|验证|复查|观察|比较|条件|待确认|取舍|停止|继续')
ENGINEERING_FIRST = re.compile(r'^(?:[#\s>*-]*)(?:业务推进图|流程图|审计日志|内部状态|JSON Schema|O/E/D/V|S1[–-]S7|技术实现清单)')


def check(text: str, mode: str = 'business') -> list[str]:
    findings=[]
    cleaned=text.lstrip('\ufeff\n\r\t ')
    initial=cleaned[:1600]
    first=cleaned.splitlines()[0].lstrip('#* >') if cleaned else ''
    if mode in ('workflow','legacy'):
        if not MAP.search(first): findings.append('FIRST_BLOCK_NOT_BUSINESS_MAP')
        if not STAGE.search(initial): findings.append('MISSING_FLOW_OR_STAGE_SEQUENCE')
        if not STATUS.search(initial): findings.append('MISSING_PROGRESS_STATUS')
        if mode=='legacy':
            if not re.search(r'法规|地域|平台|合规|约束', initial): findings.append('MISSING_CONSTRAINT_APPLICABILITY_STAGE')
            if not UX.search(initial): findings.append('MISSING_EXPERIENCE_STAGE')
            if not re.search(r'分析范围|分析方向',initial): findings.append('MISSING_ANALYSIS_SCOPE_SELECTOR')
            if not re.search(r'已识别|待确认|已确认|用户确认|确认',initial) or not re.search(r'\b[OEDV]\b',initial): findings.append('MISSING_SCOPE_CONFIRMATION_STATUS')
    else:
        if not cleaned: return ['EMPTY_RESPONSE']
        if ENGINEERING_FIRST.search(first): findings.append('ENGINEERING_INTERNALS_BEFORE_USER_JUDGEMENT')
        if not UX.search(initial): findings.append('MISSING_UX_USER_TASK_CONTEXT')
        if not JUDGEMENT.search(initial): findings.append('MISSING_RESEARCH_JUDGEMENT')
        if not NEXT.search(initial): findings.append('MISSING_NEXT_STEP_OR_CONDITION')
    return findings


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',required=True,type=Path)
    ap.add_argument('--mode',choices=['business','workflow','legacy'],default='business')
    a=ap.parse_args()
    issues=check(a.input.read_text(encoding='utf-8'),a.mode)
    print(json.dumps({'ok':not issues,'mode':a.mode,'issues':issues,'note':'heuristic_only'},ensure_ascii=False))
    return int(bool(issues))
if __name__=='__main__': raise SystemExit(main())
