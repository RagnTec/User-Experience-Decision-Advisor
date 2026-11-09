#!/usr/bin/env python3
"""Offline structural preflight for distinct UXDA collaboration-mode outputs.

Never certifies facts, source existence, legal conclusions or statistical quality.
No outbound requests; reads only --input. Never prints private report contents.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

MODES={'guided','decision','project'}
SCOPES={'O','E','D','V'}
GATES={'GO','CONDITIONAL_GO','HOLD_FOR_CRITICAL_INFO','BLOCK_PENDING_SPECIALIST_REVIEW','NO_DECISION_NEEDED'}
DIMENSIONS={'legal','mandatory_standard','voluntary_standard','industry_practice','human_factors','consumer_market','technical','business'}
STATUS={'verified','supplied','inference','unverified'}
TEACHING_DEPTH={'foundation','applied','advanced','adaptive'}
KNOWLEDGE_DISCIPLINES={'research_methods','psychology','sociology','marketing','communication','media_studies','human_factors','product_domain'}
KNOWLEDGE_EVIDENCE={'method_principle','supplied','verified_external','hypothesis'}


def filled(v):
    return isinstance(v,str) and bool(v.strip())


def require(obj, keys, prefix, errors):
    for k in keys:
        if not filled(obj.get(k)):
            errors.append(prefix+'_MISSING_'+k.upper())


def audit(s):
    errors=[]
    if not isinstance(s,dict): return ['INVALID_RECORD']
    mode=s.get('mode'); mode='project' if mode=='review' else mode
    if mode not in MODES: errors.append('INVALID_MODE')
    require(s,['project_id','progress_map','evidence_boundary','next_user_checkpoint'],'SHARED',errors)
    scope=s.get('scope')
    if not isinstance(scope,list) or not scope or any(v not in SCOPES for v in scope) or len(scope)!=len(set(scope)):
        errors.append('SCOPE_MUST_BE_USER_CONFIRMED')
    if s.get('mode_status') != 'user_confirmed': errors.append('MODE_NOT_USER_CONFIRMED')
    if s.get('scope_status') != 'user_confirmed': errors.append('SCOPE_NOT_USER_CONFIRMED')
    if mode=='guided':
        if s.get('teaching_depth') not in TEACHING_DEPTH: errors.append('GUIDED_INVALID_TEACHING_DEPTH')
        bridges=s.get('knowledge_bridges')
        if not isinstance(bridges,list) or not 1<=len(bridges)<=3:
            errors.append('GUIDED_NEEDS_RELEVANT_KNOWLEDGE_BRIDGE')
        else:
            for bridge in bridges:
                if not isinstance(bridge,dict): errors.append('GUIDED_INVALID_KNOWLEDGE_BRIDGE');continue
                if bridge.get('discipline') not in KNOWLEDGE_DISCIPLINES: errors.append('GUIDED_INVALID_DISCIPLINE')
                if bridge.get('evidence_status') not in KNOWLEDGE_EVIDENCE: errors.append('GUIDED_INVALID_BRIDGE_EVIDENCE')
                require(bridge,['concept','task_link','research_implication','limitation'],'GUIDED_BRIDGE',errors)
                if bridge.get('evidence_status')=='verified_external':
                    require(bridge,['source_locator','examined_scope','verification_event_id'],'GUIDED_EXTERNAL_SOURCE',errors)
        lens=s.get('domain_lens')
        if not isinstance(lens,dict): errors.append('GUIDED_NEEDS_DOMAIN_CONTEXT')
        else: require(lens,['product_type','use_context','special_consideration','verification_boundary'],'GUIDED_DOMAIN',errors)
        if s.get('stage') not in [f'S{x}' for x in range(1,8)]: errors.append('GUIDED_INVALID_STAGE')
        require(s,['learning_objective','decision_link'],'GUIDED',errors)
        concepts=s.get('concepts')
        if not isinstance(concepts,list) or not concepts: errors.append('GUIDED_NEEDS_CONCEPTS')
        else:
            for x in concepts:
                if not isinstance(x,dict): errors.append('GUIDED_INVALID_CONCEPT'); continue
                require(x,['term','explanation','relevance'],'GUIDED_CONCEPT',errors)
        steps=s.get('reasoning_steps')
        if not isinstance(steps,list) or not steps: errors.append('GUIDED_NEEDS_REASONING')
        else:
            for x in steps:
                if not isinstance(x,dict): errors.append('GUIDED_INVALID_REASONING'); continue
                require(x,['question','reasoning','evidence_status','alternative'],'GUIDED_REASONING',errors)
        method=s.get('method_choice')
        if not isinstance(method,dict): errors.append('GUIDED_NEEDS_METHOD_COMPARISON')
        else: require(method,['method','why','alternative','alternative_tradeoff','cannot_establish'],'GUIDED_METHOD',errors)
        practice=s.get('learner_exercise')
        if not isinstance(practice,dict): errors.append('GUIDED_NEEDS_LEARNER_EXERCISE')
        else:
            require(practice,['prompt','assessment_criteria'],'GUIDED_PRACTICE',errors)
            if practice.get('example_is_synthetic') is not True: errors.append('GUIDED_EXERCISE_MUST_BE_SYNTHETIC_OR_NO_EXAMPLE')
    elif mode=='decision':
        require(s,['decision_point','decision_rationale','responsible_owner'],'DECISION',errors)
        options=s.get('options')
        if not isinstance(options,list) or len(options)<2 or not all(filled(x) for x in options): errors.append('DECISION_NEEDS_ALTERNATIVES')
        if s.get('gate_status') not in GATES: errors.append('DECISION_INVALID_GATE')
        if s.get('actual_business_approval') is not False: errors.append('SKILL_MUST_NOT_ASSERT_APPROVAL')
        gaps=s.get('gaps')
        if not isinstance(gaps,list) or not gaps: errors.append('DECISION_NEEDS_GAP_AUDIT')
        else:
            for x in gaps:
                if not isinstance(x,dict): errors.append('DECISION_INVALID_GAP'); continue
                if x.get('dimension') not in DIMENSIONS: errors.append('DECISION_INVALID_DIMENSION')
                if x.get('source_status') not in STATUS: errors.append('DECISION_INVALID_SOURCE_STATUS')
                require(x,['issue','consequence','impact_on_choice','owner'],'DECISION_GAP',errors)
                if x.get('source_status')=='verified':
                    require(x,['source_locator','verified_scope','verification_event_id'],'DECISION_VERIFIED_SOURCE',errors)
                if x.get('conclusion_is_binding') is True and x.get('source_status') not in ('verified','supplied'):
                    errors.append('UNVERIFIED_CONSTRAINT_CANNOT_BE_BINDING')
        rev=s.get('reversal_conditions')
        if not isinstance(rev,list) or not rev or not all(filled(x) for x in rev): errors.append('DECISION_NEEDS_REVERSAL')
        req=s.get('evidence_requests')
        if not isinstance(req,list) or len(req)>3: errors.append('DECISION_INVALID_EVIDENCE_REQUESTS')
        else:
            for x in req:
                if not isinstance(x,dict): errors.append('DECISION_INVALID_REQUEST'); continue
                require(x,['item','decision_use'],'DECISION_REQUEST',errors)
    elif mode=='project':
        require(s,['user_proposal','research_stage','work_product','analysis_method','decision_link'],'PROJECT',errors)
        if s.get('user_input_status') not in ('user_provided','partial','needs_input'): errors.append('PROJECT_INVALID_USER_INPUT_STATUS')
        if s.get('research_stage') not in ('define','design','collect','analyze','report','revise'): errors.append('PROJECT_INVALID_STAGE')
        refinements=s.get('refinements')
        if not isinstance(refinements,list): errors.append('PROJECT_NEEDS_REFINEMENT_LOG')
        else:
            for x in refinements:
                if not isinstance(x,dict): errors.append('PROJECT_INVALID_REFINEMENT'); continue
                require(x,['aspect','proposed_change','rationale'],'PROJECT_REFINEMENT',errors)
                if x.get('approval_status') not in ('suggested','user_confirmed','rejected'):
                    errors.append('PROJECT_REFINEMENT_APPROVAL_REQUIRED')
        data=s.get('data_status')
        if data not in ('no_data','real_authorized','synthetic_practice','supplied_summary'): errors.append('PROJECT_INVALID_DATA_STATUS')
        if s.get('report_status') not in ('outline','draft_with_data','reviewed'): errors.append('PROJECT_INVALID_REPORT_STATUS')
        findings=s.get('findings')
        if not isinstance(findings,list): errors.append('PROJECT_FINDINGS_MUST_BE_LIST')
        if data in ('no_data','synthetic_practice'):
            if findings: errors.append('PROJECT_NO_EMPIRICAL_FINDINGS_WITHOUT_REAL_DATA')
            if s.get('report_status') != 'outline': errors.append('PROJECT_REPORT_MUST_BE_OUTLINE_WITHOUT_REAL_DATA')
        if data=='real_authorized' and not filled(s.get('analysis_trace')):
            errors.append('PROJECT_REAL_DATA_NEEDS_ANALYSIS_TRACE')
        if data=='supplied_summary':
            if not filled(s.get('source_report_locator')):
                errors.append('PROJECT_SUPPLIED_SUMMARY_NEEDS_SOURCE')
            if s.get('analysis_claims_recomputed') is not False:
                errors.append('PROJECT_SUPPLIED_SUMMARY_CANNOT_CLAIM_RECOMPUTATION')
    return sorted(set(errors))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    args=p.parse_args()
    try: record=json.loads(args.input.read_text(encoding='utf-8'))
    except (FileNotFoundError,json.JSONDecodeError,UnicodeDecodeError):
        print(json.dumps({'ok':False,'issues':['UNREADABLE_INPUT']},ensure_ascii=False));return 1
    issues=audit(record)
    print(json.dumps({'ok':not issues,'issues':issues},ensure_ascii=False))
    return int(bool(issues))

if __name__=='__main__':sys.exit(main())
