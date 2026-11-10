> v0.4D.5 routing override: new Router projects **always** show the four available O/E/D/V directions, identify likely scope, and ask whether the user confirms that scope before starting independent specialist paths. Existing clear wording is intent evidence, **not** scope-only consent. Once confirmed, retain the choice without repeated questioning. See [Router Scope Contract](router-scope-contract.md).

# Progressive Decision Collaboration | v0.3.3

## 目标

避免“一次给出很长的最终答案”剥夺用户对重点、材料和决策用途的控制；同时避免反方向变成四步强制向导。按**决策价值**选择真实需要的交互节点，在每个节点提供已知情况的初步判断、推荐、可跳过及自由输入。

## 节点选择：并非串行必经

| 节点 | 何时触发 | 提供什么 | 何时跳过 |
|---|---|---|---|
| A 决策范围 | 目标存在显著不同的业务决策（是否立项、方案选型、体验改善、风险界定等） | 指出已识别问题，给出 2–3 个与当前案例有关的具体决策方向及自由输入 | 用户明确目标/只问具体问题 |
| B 资料机会 | 某种已有资料能**直接改变**一个关键推论或选择 | 推荐 1–3 类针对性材料（见 optional-evidence-intake）；允许跳过、只提供摘要或去敏版本 | 所需证据充分、与任务不相关、已询问或用户明确不提供 |
| C 中途重点校正 | 已形成相反解释/不同用户任务/不同资源目标，继续其中一条会明显改变结论 | 先给局部发现与差异、推荐优先路径、自定义取舍 | 差异不重要，或用户已决定侧重点 |
| D 交付形式 | 结果复杂且不同受众理解需求差异大 | 推荐文字/H5/两者、面向对象及材料粒度 | 用户已指定，或短小文字足够 |

## 对话状态（概念字段，不是项目文件或对外 schema）
- decision_question：要支持的决策，不等于希望证明的结论
- decision_owner_or_audience：产品/设计/研究/跨部门/其他，仅必要时确认
- analysis_focus：当前优先分析的约束与体验维度
- accepted_sources：本轮已明确允许使用的来源及范围；未提供≠不存在
- evidence_offered_or_declined：用户已提供、暂无、暂不适用、拒绝，避免反复询问
- open_decision_critical_unknowns：会逆转方案选择的未确认条件
- provisional_claims：已可成立的阶段性判断及其依据、限制
- output_preference：用户确认的文字/H5/两者，保持用户控制
- next_checkpoint：真正需要用户参与才推进的一项，而不是全量字段清单

## 限制
1. 一般复杂任务优先 1–2 个高收益节点，确有实际价值可增加；不得通过连续分支强迫用户完成完整工作流。
2. 对用户明确“直接分析、无需问询”的指令，能给条件性有效建议就直接完成，必要关键事实才提出单个问题。
3. 先给阶段性信息：已经知道什么、哪两条合理分析路径、为什么询问会影响选择。中途不生成貌似最终的强结论。
4. 提供建议分支时永远允许“自定义目的/资料/重点”；宿主无自由输入控件就提示使用聊天框。
5. 用户跳过、拒绝、没资料时，依据现有事实继续专业判断，局限仅针对需要实证证据的断言；不无限追问。
6. 不能假设原生弹窗必定存在。使用真实工具支持的控件；否则 2–3 个短选项 + 自由输入指引。不要声称已弹窗。
7. 每项 O/E 重要发现都指向潜在业务/设计选择，而不仅罗列体验问题；D 说明备选项、选择条件、逆转条件，必要时给最小验证方式。研究保持独立，不为业务主张背书。

## 示例（虚构，不是固定模板）
用户：某公共服务终端要加入智能引导，希望评估是否值得做。
初步回应：已知目标是降低任务阻力，但“操作入口难找”和“操作中纠错困难”需要不同方案。当前更希望支持 `①是否投入引导功能` 还是 `②先找造成失败的核心环节`？也可以直接写其他目标。若已有任务流程图/错误反馈记录可以提供；没有就按概念预分析。
用户：先找失败环节，我有脱敏的任务日志。
继续：明确只读取此次授权提供的日志，核对字段和覆盖范围，提取与任务中断相关的可观察事实。随后再决定是否需要进一步问交互方案或输出形式。

## Preflight is not an extra compulsory wizard

Before recommending any user-initiated change, run [Jurisdiction & Norms Gate](jurisdiction-and-norms-gate.md) quietly as a risk-proportionate scan. Do not make ordinary users complete a long legislation/standard form; ask only jurisdiction/category when an executable compliance-sensitive conclusion depends on it. Present a user-visible human-review entry only when a nonbinding industry or organizational convention is deliberately being challenged. Existing answers and authorized local documents should be reused.
