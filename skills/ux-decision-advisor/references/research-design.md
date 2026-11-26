# Research design: an executable, decision-linked protocol

Use for a new study, a review of an existing plan, a constrained pilot, or a research brief. Include only the sections that change the decision or execution.

## 1. Background and decision

- Business context and current decision.
- Product/version, affected users, tasks, and environments.
- Existing evidence, its provenance, and what it already answers.
- Constraints: time, people, budget, recruitment lead time, prototype/data access, and release schedule.
- Consequences of deciding incorrectly and reversibility of the proposed change.

Translate broad aims (“improve experience”) into answerable research questions. Do not write a hypothesis that merely restates the desired conclusion.

## 2. Objectives, questions, and hypotheses

A useful research question identifies the population or context, phenomenon, and comparison or condition when relevant.

Maintain a small hypothesis set:

| Hypothesis | Mechanism | Observable prediction | Disconfirming evidence | Method |
|---|---|---|---|---|

Separate product hypotheses (“the entry is overlooked”) from psychological mechanisms (“the label does not match the user's mental model”) and from measured outcomes (“entry discovery rate”).

## 3. Method strategy

Compare at least the serious alternatives, including “no new study” when evidence already exists. For each option state:

- claim it can support;
- claim it cannot support;
- resource and calendar demand;
- bias and feasibility risks;
- reason for selection or rejection.

Use mixed methods only when each component has a distinct job. Sequence existing evidence → low-cost pilot → larger or more controlled study as needed.

## 4. Participants and recruitment

Define:

- eligibility and exclusion criteria tied to actual exposure or task experience;
- segment coverage and rationale;
- recruitment channel, screening burden, incentives, and lead time;
- sample target and what it is based on;
- attrition, no-show, replacement, and over-recruitment assumptions;
- representativeness limits and who is systematically missing.

Do not invent a sampling frame or claim representativeness from convenience recruitment. A recruitment screener is a measurement instrument; pretest it.

## 5. Tasks, materials, variables, and controls

For qualitative work, specify the concrete event to reconstruct, stimuli, probes, and observation focus.

For usability work, specify:

- realistic user goal without leaking interface labels;
- start state, data, device, and allowed help;
- success anchor, partial completion, failure, and recovery;
- timing boundaries and assistance rules;
- prototype fidelity and unrepresentable states.

For experiments, specify:

- independent variables and levels;
- dependent variables and measurement instruments;
- constants, randomization, allocation, and blinding where relevant;
- order/counterbalancing, task equivalence, learning, fatigue, and contamination controls;
- analysis unit and repeated-measures structure.

For analytics, specify event semantics, IDs, time windows, deduplication, missing links, exposure denominators, and privacy constraints. Unimplemented events are proposals, not existing telemetry.

## 6. Measures and analysis plan

Distinguish construct, operational indicator, source, and scoring rule. Pre-specify:

- primary and secondary outcomes;
- one primary analysis unit per metric; never mix users, sessions, and tasks in the same denominator, and report alternative units separately;
- descriptive summaries and denominators;
- inclusion/exclusion and missing-data rules;
- outlier handling and sensitivity analysis;
- qualitative coding unit, versioned codebook, double-coding subset, disagreement adjudication, and disconfirming cases;
- inferential method and assumptions only when the design and data support it;
- effect sizes, uncertainty intervals, and practical importance criteria when relevant;
- subgroup analyses and multiplicity limits.

Do not choose a test after seeing favorable results. Do not delete failures or outliers merely because they weaken the hypothesis. For synthetic demonstrations, label every result synthetic and do not infer real product effects.

## 7. Ethics, consent, and data management

Proportionate to the study, cover:

- purpose, voluntary participation, withdrawal, and compensation;
- consent for recording, quoting, and future use;
- privacy-sensitive data minimization and access control;
- retention, deletion, anonymization, and cross-border limits;
- safeguarding and escalation for vulnerable participants or hazardous work;
- employer/worksite permissions and avoidance of coerced participation;
- whether observers, supervisors, or product teams could influence responses.

Do not collect real participant data or access private materials without explicit authorization. A research plan is not permission to execute it.

## 8. Resources and schedule

Build a realistic calendar that includes recruitment, scheduling, piloting, instrument revision, data cleaning, analysis, review, and reporting—not only sessions.

| Stage | Owner | Dependency | Earliest feasible date | Fallback |
|---|---|---|---|---|

If a dependency is missing, offer a downgrade and narrow the claim. Examples:

- no external recruitment → internal structural walkthrough; no claim about target-user rates;
- static prototype only → cognitive walkthrough; no claim about network, sensor, or recovery behavior;
- no telemetry → proposed event specification; no claim that events exist;
- no comparable tasks → exploratory comparison; no clean quantitative superiority claim.

## 9. Evidence-to-decision link

For each primary result, state what it would change:

| Evidence pattern | Interpretation | Decision consequence | Remaining uncertainty |
|---|---|---|---|

Include a stop condition when further work cannot change the decision. Do not turn a study into an automatic launch gate.

## 10. Final protocol check

- Is every method tied to a live question?
- Can the team actually recruit, prepare, run, and analyze within the calendar?
- Are success, failure, missingness, and analysis units defined?
- Are consent, privacy, and data permissions explicit?
- Are learning effects, shared bias, and strongest alternatives addressed?
- Does each expected result connect to a real decision or a justified stop?
- Are fallback and conclusion limits stated?
