#!/usr/bin/env python3
"""Append a REVIEWED round to a private spiral ledger, preserving prior rounds.

Optionally require source-hash/action agreement with a V decision-update artifact.
This appends provenance; it does not infer or choose actions automatically.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3] if HERE.parents[2].name == "skills" else HERE.parents[2]
MOD=Path(__file__).with_name('spiral_audit.py')
spec=importlib.util.spec_from_file_location('uxda_spiral_audit',MOD)
auditor=importlib.util.module_from_spec(spec)
spec.loader.exec_module(auditor)


def private_file(p:Path)->Path:
    q=p.expanduser().resolve()
    if ROOT.resolve() in (q,*q.parents) or any((parent/'.git').exists() or (parent/'PUBLIC_FILE_MANIFEST.json').exists() for parent in (q.parent,*q.parents)):
        raise ValueError('PRIVATE_PATH_REQUIRED')
    return q


def append(ledger, new_round, v_record=None):
    if not isinstance(new_round,dict):raise ValueError('ROUND_OBJECT_REQUIRED')
    if not isinstance(ledger,dict) or not isinstance(ledger.get('rounds'),list) or not ledger['rounds']:
        raise ValueError('BASE_LEDGER_REQUIRED')
    last=ledger['rounds'][-1]
    if last.get('next_step',{}).get('type')=='HANDOFF':
        raise ValueError('PREVIOUS_HANDOFF_IS_TERMINAL_START_NEW_DECISION_OR_EXPLICITLY_REOPEN')
    if new_round.get('round')!=len(ledger['rounds'])+1:
        raise ValueError('ROUND_INDEX_MISMATCH')
    if v_record is not None:
        if v_record.get('decision_id') != ledger.get('decision_id'):
            raise ValueError('V_DECISION_ID_MISMATCH')
        if v_record.get('previous_action') != last.get('decision',{}).get('action'):
            raise ValueError('V_PREVIOUS_ACTION_MISMATCH')
        if v_record.get('current_action') != new_round.get('decision',{}).get('action'):
            raise ValueError('V_CURRENT_ACTION_MISMATCH')
        if (ledger.get('data_origin')=='synthetic') != (v_record.get('data_origin')=='synthetic'):
            raise ValueError('V_DATA_ORIGIN_MISMATCH')
        expected=v_record.get('source_hashes',{}).get('analysis_sha256')
        if not expected or not any(e.get('sha256')==expected and e.get('role')=='analysis_result' for e in new_round.get('evidence',[])):
            raise ValueError('V_ANALYSIS_DIGEST_NOT_LINKED')
    obj={**ledger,'rounds':[*ledger['rounds'],new_round]}
    problems=auditor.audit(obj)
    if problems:
        # No source text is echoed to stdout/stderr.
        raise ValueError('SPIRAL_AUDIT_FAILED: '+','.join(sorted({p['code'] for p in problems})))
    return obj


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ledger',type=Path,required=True)
    ap.add_argument('--round',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--v-update',type=Path,default=None)
    args=ap.parse_args()
    inp=private_file(args.ledger);rp=private_file(args.round);out=private_file(args.output)
    if out==inp or out==rp or out.exists():raise ValueError('OUTPUT_MUST_BE_NEW_VERSION_FILE')
    v=private_file(args.v_update) if args.v_update else None
    obj=append(json.loads(inp.read_text(encoding='utf-8')),
               json.loads(rp.read_text(encoding='utf-8')),
               json.loads(v.read_text(encoding='utf-8')) if v else None)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'appended':True,'rounds':len(obj['rounds']),'private_output':str(out)},ensure_ascii=False))
    return 0
if __name__=='__main__':raise SystemExit(main())
