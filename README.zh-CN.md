# UXDA — 用户体验决策助手 (Public Core v0.1.0-beta.1)

[English](README.md) | 简体中文

[![许可证：PolyForm Strict 1.0.0](https://img.shields.io/badge/License-PolyForm_Strict_1.0.0-blue.svg)](#许可证与使用说明)
[![状态：源码公开测试版](https://img.shields.io/badge/Release-v0.1.0--beta.1_(源码公开测试版)-orange.svg)](#版本映射与发布标识)
[![架构：公共核心](https://img.shields.io/badge/Architecture-Public_Core-green.svg)](#架构设计与物理隔离)

UXDA（User Experience Decision Assistant）是一套面向用户研究、交互体验与人因工程的 AI Agent 技能工具。它通过专业知识交流、研究方法引导和情境化实践，帮助使用者理解研究问题、探索不同解释、选择适当的方法，并逐步提升独立分析与开展研究的能力。

UXDA 可以辅助提出研究假设、梳理证据、设计研究方案和讨论初步建议，但不替代真实用户研究或专业研究人员的判断。模型输出属于可供交流、学习与进一步验证的参考内容，不能直接视为已经确认的用户洞察或正式研究结论。

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
UXDA 公共核心 (Public Core)
    │
    ├── skills/uxda/SKILL.md (统一核心技能入口)
    │       │
    │       ├── Guided     (教学引导：概念认知、任务拆解与问题重构)
    │       ├── Decision   (决策支持：设计取舍权衡与潜在风险识别)
    │       ├── Project    (方案推进：小规模测试规划与实验控制提示)
    │       └── Specialist (专家评审：基于证据的人因工程与触控尺寸审查)
    │
    ├── 共享参考规范 (Shared References：按需加载方法论、人因与标准规范)
    ├── 本地工具与素材 (Scripts & Assets：离线校验与证据检索工具)
    │
    └── 可选 Context Bundle 契约规范 (v0.2 外部接口约定)
            │
            └── 用户自建私有扩展 (Private Extensions：企业专有规范与数据)
```

---

<a id="版本映射与发布标识"></a>
<a id="versioning"></a>
## 🏷️ 版本映射与发布标识

UXDA Public Core 从 `v0.1.0-beta.1`（源码公开受限测试版）起开启面向公开社区的独立语义化版本线，各模块技能则保留各自组件内部演进版本历史：

| 分发层级 / 交付组件 | 公开发布版本 | 组件历史演进线 | 角色与用途定位 |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core 整体套件** | **`v0.1.0-beta.1`** | *源码公开受限测试版 (Source-Available Beta)* | UXDA Agent 技能套件的统一源码公开分发版本 |
| `skills/uxda` (统一核心技能) | `v0.1.0-beta.1` | 原 Router (v0.5.4) + Specialist (v0.7.0) 一体化重组 | 对外唯一发布的技能包，内置 Guided / Decision / Project / Specialist 四类能力 |
| 外部 Context Bundle 接口契约 | `v0.2` | 规范草案 v0.2 | 供外部解耦规则/数据源对接的标准 JSON 交换契约 |

---

## 📦 公开测试版包含内容

| 组件名称 | 目录路径 | 描述说明 |
| :--- | :--- | :--- |
| **UXDA 统一技能 (Unified Skill)** | `skills/uxda` | 核心单一技能入口（技术标识 `uxda`）。内置四类核心能力：Guided（用研方法学习）、Decision（体验取舍决策）、Project（方案设计推进）与 Specialist（人因工效专项评审）。 |
| **规约与方法库 (References)** | `skills/uxda/references/` | 核心认识论指引与专业方法规约：`analytical-quality.md`、`evidence-boundaries.md`、`design-integration-baseline.md` 等。 |
| **离线工具与资产 (Scripts & Assets)** | `skills/uxda/scripts/`, `assets/` | 离线证据定位器 (`local_evidence.py`)、H5 报告渲染器 (`render_report.py`) 及脱网原创知识库。 |
| **公共文档与指南 (Guides)** | 仓库根目录 (`*.md`) | 单机部署指南、安全隐私政策及方法边界定义。 |

---

## 🚀 安装、调用与案例演示

### 1. 安装 UXDA 技能（macOS / Linux）

UXDA 是一组 **Agent Skill，并不是独立运行的 App**。需要宿主 AI Agent 具备读取本地技能文件的能力。下面的命令安装统一的 UXDA 技能，不会安装大模型或自动启动服务；不同 Agent 的自动识别机制也可能不同。

```bash
git clone https://github.com/RagnTec/User-Experience-Decision-Assistant.git
cd User-Experience-Decision-Assistant
mkdir -p ~/.agents/skills
cp -R skills/uxda ~/.agents/skills/

# 确认技能入口文件存在
test -f ~/.agents/skills/uxda/SKILL.md
```

**Google Antigravity（如当前环境需要额外的发现目录链接）：**

```bash
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/uxda ~/.gemini/config/skills/uxda
```

重复执行前，请检查同名链接或文件夹是否已经存在。上述路径仅为已使用环境的安装示例，**不代表 Gemini CLI、Claude Code、Cursor 等平台都采用同一路径**。其他宿主应结合 [INSTALLATION.md](INSTALLATION.md) 和对应平台的 Skill 发现规则配置。**目前仓库仍为 Private，克隆时需要具备仓库访问权限。**

### 2. 如何在对话中调用？

UXDA **无需分别安装多个技能，也没有统一的专用斜杠命令或云端 API**。在可以加载本地 Skill 的 Agent 对话中，直接使用自然语言描述你的任务，UXDA 内部会自动匹配并调度对应的能力：

**能力 1：用研方法学习与探索 (Guided)**
```text
请使用已安装的 uxda 技能：我们发现购物 App 的商品筛选功能好像不太容易被用户找到，想做点用户研究确认一下。应该从哪里开始？
```

**能力 2：设计取舍与决策推演 (Decision)**
```text
请使用 uxda 技能：我们想取消批量删除文件前的确认弹窗，让操作快一点。比较“删除前二次确认”和“可撤销删除”两种方案，说明认知失误风险、适用条件、关键反例及仍需验证的事项。
```

**能力 3：研究方案设计与推进 (Project)**
```text
请使用 uxda 技能：我们准备比较两种导航布局哪个好用，想先做一轮小规模测试，应该怎么设计？
```

**能力 4：人因工效与专项评审 (Specialist，直接调用无问卷阻塞)**
```text
请使用 uxda 技能：10.1 英寸、1280×800 的工业触摸屏，36×36 像素的按钮给戴厚手套的操作员用，合适吗？
```

如果 Agent 未自动识别，可以在它支持本地文件读取的前提下，明确要求读取安装目录下的相应 `SKILL.md`。没有企业项目扩展或私有数据，也可以根据当前对话提供的通用场景材料执行 Public Core 分析。

**结合本地文档与自定义规则调用 (Local Knowledge & Rules)**

UXDA 不仅能依赖内置通用方法，也支持结合使用者主动提供的本地资料与项目约束进行分析：
- **按需加载本地资料**：在对话中直接提供说明，或授权 Agent 读取指定的本地规范文件。Public Core 内置的离线证据定位工具 `local_evidence.py`（位于 `skills/uxda/scripts/local_evidence.py`，详见 [本地知识与证据层说明](skills/uxda/references/local-knowledge-evidence.md)），可通过显式来源清单在本地检索多份授权材料，并记录引用出处与文件变更（SHA 校验）。
- **规则权属与权威性边界**：使用者自己的研究规范、团队设计守则或内部业务文档属于特定任务的上下文输入，**不自动继承通用公认标准的权威性**。当本地规则与通用人因原则冲突时，Agent 会单独提示适用性边界与潜在风险。
- **当前能力与扩展接口**：当前 Beta **尚未提供**图形界面、规则库自动导入、注册启停或版本管理系统；Context Bundle 协议仅作为可选的外部扩展接口规范，并非已内建的一键导入工具。
- **数据隐私与边界区分**：UXDA 自带的本地文件与脚本不发起网络传输、不主动上传用户资料，绝不会自动将用户自定义规则同步至 GitHub 或写入 Public Core 仓库。另一方面，底层模型调用、上下文缓存、本地日志与会话持久化完全由宿主 Agent 平台控制，无法由 UXDA 独立保证仅在当前会话中保留（参见 [SECURITY.md](SECURITY.md)）。

```text
请使用 UXDA 帮我评估这个研究方案，同时参考我提供的本地研究规范；如存在适用性冲突，请单独提示。
```

### 3. 通用案例演示 (Demonstrations)

以下截图来自 UXDA 在 Antigravity 中的实际调用，使用的是模拟业务场景，仅展示部分输出。这些截图产生于双 Skill 架构演进期，此处如实保留其原始提示词与 Antigravity 实际调用画面作为历史能力验证记录；在当前单 Skill 架构下，四类能力已完整汇聚于统一的 `uxda` 技能中。当前版本仍处于 Beta 测试阶段，功能表现和专业判断尚未经过充分验证，建议用于体验、学习与辅助分析，重要结论需人工复核。

<details>
<summary><strong>案例 1｜研究问题引导 (Router)</strong></summary>

**用户原始提示词：**

```text
我们发现购物 App 的商品筛选功能好像不太容易被用户找到，想做点用户研究确认一下。应该从哪里开始？
```

<a href="docs/media/demos/demo1.png"><img src="docs/media/demos/demo1.png" alt="Demo 01: 研究问题引导" width="760"></a>

**能力与边界说明**：将模糊的体验问题拆解为不同解释假设，提供初步研究方向与后续协作选择。

</details>

<details>
<summary><strong>案例 2｜设计决策支持 (Router)</strong></summary>

**用户原始提示词：**

```text
我们想取消批量删除文件前的确认弹窗，让操作快一点。这样设计合适吗？
```

<a href="docs/media/demos/demo2.png"><img src="docs/media/demos/demo2.png" alt="Demo 02: 设计决策支持" width="760"></a>

**能力与边界说明**：识别影响方案取舍的关键条件，分析潜在交互风险，并提出初步替代思路。

</details>

<details>
<summary><strong>案例 3｜研究方案辅助 (Router)</strong></summary>

**用户原始提示词：**

```text
我们准备比较两种导航布局哪个好用，想先做一轮小规模测试，应该怎么设计？
```

<a href="docs/media/demos/demo3.png"><img src="docs/media/demos/demo3.png" alt="Demo 03: 研究方案辅助" width="760"></a>

**能力与边界说明**：根据研究目标提出测试设计方向，并提醒关注学习效应、任务安排等实验控制问题。

</details>

<details>
<summary><strong>案例 4｜触控尺寸专项评审 (Specialist · ⚠️ Known Beta Limitation)</strong></summary>

**用户原始提示词：**

```text
用 evidence-based-design-review 帮我看看：10.1 英寸、1280×800 的工业触摸屏，36×36 像素的按钮给戴厚手套的操作员用，合适吗？
```

**局限与边界说明**：
`Known Beta Limitation`：部分专业标准引用和设计阈值可能存在偏差，重要人因、安全及合规判断需要人工核验。

<a href="docs/media/demos/demo4.png"><img src="docs/media/demos/demo4.png" alt="Demo 04: Specialist 专项评审（Known Beta Limitation）" width="760"></a>

</details>

**想看可视化报告？** 如果宿主 Agent 具备本地文件写入能力，可以在分析后补充：“请先建议适合的 H5/HTML 摘要结构，等我确认后再生成文件。”这是按需的交付形式，不是保证存在的独立图形界面。这里不使用伪造的工具运行截图或量化效果。

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
