# H5 交互报告输出协议 v0.3.1

此文件规定 **可选的展示格式**，不是新的研究方法。先完成 D/E/R 的专业分析，再做可视化；页面不得倒逼研究结果。

## 触发

用户明确说“做成 H5 / 网页报告 / 可视化报告 / HTML”时，优先生成离线单文件 HTML；明确选“纯文字”则不得擅自改成 H5；用户同时要求则同时交付。**仅描述“希望报告更直观/图文”但未明确 HTML 时，应给出可拒绝的媒介建议**，不要假定已授权生成文件。

**未指定媒介**：简单任务建议文字并直接交付；复杂多方案、任务路径或空间关系且有文件能力时，先交付可用的文字结论，再推荐 H5 或两者，用户通过编号/自然语言接受后才制作 HTML；拒绝或未回应时不生成，也不重复劝说。无文件写入或 Python 环境时，仅推荐可交付形式，并说明限制。不要因为推荐 H5 就停止当前专业分析。

## 数据合同

读取 `assets/report-data-schema.md`。形成 JSON 数据文件，包括 title、case_context、recommendation、decision_options、journey、findings、evidence。对缺失数据保持缺失，不生成无来源的数字。禁止外链脚本、遥测、远程图片，用户资料不自动上传。

## 生成和验收

在允许文件创建的环境中运行：
`python scripts/render_report.py --input <case.json> --output <report.html>`

生成物使用静态 HTML/CSS/JS（浏览器可离线打开），支持 D/E/D+E 视图切换、研究依据折叠、打印/存为 PDF。每一项可视化基于实际输入，不凭空产生量化图表。检查可读性、移动端布局、键盘与文字复制，向用户提供真实文件路径。

> 此报告是结果呈现器；单文件 HTML 不能独立调用 AI、检索外网或执行实时研究。


## v0.4D.3 first-screen behavior

The route preview and UX research snapshot are visible; the full progress dependencies, professional O/E/D/V sections and source trace are independently expandable. Printing opens all sections. This is progressive disclosure, not a license to remove methods, uncertainty, provenance or decision-critical law. See Router `references/progressive-research-presentation.md`.
