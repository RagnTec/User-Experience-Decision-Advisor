# Entry Mode Contract | v0.5B — select learning collaboration before O/E/D/V

## First turn, one human choice

For EVERY NEW project routed through UXDA, start with a compact **业务推进图** (`需求描述 → [当前] 协作方式选择 → 界定研究问题/基础规则预检 → 用户确认 O/E/D/V → 分阶段研究与证据更新 → 阶段复盘/业务取舍`). This is an overview, NOT a list of pre-authorized branches or completed work.

**Before doing deep O/E/D/V work**, offer three modes in clear language, one question, not a long questionnaire:
- **教学引导 Teaching (`guided`)**: 由学习者参与并同步获得方法解释；每个阶段阐明研究逻辑、机制与取舍，同时推进当前任务增量；不以强制练习阻断项目交付。
- **决策支持 Decision (`decision`)**: 根据已有资料给出当前有边界的专业判断和下一步决策，充分利用已有知识和用户授权材料；不牺牲证据质量。
- **方案推进 Project (`project`)**: 由用户提供初步研究想法/方案，Agent 保留原思路，在方法、招募、材料、数据分析及报告环节协作完善；评审只是推进过程的一环。原有 `review` 历史模式按本模式执行。

If the user **explicitly named a mode** in their current message, that is the user's confirmation. Do not ask again. If they explicitly named O/E/D/V too, accept that scope selection without extra round. If they named only an analysis capability (e.g., “做 O”), record detected scope but still ask which collaboration mode, and then confirm O/E/D/V **in a single compact follow-up when possible**. No deep specialist outputs while mode/scope required for a new project remain unconfirmed. Brief safety alerts and bounded preliminary issue framing are allowed. Once mode or scope is established, substantive analytical evaluations, causal claims, and decision gates must load and follow [analytical-quality](analytical-quality.md) and [evidence-boundaries](evidence-boundaries.md).

**All modes share**: baseline jurisdiction/platform/industry applicability triage, current user/market/task context, O/E/D/V scope authorization, offline-first user-supplied documents, full citation verification, decision ledger, human permission for optional studies and branch changes, accurate business-progress status. Mode is *how to collaborate*, scope is *which analysis to execute*, format is *how to present*; never conflate these independent selections.

## Same project, mode can change

Only an **explicit user statement** confirms `guided`/`decision`/`project` or switches mode. Save before/after mode events in a **PRIVATE** session record; preserve O/E/D/V scope, claims, evidence, history, approvals and current stage. Never reinterpret model recommendation as user approval. User's teaching question inside decision mode is a temporary explanation, NOT mode switch unless requested. Direct calls to a professional Skill should respect the mode contract when a new UXDA project is being initialized.

No mode can authorize a study, public browsing, scraping, deployment, legal waiver, hardware design or data disclosure by itself. Mode switch does not silently advance progress. The user may skip/reopen any learning stage with reason, without losing what was already learned or observed. Do not infer educational level from queries or label user a novice.

## Mode-specific response behavior

| Moment | `guided` | `decision` | `project` |
|---|---|---|---|
| First scoped step | Ask learner to distinguish business request vs research question, with a short example and method rationale | Present available provisional facts, decision-critical unknowns and action options | Identify what the user proposed and what has actually been provided; separate research plan from real results |
| Evidence/method | Explain why method fits, what it cannot establish, what alternative was rejected and why; give traceable sources or explicit unverified status | Use smallest useful evidence path; do not require full curriculum | Co-refine hypotheses, sampling, methods, instruments and reproducible analysis, with targeted critique |
| Turn finish | State the project increment, method rationale, current evidence boundary and next actionable step (include micro-task/quiz only if user explicitly requested learning exercise) | State current decision boundary, 1–2 useful actions and next user choice | Show revised research artifact, data/report readiness, next user input and decision link |

For `guided`, reference [Guided Research Learning Path](guided-research-learning-path.md) and [project-collaboration](project-collaboration.md); in other modes, offer a contextual explanatory sidebar when asked without re-routing the whole project. See [Teaching Stage Card](../assets/teaching-stage-card.md). The compact map is visible in each substantive turn, learning reasoning available on request; suppress generic lecture dumps.

For mode-differentiated workflow and artifacts, read [Mode Execution Contract](mode-execution-contract.md); `project` additionally follows [Research Project Co-production](research-project-coproduction.md).

## v0.5D 任务级支持选择（可选，不另设模式）

先选择 `guided`/`decision`/`project`。只有使用者需要不同讲解方式时，才提供一句简短选择：①从基础解释 ②直接讲研究实操 ③专业机制和证据复核 ④保持适度、随时追问；另可直接要求自己先尝试、看示范或共同完成。不得通过岗位、语言、学位猜测能力。使用者已说明想法或偏好时不重复确认。熟练研究员面对陌生产品也可以选择基础；入门者也可请求高级讨论。详细规范：[Adaptive Learner Support](adaptive-learner-support.md)。所有支持方式的更新不改变 O/E/D/V、用户审批或研究事实。

遇到缺少资料时，允许当前有边界的研究分析，并通过 [Evidence Discovery Guidance](evidence-discovery-guidance.md) 生成**可由用户选择**的 1–3 个主题和可回传内容，不把推荐链接冒充实际检索。离线知识只能使用有来源范围的 [Offline UX/HCI Foundations](offline-knowledge-use.md)；文件位于 `../assets/offline-ux-foundations.json`。
