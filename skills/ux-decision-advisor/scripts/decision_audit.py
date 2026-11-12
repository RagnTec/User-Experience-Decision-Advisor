#!/usr/bin/env python3
"""Check a generic, synthetic-or-private decision record's structural evidence trace.

Read-only, offline, fail-on-error. Prints issue codes and array indices only, never
claim content, input paths, IDs, evidence strings or any personal/project text.
A passing result is NOT verification that a claim or citation is true.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ALLOWED_SOURCES={'USER_PROVIDED','OBSERVED','VERIFIED_EXTERNAL','METHOD_BASED_INFERENCE','ASSUMPTION','UNVERIFIED'}
ALLOWED_STATUS={'SUPPORTED','CONDITIONAL','UNSUPPORTED'}
ALLOWED_ACTIONS={'retain','modify','compare','pilot','defer','stop','escalate'}
MAX_INPUT_BYTES=1_000_000


def scan(obj: object) -> list[str]:
    issues=[]
    if not isinstance(obj,dict):
        return ['RECORD_NOT_OBJECT']
    decision=obj.get('decision')
    if not isinstance(decision,dict):
        return ['DECISION_MISSING']
    if not isinstance(decision.get('question'),str) or not decision['question'].strip():
        issues.append('DECISION_QUESTION_MISSING')
    options=decision.get('options')
    if not isinstance(options,list) or not all(isinstance(v,str) and v.strip() for v in options) or not options:
        issues.append('OPTIONS_MISSING')
    if not isinstance(decision.get('current_action'),str) or decision['current_action'] not in ALLOWED_ACTIONS:
        issues.append('CURRENT_ACTION_INVALID')
    if decision.get('cross_market') is True:
        ms=decision.get('market_scope')
        if not isinstance(ms,dict) or not isinstance(ms.get('markets'),list) or not ms['markets']:
            issues.append('MARKET_SCOPE_MISSING')
        elif not isinstance(ms.get('comparability_note'),str) or not ms['comparability_note'].strip():
            issues.append('MARKET_COMPARABILITY_MISSING')
    claims=obj.get('claims')
    if not isinstance(claims,list):
        return issues+['CLAIMS_NOT_LIST']
    if len(claims)>100:
        issues.append('CLAIMS_TOO_MANY')
    ids=set()
    for i,c in enumerate(claims):
        prefix=f'C{i:03d}_'
        if not isinstance(c,dict):
            issues.append(prefix+'NOT_OBJECT')
            continue
        claim_id=c.get('id')
        if not isinstance(claim_id,str) or not claim_id.strip() or claim_id in ids:
            issues.append(prefix+'ID_INVALID_OR_DUPLICATE')
        if isinstance(claim_id,str):
            ids.add(claim_id)
        if not isinstance(c.get('text'),str) or not c['text'].strip():
            issues.append(prefix+'TEXT_MISSING')
        if not isinstance(c.get('source_type'),str) or c['source_type'] not in ALLOWED_SOURCES:
            issues.append(prefix+'SOURCE_INVALID')
        if not isinstance(c.get('support_status'),str) or c['support_status'] not in ALLOWED_STATUS:
            issues.append(prefix+'SUPPORT_INVALID')
        evidence=c.get('evidence_refs',[])
        if not isinstance(evidence,list) or not all(isinstance(x,str) for x in evidence):
            issues.append(prefix+'REFERENCES_INVALID')
            evidence=[]
        if c.get('source_type') == 'VERIFIED_EXTERNAL' and not any(x.strip() for x in evidence):
            issues.append(prefix+'VERIFIED_WITHOUT_REFERENCE')
        impact=c.get('decision_impact')
        if impact is not None:
            if not isinstance(impact,str) or not impact.strip():
                issues.append(prefix+'IMPACT_INVALID')
            if c.get('support_status') == 'UNSUPPORTED':
                issues.append(prefix+'UNSUPPORTED_DECISION_BASIS')
            if not isinstance(c.get('reversal_condition'),str) or not c.get('reversal_condition','').strip():
                issues.append(prefix+'REVERSAL_MISSING')
        if isinstance(c.get('source_type'),str) and c['source_type'] in {'ASSUMPTION','UNVERIFIED'} and c.get('support_status')=='SUPPORTED':
            issues.append(prefix+'INCONSISTENT_EVIDENCE_LABEL')
    if claims and not any(isinstance(c,dict) and isinstance(c.get('decision_impact'),str) and c['decision_impact'].strip() for c in claims):
        issues.append('NO_DECISION_LINKED_CLAIMS')
    return issues


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True,type=Path)
    args=ap.parse_args()
    p=args.input.resolve(strict=True)
    if p.stat().st_size>MAX_INPUT_BYTES:
        print('DECISION AUDIT: FAIL (FILE_TOO_LARGE)')
        return 1
    # This guard applies to a copy of a publicly installed Skill bundle too.
    for parent in (p.parent,*p.parents):
        if (parent/'PUBLIC_FILE_MANIFEST.json').is_file():
            print('DECISION AUDIT: FAIL (INPUT_INSIDE_PUBLIC_REPOSITORY)')
            return 1
    try:
        issues=scan(json.loads(p.read_text(encoding='utf-8')))
    except (UnicodeDecodeError,json.JSONDecodeError):
        print('DECISION AUDIT: FAIL (INVALID_JSON)')
        return 1
    if issues:
        print(f'DECISION AUDIT: FAIL ({len(issues)} issues)')
        for code in issues:
            print(' -',code)
        return 1
    print('DECISION AUDIT: PASS (structural consistency only; sources and outcomes NOT fact-verified)')
    return 0

if __name__=='__main__': sys.exit(main())
