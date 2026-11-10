# 能力交接协议：UXDA 核心与扩展能力协同

## 当前已启用的能力

| id | 能力 / 扩展组件 | 可做的输出 | 状态 |
|---|---|---|---|
| EB-01 | `Specialist` (人因专项评审) | D / E / D+E（包含输入充分性检查、工效学计算与界面走查） | UXDA 内置核心能力 |
| CT-01 | `contextual-task-opportunity-discovery` | O / 机会发现、需求重构、遗漏情境、候选方案 | v0.2.2-rc1，可选配套扩展 |
| FV-01 | `focused-experience-validation` | 可选 V / 定向研究方案、研究资料回流、复现分析与决策更新 | v0.1.0-rc1，可选配套扩展 |

上述三项以外的候选能力尚未安装，不要虚构组件存在。UXDA 内部保持各模块专业规则。

## 传入的逻辑上下文（不是强制 JSON 表单）

- `output_mode`: O / D / E / D+E / O+D+E（若确有必要） / 直接回答小问题。
- `requested_decision`: 想确认的选择及备选项（如有）。
- `product_context`: 仅来自本次用户输入的产品/定位、用户与情境。
- `consumer_context`: 本次决策是否涉及购买者/付款者/使用者/维护者差异、相关消费阶段、替代方案和触点；未经确认的市场用户习惯不得变成事实。
- `market_scope_and_comparability`: 目标国家/地区、品类、细分群体、渠道、统计窗口、数据可比性、已核验的地域依据和未知。
- `decision_trace`: 当前可采取的选择、影响选择的关键 O/E 发现及其事实/推论/假设等级、可靠反例和逆转条件。
- `task_and_material`: 用户目标、可见设计事实、设计流程、实际观察，标注来源及可访问性。
- `constraints`: 明确提供的成本、技术、安全、隐私、时间等限制；未知不得补造。
- `critical_baseline`: 对当前选择至关重要的技术/能力/认证前提，其来源（用户明确提供、材料可核、未确认）和缺失影响；不猜低阶/高阶默认配置。
- `counterfactual_options`: 若 A 类能力成立则倾向什么、若 B 类能力成立则倾向什么；只有结论会逆转才触发优先追问。若无必要，不对用户展示完整内部字段。
- `readiness`: D、E、O、可选 V 按各自任务的充分/局部充分/阻断，以及最小缺口。
- `new_information`: 当前回合新增/修正了哪些事实。
- `evidence_mode`: 当前可用的是设计事实/任务与场景资料/公开依据，还是另外包含真实用户证据；**有无真实用户数据不决定 Skill 能否运行**。
- `empirical_claim_gap`: 只有在请求真实用户发生率、偏好分布、行为效果等特定实证结论时标注该项缺口，不阻塞其余 D/E 分析。

- `presentation_preference`: 当前任务的明确载体选择/已拒绝选项/未指定及仅提供的推荐；建议不等于生成授权。只有明确要求或用户接受 H5 推荐，且宿主可创建文件时才生成 HTML。

**输出规则**：Router 不是分析报告正文；对最终用户只显示专业 Skill 的有用成果或最小追问，不输出完整交接字段。若不能可靠加载专业 Skill，明确说明未执行对应 Skill，不得将普通回答伪称 Skill 结果。

**证据表达**：设计事实、用户观察、理论依据、条件性推断、未知必须保持可区分。体验 E 仅有设计材料时使用“体验预评估”；真实研究证据也仅报告其覆盖范围。

**O→D/E 最小交接**：只传用户原始目标、材料可确认事实、1–3 个关键候选机会、各自反例/基线状态以及它们会改变哪种已有 D/E 判断。不能把“候选”升级为“用户真实需求”，不复制重复长报告。

- `continuation_candidates`: 仅在存在可行动的下一步价值时，依据本案例的已知决策瓶颈提出 1–3 个彼此不同的选项；不能默认填满。`custom_next_step` 始终接受自然语言输入，优先于模型上一轮的建议。


## v0.4B V bridge
For specific decision-sensitive evidence gaps, optional handoff to `focused-experience-validation`: provide decision ID/choice, O/E/D claim, the single missing decisive evidence, relevant consumer scope and status. User may decline a study. On returned evidence, update only impacted claims and decision, with provenance and a reversal reason.
