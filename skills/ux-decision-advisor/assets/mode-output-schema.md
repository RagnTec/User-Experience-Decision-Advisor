# Mode-specific output record (private JSON) | v0.5C

A serious user project can optionally save the **minimum structured trace** for each substantive turn, for offline auditing. This is NOT a public report schema and never stores raw interviews, respondent quotes, real product documentation or personal data in the GitHub repository. The companion `mode_output_audit.py` validates **structure**, not reasoning correctness or source existence.

Required shared fields: `project_id` (nonblank string); `mode` (`guided`, `decision`, `project`; historic `review` is accepted as `project`); `progress_map` (nonblank, truthfully labelled); `scope` (nonempty list of the explicitly user-confirmed O/E/D/V selections; no inferred tracks); `evidence_boundary` (nonblank: verified vs hypothesis/unverified limits); `next_user_checkpoint` (nonblank; may be a stop reason).

`guided` fields (v0.5C addition; represents the meaning of an actual teaching step, **not** a verified empirical outcome):
- `teaching_depth`: `foundation` / `applied` / `advanced` / `adaptive`, controlled by request, never inferred as a permanent user attribute;
- `knowledge_bridges`: 1–3 **relevant** records `{discipline, concept, task_link, research_implication, limitation, evidence_status}`. Discipline in `research_methods`, `psychology`, `sociology`, `marketing`, `communication`, `media_studies`, `human_factors`, `product_domain`. Evidence status `method_principle`, `supplied`, `verified_external`, `hypothesis`. If verified external add `source_locator`, `examined_scope`, `verification_event_id` (metadata still does not prove the source was opened);
- `domain_lens`: `{product_type, use_context, special_consideration, verification_boundary}`; mark unknown clearly where the product is not given, do not guess a target market or platform. These fields are required by the structural audit for guided output. This does NOT mean every discipline must appear.
- `stage` S1..S7 and `learning_objective`;
- `concepts` list of `{term, explanation, relevance}` in simple words;
- `reasoning_steps` list of `{question, reasoning, evidence_status, alternative}`;
- `method_choice` `{method, why, alternative, alternative_tradeoff, cannot_establish}`;
- `learner_exercise` `{prompt, assessment_criteria, example_is_synthetic}`;
- `decision_link` describing real business relevance. Advanced explanations must be provided on request; *verified_web* claims require a source trace in the actual linked evidence system.

`decision` fields:
- `decision_point`, `options` (>=2), `gate_status`: `GO`, `CONDITIONAL_GO`, `HOLD_FOR_CRITICAL_INFO`, `BLOCK_PENDING_SPECIALIST_REVIEW`, or `NO_DECISION_NEEDED`;
- `gaps` list of `{dimension, issue, consequence, source_status, impact_on_choice, owner}`; dimension one of legal, mandatory_standard, voluntary_standard, industry_practice, human_factors, consumer_market, technical, business. Source status `verified`, `supplied`, `inference`, `unverified`;
- `decision_rationale`, `reversal_conditions`, `evidence_requests` (0..3) with each `{item, decision_use}`;
- `responsible_owner`, `actual_business_approval` boolean (always false in a skill-generated record unless verified separate user/organization authorization and recorded as external evidence). Do not use `verified` without actual source locator, scope and access record under the separate citation gate.

`project` fields:
- `user_proposal` and `user_input_status` (`user_provided`, `partial`, `needs_input`);
- `research_stage` (`define`, `design`, `collect`, `analyze`, `report`, `revise`);
- `work_product`, `refinements` list of `{aspect, proposed_change, rationale, approval_status}`; approval status `suggested`, `user_confirmed`, `rejected`;
- `data_status` (`no_data`, `real_authorized`, `synthetic_practice`, `supplied_summary`), `analysis_method` and `analysis_trace` (required when real_authorized; link to actual results in *private* files);
- `report_status` (`outline`, `draft_with_data`, `reviewed`), `findings` list, `decision_link`;
- if `no_data` or `synthetic_practice`: `findings` MUST be empty and `report_status` `outline` (no real outcome claim). A user-supplied already-written study may be revised, but its claims retain original source status until audited.

Shared: no mode selection implies user approval of a study, deployment, legal exemption or extra research track. The user can switch modes without deleting existing records.

CLI: `python skills/ux-decision-advisor/scripts/mode_output_audit.py --input /private/record.json`. For actual UX data validation, additionally use V analyzer and citation checks. This checker cannot certify legality, empirical validity, statistical accuracy, or that a claim was actually checked online.

For an existing report without row-level data, set `data_status: supplied_summary`, add `source_report_locator` and `analysis_claims_recomputed: false`. You may critique the supplied author claims but must not present them as independently recomputed or empirically verified.
