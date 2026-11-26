# Method selection: match the method to the claim

Use when deciding whether research is needed, comparing methods, or explaining why a method fits. Do not default to interviews, surveys, or experiments.

## 1. Start from the decision-critical unknown

Classify the unknown:

- **Existence or mechanism**: what happens, how users understand it, why a task breaks down.
- **Frequency or distribution**: how often, among whom, across which conditions.
- **Comparative effect**: whether a change improves a pre-specified outcome.
- **Causal mechanism**: whether changing X changes Y under controlled conditions.
- **Feasibility or risk**: whether a flow, device, or environment can support the task.

If existing records, reproducible inspection, or prior applicable evidence can answer it, review those first.

## 2. Capability and boundary map

| Method | Best suited for | Does not establish by itself | Typical cost / main risk |
|---|---|---|---|
| Desk research / evidence audit | applicability, contradictions, known methods | current users' behavior or preferences | low; source quality and transfer bias |
| VOC / support-ticket analysis | language, reported failures, candidate mechanisms | prevalence among silent users; technical root cause | low–medium; exposure and selection bias |
| Semi-structured interview | mental models, context, sequences, reasons | population rates or causal effect size | medium; recall and social desirability |
| Contextual observation | real tasks, workarounds, environment | hidden attitudes or causal effect | medium–high; observer effect and access |
| Focus group | vocabulary, norms, idea reactions | private behavior; independent individual views | medium; conformity and dominance |
| Survey / concept test | structured self-report, attitudes, segment differences | observed behavior, task time, causal uplift | medium; wording, sampling, common-method bias |
| Usability test | task blockages, errors, recovery, comprehension | production conversion or long-term preference | medium; artificial tasks and small-sample limits |
| Task / cognitive task analysis | knowledge, decisions, strategies, workload demands | actual frequency or preference | medium; analyst interpretation |
| Behavioral analytics / funnel | observed frequency, paths, drop-off | intent, subjective experience, causality | low if instrumented; tracking and denominator errors |
| A/B test | causal effect of a deployed change on defined metrics | why it worked; long-term or untested outcomes | medium–high; traffic, contamination, ethics, power |
| Controlled experiment | causal effect of manipulated variables | field generalization without validation | high; construct validity and artificiality |
| Human-factors evaluation | physical/cognitive fit, error risk, constraints | legal compliance or universal thresholds | medium–high; calibration and context |
| Mixed methods | complementary scale and mechanism questions | automatic triangulation or independence | high; integration and shared bias |

## 3. Selection questions

For each candidate method, answer:

1. What exact claim could this method support?
2. What claim would be overreach?
3. What population, task, context, and version does it cover?
4. What bias or measurement artifact could mimic the expected result?
5. Is there a lower-cost method that answers the same decision?
6. What result would change the recommendation?

Prefer the least complex method that can discriminate the live alternatives. A method is not better because it is more formal.

## 4. Qualitative design

Use interviews or observation when the unknown is meaning, sequence, context, or mechanism. Anchor in a recent concrete event. Ask what happened before interpreting why it happened.

- Distinguish behavior reconstruction from opinion and self-diagnosis.
- Use neutral probes: “What happened next?”, “What did you expect?”, “Where were you looking?”
- Record disconfirming cases and alternative paths.
- Define coding unit, codebook, reviewer process, and source traceability when formal analysis is needed.
- Small qualitative samples do not estimate population proportions. Saturation is a design judgment, not a universal number.

## 5. Survey design

Use surveys for structured self-report, not as a substitute for observed task performance.

Before fieldwork, check:

- one construct per item;
- neutral wording and balanced response options;
- single- versus multi-select semantics;
- mutually exclusive options only where exclusivity is real;
- coverage of “not applicable,” “do not know,” and opted-out paths;
- complete skip logic and branch denominators;
- recall window and exposure eligibility;
- sampling frame, self-selection, language/translation equivalence, and missing items.

Pretest wording and routing with a small number of appropriate reviewers. Do not treat pilot responses as population estimates unless the sampling design supports that claim.

## 6. Comparative usability and experiments

For two or more designs, first decide whether the goal is formative friction discovery or a quantitative comparative claim.

- **Within-participant** designs reduce between-person variance but introduce order, learning, fatigue, and carryover.
- **Between-participant** designs avoid direct condition learning but require attention to individual differences and usually more participants.
- Counterbalance order when appropriate. AB/BA or Latin-square balancing does not guarantee elimination of learning effects.
- Use equivalent tasks only if information, difficulty, and cognitive load are genuinely comparable. Otherwise acknowledge task–condition confounding.
- Pre-specify primary outcomes, task success anchors, timing start/stop, errors, assistance, and analysis unit.
- Do not claim superiority from a tiny formative sample. Report observed differences and uncertainty without manufacturing significance.

## 7. Sample rationale

There is no universal correct sample size. State the purpose and basis:

- qualitative: coverage of relevant segments, mechanisms, and variation;
- formative usability: risk-based discovery across key tasks and user types;
- survey: sampling frame, expected variability, precision or subgroup needs, nonresponse;
- experiment: primary outcome, design, allocation, expected effect or smallest relevant effect, variability, attrition, and power method.

If power cannot be calculated responsibly, say so. Do not assert that a design is underpowered merely because it is small. A small pilot can still be valuable for feasibility, instrumentation, and friction discovery.

## 8. Mixed methods

Combine methods because they answer different questions, not to decorate a report. Define the integration point: which quantitative pattern needs which qualitative explanation, or which hypothesis is tested by which source.

Check independence. Two analyses of the same respondents or copied support summaries may share bias. Label complementary evidence, shared-bias evidence, and independent replication accurately.
