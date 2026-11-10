#!/usr/bin/env python3
"""Conservative structural lint for a SAVED UXDA Markdown response.

No network or code execution from documents. It checks presentation shape only, not
factual correctness or human authorization. Use on a PRIVATE answer path.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

MAP = re.compile(r'业务推进图|业务推进路线|业务推进流程图')
STAGE = re.compile(r'→|-->|\bflowchart\b|\bgraph TD\b')
STATUS = re.compile(r'已知|待核实|待评估|进行中|当前|已确认|已完成|候选|建议|待推进|可选|规划中')

def check(text: str) -> list[str]:
    """Return coded findings; no assessment of actual law/study validity."""
    findings = []
    cleaned=text.lstrip('\ufeff\n\r\t ')
    # Markdown heading allowed only when it introduces the progress map itself.
    first=cleaned.splitlines()[0].lstrip('#* >') if cleaned else ''
    if not MAP.search(first):
        findings.append('FIRST_BLOCK_NOT_BUSINESS_MAP')
    initial = cleaned[:1600]
    if not STAGE.search(initial):
        findings.append('MISSING_FLOW_OR_STAGE_SEQUENCE')
    if not STATUS.search(initial):
        findings.append('MISSING_PROGRESS_STATUS')
    if not re.search(r'法规|地域|平台|合规|约束',initial):
        findings.append('MISSING_CONSTRAINT_APPLICABILITY_STAGE')
    if not re.search(r'用户|消费者|市场|任务|体验|人因',initial):
        findings.append('MISSING_EXPERIENCE_STAGE')
    if not re.search(r'分析范围|分析方向', initial):
        findings.append('MISSING_ANALYSIS_SCOPE_SELECTOR')
    if not re.search(r'已识别|待确认|已确认|用户确认|确认', initial) or not re.search(r'\b[OEDV]\b',initial):
        findings.append('MISSING_SCOPE_CONFIRMATION_STATUS')
    return findings

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',required=True,type=Path)
    args=ap.parse_args()
    # Caller owns the private file; do not print its content.
    findings=check(args.input.read_text(encoding='utf-8'))
    print(json.dumps({'ok':not findings,'issues':findings},ensure_ascii=False))
    return 0 if not findings else 1
if __name__=='__main__':raise SystemExit(main())
