#!/usr/bin/env python3
"""Local structural check for optional private jurisdiction/norm decision records.

Does not check a statute, verify applicability, or authorize any product change.
Outputs only issue codes and row indexes: no sensitive record contents.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

TYPES = {'BINDING_LAW', 'MANDATORY_STANDARD', 'VOLUNTARY_STANDARD', 'CONTRACT_OR_PLATFORM', 'INDUSTRY_CONVENTION', 'ORGANIZATION_RULE'}
APPLICABILITY = {'APPLIES', 'POSSIBLE', 'NOT_APPLICABLE', 'UNRESOLVED'}
VERIFICATION = {'OFFICIAL_VERIFIED', 'USER_DOCUMENT_ONLY', 'UNVERIFIED'}
ACTIONS = {'FOLLOW', 'VERIFY', 'PROPOSE_DEVIATION', 'ESCALATE', 'REDESIGN', 'STOP'}
REVIEW = {'NOT_REQUESTED', 'PENDING', 'APPROVED', 'REJECTED'}
STAGES = {'EXPLORATION_ONLY', 'CONDITIONAL_RECOMMENDATION', 'HOLD_FOR_SPECIALIST', 'READY_FOR_HUMAN_DECISION', 'STOP_CONFLICT'}


def audit(data: object) -> list[str]:
    issues = []
    if not isinstance(data, dict):
        return ['ROOT_NOT_OBJECT']
    scope = data.get('scope')
    if not isinstance(scope, dict):
        issues.append('SCOPE_MISSING')
        scope = {}
    places = scope.get('jurisdictions')
    if not isinstance(places, list) or not places or not all(isinstance(p, str) and p.strip() for p in places):
        issues.append('SCOPE_JURISDICTION_UNRESOLVED')
    for k in ('product_category', 'stage'):
        if not isinstance(scope.get(k), str) or not scope[k].strip():
            issues.append(f'SCOPE_{k.upper()}_MISSING')
    constraints = data.get('constraints')
    if not isinstance(constraints, list):
        issues.append('CONSTRAINTS_NOT_ARRAY')
        constraints = []
    ids = set()
    requires_escalation = False
    for i, c in enumerate(constraints):
        pfx = f'CONSTRAINT_{i}_'
        if not isinstance(c, dict):
            issues.append(pfx + 'NOT_OBJECT')
            continue
        ident = c.get('id')
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            issues.append(pfx + 'INVALID_ID')
        else:
            ids.add(ident)
        cat, app, ver, act = (c.get('category'), c.get('applicability'), c.get('verification'), c.get('proposed_action'))
        if cat not in TYPES: issues.append(pfx + 'UNKNOWN_CATEGORY')
        if app not in APPLICABILITY: issues.append(pfx + 'UNKNOWN_APPLICABILITY')
        if ver not in VERIFICATION: issues.append(pfx + 'UNKNOWN_VERIFICATION')
        if act not in ACTIONS: issues.append(pfx + 'UNKNOWN_ACTION')
        review = c.get('human_review')
        if not isinstance(review, dict):
            issues.append(pfx + 'HUMAN_REVIEW_MISSING')
            review = {}
        if review.get('status') not in REVIEW:
            issues.append(pfx + 'UNKNOWN_REVIEW_STATUS')
        if review.get('status') == 'APPROVED' and not str(review.get('role', '')).strip():
            issues.append(pfx + 'APPROVAL_ROLE_MISSING')
        if ver == 'OFFICIAL_VERIFIED' and (not str(c.get('source_ref','')).strip() or not str(c.get('version_or_date','')).strip()):
            issues.append(pfx + 'OFFICIAL_SOURCE_DETAILS_MISSING')
        if cat in {'BINDING_LAW', 'MANDATORY_STANDARD'}:
            if act == 'PROPOSE_DEVIATION':
                issues.append(pfx + 'BINDING_REQUIREMENT_NOT_WAIVABLE_BY_APPROVAL')
            if app != 'NOT_APPLICABLE' and (app != 'APPLIES' or ver != 'OFFICIAL_VERIFIED' or act in {'VERIFY', 'ESCALATE', 'STOP', 'REDESIGN'}):
                requires_escalation = True
        if cat in {'INDUSTRY_CONVENTION', 'VOLUNTARY_STANDARD', 'CONTRACT_OR_PLATFORM', 'ORGANIZATION_RULE'} and act == 'PROPOSE_DEVIATION':
            if review.get('status') != 'APPROVED':
                requires_escalation = True
            if review.get('status') == 'NOT_REQUESTED':
                issues.append(pfx + 'DEVIATION_REQUIRES_HUMAN_REVIEW')
        if app in {'POSSIBLE', 'UNRESOLVED'} and cat in {'BINDING_LAW', 'MANDATORY_STANDARD'}:
            requires_escalation = True
    dec = data.get('decision')
    if not isinstance(dec, dict):
        issues.append('DECISION_MISSING')
        dec = {}
    stage = dec.get('stage')
    if stage not in STAGES:
        issues.append('DECISION_STAGE_INVALID')
    if dec.get('implementation_authorized') is not False:
        issues.append('AGENT_MUST_NOT_AUTHORIZE_IMPLEMENTATION')
    if dec.get('claim_of_compliance') is not False:
        issues.append('AGENT_MUST_NOT_DECLARE_COMPLIANCE')
    if requires_escalation and stage == 'READY_FOR_HUMAN_DECISION':
        issues.append('UNRESOLVED_GATE_REQUIRES_CONDITIONAL_OR_SPECIALIST_STAGE')
    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path, required=True)
    args = ap.parse_args()
    try:
        record = json.loads(args.input.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError):
        print(json.dumps({'ok': False, 'issues': ['INPUT_UNREADABLE_OR_INVALID_JSON']}, ensure_ascii=False))
        return 1
    issues = audit(record)
    print(json.dumps({'ok': not bool(issues), 'issues': issues}, ensure_ascii=False))
    return 1 if issues else 0


if __name__ == '__main__':
    raise SystemExit(main())
