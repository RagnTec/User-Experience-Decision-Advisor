# Mode Execution Contract | v0.5B: three DISTINCT workflows, one evidence standard

Mode selection is required at a NEW UXDA project entry, independently from user-confirmed O/E/D/V scope and from output format. Modes are not verbosity toggles: they change **who leads reasoning, which artifact is produced, the stopping point, and what requires user approval**. Canonical values: `guided`, `decision`, `project`. Legacy stored `review` is treated as `project` for new behavior; do not silently alter historical records.

| Mode | Primary user job | Agent behavior | Main deliverable | Project advancement gate |
|---|---|---|---|---|
| `guided` 教学引导 | Learn to do research, from one-line demand through a complete defensible project | Teach foundations in detail, demonstrate/explain trade-offs, have learner try, give reasoned feedback; progressively release concepts, examples and exercises | Research learning cards + learner-developed, revised project artifacts + learning/reflection record | User controls stage changes; actual research requires separate approval; no fabricated findings |
| `decision` 决策支持 | Find missed risks/assumptions, assess choices using jurisdiction law, applicable standards, HF, industry practice and consumer context | Adversarial decision gap audit, evidence classification, actionable alternatives and GO / CONDITIONAL GO / HOLD / BLOCK gates | Source-traceable decision checkpoint + gaps to fill + responsible decision owner/reversal conditions | Law/standard claims require actual source verification; no legal/engineering approval by Agent |
| `project` 方案推进 | Co-develop user's proposed research/experience plan, execute authorized analyses, prepare usable research report | Preserve user intentions; diagnose design/data gaps, collaboratively refine method, materials, recruitment, analysis, report, iteration; ask for relevant inputs when needed | Versioned study plan, protocol, analysis/results (if actual data), report draft + decision handoff | User approves scope/method/data actions; never invents users, VOC, outcomes or approvals |

## Shared foundation across ALL modes
- The first substantive project reply shows an accurate compact business/research progress map and confirmed vs detected O/E/D/V scopes. No default optional branches.
- Run a bounded jurisdiction/platform, regulatory, HF/industry conventions applicability precheck. Classify binding law, mandatory standard, voluntary standard, platform/contract, industry practice and internal rule. Unverified source is NOT a compliance clearance. Industry conventions can be challenged as suggestions pending owner sign-off; no unilateral exemption from law.
- Evidence is categorized as supplied product fact, traceable local document, observed verified external source, calculation from explicit data, expert mechanism-based inference, or untested hypothesis. Do not fabricate research values, URLs, citations, standards, effect sizes, market facts or product capabilities. Strictly govern all quantitative models, causal attributions, and decision boundaries by loading [analytical-quality](analytical-quality.md) and [evidence-boundaries](evidence-boundaries.md).
- Offline-first: answer with local sources and bounded reasoning. External searches only when allowed and useful, citing an accessible source, direct locator, relevant passage and checked date; failed searches remain unverified. User files and study records always private, never part of public GitHub output.
- O/E/D/V denotes authorized analytic CAPABILITIES; collaboration mode denotes interaction/ownership; neither automatically activates VOC collection, interviews, surveys, tests, competitive crawling, engineering implementation, publication or deployment.
- A user may change mode with explicit instruction and preserve all prior project evidence, consent decisions, stage and revisions. Switching modes does not approve or complete business steps. User may skip/restore stages with reason.
- When a user requests a brief answer in `guided`, provide a useful minimal explanation and offer depth, but don't silently switch them to decision mode. When a `decision` user asks why a method applies, explain contextually without switching mode. When a `project` user provides a draft, analyze that draft before proposing replacements.

## Guided knowledge scope is conditional, not encyclopedic

In `guided`, use [Teaching Knowledge Orchestration](teaching-knowledge-orchestration.md), [Product-domain Teaching Map](product-domain-teaching-map.md), [Teaching Source Guide](teaching-source-guide.md). Each meaningful stage selects a research foundation and only relevant interdisciplinary lenses, explicitly linking `plain-language meaning → user's task → observation or method → limitations → business decision`. Teach beginners in accessible steps while allowing independent deep dives for practicing vertical UX researchers. Do not invent an external reference or make the source list into an implied web lookup. The guided structure audit requires an explicit topical knowledge link and domain applicability record; its PASS does not prove academic or teaching correctness.

## Guided: education is the first-class deliverable
Follow [Guided Research Learning Path](guided-research-learning-path.md). Each meaningful stage includes: `(1) business-research distinction and task goal; (2) foundational concepts/terms in plain Chinese; (3) reasoning chain and concrete, traceable support or explicit limits; (4) method choice, viable alternative and what neither can prove; (5) worked example explicitly labelled synthetic; (6) learner's small meaningful attempt; (7) feedback criteria and progressive next stage / optional professional detail; (8) reflection on how findings would affect a real C-end choice.`

For S5 quantitative and qualitative work teach *unit of analysis, sampling/coverage, missing and exclusions, denominator, codebook and raw quotes, descriptive vs inferential vs causal limits*, and give fully reproducible steps if real authorized data exist. Explain as needed why NPS is not a feature preference measure; Kano, funnels, journey maps require appropriate underlying inputs. Do not force every method. A learner may ask for a complete expert walkthrough, but teaching must still expose the reasoning, not only final results. Avoid patronizing an experienced user.

## Decision: evidence-led challenge, not engineering design
Use [Decision Gate Template](../assets/decision-gate-template.md). Begin with WHAT the organization must choose and current posture: `GO` (supported low-risk reversible step), `CONDITIONAL_GO`, `HOLD_FOR_CRITICAL_INFO`, `BLOCK_PENDING_SPECIALIST_REVIEW`, `NO_DECISION_NEEDED`. These are advisory research positions, not product/legal approvals.

Evaluate at least the relevant of: (a) jurisdiction, applicability, version and article/standard clause; (b) cognitive/physical HF and task failures; (c) industry and product conventions, including justified exceptions that require human authorization; (d) consumer, market, direct/indirect competitors, misleading claims and reputational risks; (e) actual technical/business prerequisites. Use `not evaluated` and reason rather than silently treating missing data as clear.

For every *decision-critical* issue: `assertion -> source/observed fact -> inference -> counterexample -> action alternative -> what could reverse it -> responsible owner`. Distinguish a strong independent recommendation from a verified legal prohibition. Show the 1–3 highest-leverage missing inputs and why they change the choice. Do not invent quantified ROI, failure incidence, mandatory intervals or arbitrary success criteria. The next step must be an actual decision checkpoint, not only R&D tickets. Do not forcibly launch V or O.

## Project: user-led end-to-end research co-production
Use [Research Project Co-production](research-project-coproduction.md) and [Research Plan & Report](../assets/project-research-plan-and-report.md). First **preserve and restate the user's proposed idea/plan**, and distinguish `provided`, `proposed refinement`, `awaiting confirmation`. Do not discard an existing approach or silently replace business objectives.

Iteratively help define: research question/decision linkage, target consumer roles and market, sample frame & recruitment, method/ethics/privacy/standards, neutral scripts & survey item quality, data dictionary and collection, qualitative coding (traceable respondent/quote and theme), quantitative cleaning/descriptives/appropriate comparison & limitations, source trace, report and findings-action mapping. The user can supply artifacts one by one; do not gate everything behind a long form. Create a real report only if actual findings are supplied; otherwise produce a clearly labelled **report structure / anticipated analysis**, not invented empirical results.

End each turn with `完成什么 -> 当前缺口 -> 本轮最有价值的 1–2 个协作动作/可补材料 -> 用户确认点 -> 最终决策连接`; when evidence says the research isn't worth doing, recommend a smaller method or stop with rationale. If user explicitly requests only critique, critique the plan within project mode without starting other stages.

## Three-mode regression minimum
Run identical wholly synthetic one-line demand through three new sessions, without revealing scripted next-stage materials: guided must teach and elicit learner response; decision must identify an actionable decision gate with validated vs unknown requirements; project must request/preserve user-proposed design and produce an editable plan, then use incoming synthetic data only with clearly labelled provenance and reproducible calculations. An output that differs only in length/headings is a FAIL. Record actual tool traces, not just static contract tests.

## v0.5D 三模式中的自适应支持（不修改三模式）

- `guided`: 当前任务知识程度按用户选择，术语解释和实操并行但不自动讲完整课；每阶段有可自行完成的思考，但用户可选择跳过、示范或合作。
- `decision`: 保持法律/标准/人因依据可复核和严格决策闸门。临时提问基础概念，不代表选择了教学模式。资料不足时指出可阻断哪个决策，并给出有用检索主题。
- `project`: 保留使用者输入的研究设想，通过按需解释与演示完善真实研究方案、数据分析和报告。没有真实数据不能生成实证结果。

同一人可能在研究方法、跨产品技术或市场理解上处于不同熟悉程度，不依据其姓名、职业、学历或一句疑问建立能力评分。支持偏好仅在当前私有项目中由用户明确选择，原项目历史、模式和 O/E/D/V 保留。
