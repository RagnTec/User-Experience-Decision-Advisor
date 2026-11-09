# Cross-domain Experience Fusion | v0.4B.2

**Purpose**: produce a decision-relevant understanding of a consumer's *underlying goal, mental model, perceived costs, expectation gap, and alternatives* from heterogeneous evidence. This is a **reasoning discipline**, not an independent personality classification, a proprietary consumer model, a predictor of behavior, or a license to borrow another company's data.

## Start from the outcome, not the interface
1. **Decision**: What concrete choice is open? Include keep/status quo and scope-limited alternative, if feasible.
2. **Actor and journey**: Who experiences the issue? Distinguish buyer, payer, user, caregiver/maintainer, and directly affected others; select only decision-relevant stages.
3. **User goal and friction**: Separate explicit feature requests from goal, observed behaviors, inferred psychological need and alternative explanations. A stated desire for "AI assistance" may instead reflect uncertainty, inaccessible status information, low confidence in next steps or actual need for human escalation. None is a verified user need without suitable evidence.
4. **Mechanism bridge**: Use one or two applicable constructs such as predictability, control, mental-model fit, recognition, effort, feedback, perceived risk/trust, recovery, or social context. State task-level cause pathway and countercase. Do **not** infer diagnosis, personality, motivation hierarchy or a population preference from a feature description.
5. **Experience history and competitor learning**: Identify direct competitors (same offering), indirect competitors (different offering fulfilling a similar goal), substitutes (including no product/manual workaround), and relevant analogous services. Compare *how the user goal is met*, not brand features. Include both exemplar and failure modes; do not claim actual competitor behavior unless observed/source-backed.
6. **Transfer test**: Write the common mechanism, structural similarities, consequential differences, non-transferable assumptions, source quality, expected effect *as hypothesis*, smallest check, and what would reverse the candidate. Similar visual appearance or common industry rhetoric alone never licenses transfer.
7. **Attitude–behavior triangulation (optional)**: VOC, satisfaction and NPS identify expressed perceptions/recommendation intention for a defined instrument, sample, stage and time. Pair with task/usage/contact or transaction data **only when legitimate linked data exist**. Separate direct quote, respondent count, mentions, actor and window; absence of data is normal and cannot block conditional analysis.
8. **Return to choice**: Each major fused finding must change, qualify, or confirm one decision candidate and give a reversal condition. Do not generate unbounded "innovation" lists.

## Transfer gate (required if analogy changes recommendation)
| Gate | Required check |
|---|---|
| Source observation | Did we actually inspect a competitor, or is this a hypothetical pattern? Cite an accessible source when factual. |
| Shared structure | Same **task / outcome and cognitive or service mechanism**? Show at least one meaningful similarity. |
| Context mismatch | What differences in user, severity, environment, trust, reversibility, incentives or channel could break it? |
| Scope | What *principle* could transfer versus what surface design cannot be copied? |
| Decision consequence | What option would change, and what contrary observation would overturn transfer? |

If source is hypothetical, label `candidate_analogy`; do not write "industry best practice", "users of X prefer", or an actual product feature. Direct and indirect competitors are **sources of questions**, not proof of target-market needs. Explicitly distinguish competitor *claims* vs *verified user experience*.

## NPS and satisfaction interpretation (only if actual data supplied)
- Do not request NPS just to fill a framework. If given 0–10 likelihood-to-recommend data, the conventional promoter/passive/detractor groups are 9–10 / 7–8 / 0–6; score = 100 × (promoters – detractors) / valid responses. Record instrument wording, brand vs transaction scope, time, market, recruitment/selection, response rate when available, unit and exclusions.
- An individual 0–10 response is **not** an individual NPS score. NPS is an aggregate of a defined sample. It is not general satisfaction, a diagnostic of a specific failure, actual advocacy, causal driver of retention, or automatically comparable across countries/cohorts.
- Examine score **distribution and verbatim reasons** and, when legitimately available, observed experience/behavior. Segment only when denominator permits; no unsupported causal "driver analysis". Regression/correlation, if run, require assumptions and cannot alone establish causation.
- NPS improvement or promoter proportion alone does not establish demand for the user's proposed feature. Link the *specific task and explanation* to an option and list other plausible causes.

## When not to use fusion
- A clear one-button usability question with no relevant other-task analogy.
- User expressly requests a narrow, nonexploratory answer.
- A weak analogy adds no decision-relevant information.
- A confidential prior case would be needed: do not use or paraphrase it. Create an independent generic hypothesis instead.

## Minimal output (one short block if used)
**Goal/psychological hypothesis → evidence status → direct/indirect/substitute comparison → transferable mechanism and mismatch → impact on decision → reversal condition.** No artificial numeric scoring and no invented respondent observations.

## Public methodological basis (verify when needed)
- ISO 9241-210:2019 human-centred design (user goals, use context and the whole experience): https://www.iso.org/standard/77520.html
- Nielsen Norman Group, Competitive Usability Evaluations (including tangential offerings): https://www.nngroup.com/articles/competitive-usability-evaluations/
- Catrambone & Holyoak (1989), analogical transfer (bibliographic lead only; DOI page not accessible in this review, original claims require fresh verification): https://doi.org/10.1037/0278-7393.15.6.1147
- Bain, NPS calculation and interpretation (measurement, not causality): https://www.netpromotersystem.com/about/measuring-your-net-promoter-score/

## Authority before analogy transfer

A cross-industry analogy does not carry legal authorization, certification, standard applicability or permission to depart from an established industry convention. Use [Jurisdiction & Norms Gate](jurisdiction-and-norms-gate.md) before recommending migration, and flag any convention-breaking design as an unapproved proposal requiring human review.
