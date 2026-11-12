#!/usr/bin/env python3
"""Offline structural/temporal audit for a PRIVATE decision-iteration ledger.

Does not read raw study data, fetch references, make or authorize decisions.
Reports only issue codes and round / position, never users' private text.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
PUBLIC_ROOT = HERE.parents[3] if HERE.parents[2].name == "skills" else HERE.parents[2]
ACTIONS = {'retain','modify','compare','pilot','defer','stop','escalate'}
READINESS = {'SCOPED','EVIDENCE_GAP','DECISION_READY','HANDOFF'}
ORIGINS = {'synthetic','user_provided','mixed'}
ACCESS = {'USER_PROVIDED','AUTHORIZED_LOCAL','VERIFIED_PUBLIC','SYNTHETIC_FIXTURE'}
KINDS = {'HYPOTHESIS','METHOD_INFERENCE','USER_DECLARED','OBSERVED','VERIFIED_EXTERNAL'}
STATUS = {'CONDITIONAL','SUPPORTED','UNSUPPORTED'}
CHANGES = {'NEW','REVISED','UPHELD','RETRACTED'}
BASIS = {'NEW_EVIDENCE','CORRECTION','CONSTRAINT_CHANGE','NO_CHANGE'}
NEXT = {'SYNTHESIZE_EXISTING','CHECK_CONFLICT','REQUEST_DOCUMENT','PROPOSE_FOCUSED_V','PROVISIONAL_DECISION','HANDOFF'}
STOPS = {'READY_FOR_HUMAN_CHOICE','WAITING_ON_EXTERNAL_EVIDENCE','NO_MATERIAL_GAIN','USER_STOP'}
EXTERNAL = {'REQUEST_DOCUMENT','PROPOSE_FOCUSED_V'}
HEX64 = re.compile(r'^[a-f0-9]{64}$')


def audit(data):
    issues = []
    def flag(code, round_no=0, position=0):
        issues.append({'code':code,'round':round_no,'position':position})
    if not isinstance(data,dict) or data.get('schema_version') != '1.0':
        return [{'code':'INVALID_ROOT_OR_SCHEMA','round':0,'position':0}]
    if data.get('data_origin') not in ORIGINS or not data.get('decision_id') or not data.get('decision_question'):
        flag('MISSING_DECISION_CONTEXT')
    options = data.get('options')
    if not isinstance(options,list) or len(options)<2 or any(not isinstance(o,str) or not o.strip() for o in options):
        flag('INVALID_OPTIONS')
    rounds = data.get('rounds')
    if not isinstance(rounds,list) or not rounds:
        return issues + [{'code':'NO_ROUNDS','round':0,'position':0}]
    prior_sources = {}
    prior_claims = {}
    prior_action = None
    prior_readiness = None
    prior_next = None
    unchanged_repeat = 0
    for i,r in enumerate(rounds,1):
        if not isinstance(r,dict):
            flag('INVALID_ROUND',i); continue
        if r.get('round') != i:
            flag('ROUND_SEQUENCE',i)
        sources = {}
        evidence = r.get('evidence',[])
        if not isinstance(evidence,list):
            flag('INVALID_EVIDENCE_LIST',i); evidence=[]
        for j,e in enumerate(evidence,1):
            if not isinstance(e,dict) or not isinstance(e.get('source_id'),str) or not e.get('source_id'):
                flag('INVALID_SOURCE',i,j); continue
            sid=e['source_id']
            if sid in sources: flag('DUPLICATE_SOURCE',i,j)
            digest=e.get('sha256')
            if not isinstance(digest,str) or not HEX64.fullmatch(digest): flag('INVALID_SOURCE_HASH',i,j)
            if e.get('origin') not in ORIGINS: flag('INVALID_SOURCE_ORIGIN',i,j)
            if e.get('access') not in ACCESS: flag('MISSING_SOURCE_ACCESS_OR_AUTHORIZATION',i,j)
            if e.get('access')=='SYNTHETIC_FIXTURE' and data.get('data_origin')!='synthetic':
                flag('SYNTHETIC_FIXTURE_IN_REAL_CASE',i,j)
            sources[sid]=digest
        new_or_updated={k for k,h in sources.items() if prior_sources.get(k)!=h}
        removed_sources=set(prior_sources)-set(sources)
        claims={}
        claim_positions={}
        raw_claims=r.get('claims',[])
        if not isinstance(raw_claims,list): flag('INVALID_CLAIMS',i);raw_claims=[]
        for j,c in enumerate(raw_claims,1):
            if not isinstance(c,dict) or not isinstance(c.get('id'),str) or not c.get('id'):
                flag('INVALID_CLAIM',i,j);continue
            cid=c['id'];claim_positions[cid]=j
            if cid in claims:flag('DUPLICATE_CLAIM',i,j)
            claims[cid]=c
            if c.get('kind') not in KINDS or c.get('status') not in STATUS: flag('INVALID_CLAIM_TYPE',i,j)
            refs=c.get('source_ids',[])
            if not isinstance(refs,list) or any(s not in sources for s in refs):flag('UNKNOWN_EVIDENCE_REF',i,j)
            if c.get('kind') in {'OBSERVED','USER_DECLARED','VERIFIED_EXTERNAL'} and not refs:
                flag('FACT_WITHOUT_SOURCE',i,j)
            if c.get('status')=='SUPPORTED' and not refs:
                flag('SUPPORTED_WITHOUT_SOURCE',i,j)
            if c.get('kind')=='VERIFIED_EXTERNAL' and c.get('status')=='SUPPORTED':
                if not any(isinstance(e,dict) and e.get('source_id') in refs and e.get('role')=='verified_external' for e in evidence):
                    flag('EXTERNAL_PROVENANCE_MISSING',i,j)
            if data.get('data_origin')=='synthetic' and c.get('empirical_claim',False):
                flag('SYNTHETIC_EMPIRICAL_CLAIM',i,j)
            if data.get('data_origin')=='synthetic' and c.get('kind')=='OBSERVED' and c.get('status')=='SUPPORTED':
                flag('SYNTHETIC_OBSERVATION_MISLABELLED',i,j)
            if not isinstance(c.get('statement'),str) or len(c['statement'].strip())<12:
                flag('MISSING_CLAIM_STATEMENT',i,j)
            if not isinstance(c.get('decision_link'),str) or len(c['decision_link'].strip())<8:
                flag('CLAIM_NOT_LINKED_TO_DECISION',i,j)
        deltas=r.get('changes',[])
        if not isinstance(deltas,list):flag('INVALID_CHANGES',i);deltas=[]
        delta_lookup={}
        for j,d in enumerate(deltas,1):
            if not isinstance(d,dict) or d.get('claim_id') not in claims:
                flag('CHANGE_UNKNOWN_CLAIM',i,j);continue
            cid=d['claim_id'];kind=d.get('change');basis=d.get('basis');refs=d.get('source_ids',[])
            if cid in delta_lookup:flag('DUPLICATE_CHANGE',i,j)
            delta_lookup[cid]=d
            if kind not in CHANGES or basis not in BASIS:flag('INVALID_CHANGE_TYPE',i,j)
            if not isinstance(d.get('reason'),str) or len(d['reason'].strip())<8:flag('CHANGE_REASON_MISSING',i,j)
            if not isinstance(refs,list) or any(s not in sources for s in refs):flag('CHANGE_SOURCE_MISSING',i,j)
            if kind in {'NEW','REVISED','RETRACTED'} and basis=='NO_CHANGE':flag('MATERIAL_CHANGE_WITHOUT_BASIS',i,j)
            if basis=='NEW_EVIDENCE' and not (set(refs)&new_or_updated):flag('NEW_EVIDENCE_NOT_NEW',i,j)
            if kind=='NEW' and cid in prior_claims:flag('CLAIM_ALREADY_EXISTS',i,j)
            if kind in {'REVISED','UPHELD','RETRACTED'} and cid not in prior_claims:flag('CLAIM_NOT_PREVIOUSLY_PRESENT',i,j)
        for cid,c in claims.items():
            if cid not in prior_claims and (cid not in delta_lookup or delta_lookup[cid].get('change')!='NEW'):
                flag('UNLOGGED_NEW_CLAIM',i,claim_positions[cid])
            if cid in prior_claims:
                old=prior_claims[cid]
                if (set(old.get('source_ids',[])) & (new_or_updated | removed_sources)) and cid not in delta_lookup:
                    flag('DEPENDENT_CLAIM_UNREVIEWED_AFTER_SOURCE_CHANGE',i,claim_positions[cid])
                if (old.get('kind'),old.get('status'),old.get('source_ids'),old.get('statement'),old.get('decision_link')) != (c.get('kind'),c.get('status'),c.get('source_ids'),c.get('statement'),c.get('decision_link')):
                    if cid not in delta_lookup or delta_lookup[cid].get('change') not in {'REVISED','RETRACTED'}:
                        flag('UNLOGGED_CLAIM_REVISION',i,claim_positions[cid])
                if c.get('kind')=='OBSERVED' and old.get('kind') in {'HYPOTHESIS','METHOD_INFERENCE'}:
                    if not any(ref in new_or_updated for ref in c.get('source_ids',[])):
                        flag('INFERENCE_PROMOTED_WITHOUT_NEW_SOURCE',i,claim_positions[cid])
            if c.get('status')=='SUPPORTED' and any(ref in removed_sources for ref in c.get('source_ids',[])):
                flag('STALE_SUPPORT',i,claim_positions[cid])
        for cid in prior_claims:
            if cid not in claims:flag('CLAIM_DISAPPEARED',i,0)
        dec=r.get('decision',{})
        if not isinstance(dec,dict):flag('INVALID_DECISION',i);dec={}
        action=dec.get('action');readiness=dec.get('readiness')
        if action not in ACTIONS or readiness not in READINESS:flag('INVALID_DECISION_STATE',i)
        for field in ('rationale','reversal_trigger'):
            if not isinstance(dec.get(field),str) or len(dec[field].strip())<12:
                flag('DECISION_JUSTIFICATION_MISSING',i)
        unknowns=dec.get('unknowns')
        if not isinstance(unknowns,list):flag('INVALID_UNKNOWNS',i)
        if data.get('data_origin')=='synthetic' and dec.get('empirical_claim',False):flag('SYNTHETIC_DECISION_CLAIM',i)
        substantive=bool(new_or_updated or removed_sources or any(d.get('basis') in {'CORRECTION','CONSTRAINT_CHANGE'} for d in deltas))
        if prior_action is not None and prior_action!=action and not substantive:
            flag('ACTION_CHANGED_WITH_NO_INPUT_DELTA',i)
        if prior_readiness is not None and prior_readiness!=readiness and not substantive:
            flag('READINESS_CHANGED_WITH_NO_BASIS',i)
        nxt=r.get('next_step',{})
        if not isinstance(nxt,dict):flag('INVALID_NEXT_STEP',i);nxt={}
        step=nxt.get('type');gate=nxt.get('gate')
        if step not in NEXT:flag('INVALID_NEXT_STEP_TYPE',i)
        if step in EXTERNAL and gate!='WAITING_FOR_USER':flag('EXTERNAL_GATE_REQUIRED',i)
        if step not in EXTERNAL and gate!='NONE':flag('NONEXTERNAL_GATE_INVALID',i)
        if step!='HANDOFF':
            if not isinstance(nxt.get('potential_decision_effect'),str) or len(nxt['potential_decision_effect'].strip())<12:
                flag('NEXT_STEP_NOT_DISCRIMINATING',i)
        elif nxt.get('stop_reason') not in STOPS:flag('MISSING_STOP_REASON',i)
        if step=='HANDOFF' and i<len(rounds):flag('ROUNDS_AFTER_HANDOFF',i)
        if readiness=='DECISION_READY' and step in EXTERNAL and nxt.get('gate')=='WAITING_FOR_USER':
            # Decision may be ready for a bounded action while optional deeper study remains; no blanket failure.
            pass
        if step=='HANDOFF' and nxt.get('stop_reason')=='READY_FOR_HUMAN_CHOICE' and readiness not in {'DECISION_READY','HANDOFF'}:
            flag('PREMATURE_READY_HANDOFF',i)
        user_declined = step=='HANDOFF' and nxt.get('stop_reason')=='USER_STOP'
        if (prior_next in EXTERNAL and i>1 and not new_or_updated and not removed_sources
                and not any(d.get('basis')=='CONSTRAINT_CHANGE' for d in deltas) and not user_declined):
            flag('CONTINUED_PAST_EXTERNAL_GATE_WITHOUT_INPUT',i)
        if i>1 and not new_or_updated and not removed_sources and not deltas and action==prior_action and readiness==prior_readiness:
            unchanged_repeat+=1
            if unchanged_repeat>=2:flag('NO_GAIN_LOOP',i)
        else:unchanged_repeat=0
        prior_sources=sources;prior_claims=claims;prior_action=action;prior_readiness=readiness;prior_next=step
    if rounds[-1].get('next_step',{}).get('type')!='HANDOFF' and rounds[-1].get('next_step',{}).get('gate')!='WAITING_FOR_USER':
        flag('OPEN_LOOP_WITHOUT_GATE',len(rounds))
    return issues


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,required=True)
    args=ap.parse_args()
    inp=args.input.resolve(strict=True)
    if PUBLIC_ROOT.resolve() in (inp,*inp.parents):
        raise SystemExit('ERROR: ledger input must be outside public Skill source tree')
    data=json.loads(inp.read_text(encoding='utf-8'))
    problems=audit(data)
    print(json.dumps({'ok':not problems,'rounds':len(data.get('rounds',[])),'issues':problems},ensure_ascii=False))
    return 0 if not problems else 1

if __name__=='__main__':raise SystemExit(main())
