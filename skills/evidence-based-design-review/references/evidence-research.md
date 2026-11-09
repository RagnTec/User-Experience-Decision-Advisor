# 动态证据获取（专业 Skill 内部执行）

执行前先判断新证据是否会改变设计行动；不要因为可以联网就无差别搜索。使用此顺序：

1. **当前任务材料优先**：梳理输入中的产品目标、流程、截图、条件与约束；如额外提供用户观察和数据则一并利用，按来源定位。**不得因缺少真实用户资料而跳过专业分析**，区别已知与推断。
2. **选择触发**：无需检索 NO_SEARCH；核实标准/法规 PUBLIC_VERIFY；需要可比人群实证 EMPIRICAL_SEARCH；必须获取产品事实 ASK_PRODUCT_DATA；重大安全/隐私/法规 SAFETY_REVIEW。
3. **限定检索问题**：结合产品类型、用户、目标任务、环境、指标和争议点；只查可能改变结论的信息。
4. **来源适配与核验**：官方标准/法规版本和适用条款；原始研究的用户、方法、场景、指标与限制；至少识别重要反例或相冲突结果。没有外部搜索能力时不得假装核验完成。
5. **合成证据链**：具体论断 → 用户材料/公开来源 → 推断性质 → 适用条件 → 对决策的影响；统计数据说明方法和口径。
6. **停止**：补充检索难以改变行动，或必须通过当前产品观察才能解决时，停止搜集并给出具体补证任务。

**隐私底线**：不能向公开搜索服务提交用户未经授权的内部设计资料、个人信息或产品配置。公开方法及逻辑来自独立公知资料，不携带任何企业内部字段、程序或规则。详见项目审核文档 `docs/EVIDENCE_RESEARCH_CORE.md`（安装包不依赖该文件）。

## Specific rule/standard citations

When an official standard or local law materially changes the decision, use the shared [Claim Provenance Gate](../../ux-decision-assistant-router/references/source-provenance-gate.md). If official lookup is unavailable or not executed, do not give remembered standard numbers as verified law, or invent thresholds and regulatory consequences. State the verification status explicitly. A static reference link is not proof of retrieval.
