# Evidence Session & Learning Boundary Record | v0.4D.7

**Optional local-private audit metadata**, not a mandatory user-facing form. Save completed project records **outside** the publicly distributed Skills and GitHub repository. No source excerpt or sensitive data must be written merely to satisfy this schema. This record does not execute retrieval, enforce network isolation or prove source authenticity.

```json
{
  "network_mode": "OFFLINE",
  "external_search_performed": false,
  "user_forbids_network": true,
  "sources": [
    {
      "id": "S1", "kind": "LOCAL_DOCUMENT", "locator": "spec.md#section-2",
      "version": "draft-A", "scope": "synthetic product description"
    }
  ],
  "claims": [
    {
      "id": "C1", "claim_type": "PROJECT_FACT", "status": "LOCAL_DOCUMENT",
      "source_refs": ["S1"], "decision_strength": "PROVISIONAL",
      "applicability": "synthetic item; version draft-A"
    },
    {
      "id": "C2", "claim_type": "UX_MECHANISM", "status": "HYPOTHESIS",
      "source_refs": [], "decision_strength": "PROVISIONAL",
      "applicability": "to be checked against actual use"
    }
  ],
  "interaction": {
    "intent": "EXPLAIN_METHOD", "project_event": "NONE",
    "explicit_user_authorization": false
  }
}
```

Top-level `network_mode`: `OFFLINE`, `ONLINE_AVAILABLE_UNUSED`, `ONLINE_USED`. `external_search_performed` must be true **only** for `ONLINE_USED` with a real host trace. `user_forbids_network=true` prohibits online use. `LOCAL_DOCUMENT` sources must have a locator; `CURRENT_EXTERNAL` sources must identify publisher, exact HTTPS URL, retrieval time, locator and applicable market/version, and should also attach an actual host trace reference in `retrieval_record`. A link alone, or tool-call-looking prose, is not evidence of retrieval.

Claim `status`: `LOCAL_DOCUMENT`, `USER_STATED`, `DETERMINISTIC_RESULT`, `METHODOLOGICAL_INFERENCE`, `MODEL_BACKGROUND_UNVERIFIED`, `HYPOTHESIS`, `UNKNOWN`, `CURRENT_EXTERNAL_VERIFIED`. Strong current law/empirical/quantitative claims may only be treated as final if actual reviewed evidence, applicability and technical input warrant it. `decision_strength`: `PROVISIONAL` or `FINAL`; provisional is not false, final is not a compliance authorization. Neither status can establish market representativeness absent study context.

Interaction intents: `PROJECT_ADVANCE`, `EXPLAIN_METHOD`, `PRACTICE_OR_EXAMPLE`, `AUDIT_REASONING`, `RETURN_TO_PROJECT`. `project_event`: `NONE`, `SCOPE_CHANGE`, `EVIDENCE_UPDATE`, `DECISION_UPDATE`, `CORRECTION`. `EXPLAIN_METHOD`, `PRACTICE_OR_EXAMPLE` and `RETURN_TO_PROJECT` must not cause unauthorized mutation. The audit only checks this recorded separation; real interaction semantics require independent Agent tests.

**Reproducibility**: run `python scripts/evidence_session_audit.py --input /authorized/private/session.json`. Outputs issue codes and counts without printing full user content. No tool in this package automatically sends files or metadata to an external endpoint.
