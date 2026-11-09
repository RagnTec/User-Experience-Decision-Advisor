#!/usr/bin/env python3
"""Generate an offline, self-contained UX decision report from UTF-8 JSON.

No imports beyond stdlib, no network access, no storage or telemetry.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SHELL = BASE / 'assets' / 'report-shell.html'
REQUIRED = {'title', 'recommendation', 'next_step'}
COLLECTIONS = {'decision_options', 'journey', 'findings', 'evidence', 'opportunities', 'scenario_path'}


def validate(payload: object) -> dict:
    if not isinstance(payload, dict):
        raise ValueError('Input must be an object.')
    missing = [k for k in sorted(REQUIRED) if not isinstance(payload.get(k), str) or not payload[k].strip()]
    if missing:
        raise ValueError('Required nonempty strings: ' + ', '.join(missing))
    for key in COLLECTIONS:
        val = payload.get(key, [])
        if not isinstance(val, list) or any(not isinstance(v, dict) for v in val):
            raise ValueError(f'{key} must be a list of objects')
        if len(val) > 40:
            raise ValueError(f'{key} has too many records (max 40)')
    # Strict report-link policy: a URL alone is never treated as a verified citation.
    # Legacy reports without evidence URLs remain compatible; inaccurate links fail closed.
    from urllib.parse import urlsplit
    for row in payload.get('evidence', []):
        if 'url' not in row or not row.get('url'):
            continue
        url = row['url']
        parsed = urlsplit(url) if isinstance(url,str) else None
        if (parsed is None or parsed.scheme!='https' or not parsed.hostname
            or parsed.hostname.lower() in ('example.com','example.org','example.net','localhost')
            or parsed.hostname.lower().endswith(('.invalid','.local','.internal'))):
            raise ValueError('UNVERIFIABLE_OR_PLACEHOLDER_EVIDENCE_URL')
        needed=('source_status','source_title','source_publisher','source_locator','source_retrieval_ref','support_excerpt')
        if (row.get('source_status')!='CONTENT_INSPECTED'
            or any(not isinstance(row.get(k),str) or not row[k].strip() for k in needed)):
            raise ValueError('EVIDENCE_URL_WITHOUT_INSPECTION_RECORD')
    research = payload.get('research_summary')
    if research is not None:
        if not isinstance(research, dict):
            raise ValueError('research_summary must be an object')
        for key in ('mechanism', 'evidence_status', 'decision_condition'):
            if not isinstance(research.get(key), str) or not research[key].strip():
                raise ValueError(f'research_summary.{key} requires a nonempty statement')
        if research.get('mechanism_status') not in ('observed','supported','hypothesis','unknown'):
            raise ValueError('research_summary.mechanism_status must be observed/supported/hypothesis/unknown')
        for key in ('focus',):
            if key in research and not isinstance(research[key], str):
                raise ValueError(f'research_summary.{key} must be a string')
    workflow = payload.get('workflow_map')
    if workflow is not None:
        if not isinstance(workflow, dict) or not isinstance(workflow.get('objective'), str) or not workflow['objective'].strip():
            raise ValueError('workflow_map.objective required')
        if type(workflow.get('revision')) is not int or workflow['revision'] < 0:
            raise ValueError('workflow_map.revision invalid')
        nodes = workflow.get('steps')
        if not isinstance(nodes, list) or not 1 <= len(nodes) <= 12:
            raise ValueError('workflow_map.steps must have 1-12 rows')
        ids = set()
        for node in nodes:
            if not isinstance(node, dict) or not isinstance(node.get('id'),str) or not node['id'].strip() or node['id'] in ids:
                raise ValueError('workflow_map step id invalid or duplicated')
            ids.add(node['id'])
            if not isinstance(node.get('title'), str) or not node['title'].strip():
                raise ValueError('workflow_map step title required')
            if node.get('state') not in ('candidate','ready','active','completed','blocked','paused','skipped'):
                raise ValueError('workflow_map step state invalid')
            if type(node.get('confirmed')) is not bool:
                raise ValueError('workflow_map step confirmed boolean required')
            if node['state']=='candidate' and node['confirmed']:
                raise ValueError('workflow_map candidate cannot be confirmed')
            if node['state']=='completed' and not node.get('evidence_refs'):
                raise ValueError('workflow_map completed requires evidence references')
        if workflow.get('current_step') not in ids:
            raise ValueError('workflow_map.current_step invalid')
        scope=workflow.get('analysis_scope')
        if scope is not None:
            if (not isinstance(scope,dict) or type(scope.get('confirmed')) is not bool
                or not isinstance(scope.get('detected'),list) or not isinstance(scope.get('selected'),list)
                or any(mode not in {'O','E','D','V'} for mode in scope['detected']+scope['selected'])
                or len(set(scope['selected']))!=len(scope['selected'])):
                raise ValueError('workflow_map.analysis_scope invalid')
            if not scope['confirmed'] or not scope['selected']:
                raise ValueError('UNCONFIRMED_ANALYSIS_SCOPE_CANNOT_RENDER_FULL_REPORT')
            selected=set(scope['selected'])
            content_modes={}
            if payload.get('decision_options'):content_modes['D']='decision_options'
            if payload.get('journey') or payload.get('findings'):content_modes['E']='journey/findings'
            if payload.get('opportunities') or payload.get('scenario_path') or payload.get('problem_reframe'):content_modes['O']='opportunities/scenario_path'
            if payload.get('validation'):content_modes['V']='validation'
            for mode, field in content_modes.items():
                if mode not in selected:
                    raise ValueError(f'UNAUTHORIZED_ANALYSIS_SECTION_{mode}: {field}')
            requested=payload.get('analysis_mode')
            if requested in ('O','E','D','V') and requested not in selected:
                raise ValueError('UNAUTHORIZED_DEFAULT_VIEW')
            if requested=='both' and not {'D','E'}.issubset(selected):
                raise ValueError('UNAUTHORIZED_COMBINED_VIEW')
            if requested=='all' and selected!={'O','E','D','V'}:
                raise ValueError('UNAUTHORIZED_ALL_VIEW')

    if payload.get('validation') is not None and not isinstance(payload['validation'], dict):
        raise ValueError('validation must be an object')
    v = payload.get('validation')
    if isinstance(v, dict):
        if v.get('evidence_origin') not in ('synthetic', 'respondent_observed', 'administrative', 'unknown'):
            raise ValueError('validation.evidence_origin required')
        if v.get('update_status') not in ('UPHOLDS', 'QUALIFIES', 'CHANGES', 'DOES_NOT_RESOLVE'):
            raise ValueError('validation.update_status required')
        if not isinstance(v.get('boundary'), str) or len(v['boundary'].strip()) < 12:
            raise ValueError('validation.boundary required')
        for k in ('task_outcomes', 'themes'):
            if k in v and (not isinstance(v[k], list) or len(v[k]) > 40):
                raise ValueError(f'validation.{k} must be <=40 rows')
        for row in v.get('task_outcomes', []):
            if not isinstance(row,dict) or not isinstance(row.get('label'),str) or not row['label'].strip():
                raise ValueError('Task outcome needs a label')
            n, rate = row.get('n'), row.get('success_pct')
            if type(n) is not int or n <= 0 or type(rate) not in (int,float) or not math.isfinite(rate) or not (0<=rate<=100):
                raise ValueError('Task outcome requires valid n and percentage')
        if v.get('task_outcomes') and not isinstance(v.get('quant_note'),str):
            raise ValueError('Task results require quant_note with denominator and scope')
        for row in v.get('themes', []):
            if not isinstance(row,dict) or not isinstance(row.get('code'),str) or not row['code'].strip():
                raise ValueError('Coded theme needs name')
            m, n = row.get('mentions'), row.get('respondents')
            if type(m) is not int or type(n) is not int or m<0 or n<0 or n>m:
                raise ValueError('Coded theme counts invalid')
    if not (payload.get('decision_options') or payload.get('journey') or payload.get('findings') or payload.get('opportunities') or payload.get('validation')):
        raise ValueError('At least one analysis section is required (D/E/O/V)')
    return payload


def render(payload: dict) -> str:
    template = SHELL.read_text(encoding='utf-8')
    data = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    # Script-json injection must never terminate the script element.
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    if template.count('__JSON_DATA__') != 1:
        raise ValueError('Template marker invalid')
    return template.replace('__JSON_DATA__', data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    # A report may embed private case facts even if source templates are public.
    # Never write user-derived reports into a published Skill or public source repo.
    out = args.output.resolve()
    source_skill = BASE.resolve()
    if out == source_skill or source_skill in out.parents:
        raise ValueError('Report output cannot be written inside installed/public Skill sources')
    for folder in (out.parent, *out.parents):
        if (folder / 'PUBLIC_FILE_MANIFEST.json').exists():
            raise ValueError('Report output cannot be written inside a public-source repository')
    payload = validate(json.loads(args.input.read_text(encoding='utf-8')))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(payload), encoding='utf-8')
    print(f'Wrote {args.output} ({args.output.stat().st_size} bytes)')

if __name__ == '__main__':
    main()
