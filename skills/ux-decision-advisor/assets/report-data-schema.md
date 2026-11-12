# 报告数据结构（离线 H5）

所有字段均由当前任务的分析输出构成，不得混入安装包固定产品知识。

```json
{
  "title": "当前任务标题",
  "subtitle": "产品、目标用户与任务",
  "scope": "设计材料预评估／真实用户研究总结",
  "recommendation": "一句结论与行动方向",
  "confidence": "依据范围：输入可核实的事实与条件；不可声称无依据概率",
  "decision_options": [
    {"name": "方案名", "benefit": "体验收益", "tradeoff": "代价/条件", "status": "推荐候选/保留/需验证"}
  ],
  "journey": [
    {"step": "任务步骤", "experience": "用户任务影响", "type": "已知事实/机制推断/待验证"}
  ],
  "findings": [
    {"title": "体验发现", "fact": "设计事实", "principle": "适用原则与机制", "action": "设计行动", "evidence": "证据类型"}
  ],
  "evidence": [
    {"title": "来源或材料", "note": "支持什么/不支持什么", "url": "可选的已核验公开来源链接"}
  ],
  "next_step": "最小下一步",
  "analysis_mode": "O | D | E | both | all (可选)",
  "problem_reframe": "当前需求与用户目标的区分（仅 O 使用）",
  "scenario_path": [
    {"step": "现有任务", "role": "已知", "description": "当前用户目标或设计事实"},
    {"step": "遗漏情境", "role": "待核查", "description": "条件化场景"},
    {"step": "候选机会", "role": "机会", "description": "可能改变的体验/设计动作"}
  ],
  "opportunities": [
    {"title": "候选机会", "gap": "遗漏的任务/情境", "rationale": "适用机制与为什么有价值", "action": "具体动作", "boundary": "适用条件或反例", "evidence": "设计事实/机制推断/待验证"}
  ]
}
```

- `status`、`type`、`evidence` 为标签而非自动评分。
- 没有真实量化数据，页面只提供比较卡和任务链，不生成百分比图。
- URL 只可使用经确认的 http(s) 来源，不能插入本地隐私路径；UI 以安全纯文本渲染。

**兼容说明**：`opportunities` 和 `scenario_path` 均可省略，旧版 D/E JSON 仍可生成并切换原有视图；仅 O 时不展示空白 D/E 面板。`analysis_mode` 仅作为默认视图提示，内容存在性决定是否提供可选视图。


## v0.4B optional V (evidence return; always private generated output)

`validation` is **optional** and must come from actual computed analysis or clearly labeled synthetic pilot. Example field shape, not actual numbers:

```json
"validation": {
  "evidence_origin":"synthetic",
  "task_outcomes": [{"label":"A","n":0,"success_pct":0}, {"label":"B","n":0,"success_pct":0}],
  "themes": [{"code":"coder-defined label","mentions":0,"respondents":0}],
  "quant_note":"Design, denominator, and sampling note",
  "qual_note":"Coding unit, source row references, and reviewer caveat",
  "boundary":"SYNTHETIC / NOT EMPIRICAL or actual study scope",
  "update_status":"DOES_NOT_RESOLVE",
  "decision_impact":"What remains open / why the recommendation changed or not"
}
```
The supplied zeros are placeholders, not research statistics. Bar widths are computed from `success_pct` and only rendered for positive `n`. Chart presence cannot establish causality, population representativeness, study quality, or correctness. The older D/E/O JSON is backward compatible. Avoid raw interview quotes by default; all populated reports are private project artifacts.


## v0.4D.1 可选法规与行业惯例摘要

当当前建议涉及具体地域的约束、上市判断或行业惯例突破，可在**私有输出**中增加 `constraint_gate` 对象（例如 `jurisdictions`、`applicability_status`、`binding_requirements`、`conventions_proposed_for_review`、`review_owner`、`implementation_not_authorized`）。此对象是**可选展示字段**；当前渲染器未专门实现该对象的独立卡片，不能声称网页会显示未被渲染器支持的内容。必须在 `recommendation`、`confidence` 或 `next_step` 的可见文本中保留具有决策影响的合规疑义与人工确认要求。


## v0.4D.2 optional business-progress snapshot

To show the **user-approved or explicitly provisional business workflow at the very top** of the offline report, add `workflow_map` with `objective`, `revision`, `current_step`, and an array of `steps` (`id`, `title`, `role`, `state`, `confirmed`, `recheck`, `next_input`, `evidence_refs`). This is a **read-only snapshot**, not a live workflow editor. The actual private full history is maintained by Router `scripts/workflow_map.py` and stays outside public sources. The renderer checks snapshot status/IDs; it does not assume a plan step implies project authorization. Old reports without `workflow_map` are unaffected. Use text/Mermaid in chat without requiring H5.


## v0.4D.3 optional research_summary

For an explicit first-screen UX synopsis, provide an optional `research_summary` object with `mechanism`, `mechanism_status` (`observed|supported|hypothesis|unknown`), `evidence_status`, `decision_condition`, optional `focus`. It summarizes already-grounded research, never invents studies or percentages. Older payloads remain valid. The first screen is concise; O/E/D/V professional details and traceable sources remain accessible in individual expandable sections, via expand-all, and in print.

## v0.4D.5 用户明确授权的分析范围

新版本的 Router 项目报告应在 `workflow_map` 中嵌入私有流程记录的 `analysis_scope`：`{"detected":["O"],"selected":["O"],"confirmed":true}`。若有该字段但未确认，则不允许生成完整 O/E/D/V 研究报告；若选中 O，`decision_options`、`journey/findings` 或 `validation` 等未授权专业板块不能一并渲染。无该字段的历史数据继续兼容，但**不能据此声称用户已确认路线**。报告顶部可显示已确认方向，初始路线及其未确认状态应先在 Router 对话中表达，不要通过伪造报告数据绕过。

## v0.4D.9 引用真实性约束

`evidence[].url` 只能附上经实际访问和内容检查的公开 HTTPS 页面，不应为示例域名、占位符、仅有书名的检索页或打不开的 PDF。若填写 `url`，需要 `source_status: "CONTENT_INSPECTED"`、`source_title`、`source_publisher`、`source_locator`、`source_retrieval_ref` 与 `support_excerpt`；这只用于保护 H5 结构，不能证明元数据不是模型伪造。没核实的文献可以以 `note` 标记待核实，但**不得显示可点击的假链接**。法规及标准结论还需具体条款、适用范围和当前版本。额外的私有 Claim Ledger 可用共享 `citation_integrity.py` 校验；离线 H5 不会访问外部网站。
