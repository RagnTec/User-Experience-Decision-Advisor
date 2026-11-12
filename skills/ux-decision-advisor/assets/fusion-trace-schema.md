# Fusion Trace (private optional working artifact) | v0.4B.2

A JSON structure for a traceability *preflight*. It is **not** an AI confidence score, psychometric diagnosis, scientific truth certification, or source-verification engine. Its fields are designed to make transfer assumptions and an NPS computation auditable.

```json
{
  "case_id":"synthetic_example_id",
  "synthetic":true,
  "decision":{"question":"...", "options":["keep","pilot"],"current_recommendation":"...", "reversal_condition":"..."},
  "target":{"actor":"...","task_goal":"...","journey_stage":"...","market_scope":"..."},
  "sources":[{"id":"SRC1","kind":"case_input|public_primary|public_secondary|hypothetical|synthetic","locator":"synthetic case brief or real citation"}],
  "need_hypotheses":[{"id":"N1","goal":"...","candidate_need":"...","mechanism":"...","evidence_status":"hypothesis|partially_supported|observed","alternative_explanation":"...","decision_effect":"..."}],
  "analogies":[{"id":"A1","relation":"direct|indirect|substitute","source_domain":"...","source_pattern":"...","source_status":"hypothetical|documented","source_ids":["SRC1"],"shared_mechanism":"...","similarities":["..."],"differences":["..."],"non_transferable":"...","falsifier":"...","target_decision":"...","recommendation_strength":"candidate|supported"}],
  "nps":null
}
```

`nps` can be null. If present, record `instrument`, `unit`, `market_scope`, `survey_window`, `sample_size`, `promoters`, `passives`, `detractors`, `reported_nps`, `sampling_limitations`, `claim_scope`, `causal_claim` (must be false). Additional stage, source and segment information is encouraged. Do not input raw respondent PII into a portable trace; do not store private traces in the public GitHub source.

**Validator availability:** The current public package does **not** include `fusion_trace_check.py`. This schema is provided as a reference specification; do not assume automated validation is available. Any independent schema or numeric-consistency checks must be implemented and verified separately. Such checks cannot establish the truth of source claims or analogies.
