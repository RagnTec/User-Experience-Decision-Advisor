#!/usr/bin/env python3
"""Offline structural audit of evidence modes and conversation/project boundary.

This tool does not access the network, check whether links were visited, assess
legal applicability, or establish truth. It does not print project content.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

NETWORK_MODES = {'OFFLINE', 'ONLINE_AVAILABLE_UNUSED', 'ONLINE_USED'}
STATUSES = {
    'LOCAL_DOCUMENT', 'USER_STATED', 'DETERMINISTIC_RESULT',
    'METHODOLOGICAL_INFERENCE', 'MODEL_BACKGROUND_UNVERIFIED',
    'HYPOTHESIS', 'UNKNOWN', 'CURRENT_EXTERNAL_VERIFIED',
}
SENSITIVE_CLAIMS = {'LEGAL', 'STANDARD', 'MARKET_STATISTIC', 'CURRENT_COMPETITOR', 'QUANTITATIVE_EFFECT'}
AUTHORITY_TYPES = {'OFFICIAL', 'PRIMARY_STUDY', 'FIRST_PARTY_PRODUCT', 'SECONDARY', 'OTHER'}
LEARNING_INTENTS = {'EXPLAIN_METHOD', 'PRACTICE_OR_EXAMPLE', 'AUDIT_REASONING', 'RETURN_TO_PROJECT'}
PROJECT_EVENTS = {'NONE', 'SCOPE_CHANGE', 'EVIDENCE_UPDATE', 'DECISION_UPDATE', 'CORRECTION'}


def is_iso_date(s: object) -> bool:
    if not isinstance(s, str) or not s.strip():
        return False
    try:
        dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False


def is_https_url(s: object) -> bool:
    if not isinstance(s, str):
        return False
    try:
        p = urlsplit(s)
        return p.scheme == 'https' and bool(p.hostname) and not p.username and not p.password
    except ValueError:
        return False


def present(o: dict, key: str) -> bool:
    return isinstance(o.get(key), str) and bool(o[key].strip())


def audit(data: object) -> list[str]:
    issues: list[str] = []
    if not isinstance(data, dict):
        return ['BAD_RECORD']
    mode = data.get('network_mode')
    searched = data.get('external_search_performed')
    forbids = data.get('user_forbids_network', False)
    if mode not in NETWORK_MODES:
        issues.append('BAD_NETWORK_MODE')
    if type(searched) is not bool or type(forbids) is not bool:
        issues.append('BAD_NETWORK_FLAGS')
    else:
        if bool(searched) != (mode == 'ONLINE_USED'):
            issues.append('MODE_SEARCH_MISMATCH')
        if forbids and searched:
            issues.append('FORBIDDEN_NETWORK_USE')
    sources = data.get('sources', [])
    claims = data.get('claims', [])
    if not isinstance(sources, list) or not isinstance(claims, list):
        return sorted(set(issues + ['BAD_SOURCES_OR_CLAIMS']))
    byid: dict[str, dict] = {}
    for source in sources:
        if not isinstance(source, dict) or not present(source, 'id') or source['id'] in byid:
            issues.append('BAD_OR_DUPLICATE_SOURCE_ID')
            continue
        sid = source['id']
        byid[sid] = source
        kind = source.get('kind')
        if kind == 'LOCAL_DOCUMENT':
            if not present(source, 'locator'):
                issues.append('LOCAL_SOURCE_MISSING_LOCATOR')
        elif kind == 'CURRENT_EXTERNAL':
            if source.get('authority_type') not in AUTHORITY_TYPES:
                issues.append('EXTERNAL_SOURCE_MISSING_AUTHORITY_CLASS')
            for field in ('publisher', 'locator', 'applicability', 'retrieval_record'):
                if not present(source, field):
                    issues.append('EXTERNAL_SOURCE_MISSING_' + field.upper())
            if not is_iso_date(source.get('retrieved_at')):
                issues.append('EXTERNAL_SOURCE_BAD_RETRIEVAL_DATE')
            if not is_https_url(source.get('url')):
                issues.append('EXTERNAL_SOURCE_BAD_URL')
            if mode != 'ONLINE_USED' or searched is not True:
                issues.append('EXTERNAL_SOURCE_WITHOUT_LOOKUP')
        else:
            issues.append('BAD_SOURCE_KIND')
    known_ids: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict) or not present(claim, 'id') or claim['id'] in known_ids:
            issues.append('BAD_OR_DUPLICATE_CLAIM_ID')
            continue
        known_ids.add(claim['id'])
        status = claim.get('status')
        kind = claim.get('claim_type')
        strength = claim.get('decision_strength')
        refs = claim.get('source_refs', [])
        if status not in STATUSES:
            issues.append('BAD_CLAIM_STATUS')
        if strength not in {'FINAL', 'PROVISIONAL'}:
            issues.append('BAD_DECISION_STRENGTH')
        if not isinstance(refs, list) or any(not isinstance(r, str) for r in refs):
            issues.append('BAD_SOURCE_REFS')
            refs = []
        for r in refs:
            if r not in byid:
                issues.append('UNKNOWN_SOURCE_REFERENCE')
        if status == 'LOCAL_DOCUMENT' and not any(byid.get(r, {}).get('kind') == 'LOCAL_DOCUMENT' for r in refs):
            issues.append('LOCAL_CLAIM_WITHOUT_DOCUMENT')
        if status == 'CURRENT_EXTERNAL_VERIFIED':
            if mode != 'ONLINE_USED' or searched is not True:
                issues.append('FAKE_ONLINE_VERIFICATION')
            if not any(byid.get(r, {}).get('kind') == 'CURRENT_EXTERNAL' for r in refs):
                issues.append('VERIFIED_CLAIM_MISSING_RETRIEVED_SOURCE')
        if strength == 'FINAL' and status in {'UNKNOWN', 'HYPOTHESIS', 'MODEL_BACKGROUND_UNVERIFIED', 'METHODOLOGICAL_INFERENCE'}:
            issues.append('UNVERIFIED_FINAL_DECISION')
        if kind in SENSITIVE_CLAIMS and strength == 'FINAL':
            if status not in {'CURRENT_EXTERNAL_VERIFIED', 'DETERMINISTIC_RESULT'}:
                issues.append('SENSITIVE_FINAL_WITHOUT_VERIFICATION')
            if not present(claim, 'applicability'):
                issues.append('SENSITIVE_FINAL_MISSING_APPLICABILITY')
            if status == 'CURRENT_EXTERNAL_VERIFIED' and kind in {'LEGAL', 'STANDARD'}:
                if not any(byid.get(r, {}).get('authority_type') == 'OFFICIAL' for r in refs):
                    issues.append('NORMATIVE_FINAL_WITHOUT_OFFICIAL_SOURCE')
            if status == 'CURRENT_EXTERNAL_VERIFIED' and kind in {'MARKET_STATISTIC', 'QUANTITATIVE_EFFECT'}:
                if not any(byid.get(r, {}).get('authority_type') in {'OFFICIAL', 'PRIMARY_STUDY'} for r in refs):
                    issues.append('EMPIRICAL_FINAL_WITHOUT_PRIMARY_SOURCE')
            if status == 'CURRENT_EXTERNAL_VERIFIED' and kind == 'CURRENT_COMPETITOR':
                if not any(byid.get(r, {}).get('authority_type') in {'OFFICIAL', 'FIRST_PARTY_PRODUCT'} for r in refs):
                    issues.append('COMPETITOR_FINAL_WITHOUT_DIRECT_SOURCE')
        if status == 'DETERMINISTIC_RESULT' and not present(claim, 'calculation_ref'):
            issues.append('COMPUTATION_WITHOUT_REPRODUCTION_REF')
        if status == 'CURRENT_EXTERNAL_VERIFIED' and strength == 'FINAL':
            if not present(claim, 'crosscheck_ref') and not present(claim, 'single_source_limitation'):
                issues.append('CRITICAL_CLAIM_NO_CROSSCHECK_STATUS')
    interaction = data.get('interaction')
    if interaction is not None:
        if not isinstance(interaction, dict):
            issues.append('BAD_INTERACTION')
        else:
            intent = interaction.get('intent')
            event = interaction.get('project_event')
            approved = interaction.get('explicit_user_authorization')
            if intent not in LEARNING_INTENTS | {'PROJECT_ADVANCE'} or event not in PROJECT_EVENTS or type(approved) is not bool:
                issues.append('BAD_INTERACTION_FIELDS')
            else:
                if intent in LEARNING_INTENTS and event in {'SCOPE_CHANGE', 'EVIDENCE_UPDATE', 'DECISION_UPDATE'}:
                    issues.append('LEARNING_CHANGED_PROJECT')
                if event == 'SCOPE_CHANGE' and not approved:
                    issues.append('UNAUTHORIZED_SCOPE_CHANGE')
                if event == 'CORRECTION' and not present(interaction, 'correction_ref'):
                    issues.append('UNTRACED_CORRECTION')
    return sorted(set(issues))


def main() -> int:
    ap = argparse.ArgumentParser(description='Offline metadata consistency check, not factual source verification')
    ap.add_argument('--input', type=Path, required=True)
    args = ap.parse_args()
    try:
        result = audit(json.loads(args.input.read_text(encoding='utf-8')))
    except (OSError, ValueError, UnicodeError):
        print(json.dumps({'ok': False, 'issues': ['UNREADABLE_OR_INVALID_RECORD']}, ensure_ascii=False))
        return 2
    print(json.dumps({'ok': not result, 'issues': result, 'issues_count': len(result)}, ensure_ascii=False))
    return 1 if result else 0


if __name__ == '__main__':
    sys.exit(main())
