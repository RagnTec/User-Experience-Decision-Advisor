# Research materials: concrete, reviewable, usable artifacts

Use when generating or revising a brief, interview guide, survey, screener, usability session, experiment matrix, metric dictionary, or report. Start from the user's actual product and supplied materials; do not replace them with a generic competitor study.

## 1. Research brief

A brief should make the decision understandable before method details:

- decision and owner;
- affected users, tasks, and context;
- current evidence and gaps;
- research questions;
- proposed approach and serious alternatives;
- constraints and dependencies;
- deliverable, audience, and decision date;
- scope exclusions and authorization needs.

If information is missing but analysis can proceed, use explicit conditional assumptions. Ask only for gaps that change the design.

## 2. Interview and focus-group guides

For interviews, build around a recent concrete episode:

1. context and trigger;
2. sequence of actions and observed artifacts;
3. expectations, interpretation, and feedback;
4. interruption, workaround, or recovery;
5. perceived consequences and alternatives;
6. neutral summary check.

Separate behavioral prompts from opinion prompts. A user's explanation is a subjective account, not automatically the objective cause. Record the source and confidence of each claim.

For focus groups, avoid asking for private behavior or forcing consensus. Use individual writing or round-robin responses before group discussion when domination is a risk.

## 3. Questionnaire review and revision

For each item, check:

| Check | Question |
|---|---|
| Purpose | Which construct or decision does this item serve? |
| Eligibility | Who can answer it accurately? |
| Wording | Is it neutral, single-barreled, and understandable? |
| Options | Do they match single/multi-select semantics and avoid overlap? |
| Coverage | Are not-applicable, do-not-know, and refusal paths available? |
| Routing | Does every option lead to a valid next item or end? |
| Denominator | Which branch population will interpret the result? |
| Interpretation | Is this self-report being kept distinct from observed behavior? |

When revising, show the original item, the concrete defect, the replacement, and why. Preserve unaffected items. If behaviors can coexist, split them into separate questions, anchor a single event, or use multi-select plus an importance question. Do not force “the main reason” when the study needs multiple contributors.

## 4. Recruitment screener

Screen for actual task exposure, relevant context, and necessary diversity—not desired opinions. Include:

- eligibility and disqualifying criteria;
- recent behavior with a defined window;
- product/version/device used;
- segment variables needed for coverage;
- availability, consent, incentive, and accommodation needs;
- quality checks that do not coach the desired response.

Check for fraud and professional participants without making the sample artificially homogeneous. Document who is excluded and how that limits inference.

## 5. Usability session

A usable session package includes:

- moderator script and consent reminder;
- participant profile and device/environment setup;
- task cards with realistic goals and start states;
- success/partial/failure anchors;
- observation fields for errors, hesitation, help, recovery, and quotes;
- timing and assistance rules;
- post-task ratings with exact wording and scale;
- debrief questions that do not lead;
- data handling and session-end steps.

Do not reveal button names in task instructions. Distinguish moderator interpretation from observed behavior. Think-aloud can change performance; use it deliberately and record the method.

## 6. Experiment and variable matrix

| Element | Specification |
|---|---|
| Design | within / between / factorial / other, with rationale |
| Conditions | exact product states and versions |
| Allocation/order | randomization, counterbalancing, contamination controls |
| Tasks | equivalence, difficulty, practice, and carryover |
| Primary outcome | construct, indicator, timing, success anchor |
| Secondary/guardrail | errors, recovery, complaints, trust, workload |
| Sample | target, rationale, attrition, segment coverage |
| Analysis | unit, pairing, missingness, model/test, practical threshold |
| Limits | learning, artificiality, sample, untested contexts |

Do not promise that counterbalancing eliminates learning. If task equivalence cannot be established, narrow the claim to exploratory differences.

## 7. Metric dictionary and event plan

For each event or metric, define:

- business/research purpose;
- trigger and exclusion conditions;
- event name and required properties;
- user/session/attempt identifiers;
- timestamp and time zone;
- exposure and deduplication rules;
- downstream completion anchor;
- missing-link and retry handling;
- privacy and retention constraints;
- implementation status: existing / proposed / unknown.

Never call a click a task success or a front-end trigger a completed file save unless the completion is actually observable. Shared menus need a sub-choice event if a specific feature is being measured.

## 8. Analysis and report materials

An analysis plan should be reproducible from raw input to reported table. Include cleaning rules, code or exact steps, denominators, effect summaries, qualitative traceability, and limitations.

A findings report should connect:

**objective → method/sample → observed result → competing interpretation → decision consequence → limits/next step.**

If no real data exist, produce a plan or clearly labeled synthetic demonstration. Never write “findings,” quotes, significance, or improvement direction without supporting observations.
