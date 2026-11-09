# Decision-Centred Research Closure | D/E and combined reports

A D/E result is not finished when it lists an implementation design or a development API. Keep the UX research role: discover relevant task and expectation mechanisms, evaluate alternatives, separate uncertainty, then hand a conditional decision to accountable people.

## Required closing sequence

1. **Current decision state**: what can be supported now? Choose `CONDITIONAL_RECOMMENDATION`, `COMPARE/TEST_FIRST`, `HOLD_FOR_CRITICAL_FACT`, `MAINTAIN_STATUS_QUO` or `STOP`. Explicitly say what is *not* yet supported. Do not conflate user-facing default setting with automatic download, install or activation.
2. **The decisive UX reasoning**: tie recommendation to user task, perceived control, predictability, interruption, error recovery, cost or trust. Label facts versus hypothesis and show at least one credible countercase. Technical feasibility and legal review are constraints, not substitutes for UX conclusions.
3. **Most valuable next action**: select one action that changes choice; optionally suggest a second. It may be reviewing product behavior or an existing VOC dataset, not necessarily launching a study. Do not start any O/V branch without explicit scope confirmation.
4. **Targeted optional evidence**: name up to three possible user inputs and *what each would resolve* (e.g. update architecture to distinguish install/restart risk; opt-in and update logs to evaluate behavior; VOC or UX feedback to identify perceived control risks). Always permit no more data and a conditional conclusion.
5. **Ownership and decision trigger**: separate UX study/evaluation, technical feasibility, legal compliance and accountable release approval. Name the reversal trigger and how the main progress map changes. Avoid invented API names, numerical safety cutoffs or automatic approval.
6. **End state**: when enough is known, stop the research; when insufficient, preserve an explicit blocker, a bounded action, and an optional next user checkpoint. Do not end with a generic engineering task list or a report that abruptly stops.

## Response proportions

Brief: flow map + current advice + 1–3 research mechanisms + conditional decision + concise next evidence/owner checkpoint. High-risk complex D/E can be longer. In a folded H5 the decision state, evidence gaps, next step, and reversal condition remain visible above the fold; technical implementation detail belongs in expandable or owner-specific handoff.
