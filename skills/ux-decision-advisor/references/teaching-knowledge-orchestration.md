# Guided Knowledge Orchestration | v0.5C — methods and cross-disciplinary reasoning inside the project

**Goal.** Teach beginners, prospective researchers, career switchers and vertical-domain practitioners to conduct and defend a consumer UX study, not to memorize a dictionary or consume a general lecture. This protocol is for `guided` mode. `decision` and `project` remain distinct; users in those modes may request an explanation without changing mode.

## Mandatory two-layer teaching selection

1. **Universal UX research foundation**: distinguish business goal / user problem / solution assumption; who uses, buys, pays and is affected; research question / construct / observable variable; qualitative vs quantitative, attitude vs behavior, sampling and representativeness; method fit; measurement validity/reliability; bias, ethics and privacy; analysis trace and limits; business decision implication. Teach *only* the foundational elements needed for the present stage.
2. **Conditional interdisciplinary bridge**: choose **zero to two** additional perspectives that materially sharpen this problem (at least one meaningful foundational or interdisciplinary bridge in each substantive guided stage). Explain `discipline → relevant concept in ordinary language → connection to this user task → research implication / measurable question → alternative explanation or misuse → source status`. More disciplines do **not** imply better research. If a link cannot be justified, omit it.
3. **Product/domain lens**: explicitly identify the user's product category only if provided/grounded; otherwise mark product context **unknown**, and ask only the material missing detail. Identify domain-specific task constraints and user roles; distinguish product characteristics from inferred regulatory obligations, engineering requirements or generalized market facts. See [Product-domain Teaching Map](product-domain-teaching-map.md).

**Never introduce the whole knowledge tree automatically.** Begin with one causal/research reasoning thread and one learner challenge. Offer `基础释义 / 思路拆解 / 方法操作 / 进阶争议 / 实战演练 / 来源复核` as natural-language depth choices only when useful. The learner may request deep end-to-end explanation; adapt detail to their explicit request, *never infer or permanently label their proficiency based on occupation, age, or question style*.

## Context-triggered disciplinary lens map (options, NOT all required)

| Domain | Trigger in a real research question | Teachable bridge and resulting research question | Typical overreach to avoid |
|---|---|---|---|
| **Research methods & statistics** | Claims about rates, behaviors, effects, needs or comparisons | Construct/operational definition; recruitment frame, denominator, coding and counterexamples; which evidence would change a decision? | Assuming a survey estimate generalizes to every user, or qualitative quotes establish prevalence |
| **Cognitive / social psychology** | Perception, recognition, mental models, habit, motivation, trust, choice, emotion | Attention/memory/feedback; perceived control and decision contexts; distinguish stated attitudes from observed task behavior | Diagnosing psychology from UI alone; claiming 'users all feel X' without participant evidence |
| **Sociology / social context** | Household/shared device, group norms, roles, social hierarchy, community practices | Social roles, situated context, interpersonal power and norm formation; who controls, who bears consequences, whose account is absent? | Demographic/cultural stereotypes; treating a family or country as a homogeneous user segment |
| **Marketing & consumer behavior** | Paid vs free tiers, acquisition, switching, purchase/usage separation, retention | Segmentation, perceived value, consideration vs usage, customer lifetime context; are buyers, users and payers the same? | Mistaking conversion, NPS, or brand preference for a single feature's causal effect |
| **Communication / information theory (applied)** | Notifications, warnings, onboarding, instructions, cross-device communication | Sender/receiver context, message interpretation, signal/noise, feedback and comprehension; does the recipient notice and understand the message? | Assuming a message was understood merely because it was sent/delivered |
| **Media / platform studies** | Feeds, creators, recommendations, social sharing, publicity, misinformation | Distribution gatekeeping, framing, media literacy, algorithmic visibility and audience selection; who is exposed and why? | Treating platform engagement data as representative of the entire population, or treating correlation as persuasion effect |
| **Human factors / ergonomics / HCI** | Driving, multitasking, safety-sensitive interactions, wearables, accessibility | Task demands, attention allocation, interaction costs, error recovery, environment and capability variability; what failure is observable? | Inventing design threshold, vehicle safety interlock or mandatory clause from a generic principle |
| **Specific product domain** | Automotive, smartphones, ecommerce, IoT, games/media, finance, health-related or children/family products | Domain task topology, context and constraints; which mechanisms transfer across products and which do not? | Applying a familiar industry rule/UX metric as an unverified universal prescription |

## Seven-stage integration with explicit progress

- **S1 Problem framing**: teach demand vs proposed feature vs evidence of need; psychological construct and possible market motive only if they explain the ask. Practice rewriting a *researchable*, not solution-leading question.
- **S2 Users / social / market contexts**: separate purchaser, payer, operator, bystander and affected third parties; choose sociology/marketing or communication lens as indicated. Practice mapping roles and omissions.
- **S3 Hypotheses & mechanisms**: differentiate mechanism hypothesis, observed behavior, motive attribution and plausible alternatives; apply cognitive/social psychology selectively. Practice falsification.
- **S4 Method selection**: explain why interview, observation, survey, task study, analytics, field inquiry, controlled comparison or existing-document review is or isn't the smallest informative option. Teach attitude vs behavior and qual vs quant; no automatic data collection.
- **S5 Execution / analysis**: show question neutrality, sampling, respondent vs mention counts, audit trail, qualitative theme coding, simple descriptive statistics and uncertainty; reproducible steps for real data; separate practice data.
- **S6 Synthesis & trade-off**: connect valid findings with consumer segments, market conditions, communication consequences, accessibility and safety; compare maintain/change/experiment/stop without made-up ROI.
- **S7 Reflection & transfer**: learner independently explains why the study did or didn't change the decision, identifies one error and tests transfer to a **different product** with explicit similarity and boundary.

## Response micro-loop for every *meaningful* guided turn

`stage + user's current attempt → one useful concept (plain language) → why it is relevant / competing view → method and evidence path (including what cannot be established) → specific product/consumer context → actionable micro-practice or annotated example → targeted feedback or next learner choice → business/market decision linkage`.

A learner is not required to complete exercises to receive help. In live projects, advance the project deliverables alongside the method explanation; never gate delivery behind a mandatory exercise. For user requests to see the complete worked solution, demonstrate fully but mark observed vs hypothetical vs illustrative. In learner feedback, show **what they got right, the most consequential weakness, why it matters, a better next attempt**; do not reward verbosity or agreement. Track learning progress separately from project stage and external approvals.

## Offline epistemic boundary and sources

The knowledge map is a **curriculum/index**, not a database of asserted empirical outcomes. It works offline with stored text, user-authorized documents and marked methodological reasoning. **Never claim to have opened a source in the current offline session simply because the URL or citation is present in a bundled guide.** All user-specific or market-specific facts need genuinely supplied/inspected evidence; current laws, official standards, product specs, social statistics and scientific effect sizes need actual validation. Refer to [Teaching Source Guide](teaching-source-guide.md), [Citation Integrity Gate](citation-integrity-gate.md) and [Evidence Operation Modes](evidence-operation-modes.md). If the source is absent, explain the *concept* with a clear uncertainty label but do not invent citation details.

## Pedagogical quality gate (human + structural)

For each teaching stage the answer should let a reader explain **what problem we are researching, why this lens helps, how to test or observe it, what a result can/cannot mean, and how it changes a product decision**. Do not teach unneeded domains as decoration. Formal structure check in `mode_output_audit.py` enforces a relevant knowledge bridge + a product-domain applicability record, not factual truth or educational effectiveness. Independent novice transfer exercises remain necessary.

## v0.5D 可复用的离线 HCI 概念卡

按任务检索 `../assets/offline-ux-foundations.json` 中的原创摘要，优先仅选择 1–2 条相关概念。每条包含通俗解释、转化为可观察研究问题的方法、反例/边界以及精确的预置书目定位。来源具有不同审阅级别：Nielsen 原文与 NN/g 研究方法文章已审阅公开正文；About Face 仅出版社书目信息；Norman 为作者公开导读；ISO 仅公开摘要，禁止推出付费全文条款。用户自行补回相关权威材料后，按新内容修正，而非以自带资料代替用户的真实产品证据。
