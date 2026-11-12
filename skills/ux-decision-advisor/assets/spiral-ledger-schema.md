# Optional private Spiral Decision Ledger: minimal schema v1

Machine-readable ledger is **optional for substantial decisions**, not a form users must fill. Place only in an authorized **private** directory, never alongside GitHub/public Skill code. Examples below are generic; do not place actual organization, respondent, document excerpts, company mapping, or raw observations in public tests.

```json
{
  "schema_version": "1.0",
  "decision_id": "example-local-id",
  "data_origin": "synthetic",
  "decision_question": "Which initial service path is worth a bounded comparison?",
  "options": ["retain current flow", "compare guided flow", "defer"],
  "rounds": [
    {
      "round": 1,
      "evidence": [{"source_id": "spec", "sha256": "64 lowercase hex digits", "origin": "synthetic", "role": "design_spec", "access": "SYNTHETIC_FIXTURE"}],
      "claims": [{"id": "c1", "kind": "HYPOTHESIS", "status": "CONDITIONAL", "source_ids": ["spec"], "statement": "The proposed design might create a discoverability risk", "decision_link": "Compare understanding before replacement"}],
      "changes": [{"claim_id": "c1", "change": "NEW", "basis": "NEW_EVIDENCE", "source_ids": ["spec"], "reason": "Initial design description"}],
      "decision": {"action": "compare", "readiness": "EVIDENCE_GAP", "unknowns": ["task understanding"], "rationale": "Only design claims exist", "reversal_trigger": "Users misunderstand both alternatives"},
      "next_step": {"type": "REQUEST_DOCUMENT", "discriminating_question": "Are prior task observations available?", "potential_decision_effect": "Could allow us to avoid unnecessary study", "gate": "WAITING_FOR_USER"}
    }
  ]
}
```

`data_origin`: `synthetic`, `user_provided`, `mixed`; the code rejects `empirical_claim=true` when case data are synthetic. Each round lists **current active evidence snapshot** (stable `source_id`; source `sha256` updated on change) and **current claims snapshot** (stable claim IDs). `changes` identify important additions, revisions, confirmations or withdrawals since previous round. `basis`: `NEW_EVIDENCE`, `CORRECTION`, `CONSTRAINT_CHANGE`, `NO_CHANGE`. A material change of claim or recommended action cannot cite only `NO_CHANGE`. Evidence references for `NEW_EVIDENCE` must exist in the current snapshot and differ from the previous snapshot, or be accompanied by an explicit `CORRECTION`/`CONSTRAINT_CHANGE`.

`decision.readiness`: `SCOPED`, `EVIDENCE_GAP`, `DECISION_READY`, `HANDOFF`. `decision.action`: `retain`, `modify`, `compare`, `pilot`, `defer`, `stop`, `escalate`. `decision.unknowns` may be nonempty even when a **bounded** pilot is the choice; it may not be described as fully proven or outcome-observed. `next_step.type`: `SYNTHESIZE_EXISTING`, `CHECK_CONFLICT`, `REQUEST_DOCUMENT`, `PROPOSE_FOCUSED_V`, `PROVISIONAL_DECISION`, `HANDOFF`. User/external data steps require `gate=WAITING_FOR_USER`; analytical steps use `gate=NONE`. A `HANDOFF` step requires `stop_reason` in `READY_FOR_HUMAN_CHOICE`, `WAITING_ON_EXTERNAL_EVIDENCE`, `NO_MATERIAL_GAIN`, `USER_STOP`. Neither `DECISION_READY` nor `HANDOFF` means empirical confirmation.

`spiral_audit.py` emits issue codes and round/claim positions only, no raw text. It checks referenced source IDs, round succession, source/version deltas, unsupported/verified labels, material updates, premature empirical claims, handoff and no-gain loops. Passing establishes **schema/temporal coherence only**. It is not an independent UX-quality verdict.

`evidence[].access` must explicitly be `USER_PROVIDED`, `AUTHORIZED_LOCAL`, `VERIFIED_PUBLIC`, or `SYNTHETIC_FIXTURE`. This records an authorization/provenance **claim**; the structural checker cannot independently verify permission or ownership. Real-case records must not mark simulated fixtures as real observations.

Stable claim IDs must include `claims[].statement`. Changing a statement, evidence list, source status or decision impact requires a documented `REVISED`/`RETRACTED` entry, not a silent prose rewrite. When a user declines to supply materials, `HANDOFF` with `USER_STOP` is permitted without inventing new evidence.


## v0.4D.1 constraint re-check trigger

Across rounds, a new jurisdiction, product classification, audience, collection channel, version or material change affecting regulations or standard applicability must trigger a fresh authority check of the dependent decision branch. An optional local [Constraint Gate Record](jurisdiction-gate-schema.md) can be linked from a **private** project record; do not put real regulatory interpretations or company exception approvals into the public Skill repo. This is separate from proof of legal compliance.
