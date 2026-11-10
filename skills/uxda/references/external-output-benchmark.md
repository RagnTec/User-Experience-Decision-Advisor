# External Skills / repository comparison: evidence-first benchmark | v0.4B.1

## Purpose and boundary
External Skills, GitHub repositories, research platforms and general-model outputs are **comparators, not truth authorities**. Do not require exact agreement, automatically treat the longest answer as best, or adopt a third party's conclusion without checking primary sources. Compare **method quality, factual support, context fit, and decision consequences** instead of rhetorical similarity.

## Two independent checks
1. **Method / implementation**: inspect actual public skill instructions, referenced standards and code from an identified repository URL + pinned commit/hash and path (if accessible). Record date checked and license/provenance. Do not copy external source into our public project by default. Explain when the repository is inaccessible, incomplete, unlicensed, or not an actual UX research Skill.
2. **Output comparison**: give each comparator the same independent case, decision question, known facts, missing data, intended market/user, allowed tools and requested deliverable. Record model/version, tool/search access, run date and any unavoidable differences. Use withheld synthetic fixtures or licensed public case materials; do not upload the user's private project data to a third-party Agent without explicit authorization.

## Claim-level adjudication
For **each material disagreement**: record `decision_item`, ours vs external claim, the respective stated evidence and applicable source, `difference_cause` (`input_scope` / `source_quality` / `framework_applicability` / `assumption` / `stakeholder_weights` / `reasoning_or_math_error` / `unresolved`), and whether it changes the actionable decision. Status can be `reasonable_difference`, `ours_requires_correction`, `external_requires_correction`, or `unresolved_needs_evidence`.

A **reasonable difference** needs traceable assumptions, legitimate alternative weights or a distinct but stated interpretation. Differences rooted in unverified market facts, invented standards or incorrect calculations are errors, not creative 'perspectives'. When both lack evidence, mark unresolved and provide a narrow validation path, not a forced consensus.

## Quality criteria / release stops
- Grounding: material facts have actual sources or are labeled hypotheses; source truly supports the claim and is applicable to the specific product/market/time.
- Research method: appropriate sampling, task/construct, denominator, selection bias and limits; actual statistical methods when numerical data are present.
- Decision integrity: viable alternatives including status quo, explicit implementation context, reversible/irreversible risks and reversal condition.
- Independent research: avoids marketing/public relations pressure, adversarial strawmen and selectively ignoring unfavorable observations.
- Collaboration and usability: case-specific questions, optional evidence input, practical recommendations and no unnecessary mandatory research.
- Fatal failures: invented actual research results, false legal/safety compliance, confidential/private disclosure, or uncorrected major calculations/attributions.

Compare A (general AI, no skill), B (other relevant published skill), C (our package). Use independent scored reviews, preferably blinded and shuffled, with fixed model/settings where possible, repeated runs and original outputs retained. Never claim quantified superiority before running this protocol. Repo age, stars, license or apparent professionalism are not outcome accuracy metrics.

For structured trace, use private `comparison.json` and `scripts/quality_trace_check.py --comparison ...`; schema validation is not a factual verdict.
