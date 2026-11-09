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

## 🚀 快速上手

### 1. 安装配置 (Installation)
将技能克隆或复制至智能体平台的共享技能目录（默认为 `~/.agents/skills/`）：

```bash
# 克隆代码仓库
git clone https://github.com/<org>/uxda.git

# 复制技能到 Agent 共享技能目录
mkdir -p ~/.agents/skills
cp -r uxda/skills/ux-decision-assistant-router ~/.agents/skills/
cp -r uxda/skills/evidence-based-design-review ~/.agents/skills/

# (可选) 建立指向 Antigravity 全局配置的软链接
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/ux-decision-assistant-router ~/.gemini/config/skills/
ln -s ~/.agents/skills/evidence-based-design-review ~/.gemini/config/skills/
```
详细平台配置与注意事项见 [安装指南 (INSTALLATION.md)](INSTALLATION.md)。

### 2. 基础调用示例 (Basic Invocation)
在对话中直接向 AI 编程助手输入自然语言提示词：

```text
"请评审这一结账流程改版方案：产品团队希望移除最终确认弹窗以提升转化速度。
请从认知失误模式、容错风险等维度进行评估，并给出具有防御性的替代方案建议。"
```

UXDA 将引导智能体自动执行以下步骤：
1. 触发**单门禁前置审查 (Single-Gate pre-flight audit)**（校验输入证据边界）；
2. 在输出顶部渲染**业务推进图 (`业务推进图`)**；
3. 构建结构化的**竞争性假说 (Competing Hypotheses)**（如操作习惯化滑退 vs 反馈延迟容忍）；
4. 提供具有可操作性、解耦的权衡取舍建议，杜绝“零风险”等无依据断言。

---

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

我们欢迎个人用户、研究者及符合许可条件的组织使用 UXDA，探索其在人因工程、用户体验研究和交互设计评审中的实际价值，并通过 [GitHub Issues](https://github.com/your-org/uxda/issues) 分享使用体验、发现的问题和改进建议。

由于项目仍处于持续开发与验证阶段，部分专业规则、分析能力及跨平台适配尚未完成充分的实际应用验证。因此，**现阶段更建议将 UXDA 用于学习、研究、功能体验和方法评估，不建议直接部署至正式生产环境，或将其输出作为关键业务、安全与合规决策的唯一依据。**

本项目采用 **[PolyForm Strict License 1.0.0](LICENSE)**（[官方条款说明](https://polyformproject.org/licenses/strict/1.0.0)），以源码公开、使用受限（Source-Available）的方式发布。用户可在许可证允许的非商业范围内使用；商业使用、软件修改或再分发需要获得维护者的另行授权。具体权利与限制以仓库中的 `LICENSE` 为准。

随着测试反馈的积累和产品成熟度提升，我们将持续改进 UXDA，并适时评估后续版本的使用与授权方式。
