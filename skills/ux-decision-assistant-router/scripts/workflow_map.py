#!/usr/bin/env python3
"""A private, event-versioned business workflow map for UX decision sessions.

No network, no AI decisions, no auto-approval. Renders compact Mermaid/text and an
optional offline HTML preview. All user-derived files must live outside public sources.
"""
from __future__ import annotations
import argparse
import copy
import html
import json
import re
from pathlib import Path

# Installed bundles omit the leading 'skills/' segment; locate the actual code root.
_SCRIPT = Path(__file__).resolve()
ROOT = _SCRIPT.parents[3] if _SCRIPT.parents[2].name == 'skills' else _SCRIPT.parents[2]
MAX_STEPS = 12
STATES = {'candidate', 'ready', 'active', 'completed', 'blocked', 'paused', 'skipped'}
ROLES = {'core', 'optional', 'check'}
ACTORS = {'agent', 'user', 'authorized_reviewer'}
EVENTS = {'progress', 'confirm', 'reopen', 'revise', 'add', 'flag_recheck', 'resolve_recheck', 'focus', 'scope_detect', 'scope_confirm', 'assess_applicability', 'reopen_applicability'}
MODES = ('O','E','D','V')
APPLICABILITY = {'unknown', 'applicable', 'not_applicable'}
ID_RE = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,27}$')


def private_path(path: Path) -> Path:
    p = path.expanduser().resolve()
    if ROOT.resolve() in (p, *p.parents) or any((q/'PUBLIC_FILE_MANIFEST.json').exists() or (q/'.git').exists() for q in (p.parent,*p.parents)):
        raise ValueError('PRIVATE_PATH_REQUIRED')
    return p


def validate(plan: dict) -> dict:
    if not isinstance(plan,dict) or plan.get('schema_version')!=1:
        raise ValueError('SCHEMA_VERSION_REQUIRED')
    if not isinstance(plan.get('decision_id'),str) or not ID_RE.fullmatch(plan['decision_id']):
        raise ValueError('DECISION_ID_REQUIRED')
    if not isinstance(plan.get('objective'),str) or not plan['objective'].strip():
        raise ValueError('OBJECTIVE_REQUIRED')
    if type(plan.get('revision')) is not int or plan['revision']<0:
        raise ValueError('REVISION_INVALID')
    items=plan.get('steps')
    if not isinstance(items,list) or not 1<=len(items)<=MAX_STEPS:
        raise ValueError('STEPS_INVALID')
    ids=set()
    for s in items:
        if not isinstance(s,dict) or not ID_RE.fullmatch(str(s.get('id',''))):
            raise ValueError('STEP_ID_INVALID')
        if s['id'] in ids:raise ValueError('DUPLICATE_STEP_ID')
        ids.add(s['id'])
        if not isinstance(s.get('title'),str) or not s['title'].strip() or len(s['title'])>90:
            raise ValueError('STEP_TITLE_INVALID')
        if s.get('role') not in ROLES or s.get('state') not in STATES:
            raise ValueError('STEP_ROLE_OR_STATE_INVALID')
        if type(s.get('confirmed')) is not bool:
            raise ValueError('CONFIRMED_FLAG_REQUIRED')
        if s['state']=='candidate' and s['confirmed']:
            raise ValueError('CANDIDATE_CANNOT_BE_CONFIRMED')
        if s.get('recheck') not in (True,False):
            raise ValueError('RECHECK_FLAG_REQUIRED')
        if not isinstance(s.get('depends_on'),list) or any(not isinstance(d,str) for d in s['depends_on']):
            raise ValueError('DEPENDENCY_INVALID')
        if not isinstance(s.get('decision_link'),str) or not s['decision_link'].strip():
            raise ValueError('DECISION_LINK_REQUIRED')
        if not isinstance(s.get('readiness',''),str) or not isinstance(s.get('next_input',''),str):
            raise ValueError('STEP_METADATA_INVALID')
        # Completion requires a verifiable local deliverable/source reference,
        # not an ungrounded progress checkmark.
        if not isinstance(s.get('evidence_refs',[]),list) or any(not isinstance(x,str) or not x for x in s.get('evidence_refs',[])):
            raise ValueError('EVIDENCE_REFS_INVALID')
        if s['state']=='completed' and not s.get('evidence_refs'):
            raise ValueError('COMPLETED_REQUIRES_EVIDENCE_REF')
    graph={s['id']:s['depends_on'] for s in items}
    for sid,ds in graph.items():
        if sid in ds or any(d not in ids for d in ds) or len(ds)!=len(set(ds)):
            raise ValueError('UNKNOWN_OR_DUPLICATE_DEPENDENCY')
    visited=set();stack=set()
    def visit(sid):
        if sid in stack:raise ValueError('CYCLIC_DEPENDENCY')
        if sid in visited:return
        stack.add(sid)
        for d in graph[sid]:visit(d)
        stack.remove(sid);visited.add(sid)
    for sid in graph:visit(sid)
    scope = plan.get('analysis_scope', {'detected': [], 'selected': [], 'confirmed': False})
    if not isinstance(scope,dict) or not isinstance(scope.get('detected'),list) or not isinstance(scope.get('selected'),list) or type(scope.get('confirmed')) is not bool:
        raise ValueError('ANALYSIS_SCOPE_INVALID')
    if any(m not in MODES for m in scope['detected']+scope['selected']) or len(set(scope['detected']))!=len(scope['detected']) or len(set(scope['selected']))!=len(scope['selected']):
        raise ValueError('ANALYSIS_SCOPE_MODES_INVALID')
    if not scope['confirmed'] and scope['selected']:
        raise ValueError('UNCONFIRMED_SCOPE_CANNOT_BE_SELECTED')
    for s in items:
        app=s.get('applicability','unknown')
        if app not in APPLICABILITY:raise ValueError('APPLICABILITY_INVALID')
        if app=='not_applicable' and (not s.get('applicability_reason') or not s.get('applicability_refs')):
            raise ValueError('NOT_APPLICABLE_REQUIRES_REASON_AND_SOURCE')
        if s['role']=='optional' and s['confirmed'] is False and s['state'] not in ('candidate','skipped'):
            raise ValueError('UNCONFIRMED_BRANCH_CANNOT_RUN')
    current=plan.get('current_step')
    if current is not None and current not in ids:
        raise ValueError('CURRENT_STEP_UNKNOWN')
    hist=plan.get('history',[])
    if not isinstance(hist,list) or len(hist)!=plan['revision']:
        raise ValueError('HISTORY_REVISION_MISMATCH')
    for i,ev in enumerate(hist,1):
        if not isinstance(ev,dict) or ev.get('revision')!=i or ev.get('type') not in EVENTS or ev.get('actor') not in ACTORS:
            raise ValueError('HISTORY_INVALID')
    return plan


def initial(payload: dict) -> dict:
    if not isinstance(payload,dict):raise ValueError('PLAN_OBJECT_REQUIRED')
    # The agent can propose routes and designate a current work focus; it cannot
    # retroactively assert that the user approved or completed one.
    detected=payload.get('detected_modes',[])
    if not isinstance(detected,list) or any(m not in MODES for m in detected) or len(set(detected))!=len(detected):
        raise ValueError('INVALID_DETECTED_MODES')
    steps=[]
    for s in payload.get('steps',[]):
        steps.append({'id':s.get('id'),'title':s.get('title'),'role':s.get('role','core'),
                      'state':'candidate','confirmed':False,'recheck':False,
                      'depends_on':s.get('depends_on',[]),'decision_link':s.get('decision_link',payload.get('decision_id','')),
                      'readiness':s.get('readiness',''),'next_input':s.get('next_input',''),'evidence_refs':[],
                      'applicability':'unknown','applicability_reason':'','applicability_refs':[]})
    plan={'schema_version':1,'decision_id':payload.get('decision_id'),'objective':payload.get('objective'),
          'revision':0,'current_step':payload.get('current_step'),'steps':steps,'history':[],
          'analysis_scope':{'detected':detected,
                            'selected':[],'confirmed':False}}
    return validate(plan)


def preset(decision_id: str, objective: str, profile: str = 'consumer_product') -> dict:
    """A generic, adaptable decision-stage proposal; no completed steps or implicit approval."""
    if profile not in {'consumer_product', 'digital_service', 'general'}:
        raise ValueError('UNKNOWN_PRESET_PROFILE')
    # Names are general public patterns, never copied from actual user/company cases.
    subjects = {
        'consumer_product': '目标消费者、市场与使用任务',
        'digital_service': '目标用户、渠道与关键任务',
        'general': '相关使用者、业务情境与任务',
    }
    stage = [
        ('goal', '需求与业务决策界定', 'core', [], '要改变的选择及理由'),
        ('law', '地域法规、平台及数据规则适用性', 'check', ['goal'], '目标地区、平台与实际实现机制'),
        ('norms', '人因、行业惯例及内部约束适用性', 'check', ['goal'], '涉及的任务与现有规则'),
        ('audience', subjects[profile], 'core', ['goal'], '使用者角色与主要场景'),
        ('mechanism', '体验机制、备选方案与潜在代价', 'core', ['law', 'norms', 'audience'], '候选方案与可用产品资料'),
        ('evidence', '既有证据与决定性未知核查', 'check', ['mechanism'], '已有用户研究或测试资料（可无）'),
        ('decision', '阶段结论、决策交接或停止（不预设 D 分析）', 'core', ['evidence'], '适用条件、剩余未知与下一步选择'),
    ]
    proposal = {'decision_id': decision_id, 'objective': objective,
                'current_step': 'goal', 'steps': [
                    {'id':sid, 'title':title, 'role':role, 'depends_on':deps,
                     'decision_link':decision_id, 'next_input':preparation}
                    for sid,title,role,deps,preparation in stage
                ]}
    return initial(proposal)


def apply(plan:dict,event:dict)->dict:
    validate(plan)
    if not isinstance(event,dict) or event.get('type') not in EVENTS or event.get('actor') not in ACTORS:
        raise ValueError('EVENT_INVALID')
    if type(event.get('expected_revision')) is not int or event['expected_revision'] != plan['revision']:
        raise ValueError('STALE_REVISION')
    action=event['type']; actor=event['actor']
    target=event.get('step_id')
    steps={s['id']:s for s in plan['steps']}
    if action not in ('add','scope_detect','scope_confirm') and target not in steps:raise ValueError('UNKNOWN_STEP')
    reason=event.get('reason','')
    if not isinstance(reason,str):raise ValueError('REASON_INVALID')
    payload=event.get('changes',{})
    if not isinstance(payload,dict):raise ValueError('CHANGES_INVALID')
    evidence=event.get('evidence_refs',[])
    if not isinstance(evidence,list) or any(not isinstance(v,str) or not v.strip() for v in evidence):
        raise ValueError('EVENT_EVIDENCE_INVALID')
    user_explicit=actor=='user' and event.get('explicit_user_request') is True
    result=copy.deepcopy(plan)
    dst={s['id']:s for s in result['steps']}
    s=dst.get(target)
    before_scope=copy.deepcopy(plan.get('analysis_scope',{'detected':[],'selected':[],'confirmed':False}))
    if action=='scope_detect':
        # Pure inference; never starts a branch. Existing confirmed choice stays in force.
        detected=payload.get('detected')
        if not isinstance(detected,list) or any(m not in MODES for m in detected) or len(set(detected))!=len(detected):
            raise ValueError('INVALID_DETECTED_MODES')
        result['analysis_scope']['detected']=detected
    elif action=='scope_confirm':
        if not user_explicit:raise ValueError('EXPLICIT_USER_SCOPE_CONFIRM_REQUIRED')
        selected=payload.get('selected')
        if not isinstance(selected,list) or not selected or any(m not in MODES for m in selected) or len(set(selected))!=len(selected):
            raise ValueError('INVALID_CONFIRMED_MODES')
        result['analysis_scope']['selected']=[m for m in MODES if m in selected]
        result['analysis_scope']['confirmed']=True
    elif action=='assess_applicability':
        app=payload.get('applicability')
        if app not in {'applicable','not_applicable'}:raise ValueError('INVALID_APPLICABILITY')
        if not reason.strip() or not evidence:raise ValueError('APPLICABILITY_REQUIRES_REASON_AND_SOURCE')
        if s['confirmed'] and not user_explicit:raise ValueError('CONFIRMED_STAGE_APPLICABILITY_REQUIRES_USER')
        s['applicability']=app
        s['applicability_reason']=reason
        s['applicability_refs']=evidence
    elif action=='reopen_applicability':
        if not user_explicit or not reason.strip():raise ValueError('EXPLICIT_USER_REOPEN_APPLICABILITY_REQUIRED')
        if s.get('applicability')!='not_applicable':raise ValueError('NOT_APPLICABLE_STAGE_REQUIRED')
        s['applicability']='unknown'
        s['applicability_reason']=''
        s['applicability_refs']=[]
        s['recheck']=True
        result['current_step']=target
    elif action=='add':
        if not user_explicit:raise ValueError('EXPLICIT_USER_BRANCH_ADD_REQUIRED')
        if len(result['steps'])>=MAX_STEPS:raise ValueError('TOO_MANY_STEPS')
        item={'id':payload.get('id'),'title':payload.get('title'),'role':payload.get('role','optional'),
              'state':'ready','confirmed':True,'recheck':False,'depends_on':payload.get('depends_on',[]),
              'decision_link':payload.get('decision_link',plan['decision_id']),
              'readiness':payload.get('readiness',''),'next_input':payload.get('next_input',''), 'evidence_refs':[],
              'applicability':'unknown','applicability_reason':'','applicability_refs':[]}
        if not item['id'] or item['id'] in steps:raise ValueError('NEW_ID_REQUIRED')
        result['steps'].append(item)
        target=item['id']
    elif action=='confirm':
        if not user_explicit:raise ValueError('ONLY_EXPLICIT_USER_CAN_CONFIRM')
        if s['state']=='candidate':s['state']='ready'
        s['confirmed']=True
    elif action=='progress':
        if s['role']=='optional' and not s['confirmed']:
            raise ValueError('UNCONFIRMED_BRANCH_CANNOT_PROGRESS')
        state=payload.get('state')
        if s.get('applicability')=='not_applicable' and state not in ('skipped','paused'):
            raise ValueError('REOPEN_APPLICABILITY_BEFORE_PROGRESS')
        if state not in STATES or state=='candidate':raise ValueError('PROGRESS_STATE_INVALID')
        if s['state'] in ('completed','skipped') and state!=s['state']:
            raise ValueError('USE_EXPLICIT_REOPEN_FOR_HISTORY')
        if state=='skipped' and s['confirmed'] and not user_explicit:
            raise ValueError('CONFIRMED_SKIP_REQUIRES_EXPLICIT_USER')
        if state in ('completed','skipped') and (not reason.strip() or not evidence):
            raise ValueError('OUTCOME_EVIDENCE_REQUIRED')
        if state=='completed':s['evidence_refs']=list(dict.fromkeys(s['evidence_refs']+evidence))
        s['state']=state
    elif action=='reopen':
        if not user_explicit or not reason.strip():raise ValueError('EXPLICIT_USER_REOPEN_REQUIRED')
        if s['state'] not in ('completed','skipped','paused','blocked'):
            raise ValueError('REOPEN_STATE_INVALID')
        s['state']='active';s['recheck']=True
        result['current_step']=target
    elif action=='revise':
        allowed={'title','role','depends_on','readiness','next_input','decision_link'}
        if not payload or any(k not in allowed for k in payload):raise ValueError('REVISE_FIELDS_INVALID')
        if (s['confirmed'] or s['state'] in ('completed','skipped')) and (not user_explicit or not reason.strip()):
            raise ValueError('LOCKED_HISTORY_REQUIRES_EXPLICIT_USER')
        for k,v in payload.items():s[k]=v
        if s['state']=='completed':s['recheck']=True
    elif action=='flag_recheck':
        if not reason.strip() or not evidence:raise ValueError('RECHECK_REQUIRES_REASON_AND_SOURCE')
        s['recheck']=True
    elif action=='resolve_recheck':
        if not reason.strip() or not evidence:raise ValueError('RESOLVE_REQUIRES_EVIDENCE')
        if s['confirmed'] and not user_explicit:raise ValueError('CONFIRMED_RECHECK_REQUIRES_USER')
        s['recheck']=False
    elif action=='focus':
        if s['role']=='optional' and not s['confirmed']:
            raise ValueError('UNCONFIRMED_BRANCH_CANNOT_FOCUS')
        result['current_step']=target
    # Reopening or changing a previously confirmed stage does not rewrite its
    # dependents. Instead, visibly flag every affected downstream outcome for
    # review while preserving its status and provenance.
    affected=[]
    if action in ('reopen','flag_recheck','reopen_applicability') or (action=='revise' and (steps[target]['confirmed'] or steps[target]['state'] in ('completed','skipped'))):
        affected_ids={target}
        changed=True
        while changed:
            changed=False
            for candidate in result['steps']:
                if candidate['id'] not in affected_ids and any(d in affected_ids for d in candidate['depends_on']):
                    affected_ids.add(candidate['id']);changed=True
        for downstream in result['steps']:
            if downstream['id']!=target and downstream['id'] in affected_ids and downstream['state']!='candidate':
                downstream['recheck']=True
                affected.append(downstream['id'])
    result['revision']+=1
    result['history'].append({'revision':result['revision'],'type':action,'actor':actor,
                              'step_id':target,'reason':reason,'evidence_refs':evidence,
                              'before':copy.deepcopy(steps.get(target)) if target in steps else before_scope,
                              'affected_downstream':affected,
                              'after':copy.deepcopy({t['id']:t for t in result['steps']}[target]) if target in steps else copy.deepcopy(result['analysis_scope'])})
    return validate(result)


STATE_LABEL={'candidate':'建议','ready':'待执行','active':'进行中','completed':'已完成',
             'blocked':'受阻','paused':'暂缓','skipped':'已跳过'}

def short_label(s:dict)->str:
    status=STATE_LABEL[s['state']]
    if s['confirmed']:
        status+=' / 路径已确认'
    if s['recheck']:
        status+=' / 待复核'
    if s.get('applicability')=='not_applicable':
        status='建议省略（有依据，可由用户重开）'
    if s['role']=='optional' and not s['confirmed']:
        status+=' / 可选'
    return status


def mermaid(plan:dict)->str:
    validate(plan)
    rows=['flowchart TD']
    for s in plan['steps']:
        if s['role']=='optional' and not s['confirmed']:continue
        label=f"{s['title']}（{short_label(s)}）"
        label=label.replace('"','＂').replace('\n',' ')
        rows.append(f'  {s["id"]}["{label}"]')
        for d in s['depends_on']:
            edge='-. 可选 .->' if s['role']=='optional' and not s['confirmed'] else '-->'
            rows.append(f'  {d} {edge} {s["id"]}')
    for s in plan['steps']:
        if s['role']=='optional' and not s['confirmed']:continue
        klass=('current' if s['id']==plan.get('current_step') else
               'done' if s['state']=='completed' else 'hold' if s['recheck'] or s['state'] in ('blocked','paused') else
               'future' if s['state']=='candidate' else 'committed')
        rows.append(f'  class {s["id"]} {klass}')
    rows.extend(['  classDef current fill:#d7ede8,stroke:#23756b,color:#143d38,stroke-width:2px',
                 '  classDef done fill:#edf4f0,stroke:#6c9b7e,color:#184832',
                 '  classDef hold fill:#fff2df,stroke:#bf8844,color:#694315',
                 '  classDef future fill:#f3f4f6,stroke:#8b929b,color:#434b55,stroke-dasharray:4 4',
                 '  classDef committed fill:#e9eef9,stroke:#5c78a3,color:#21375e'])
    return '\n'.join(rows)+'\n'


def compact(plan:dict)->str:
    validate(plan)
    primary=[s for s in plan['steps'] if (s['role']!='optional' or s['confirmed']) and s.get('applicability')!='not_applicable']
    # Keep the seven meaningful core/check stages in a new-project preset.
    # Optional research stays a separate branch, never an implied prerequisite.
    if len(primary)>7:
        primary=primary[:4]+primary[-3:]
    steps=' → '.join(f"{s['title']}〔{short_label(s)}{'·当前' if s['id']==plan.get('current_step') else ''}〕" for s in primary)
    extra=[s for s in plan['steps'] if s['role']=='optional' and s['confirmed']]
    alt='；已选择的扩展分支：'+'、'.join(s['title'].removeprefix('可选：').strip() for s in extra[:3]) if extra else ''
    now=next((s for s in plan['steps'] if s['id']==plan.get('current_step')),None)
    inp=f"；当前需准备：{now['next_input']}" if now and now.get('next_input') else ''
    omitted=[s for s in plan['steps'] if s.get('applicability')=='not_applicable']
    omitted_note='；建议省略（可重新启用）：'+'、'.join(s['title'] for s in omitted) if omitted else ''
    scope=plan.get('analysis_scope',{'detected':[],'selected':[],'confirmed':False})
    detected='、'.join(scope['detected']) or '待识别'
    if scope['confirmed']:
        scope_note='分析方向｜用户已确认：'+ '、'.join(scope['selected'])+'；其他方向保留可选，不自动启动'
    else:
        scope_note='分析方向｜已识别：'+detected+'（仅识别，未启用）；O 机会发现 / E 体验评价 / D 决策支持 / V 定向验证均待用户确认'
    return f"业务推进图｜{plan['objective']}（版本 r{plan['revision']}）\n{steps}{alt}{omitted_note}{inp}\n{scope_note}\n"


def preview_html(plan:dict)->str:
    validate(plan)
    cards=[]
    for s in plan['steps']:
        if s['role']=='optional' and not s['confirmed']:continue
        status=html.escape(short_label(s));title=html.escape(s['title']);intent=html.escape(s['decision_link'])
        inp=html.escape(s.get('next_input',''))
        css='current' if s['id']==plan.get('current_step') else ('past' if s['state']=='completed' else 'future')
        hint=(f'<p>准备资料：{inp}</p>' if inp else '')
        deps=('依赖：'+', '.join(html.escape(x) for x in s['depends_on'])) if s['depends_on'] else '起点/并行节点'
        cards.append(f'<article class="node {css}"><div class="status">{status}</div><h2>{title}</h2><p>关联决策：{intent}</p>{hint}<small>{deps}</small></article>')
    title=html.escape(plan['objective'])
    scope=plan.get('analysis_scope',{'detected':[],'selected':[],'confirmed':False})
    scope_summary=('用户已确认：'+', '.join(scope['selected'])) if scope['confirmed'] else ('待确认：O/E/D/V；识别倾向 '+', '.join(scope['detected']))
    scope_summary=html.escape(scope_summary)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>业务推进图 · {title}</title><style>
*{{box-sizing:border-box}}body{{font:15px/1.65 system-ui,'PingFang SC',sans-serif;background:#f6f8f9;color:#25333c;margin:0}}main{{max-width:760px;margin:auto;padding:24px 18px 70px}}h1{{font-size:24px;margin:8px 0}}.muted{{color:#596a77}}.node{{border:1px solid #d8e1e5;background:white;border-radius:12px;padding:16px 20px;margin:12px 0;position:relative}}.node:not(:last-child)::after{{content:'↓';position:absolute;bottom:-22px;left:50%;color:#879da4;z-index:2}}.node.current{{border:2px solid #23756b;background:#eaf6f3}}.node.past{{border-color:#89ae97}}.node.future{{border-style:dashed}}h2{{font-size:17px;margin:4px 0 8px}}p{{margin:4px 0}}.status{{font-size:12px;font-weight:700;color:#35776f}}small{{color:#60717a}}.notice{{padding:12px 15px;background:#eef2f4;border-radius:8px;margin:18px 0}}@media print{{body{{background:white}}.node{{break-inside:avoid}}}}
</style></head><body><main><p class="muted">UXDA / 仅本地展示 · r{plan['revision']}</p><h1>{title}</h1><div class="notice">箭头表示概览顺序，实际依赖见节点标注。未确认的未来步骤仅为推荐。完成状态不代表业务上线或法规合规。历史回退需用户明确要求。此文件只展示静态快照，不会自动修改流程。</div><div class="notice"><strong>分析方向</strong>：{scope_summary}。未确认分支不自动运行。</div>{''.join(cards)}<p class="muted">可要求 Agent 修改、回退、增补节点后重新生成版本。未取得资料或授权时不得标记完成。</p></main></body></html>'''


def write_new(p:Path,content:str):
    q=private_path(p)
    if q.exists():raise ValueError('OUTPUT_ALREADY_EXISTS_USE_VERSIONED_PATH')
    q.parent.mkdir(parents=True,exist_ok=True)
    q.write_text(content,encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    init=sub.add_parser('init');init.add_argument('--input',type=Path,required=True);init.add_argument('--output',type=Path,required=True)
    pre=sub.add_parser('preset');pre.add_argument('--decision-id',required=True);pre.add_argument('--objective',required=True);pre.add_argument('--profile',choices=['consumer_product','digital_service','general'],default='consumer_product');pre.add_argument('--output',type=Path,required=True)

    update=sub.add_parser('update');update.add_argument('--input',type=Path,required=True);update.add_argument('--event',type=Path,required=True);update.add_argument('--output',type=Path,required=True)
    render=sub.add_parser('render');render.add_argument('--input',type=Path,required=True);render.add_argument('--format',choices=['text','mermaid','html'],default='text');render.add_argument('--output',type=Path)
    args=ap.parse_args()
    inp=private_path(args.input) if args.command!='preset' else None
    if args.command=='preset':
        write_new(args.output,json.dumps(preset(args.decision_id,args.objective,args.profile),ensure_ascii=False,indent=2)+'\n')
    elif args.command=='init':
        plan=initial(json.loads(inp.read_text(encoding='utf-8')))
        write_new(args.output,json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    elif args.command=='update':
        plan=apply(json.loads(inp.read_text(encoding='utf-8')),json.loads(private_path(args.event).read_text(encoding='utf-8')))
        write_new(args.output,json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    else:
        plan=validate(json.loads(inp.read_text(encoding='utf-8')))
        text=compact(plan) if args.format=='text' else mermaid(plan) if args.format=='mermaid' else preview_html(plan)
        if args.output:write_new(args.output,text)
        else:print(text)

if __name__=='__main__':
    main()
