# Business Workflow Plan | private schema and edit protocol

Optional private workflow map, separate from Decision Ledger. Real project plans must never be committed to the public repository, exported as synthetic examples, or included in install ZIPs. The workflow is editable through user-authorized *events*; every update creates a new versioned file.

## Initial proposal

```json
{
  "decision_id": "SYN_DEC_01",
  "objective": "Decide which fictional renewal explanation to test",
  "current_step": "rules",
  "steps": [
    {"id": "scope", "title": "界定待决策问题", "role": "core", "decision_link": "SYN_DEC_01", "depends_on": []},
    {"id": "rules", "title": "地域与平台规则预检", "role": "check", "decision_link": "SYN_DEC_01", "depends_on": ["scope"], "next_input": "目标市场及平台约束"},
    {"id": "analysis", "title": "比较用户任务与方案", "role": "core", "decision_link": "SYN_DEC_01", "depends_on": ["rules"]},
    {"id": "decision", "title": "形成条件性行动建议", "role": "core", "decision_link": "SYN_DEC_01", "depends_on": ["analysis"]}
  ]
}
```

`init` turns all steps into `candidate` and `confirmed=false`. Never infer historical approvals. `confirmed=true` requires an `actor=user`, `explicit_user_request=true` confirmation event. `progress` events require actual evidence references for completed/skipped states. Reopening or revising a confirmed/historically completed node requires explicit user action and a reason. `flag_recheck` marks a dependency at risk without silently reopening it.

## Event shape

```json
{
  "type": "confirm",
  "actor": "user",
  "explicit_user_request": true,
  "step_id": "scope",
  "expected_revision": 0,
  "reason": "User accepted this stage",
  "evidence_refs": [],
  "changes": {}
}
```

Valid event actions: `confirm`, `progress` (changes.state and actual evidence for completion), `reopen`, `revise` (only allowed stage metadata), `add` (explicit user request only), `flag_recheck`, `resolve_recheck`, `focus`. Exact constraints enforced in `scripts/workflow_map.py`. A state audit is **not** regulatory approval or research validity testing. No agent action may counterfeit `actor=user`.

## Presentation and consistency

- `current_step` identifies the stage currently under discussion; it does not authorize action.
- `role=optional` remains speculative until user confirms it. Nonoptional future steps still remain candidates until selected.
- `depends_on` expresses planning dependencies, not legal permission or automatic scheduling.
- `readiness` and `next_input` may describe evidence needed to decide whether to continue; they are **not** compulsory surveys/forms.
- `evidence_refs` are provenance locators, not raw personally identifiable content, raw VOC, or secrets.
- Every event stores a before/after version and current revision. Do not delete old versions; they allow user-initiated rollback and auditing.
- A structured Workflow Map complements Decision Record, Spirals and H5. A workflow milestone being complete does not imply its associated business decision is authorized, compliant or empirically validated.

## v0.4D.5 additional scope state and event contract

`analysis_scope` is separate from workflow steps. `detected` is an agent guess, `selected` can be populated **only** by user-authorized `scope_confirm` with `explicit_user_request=true`, and `confirmed` indicates whether the user has made this choice. A new plan starts with `selected=[]` and `confirmed=false`. Modes are a unique subset of `O,E,D,V`. Newly proposed optional studies or extra methods must **not** appear as preset steps. The user can explicitly `add` a branch, and any scope revision preserves event history.

Example (purely synthetic user intent):

```json
{"type":"scope_confirm","actor":"user","explicit_user_request":true,"step_id":null,"expected_revision":0,"changes":{"selected":["O"]},"reason":"User requested O only","evidence_refs":[]}
```

To mark a core stage not applicable, run an `assess_applicability` event with `changes.applicability="not_applicable"`, a case-specific reason and `evidence_refs`. Its compact visibility changes, but history is retained. `reopen_applicability` requires explicit user request and a reason. An inapplicable method may still lack necessary inputs; reopening never permits fabricating results.
