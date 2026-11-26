# Analysis and statistics: reproducible interpretation without false certainty

Use for data review, metric interpretation, experiment results, survey analysis, or synthetic demonstrations. Run actual code for calculations when available.

## 1. Audit the data before analyzing

Record:

- source, authorization, date, version, and whether data are real or synthetic;
- row/observation unit and whether observations are nested or repeated;
- inclusion/exclusion criteria;
- duplicates and retries;
- missing, censored, failed, and out-of-scope records;
- group sizes and branch denominators;
- instrument, scale, language, and scoring rules;
- known instrumentation or coverage changes.

Never silently drop failures, missing values, or extreme observations. Report counts and rationale. Use sensitivity analysis when a reasonable alternative rule could change the conclusion.

## 2. Denominators and units

For every rate, state the denominator and eligibility. A participant can contribute multiple tasks; a task is not an independent participant. Repeated measures require paired, clustered, or mixed handling as appropriate. When outcomes are missing, report complete-pair results separately from all-observed results; sensitivity bounds that treat missing outcomes as all failures versus all successes are bounds, not imputed estimates.

For funnels, define exposure, step order, time window, deduplication key, and orphan events. Aggregate counts cannot reconstruct individual paths without reliable linking IDs.

## 3. Descriptive results

Report raw counts with percentages. Include sample size, missingness, and variability. Use medians and IQR for skewed durations; means may be supplementary. Do not report only successful-task times without failure and missing-time counts.

Outliers may be valid difficult cases. Flag them using a stated rule and show results with and without their influence. Do not remove them automatically.

## 4. Inference

Choose methods based on the design and measurement scale, not on a desired p-value.

- Non-significance is not equivalence. An equivalence claim needs a predefined equivalence margin and an appropriate analysis.
- Statistical significance is not practical importance. Report effect size and uncertainty interval where supported.
- Do not assert low power from sample size alone. Power depends on design, outcome, effect, variability, and test.
- One-sided tests must be justified in advance by the question and tail.
- Correlation and observational associations do not establish causation.
- Multiple outcomes, subgroups, and peeking increase false-positive risk; pre-specify or adjust transparently.
- Non-probability samples do not automatically prohibit sample-level tests, but population generalization requires an appropriate sampling argument.

For small samples, prefer transparent descriptive results and exploratory comparisons over confident hypothesis tests. Exact methods may be useful for simple categorical designs, but their assumptions and interpretation still matter.

## 5. Qualitative coding and synthesis

Use this operational slice for interview, usability, open-text, or support evidence. AI may propose codes and summaries; the accountable researcher approves the codebook and interpretation.

1. **Fix the coding unit.** Choose participant-statement, event episode, session-task, or another unit before coding. Record source ID, pseudonym, timecode or locator, and language. Do not count repeated excerpts from one participant as independent sources.
2. **Version the codebook.** For each code record definition, inclusion/exclusion rules, positive example, and near-neighbor distinction. Keep `codebook_version` and a change log; do not silently redefine codes mid-study.
3. **Double-code a planned subset.** Two reviewers code independently before discussion. Choose the subset and coverage before looking at agreement. Record agreement and disagreements; an agreement statistic does not establish validity.
4. **Adjudicate without erasing history.** Preserve both original codes, the resolution, rationale, and reviewer. Update the codebook only when the disagreement exposes a definition problem, then recheck affected material.
5. **Retain negative cases.** Keep excerpts that contradict the emerging theme, including source and context. Report how many independent participants or sessions support and contradict a claim; do not convert theme frequency into population prevalence.
6. **Make saturation claims inspectable.** Record when new codes or meaningful variations stopped appearing, what material was reviewed, and remaining coverage gaps. Do not use a fixed interview count as proof of saturation.
7. **Separate observation from interpretation.** For each synthesized claim record the raw observation, analyst interpretation, alternative mechanism, disconfirming evidence, and decision implication.

A compact working sheet is available in [qualitative-coding](../assets/qualitative-coding.md). Use short de-identified excerpts only when authorized and necessary.

## 6. Survey analysis

Report item-level missingness and routing denominators. Do not combine items into a score unless the construct, item set, direction, and scoring rule are established. Check reliability and dimensionality only when the data and sample support them.

A single overall satisfaction item does not diagnose issue causes. NPS is not a causal mechanism. Kano requires appropriate paired functional/dysfunctional responses and classification rules; do not improvise categories from unrelated items.

Translation or market comparisons require evidence of measurement equivalence; identical wording alone is insufficient.

## 7. Synthetic demonstrations

Label synthetic data in the title, input manifest, output, and interpretation. Synthetic results can demonstrate code, denominators, or analytic choices; they cannot support product claims.

Do not turn illustrative zeros or placeholders into charts that imply observed performance. Keep raw synthetic inputs and reproducible scripts with the test artifact.

## 8. Reproducible workflow

1. Preserve the raw input and hash.
2. Write the data dictionary and analysis unit.
3. Apply explicit cleaning rules in code.
4. Produce counts, denominators, and missingness first.
5. Calculate descriptive and, if justified, inferential results.
6. Inspect sensitivity to outliers, exclusions, and model choices.
7. Write the interpretation separately from the output table.
8. State limitations and the minimum additional evidence needed.

Use `scripts/analyze_synthetic.py` for a small participant–condition–task table. It reports descriptive counts, complete-pair success, missing-outcome bounds, paired differences when possible, Tukey flags, and sensitivity summaries that exclude flagged rows without altering the primary results. The input column is `duration_seconds`; configurations using another unit are rejected rather than silently mislabeled.
