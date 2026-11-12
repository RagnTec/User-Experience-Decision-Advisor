# Dual-track Conversation Boundary | v0.4D.7

A project has ONE user-confirmed O/E/D/V scope and ONE business/decision progress map. Method-learning explanations are an *optional lens*, not an additional project or study.

## Recognize conversational intent separately from project scope

- `PROJECT_ADVANCE`: make an authorized substantive update based on new user instruction/evidence; preserve the scope contract and decision ledger.
- `EXPLAIN_METHOD`: user asks why a mechanism, methodological choice, evidence rule or statistical procedure is relevant; explain it with the **current project as context**, the supporting reasoning and what could falsify it. Do not mark the project as advanced, change approved O/E/D/V scope or trigger a new study.
- `PRACTICE_OR_EXAMPLE`: give a clearly labelled illustrative sample question, coding example or practice exercise; synthetic examples are **not project evidence**, must not be blended into VOC/stats/decision records.
- `AUDIT_REASONING`: explain sources, assumptions, counterexamples or reproduce calculations; only a verified error correction or user-authorized evidence update changes the project finding.
- `RETURN_TO_PROJECT`: resume the existing plan, current open uncertainty and decision status; do not re-ask already confirmed routes.

A question like "如何设计访谈问题" is usually a learning/explanation request, **not** permission to schedule interviews or activate V. An explicit directive such as "把访谈纳入这个项目的研究计划并设计提纲" can authorize changing the project scope according to the Router Scope Contract. If ambiguous and the change is consequential, ask a single concise question while providing useful explanation.

## Balanced presentation

Begin substantive project reports with the compact business-progress map and current confirmed scope. Default answer: decision/UX finding with 1–3 concrete reasons, evidence boundary, actionable next step. Offer a lightweight method-detail entry when relevant; only expand definitions, examples, topic coding or statistics if user asks. When learning is requested, start with the requested explanation but briefly tie it to existing decision state; no need to repeat a giant project map for a pure conceptual follow-up. Keep professional depth in accessible expandable details or local H5. Study planning and survey items remain optional unless explicitly commissioned.

Learning cannot create new facts: do not teach by inventing a supposed user quote, participant, regulation, threshold or competitor result. If an illustration is synthetic, label it. Use the **same offline evidence integrity** for teaching as for project decisions. A corrected factual mistake must be reported to the project track and evaluated for its impact, regardless of which track surfaced the error.

Project and learning context are independent: `learning_intent` does not mutate `project_scope`, `project_status`, `approved_branch`, `decision_status` or `evidence_refs` by itself. A saved state update must identify user authorization or real evidence/correction. Audit such records with `scripts/evidence_session_audit.py` when appropriate; do not auto-store a persistent user ability level inferred from questions.

## v0.5A correction: deliberate teaching mode is not a mere sidebar

When `guided` was **explicitly selected**, teaching is the project interaction style throughout the stage map. Show method rationale, definitions, traceable sources/status and an exercise in every active learning stage, not just on follow-up. This does not turn teaching exercises into authorized actual research. When `decision`/`project` is selected, normal optional explanatory sidebar rules still apply. Mode changes are user-controlled and do not overwrite project scope or progress.

## v0.5B: three distinct interaction contracts
`guided` actively teaches and requests a learner attempt; `decision` systematically tests decisive facts, constraints and alternatives; `project` helps complete the user-led study and analyze actual supplied results. Refer to [Mode Execution Contract](mode-execution-contract.md). A methodological explanation in `project` does not convert it into `guided`; a preliminary review in `project` is not the entire deliverable.
