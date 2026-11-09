# UXDA — 用户体验决策助手 (Public Core v0.1.0-beta.1)

[English](README.md) | 简体中文

[![许可证：PolyForm Strict 1.0.0](https://img.shields.io/badge/License-PolyForm_Strict_1.0.0-blue.svg)](#许可证与使用说明)
[![状态：源码公开测试版](https://img.shields.io/badge/Release-v0.1.0--beta.1_(源码公开测试版)-orange.svg)](#版本映射与发布标识)
[![架构：公共核心](https://img.shields.io/badge/Architecture-Public_Core-green.svg)](#架构设计与物理隔离)

**UXDA (User Experience Decision Assistant，用户体验决策助手)** 是一套源码公开（Source-Available）、循证的人因工程 (Human Factors, HF) 与交互设计推理 Agent 技能库（Skill Suite），专为 AI 结对编程及具备工具调用能力的智能体环境设计（包括 Google Antigravity、Gemini CLI、Claude Code、Cursor 及各类自定义 Agent 框架）。

它提供结构化的决策推演框架、认知失误审计机制（如 Norman 动作执行失误/Action Slips、操作自动化组块效应/Motor Chunking、操作习惯化/Habituation）、人因工效学物理尺寸换算以及研究方法论准入把关（Methodology Gating），协助 AI 编程助手输出可论证、可验证且兼顾真实情境的用户体验建议。

---

> ### ⚠️ 关键专业职责与安全免责声明
> **UXDA 是结构化推理与决策支持工具，而非自动化合规认证机构。**
> - UXDA 的所有输出均为**拟议审议建议（Conditional proposals for discussion）**，绝不构成企业最终业务决议、法定合规结论或工程变更批准。
> - UXDA **不能替代合格专业人类专家的判断**，不能替代政府监管机构审批（如美国 FDA、FAA）、法定技术法规审查（如欧盟 MDR）、技术标准合规认证（如 ISO 国际标准、中国 GB 国家标准），亦不能替代专用的物理、热学、电气或车载碰撞安全测试。
> - 涉及高风险安全决策领域（医疗设备、车载座舱、工业仪器等），必须始终由具备资质的人类领域专家进行最终复核与批准。
> - **宿主平台范围说明**：UXDA 本身仅由 Agent 提示词指令规范、结构化参考卡片及本地 Python 校验脚本组成。底层模型的网络传输、推理机制与多轮会话持久化完全由您所使用的宿主 AI 智能体平台决定。

---

<a id="架构设计与物理隔离"></a>
<a id="architecture"></a>
## 🏛️ 架构设计与物理隔离

UXDA 遵循“**独立优先、设计即互通** (Standalone-First, Interoperable-by-Design)”原则构建，在**公共核心 (Public Core)**与可选的企业私有扩展机制之间维持严格的物理与概念隔离：

```
+-------------------------------------------------------------------------+
|                        UXDA 公共核心 (Public Core，本仓库)                |
|                                                                         |
|  [路由技能: ux-decision-assistant-router (v0.5.4-beta.1)]                |
|   - 任务分类 (教学引导 Guided / 决策支持 Decision / 项目推进 Project)       |
|   - 单门禁前置核验 (Single-Gate) 与 业务推进图生成 (Business Progress Map) |
|   - 证据分级体系与研究方法边界约束                                        |
|                                                                         |
|  [专家技能: evidence-based-design-review (v0.7.0-beta.1)]               |
|   - 独立调用的设计评审专家                                                |
|   - 人因失误模式审查 (Norman 动作执行失误, 菲茨定律/Fitts 目标约束)        |
|   - 权衡分析、竞争性假说推演与防呆设计 (Poka-Yoke) 替代方案                 |
|                                                                         |
|  [公共方法论参考与通用知识模型]                                           |
|   - ISO 9241 系列、KLM/GOMS 认知参数校准准则、交互启发式规则              |
+-------------------------------------------------------------------------+
                                    │
                                    │ (可选 Context Bundle v0.2 标准契约)
                                    ▼
+-------------------------------------------------------------------------+
|                    私有扩展机制 (Private Extensions，用户自建维护)          |
|                                                                         |
|  - 企业专有规范、私有设计系统与内部审查规则                               |
|  - 私有项目登记表、文档物理存储与授权绑定                                 |
|  - 机密遥测埋点、内部用户研究记录与商业审批流                             |
|                                                                         |
|  *注：公共核心完全独立运行于用户提供的上下文资料之上，零私有依赖。          |
+-------------------------------------------------------------------------+
```

---

<a id="版本映射与发布标识"></a>
<a id="versioning"></a>
## 🏷️ 版本映射与发布标识

UXDA Public Core 从 `v0.1.0-beta.1`（源码公开受限测试版）起开启面向公开社区的独立语义化版本线，各模块技能则保留各自组件内部演进版本历史：

| 分发层级 / 交付组件 | 公开发布版本 | 组件历史演进线 | 角色与用途定位 |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core 整体套件** | **`v0.1.0-beta.1`** | *源码公开受限测试版 (Source-Available Beta)* | UXDA Agent 技能套件的统一源码公开分发版本 |
| `skills/ux-decision-assistant-router` | `v0.5.4-beta.1` | v0.1.0 → v0.5.4-beta.1 | 工作流总入口、多模式路由分发、业务推进图渲染 |
| `skills/evidence-based-design-review` | `v0.7.0-beta.1` | v0.1.0 → v0.7.0-beta.1 | 独立调用的交互摩擦与人因认知失误评审专家 |
| 外部 Context Bundle 接口契约 | `v0.2` | 规范草案 v0.2 | 供外部解耦规则/数据源对接的标准 JSON 交换契约 |

---

## 📦 公开测试版包含内容

| 组件名称 | 目录路径 | 描述说明 |
| :--- | :--- | :--- |
| **路由技能 (Router)** | `skills/ux-decision-assistant-router` | 主会话入口。负责问题界定、绘制业务推进图、执行证据边界门禁，并引导 O/E/D/V 研究流转。 |
| **评审专家技能 (Specialist)** | `skills/evidence-based-design-review` | 专项交互评审器。依据认知心理学与物理人机工效学，评估线框图、界面变动、硬件面板与业务流程。 |
| **单门禁规范资产 (Single-Gate)** | `skills/*/references/` | 核心认识论指引：`analytical-quality.md`、`evidence-boundaries.md`、`design-integration-baseline.md` 等。 |
| **公共文档与指南 (Guides)** | 仓库根目录 (`*.md`) | 单机部署指南、合成推演示例、安全隐私政策及方法边界定义。 |

---

## 🚀 安装、调用与案例演示

### 1. 安装两套 Skill（macOS / Linux）

UXDA 是一组 **Agent Skill，并不是独立运行的 App**。需要宿主 AI Agent 具备读取本地技能文件的能力。下面的命令只安装公共技能，不会安装大模型或自动启动服务；不同 Agent 的自动识别机制也可能不同。

```bash
git clone https://github.com/RagnTec/User-Experience-Decision-Assistant.git
cd User-Experience-Decision-Assistant
mkdir -p ~/.agents/skills
cp -R skills/ux-decision-assistant-router ~/.agents/skills/
cp -R skills/evidence-based-design-review ~/.agents/skills/

# 确认两个技能入口文件存在
test -f ~/.agents/skills/ux-decision-assistant-router/SKILL.md
test -f ~/.agents/skills/evidence-based-design-review/SKILL.md
```

**Google Antigravity（如当前环境需要额外的发现目录链接）：**

```bash
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/ux-decision-assistant-router ~/.gemini/config/skills/ux-decision-assistant-router
ln -s ~/.agents/skills/evidence-based-design-review ~/.gemini/config/skills/evidence-based-design-review
```

重复执行前，请检查同名链接或文件夹是否已经存在。上述路径仅为已使用环境的安装示例，**不代表 Gemini CLI、Claude Code、Cursor 等平台都采用同一路径**。其他宿主应结合 [INSTALLATION.md](INSTALLATION.md) 和对应平台的 Skill 发现规则配置。**目前仓库仍为 Private，克隆时需要具备仓库访问权限。**

### 2. 如何在对话中调用？

UXDA Beta **没有统一的专用斜杠命令或云端 API**。在可以加载本地 Skill 的 Agent 对话中，直接明确指定技能和任务范围即可。

**Router：适合教学引导、方案决策与研究项目推进**

```text
请使用已安装的 ux-decision-assistant-router Skill，以 decision（决策支持）
模式分析一个文件批量删除流程。比较“删除前二次确认”和“可撤销删除”
两种方案，说明认知失误风险、适用条件、关键反例及仍需验证的事项。
如果无法读取 Skill，请明确告知，不要假装已经调用。
```

**Specialist：适合直接进行设计与人因专项评审**

```text
请直接使用 evidence-based-design-review Skill，不进入 Router 的模式选择。
基于我提供的界面和任务，评价关键交互机制、潜在体验风险和可执行的
修改建议；区分设计已知事实、人因推论与尚未验证的信息。
若无法读取 Skill，请说明限制。
```

如果 Agent 未自动识别，可以在它支持本地文件读取的前提下，明确要求读取安装目录下的相应 `SKILL.md`。没有企业项目扩展或私有数据，也可以根据当前对话提供的通用场景材料执行 Public Core 分析。

### 3. 四个不同能力的通用案例

以下均为**合成情境下的输出结构示例，不是真实 Agent 运行截图，也不是用户研究实测结果**。片段只展示 UXDA 预期支持的分析方式，实际回复取决于宿主模型、输入材料与确认的任务范围。

<details>
<summary><strong>案例 A｜教学引导：研究方法如何选择（Router · guided）</strong></summary>

**直接复制这段提示词：**

```text
请使用 ux-decision-assistant-router 的 guided（教学引导）模式。
某通用购物 App 的团队怀疑用户难以找到筛选功能。
请解释访谈、任务型可用性测试和问卷分别能回答什么问题，
并设计一个最小 Pilot，说明每种方法不能支持的结论。
目前没有任何真实受访者数据。
```

**效果片段（示意）：**

```text
研究问题：用户能否在商品查找任务中发现并使用筛选功能？
建议路径：先做小规模任务型 Pilot，再决定是否量化问题分布。
观察内容：任务完成、绕行路径、犹豫节点、参与者解释。
证据边界：“筛选难找”仍是待验证假设，不能报告问题发生率。
后续决策：依据观察结果细化问题，再判断是否需要问卷。
```

</details>

<details>
<summary><strong>案例 B｜设计决策：操作效率与容错权衡（Router · decision）</strong></summary>

**直接复制这段提示词：**

```text
请使用 ux-decision-assistant-router 的 decision（决策支持）模式。
某素材管理工具准备取消批量删除前的确认弹窗。
比较保留弹窗、可撤销删除两种方案，考虑误操作、习惯化、
不可逆后果与任务效率；给出有条件的推荐，不要编造效率提升幅度。
```

**效果片段（示意）：**

```text
当前建议：若删除可可靠恢复，可比较“删除后撤销”与确认弹窗；
          若不可逆，应保留更强的执行前保护。
最强反例：无法保证撤销成功时，Undo 不等同于可靠恢复。
关键未知：恢复机制、操作频次和真实误删证据。
决策边界：条件未确认前，不应宣称某方案全面优于另一方案。
```

</details>

<details>
<summary><strong>案例 C｜项目推进：低成本可用性 Pilot（Router · project）</strong></summary>

**直接复制这段提示词：**

```text
请使用 ux-decision-assistant-router 的 project（方案推进）模式。
为一款通用任务管理工具的两版导航布局设计小规模可用性 Pilot。
明确任务、观察指标、顺序效应控制、记录字段及结果可支持的决策。
现在仅设计方案，尚未实施研究，请勿生成虚构结果。
```

**效果片段（示意）：**

```text
Pilot 目标：识别显著的任务查找障碍，而非推断总体差异。
执行控制：尽可能平衡方案呈现顺序，保持两版任务目标一致。
记录字段：方案、顺序、任务是否完成、求助、绕行和观察备注。
下一步：试跑并检查相互矛盾的案例，再决定是否扩大样本。
未评估：任何优势比例、显著性检验或用户偏好率。
```

</details>

<details>
<summary><strong>案例 D｜专项评审：触控尺寸与真实操作情境（Specialist）</strong></summary>

**直接复制这段提示词：**

```text
请独立使用 evidence-based-design-review Skill，不进入 Router 模式选择。
某工业设备采用 10.1 英寸、1280×800 分辨率的触摸屏，
控件可视尺寸为 36×36 px，操作员可能佩戴保温手套。
请估算物理显示尺寸，区分可视图形与实际触控热区，
分析可能的人因风险和需要补充的测量或测试。
不要自行编造 ISO 强制尺寸阈值。
```

**效果片段（示意）：**

```text
参数换算：约 149.5 PPI；36 px 对应约 6.1 mm（基于所给屏幕参数）。
体验风险：可视图形、有效触控热区、戴手套时的接触范围未必一致；
          仅靠像素尺寸无法判断实际可用性。
建议行动：补充有效热区尺寸，使用真实手套和任务验证触控表现。
结论边界：这不是合规认证，也不是已观察到的误触率。
```

</details>

**想看可视化报告？** 如果宿主 Agent 具备本地文件写入能力，可以在分析后补充：“请先建议适合的 H5/HTML 摘要结构，等我确认后再生成文件。”这是按需的交付形式，不是保证存在的独立图形界面。后续可将真实测试会话的局部截图补入仓库；这里不使用伪造的工具运行截图或量化效果。

## 📖 文档导航

- [安装指南 (Installation Guide)](INSTALLATION.md) — 支持的 Agent 平台配置与单机验证步骤。
- [快速入门 (Quick Start Guide)](QUICK_START.md) — 5 分钟上手教程与合成推演案例。
- [方法边界与系统局限 (Methodology & Limitations)](LIMITATIONS.md) — 认识论边界、样本量规则与非目标范围。
- [贡献指南 (Contributing Guidelines)](CONTRIBUTING.md) — 如何提交改进与补充通用人因卡片。
- [安全与隐私政策 (Security & Privacy)](SECURITY.md) — 数据隔离边界、宿主平台差异说明及漏洞反馈渠道。
- [版本发布说明 (Initial Release Notes)](RELEASE_NOTES.md) — `v0.1.0-beta.1` 变更日志与基线特性。

> *注：上述下级技术文档目前提供英文版原文。*

---

<a id="许可证与使用说明"></a>
<a id="许可证与代码使用条件"></a>
<a id="许可证评估"></a>
<a id="license-review"></a>
<a id="license"></a>
## ⚖️ 许可证与使用说明

**UXDA Public Core 目前处于公开 Beta 测试阶段。**

我们欢迎个人用户、研究者及符合许可条件的组织使用 UXDA，探索其在人因工程、用户体验研究和交互设计评审中的实际价值，并通过 [GitHub Issues](https://github.com/RagnTec/User-Experience-Decision-Assistant/issues) 分享使用体验、发现的问题和改进建议。

由于项目仍处于持续开发与验证阶段，部分专业规则、分析能力及跨平台适配尚未完成充分的实际应用验证。因此，**现阶段更建议将 UXDA 用于学习、研究、功能体验和方法评估，不建议直接部署至正式生产环境，或将其输出作为关键业务、安全与合规决策的唯一依据。**

本项目采用 **[PolyForm Strict License 1.0.0](LICENSE)**（[官方条款说明](https://polyformproject.org/licenses/strict/1.0.0)），以源码公开、使用受限（Source-Available）的方式发布。用户可在许可证允许的非商业范围内使用；商业使用、软件修改或再分发需要获得维护者的另行授权。具体权利与限制以仓库中的 `LICENSE` 为准。

随着测试反馈的积累和产品成熟度提升，我们将持续改进 UXDA，并适时评估后续版本的使用与授权方式。
