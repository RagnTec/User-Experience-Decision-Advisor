# Optional machine-readable Decision Record (v0.4A)

For substantial decisions, the Agent may structure a *local/private* JSON document matching the illustrative fields below. Users should not be required to fill this file for a normal chat. The fields are generic, independently designed, and **not a company mapping, export mechanism or business schema**. Do not publish populated records from real projects.

```json
{
  "decision": {
    "question": "Which initial interaction path should be compared?",
    "options": ["keep simple navigation", "introduce guided entry"],
    "current_action": "compare",
    "cross_market": false
  },
  "claims": [
    {
      "id": "E1",
      "text": "A guided entry could reduce initial discovery effort under the specified task assumptions.",
      "source_type": "METHOD_BASED_INFERENCE",
      "support_status": "CONDITIONAL",
      "evidence_refs": [],
      "decision_impact": "Consider a bounded comparison before choosing the entry path.",
      "reversal_condition": "If the task is already familiar and repeated frequently, a guided path may add unnecessary steps."
    }
  ]
}
```

- `source_type`: USER_PROVIDED, OBSERVED, VERIFIED_EXTERNAL, METHOD_BASED_INFERENCE, ASSUMPTION, UNVERIFIED.
- `support_status`: SUPPORTED, CONDITIONAL, UNSUPPORTED. Neither status is a probability or measured confidence score.
- `current_action`: retain, modify, compare, pilot, defer, stop, escalate.
- For `cross_market: true`, add `market_scope: {"markets": ["target market label"], "comparability_note": "Product and segment match not yet checked"}`. This alone does **not** establish comparability.
- An externally verified claim needs `evidence_refs`; the presence of text here cannot prove a source was actually opened or accurately interpreted.

The optional offline structural checker is `scripts/decision_audit.py --input /path/outside/public/repo/decision-record.json`. It prints only issue codes and claim **positions** to avoid printing business content. It cannot authenticate web citations, decide regulatory compliance or prove market demand.

For legal/industry-norm-sensitive decisions, optionally link to a **separate private** [Constraint Gate Record](jurisdiction-gate-schema.md). Its checks do not certify legal compliance and do not authorize implementation. In quick UX chats the preflight is conversational, not a mandatory file upload.
