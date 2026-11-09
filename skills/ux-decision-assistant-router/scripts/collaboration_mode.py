#!/usr/bin/env python3
"""Offline, private project collaboration-mode state checker.

This enforces authorization/structure only. It does NOT establish empirical UX
quality, source authenticity or user learning. Do not keep private state in the
public Skill/source directory.
"""
from __future__ import annotations
import argparse
import copy
import json
import sys
from pathlib import Path

MODES = {'guided', 'decision', 'project'}
# Legacy sessions from v0.5A retain 'review'; new selection maps to project.
LEGACY_MODES = {'review'}
MODE_LABELS = {'guided': '教学引导', 'decision': '决策支持', 'project': '方案推进', 'review': '方案推进（旧评审记录）'}
STAGES = tuple(f'S{i}' for i in range(1, 8))
STAGE_NAMES = {
    'S1': '问题界定', 'S2': '用户与市场情境', 'S3': '研究问题与假设',
    'S4': '证据与方法选择', 'S5': '研究执行及数据分析',
    'S6': '综合分析与方案取舍', 'S7': '复盘与迭代',
}
BASIS = {'local_doc', 'verified_web', 'method_reasoning', 'unverified_external'}
SUPPORT_DEPTH={'foundation','applied','advanced','adaptive'}
COACHING={'self_try','scaffold','worked_example','collaborate','adaptive'}


def initial(project_id: str) -> dict:
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError('PROJECT_ID_REQUIRED')
    return {'schema_version': '0.5A', 'project_id': project_id, 'revision': 0,
            'collaboration': {'mode': None, 'confirmed': False},
            'support': {'depth':'adaptive','coaching':'adaptive','selected_by_user':False},
            'learning': {'active_stage': 'S1', 'cards': [], 'stage_decisions': []},
            'events': []}


def _check_explicit(event: dict, label: str):
    if event.get('actor') != 'user' or event.get('explicit_user_request') is not True:
        raise ValueError(label + '_EXPLICIT_USER_CONFIRM_REQUIRED')


def _card_validate(c: dict):
    required = ['stage', 'decision_link', 'why', 'method', 'method_alternative',
                'method_limit', 'terms', 'counterexample', 'learner_task',
                'success_criteria', 'basis', 'evidence_boundary']
    for k in required:
        v = c.get(k)
        if not isinstance(v, (str, list, dict)) or not v:
            raise ValueError('STAGE_CARD_REQUIRED_' + k.upper())
    if c['stage'] not in STAGES:
        raise ValueError('INVALID_STAGE')
    if not isinstance(c['terms'], list) or not 1 <= len(c['terms']) <= 3 or any(not isinstance(t, dict) or not t.get('name') or not t.get('meaning') for t in c['terms']):
        raise ValueError('STAGE_TERMS_NEED_DEFINITIONS')
    basis = c['basis']
    if not isinstance(basis, list) or not basis:
        raise ValueError('STAGE_BASIS_REQUIRED')
    for b in basis:
        if not isinstance(b, dict) or b.get('kind') not in BASIS:
            raise ValueError('INVALID_BASIS_KIND')
        if b['kind'] in ('local_doc', 'verified_web'):
            if not b.get('locator') or not b.get('verified_scope'):
                raise ValueError('VERIFIED_BASIS_NEEDS_LOCATOR_AND_SCOPE')
        if b['kind'] == 'verified_web':
            if not b.get('access_log_id') or not b.get('observed_title'):
                raise ValueError('WEB_BASIS_NEEDS_OBSERVED_TRACE')
        if b['kind'] == 'unverified_external' and b.get('supports_definitive_claim'):
            raise ValueError('UNVERIFIED_BASIS_CANNOT_PROVE_FACT')
        if b['kind'] == 'method_reasoning' and not b.get('rationale'):
            raise ValueError('METHOD_REASONING_NEEDS_RATIONALE')
    return True


def apply(state: dict, event: dict) -> dict:
    audit(state)
    t = event.get('type')
    if t not in ('choose_mode', 'choose_support', 'record_stage', 'complete_stage', 'skip_stage', 'set_learning_stage'):
        raise ValueError('INVALID_EVENT_TYPE')
    if event.get('expected_revision') != state['revision']:
        raise ValueError('STALE_REVISION')
    s = copy.deepcopy(state)
    if t == 'choose_mode':
        _check_explicit(event, 'MODE')
        m = event.get('mode')
        if m not in MODES | LEGACY_MODES:
            raise ValueError('INVALID_MODE')
        s['collaboration'] = {'mode': ('project' if m == 'review' else m), 'confirmed': True}
    else:
        if not s['collaboration']['confirmed']:
            raise ValueError('MODE_NOT_CONFIRMED')
        if t == 'choose_support':
            _check_explicit(event, 'SUPPORT')
            depth=event.get('depth'); coaching=event.get('coaching')
            if depth not in SUPPORT_DEPTH or coaching not in COACHING:
                raise ValueError('INVALID_SUPPORT_SELECTION')
            s['support']={'depth':depth,'coaching':coaching,'selected_by_user':True}
        elif t == 'record_stage':
            if s['collaboration']['mode'] != 'guided':
                raise ValueError('TEACHING_CARD_ONLY_IN_GUIDED')
            c = event.get('card')
            if not isinstance(c, dict):
                raise ValueError('INVALID_STAGE_CARD')
            _card_validate(c)
            if c['stage'] != s['learning']['active_stage']:
                raise ValueError('CARD_STAGE_NOT_ACTIVE')
            s['learning']['cards'].append({'card': c, 'iteration': len(s['learning']['cards'])+1})
        elif t in ('complete_stage', 'skip_stage', 'set_learning_stage'):
            _check_explicit(event, t.upper())
            step = event.get('stage')
            if step not in STAGES:
                raise ValueError('INVALID_STAGE')
            if t == 'complete_stage' and not any(x['card']['stage']==step for x in s['learning']['cards']):
                raise ValueError('NO_TEACHING_CARD_FOR_STAGE')
            if t == 'skip_stage' and not event.get('reason'):
                raise ValueError('SKIP_REQUIRES_REASON')
            if t == 'set_learning_stage':
                s['learning']['active_stage'] = step
            else:
                s['learning']['stage_decisions'].append({'stage': step, 'action': t,
                    'reason': event.get('reason', ''), 'actor': 'user'})
    s['revision'] += 1
    # Store event metadata only; never paste real text, VOC or documents into public source.
    ev = {'revision': s['revision'], 'type': t, 'actor': event.get('actor', 'agent')}
    if t == 'choose_mode': ev['mode'] = event['mode']
    if t == 'choose_support': ev['depth'] = event['depth']; ev['coaching'] = event['coaching']
    if t in ('complete_stage', 'skip_stage', 'set_learning_stage'): ev['stage'] = event['stage']
    if t == 'record_stage': ev['stage'] = event['card']['stage']
    s['events'].append(ev)
    audit(s)
    return s


def audit(s: dict) -> bool:
    if s.get('schema_version') != '0.5A' or not s.get('project_id'):
        raise ValueError('INVALID_PROJECT_STATE')
    c = s.get('collaboration', {})
    if c.get('confirmed') not in (True, False):
        raise ValueError('INVALID_CONFIRMATION')
    if c.get('confirmed') is True and c.get('mode') not in MODES | LEGACY_MODES:
        raise ValueError('CONFIRMED_MODE_MISSING')
    if c.get('confirmed') is False and c.get('mode') is not None:
        raise ValueError('UNCONFIRMED_MODE_CANNOT_BE_SELECTED')
    support=s.get('support',{'depth':'adaptive','coaching':'adaptive','selected_by_user':False}) # legacy v0.5A session
    if not isinstance(support,dict) or support.get('depth') not in SUPPORT_DEPTH or support.get('coaching') not in COACHING or support.get('selected_by_user') not in (True,False):
        raise ValueError('INVALID_SUPPORT_STATE')
    if s.get('learning', {}).get('active_stage') not in STAGES:
        raise ValueError('INVALID_ACTIVE_STAGE')
    for entry in s.get('learning', {}).get('cards', []):
        _card_validate(entry['card'])
    if s.get('revision') != len(s.get('events', [])):
        raise ValueError('REVISION_HISTORY_MISMATCH')
    if s.get('events') and any(ev.get('type')=='choose_mode' and ev.get('actor')!='user' for ev in s['events']):
        raise ValueError('MODE_MUST_BE_USER_CHOSEN')
    return True


def compact(s: dict) -> str:
    audit(s)
    selected = s['collaboration']['mode']
    mode = MODE_LABELS.get(selected, '待用户确认（教学/决策/方案推进）')
    phase=s['learning']['active_stage']; title=STAGE_NAMES[phase]
    if selected == 'guided':
        depth=s.get('support',{}).get('depth','adaptive')
        position=f'[当前教学] {phase} {title}（讲解深度：{depth}）→ [待用户选择] 练习/评审/下一阶段'
    elif selected == 'decision':
        position='[当前] 决策关键未知与证据闸门 → [候选] 有条件推进/暂缓/核验'
    elif selected in ('project', 'review'):
        position='[当前] 用户研究方案完善 → [候选] 资料/执行/分析/报告（按授权）'
    else:
        position='[待确认] 三模式协作方式 → [候选] 研究问题/证据/决策'
    return f"业务推进图 r{s['revision']}｜需求界定 → 协作方式：{mode} → {position}；O/E/D/V 范围须独立确认"


def _private_output(p: Path):
    """Never write within an installed Skills tree or the public repo.

    The installed ZIP may be extracted under ANY parent (including /tmp), so
    treating a fixed ancestor as a repository would block legitimate private
    output paths near an installation.
    """
    skill_root=Path(__file__).resolve().parents[1]
    skills_root=skill_root.parent
    public_root=skills_root.parent
    r=p.resolve()
    protected=[skills_root]
    if (public_root/'PUBLIC_FILE_MANIFEST.json').is_file():
        protected.append(public_root)
    if any(r == base or base in r.parents for base in protected):
        raise ValueError('PRIVATE_STATE_MUST_BE_OUTSIDE_PUBLIC_SOURCE')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command', choices=('init','apply','audit','view'))
    ap.add_argument('--input',type=Path)
    ap.add_argument('--event',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--project-id')
    args=ap.parse_args()
    if args.command=='init':
        s=initial(args.project_id)
    else:
        if not args.input:
            raise ValueError('INPUT_REQUIRED')
        s=json.loads(args.input.read_text(encoding='utf-8'))
        if args.command=='apply':
            if not args.event: raise ValueError('EVENT_REQUIRED')
            s=apply(s,json.loads(args.event.read_text(encoding='utf-8')))
        else: audit(s)
    if args.output:
        _private_output(args.output)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(compact(s) if args.command=='view' else json.dumps({'ok': True,'revision':s['revision'],'mode':s['collaboration']['mode'],'cards':len(s['learning']['cards']),'support':s.get('support',{'depth':'adaptive','coaching':'adaptive'})},ensure_ascii=False))

if __name__ == '__main__':
    try: main()
    except (ValueError,FileNotFoundError,json.JSONDecodeError) as exc:
        print(f'FAIL: {exc}',file=sys.stderr);sys.exit(1)
