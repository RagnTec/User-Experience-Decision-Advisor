# 路由中的证据研究与输出选择

Router 不直接代替研究工作，但在交接给专业 Skill 前判定分析需求：

- 用户资料是否已经能够回答？若能，直接进入专业分析，**不因为有网络工具而强制搜索**。
- 是否涉及准确时效事实、标准或法规？必要时标记 `PUBLIC_VERIFY`，并提醒后续核验版本和适用范围。
- 是否需要用户群体行为规律的外部实证？标记 `EMPIRICAL_SEARCH`，约束相关人群、任务和情境。
- 是否缺少本产品的关键设计状态、流程或重要技术边界？仅当这类事实会改变本次方向性判断时标记 `ASK_PRODUCT_DATA`；**无真实用户观察本身不触发追问**。若用户要求的具体结论必须由实测支持（发生率、偏好分布、效果量），才单独标记 `EMPIRICAL_GAP`，告知该项暂不能证实，但继续输出其他可支持的设计判断。
- 涉及重大安全、法律或隐私风险时，标记 `SAFETY_REVIEW` 并说明专业责任边界。

输出目标由用户决定：D、E、D+E；研究层 R 在必要时按需附加追溯，**不是未经用户要求的第三份长报告**。可视化应服务决策与用户任务理解，不自动装饰。宿主无法检索/读取附件时必须披露限制，不可声称已完成。


## Optional validation routing
`VALIDATE_OPTIONAL`: when an unresolved empirical question would plausibly change a consequential decision, offer the smallest study design using `focused-experience-validation`, if present. `RESEARCH_RETURN`: when user supplies authorized research data, inspect input types, maintain denominator/source rules and route to V; keep other O/E/D findings. No data or declined V must not block conditional expert analysis.

## v0.4B.1 optional source and comparator routes
- `VOC_OFFER`: feedback may change the active decision; request a narrowly scoped user-authorized export or optional lawful external acquisition **performed outside the Skill**. Route provenance via [VOC Source Routing](voc-source-routing.md). A decline does not block existing analysis.
- `EXTERNAL_COMPARE`: user wants to understand disagreements with other public Skills/repositories; identify exact external version and use [External Output Benchmark](external-output-benchmark.md) with shared synthetic case inputs and claim-by-claim evidence. Do not treat a GitHub result as ground truth.
