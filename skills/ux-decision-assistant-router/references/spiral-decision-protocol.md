# Spiral Decision Loop | v0.4D | shared O/E/D/V protocol

## Goal and meaning of "self-closing"

The agent should be able to **plan and perform bounded reasoning rounds** with evidence already authorized and available, revise an answer when evidence changes, and reach a meaningful **decision-support checkpoint**. This does NOT authorize unattended user recruitment, web crawling, contacting people, changing business systems, approving business investments, or working in the background. An external-input gate is a valid and often necessary stop, not a failure to close the loop. Do not create fictional respondents or claim real UX effects from generated data.

## One decision, several evidence-conditioned rounds

For a consequential case, retain one private running Decision Ledger (informal in chat or optional machine-readable JSON). Each round must answer:
1. **Decision focus:** who will choose what, among which actionable alternatives including maintain/defer; what cannot yet be concluded?
2. **Evidence delta:** which authorized source, method, assumption or user constraint is new/updated/withdrawn? File existence and citations are not proof of correctness.
3. **Claim delta:** which prior claim is NEW / REVISED / UPHELD / RETRACTED; what changed it; which claims did NOT change? Never silently upgrade HYPOTHESIS or INFERENCE to OBSERVED/PROVEN.
4. **Choice delta:** did the candidate action change, remain conditional, or remain unresolved? A no-change result may be correct.
5. **Highest-value next step:** use an existing document or already-available data first; select focused V only if a consequential unknown might change the choice. Say what plausible finding would reverse the choice. Offer hold/skip and free-text correction.
6. **Stop/hand-off:** deliver a bounded decision with conditions, or stop at an external/user permission gate. Do not keep iterating without evidence, a changed constraint, or a corrected analysis.

## Four decision-support checkpoints (not mandatory levels)

- `SCOPED`: the choice and user/task/market boundaries are established; initial assessment can be conditional.
- `EVIDENCE_GAP`: an explicit, decision-critical unknown prevents a more specific recommendation; offer the least burdensome evidence source, or a bounded provisional action.
- `DECISION_READY`: specific options, evidential limits, alternatives, reversal and action owner are explicit; human/business approval remains necessary.
- `HANDOFF`: iteration stops with either `READY_FOR_HUMAN_CHOICE`, `WAITING_ON_EXTERNAL_EVIDENCE`, `NO_MATERIAL_GAIN`, or `USER_STOP`. This is loop closure, not product outcome verification.

These are **epistemic workflow states**, not a monotonic user research maturity score. New contradictory evidence may move `DECISION_READY` back to `EVIDENCE_GAP`. Progress is measured by fewer *consequential* untested assumptions or a better-conditioned choice, not number of rounds, pages, or studies.

## Selection of next step

Use the highest-value *discriminating* action, not a blanket research menu:
- `SYNTHESIZE_EXISTING`: review already authorized product spec, internal/market notes, past research, coded feedback, available metrics; preserve provenance.
- `CHECK_CONFLICT`: reconcile contradictory sources or definitions before collecting more.
- `REQUEST_DOCUMENT`: invite at most 1–2 case-specific files; user may skip.
- `PROPOSE_FOCUSED_V`: produce neutral task/interview/survey plan **only if** meaningful evidence could change the choice. Never generate study results.
- `PROVISIONAL_DECISION`: articulate a bounded low-risk/reversible step with assumptions and reversal triggers.
- `HANDOFF`: stop requesting information if marginal decision value is weak, all available evidence is exhausted, or user has asked for finalization.

Choose the next step using *potential to reverse/qualify the decision*, importance of the decision, availability, burden and safety. Do not invent numeric value-of-information or statistical thresholds. If external permissions/files are required, explicitly request them and pause that branch. No self-directed endless tool loops.

## Reopen mandatory rule gate when context changes

If the product category, user population, jurisdictions, data flows, launch stage, regulation/standards version or relevant feature changes between rounds, revisit [Jurisdiction & Norms Gate](jurisdiction-and-norms-gate.md), retain the previous assessment as historical and mark affected recommendation/implementation branch for re-review. A newly approved convention challenge is not evidence of a legal exemption. Record a stopped/conditional branch if specialized review is pending.

## Cross-round integrity checks

- Keep stable claim IDs; do not change the meaning of an ID when rewriting text. Distinguish corrections from new empirical observations.
- Record evidence provenance, version, scope and synthetic/real status. Do not treat VOC mentions as representative counts; do not infer NPS causation or competitor generalizability.
- Each material claim revision needs an associated evidence or documented correction/changed assumption. Updating a product spec should flag **dependent claims only** for re-review, not mechanically reverse all decisions.
- Distinguish `analysis_complete` from `decision_authorized` and `outcome_observed`. Never falsely mark outcomes observed because the agent reached a recommendation.
- Private source documents, research records, excerpts and round outputs remain outside GitHub public source and install directories.

## Optional implementation and evaluator

Use the private `spiral-ledger.json` example contract in `assets/spiral-ledger-schema.md` and `scripts/spiral_audit.py --input /private/spiral-ledger.json`. This validator checks **temporal/structural consistency and common provenance errors**. It does not itself plan rounds, infer psychology, verify public sources, run a study, approve a decision or certify an independent Agent trial. The Agent must still do professional O/E/D/V reasoning and make its limits visible. Simple chat tasks do not need a JSON artifact.

## Incremental private version writing

For projects keeping optional JSON records, `scripts/spiral_append.py --ledger /private/ledger-v1.json --round /private/round-v2.json --output /private/ledger-v2.json` appends one user/agent-reviewed round after structural validation. Never overwrite the prior record. Optional `--v-update /private/decision-update.json` checks a returned V analysis digest and decision/action match before appending. This is an **audit bridge**, not automatic research, judgment or outcome measurement.
