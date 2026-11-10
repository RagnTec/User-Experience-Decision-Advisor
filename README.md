# UXDA — User Experience Decision Assistant (Public Core v0.1.0-beta.1)

English | [简体中文](README.zh-CN.md)

[![License: PolyForm Strict 1.0.0](https://img.shields.io/badge/License-PolyForm_Strict_1.0.0-blue.svg)](#license)
[![Status: Source-Available Public Beta](https://img.shields.io/badge/Release-v0.1.0--beta.1_(Source--Available_Beta)-orange.svg)](#version-mapping--release-identity)
[![Architecture: Public Core](https://img.shields.io/badge/Architecture-Public_Core-green.svg)](#architecture--clean-separation)

UXDA (User Experience Decision Assistant) is an AI agent skill suite for UX research, interaction design, and human factors. Through professional knowledge exchange, methodological guidance, and scenario-based practice, it helps users frame research questions, explore alternative explanations, choose appropriate methods, and progressively develop independent research capabilities.

UXDA can help users formulate hypotheses, examine evidence, plan studies, and discuss preliminary recommendations. It does not replace empirical user research or professional judgment. Its outputs are intended for learning, discussion, and further validation, not as established user insights or validated research findings.

---

> ### ⚠️ Critical Professional & Safety Disclaimer
> **UXDA is a structured reasoning and decision-support tool, NOT an automated certification authority.**
> - UXDA outputs are **conditional proposals for discussion (拟议审议建议)**, never finalized corporate resolutions, legal clearances, or engineering change approvals.
> - UXDA does **not replace qualified professional human judgment**, approvals by government regulatory agencies (e.g., US FDA, FAA), statutory regulations compliance (e.g., EU MDR), consensus technical standards certifications (e.g., ISO, national GB standards), or specialized physical/thermal/electrical/crash testing.
> - High-consequence safety decisions (medical devices, automotive cockpits, industrial appliances) must always be reviewed and approved by certified human domain experts.
> - **Host Platform Scope**: UXDA consists of instruction files, structured reference cards, and local Python validation utilities. The underlying network transmission, model inference, and conversational session management are governed entirely by your host AI agent platform.

---

<a id="architecture--clean-separation"></a>
<a id="architecture"></a>
## 🏛️ Architecture & Clean Separation

UXDA is built on the **Standalone-First, Interoperable-by-Design** principle, maintaining a strict physical and conceptual separation between its **Public Core** and optional enterprise extension mechanisms:

```
UXDA Public Core
    │
    ├── skills/uxda/SKILL.md (Unified Core Skill Entrypoint)
    │       │
    │       ├── Guided     (Guided learning, task decomposition & problem framing)
    │       ├── Decision   (Design trade-off evaluation & risk identification)
    │       ├── Project    (Small-scale test planning & experimental controls)
    │       └── Specialist (Evidence-based human-factors & touch target review)
    │
    ├── Shared References (On-demand methodology, ergonomics & standards)
    ├── Scripts & Assets  (Offline verification & evidence locator utilities)
    │
    └── Optional External Context Bundle Contract (v0.2 Interface Specification)
            │
            └── User-Maintained Private Extensions (Proprietary rules & data)
```

---

<a id="version-mapping--release-identity"></a>
<a id="versioning"></a>
## 🏷️ Version Mapping & Release Identity

UXDA Public Core begins its public semantic versioning lifecycle at `v0.1.0-beta.1` (Source-Available Public Beta), while individual modular skills preserve their internal component development version histories:

| Component / Distribution Layer | Public Release Version | Component Evolution Track | Role & Purpose |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core Suite** | **`v0.1.0-beta.1`** | *Source-Available Public Beta* | Unified source-available distribution of the UXDA agent skills |
| `skills/uxda` (Unified Core Skill) | `v0.1.0-beta.1` | Unified integration of Router (v0.5.4) & Specialist (v0.7.0) | Single entrypoint skill delivering Guided, Decision, Project, and Specialist capabilities |
| External Context Bundle Contract | `v0.2` | Specification v0.2 | Decoupled JSON data exchange schema for optional extensions |

---

## 📦 What's Included in the Public Beta

| Component | Path | Description |
| :--- | :--- | :--- |
| **UXDA Unified Skill** | `skills/uxda` | Single entrypoint skill (`uxda`). Delivers four core capabilities: Guided (learning & discovery), Decision (trade-off analysis), Project (study protocol coproduction), and Specialist (ergonomics & design review). |
| **References & Methodology** | `skills/uxda/references/` | Core epistemological guides & protocols: `analytical-quality.md`, `evidence-boundaries.md`, `design-integration-baseline.md`, etc. |
| **Offline Tools & Assets** | `skills/uxda/scripts/`, `assets/` | Offline evidence locator (`local_evidence.py`), H5 brief generator (`render_report.py`), and offline foundations catalog. |
| **Documentation & Guides** | Root (`*.md`) | Standalone setup guides, synthetic walk-throughs, and methodology boundary definitions. |

---

## 🚀 Install, Invoke, and Explore

### 1. Install the UXDA skill (macOS / Linux)

UXDA is an **agent skill package, not a standalone app**. You need an AI agent that can read local skill files. The commands below install the unified UXDA skill; they do not install an LLM, run a service, or guarantee that every host will discover the skills automatically.

```bash
git clone https://github.com/RagnTec/User-Experience-Decision-Assistant.git
cd User-Experience-Decision-Assistant
mkdir -p ~/.agents/skills
cp -R skills/uxda ~/.agents/skills/

# Verify the entry file exists
test -f ~/.agents/skills/uxda/SKILL.md
```

**Google Antigravity (optional discovery links, if required by your setup):**

```bash
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/uxda ~/.gemini/config/skills/uxda
```

Check for an existing link or folder before running `ln -s` again. This is a setup example from the tested environment, **not a universal installation path** for Gemini CLI, Claude Code, Cursor, or every agent host. Consult [INSTALLATION.md](INSTALLATION.md) and your host's skill-discovery settings. **While this repository is Private, cloning requires GitHub access to it.**

### 2. Invoke UXDA in your agent chat

There is **no need to install separate skills, nor is there a proprietary slash command or hosted API**. In a compatible agent session, simply describe your research or design task in natural language, and UXDA automatically dispatches the appropriate internal capability:

**Capability 1: Methodology Learning & Discovery (Guided)**
```text
Use the installed uxda skill: We noticed shoppers seem to have trouble finding the product filter in our shopping app and want to run some user research to check. Where should we start?
```

**Capability 2: Design Decision & Trade-off Analysis (Decision)**
```text
Use the installed uxda skill: We want to remove the confirmation dialog before bulk-deleting files to make operations faster. Compare a confirmation dialog vs. reversible deletion with Undo, and explain the trade-offs and risks.
```

**Capability 3: Study Protocol & Project Coproduction (Project)**
```text
Use the installed uxda skill: We want to compare which of two navigation layouts is easier to use and plan to run a small pilot test first. How should we design it?
```

**Capability 4: Ergonomics & Direct Specialist Review (Specialist, direct invocation without questionnaires)**
```text
Use the installed uxda skill: For a 10.1-inch 1280×800 industrial touchscreen, are 36×36 px buttons suitable for operators wearing thick gloves?
```

If your host cannot auto-discover a skill, point it to the corresponding `SKILL.md` in the installed folder **only if the host supports reading local files**. You can also paste a sanitized design description directly; no private extension or company project data is required.

**Using Local Documents and Custom Research Rules**

Beyond its built-in generic methods, UXDA supports contextual analysis using documents, project constraints, and custom research rules provided by the user:
- **On-Demand Local Knowledge**: Provide context directly in chat or authorize your agent to inspect specific local guideline files. The offline evidence locator `local_evidence.py` (`skills/uxda/scripts/local_evidence.py`, see [Local Knowledge & Evidence Layer](skills/uxda/references/local-knowledge-evidence.md)) can search across an explicit manifest of authorized materials and track file SHA deltas without network access.
- **Authority Boundaries**: User-supplied guidelines, team design rules, and project documents serve as task-specific contextual inputs; they **do not automatically inherit the authority of general industry standards**. When local rules conflict with established ergonomics or methodology principles, the agent will flag the discrepancy and applicability limits.
- **Current Capabilities & Extension Interface**: The current Beta **does not** include a GUI, automated rule repository, dynamic toggle, or rule versioning system. The Context Bundle specification is an optional external extension interface, not an implemented one-click import tool.
- **Privacy & Boundary Distinction**: UXDA's local files and scripts do not initiate network transmission, do not actively upload user data, and never automatically sync custom rules to GitHub or the Public Core repository. Separately, model inference, context caching, local logs, and conversational session persistence are governed entirely by your host AI agent platform; UXDA cannot independently guarantee that data is retained only within the current session (see [SECURITY.md](SECURITY.md)).

```text
Use UXDA to evaluate this research proposal, taking into account the local research guidelines I provided. If there is any applicability conflict with general standards, please flag it separately.
```

### 3. Generic Demonstrations

The following screenshots show actual UXDA outputs in Antigravity across simulated business scenarios, displaying selected excerpts. These screenshots were captured during the dual-skill architecture validation phase and are preserved as historical verification milestones; in the current single-skill architecture, all capabilities are seamlessly consolidated within the unified `uxda` skill package. UXDA is currently in Beta; its analytical performance and professional judgments have not been fully validated. It is recommended for exploration, learning, and decision support—critical conclusions still require manual human review.

<details>
<summary><strong>Case 1 · Research Question Framing (Router)</strong></summary>

**Original user prompt (Chinese):**

```text
我们发现购物 App 的商品筛选功能好像不太容易被用户找到，想做点用户研究确认一下。应该从哪里开始？
```

*English translation: "We noticed shoppers seem to have trouble finding the product filter in our shopping app and want to run some user research to check. Where should we start?"*

<a href="docs/media/demos/demo1-en.png"><img src="docs/media/demos/demo1-en.png" alt="Demo 01: Research Question Framing" width="760"></a>

**Capabilities & boundaries**: Breaks down ambiguous experience problems into competing explanatory hypotheses, offering initial research directions and follow-up collaboration choices.

</details>

<details>
<summary><strong>Case 2 · Design Decision Support (Router)</strong></summary>

**Original user prompt (Chinese):**

```text
我们想取消批量删除文件前的确认弹窗，让操作快一点。这样设计合适吗？
```

*English translation: "We want to remove the confirmation dialog before bulk-deleting files to make operations faster. Is this design appropriate?"*

<a href="docs/media/demos/demo2-en.png"><img src="docs/media/demos/demo2-en.png" alt="Demo 02: Design Decision Support" width="760"></a>

**Capabilities & boundaries**: Identifies critical conditions governing design trade-offs, analyzes potential interaction risks, and proposes preliminary alternative approaches.

</details>

<details>
<summary><strong>Case 3 · Research Planning Support (Router)</strong></summary>

**Original user prompt (Chinese):**

```text
我们准备比较两种导航布局哪个好用，想先做一轮小规模测试，应该怎么设计？
```

*English translation: "We want to compare which of two navigation layouts is easier to use and plan to run a small pilot test first. How should we design it?"*

<a href="docs/media/demos/demo3-en.png"><img src="docs/media/demos/demo3-en.png" alt="Demo 03: Research Planning Support" width="760"></a>

**Capabilities & boundaries**: Outlines test design directions aligned with research goals and highlights experimental controls like learning effects and task sequencing.

</details>

<details>
<summary><strong>Case 4 · Touch Target Review (Specialist · ⚠️ Known Beta Limitation)</strong></summary>

**Original user prompt (Chinese):**

```text
用 evidence-based-design-review 帮我看看：10.1 英寸、1280×800 的工业触摸屏，36×36 像素的按钮给戴厚手套的操作员用，合适吗？
```

*English translation: "Review this with evidence-based-design-review: for a 10.1-inch 1280×800 industrial touchscreen, are 36×36 px buttons suitable for operators wearing thick gloves?"*

**Limitations & boundaries**:
`Known Beta Limitation`: Professional standard citations and design thresholds may contain inaccuracies; critical human-factors, safety, and compliance judgments require manual expert verification.

<a href="docs/media/demos/demo4-en.png"><img src="docs/media/demos/demo4-en.png" alt="Demo 04: Specialist Review (Known Beta Limitation)" width="760"></a>

</details>

**Want a visual report?** If your host allows local file writing, you may additionally ask: `After the review, offer an HTML/H5 summary. Create it only after I approve the format.` This is an optional presentation workflow, not a guaranteed built-in GUI. No fabricated tool screenshots or metrics are used.

## 📖 Documentation Index

- [Installation Guide](INSTALLATION.md) — Setup across supported Agent platforms and standalone checks.
- [Quick Start Guide](QUICK_START.md) — 5-minute hands-on tutorial with synthetic examples.
- [Methodology & Limitations](LIMITATIONS.md) — Epistemic boundaries, sample size rules, and non-goals.
- [Contributing Guidelines](CONTRIBUTING.md) — How to propose enhancements and add generic knowledge cards.
- [Security & Privacy](SECURITY.md) — Data boundary definitions, host platform distinctions, and vulnerability reporting.
- [Initial Release Notes](RELEASE_NOTES.md) — Changelog and baseline features of `v0.1.0-beta.1`.

---

<a id="license"></a>
<a id="license-review"></a>
## ⚖️ License & Beta Usage Guidance

**UXDA Public Core is currently available as a public beta.**

We welcome individuals, researchers, and eligible organizations to explore UXDA's potential in human factors, user experience research, and interaction design review, and to share their experiences, issues, and suggestions through [GitHub Issues](https://github.com/RagnTec/User-Experience-Decision-Assistant/issues).

As the project is still under active development and validation, some methodological rules, analytical capabilities, and cross-platform integrations have not yet been sufficiently validated in real-world use. **At this stage, UXDA is best suited for learning, research, evaluation, and experimentation. Direct production deployment is not recommended, nor should its outputs serve as the sole basis for critical business, safety, or compliance decisions.**

UXDA is distributed as **source-available software under the [PolyForm Strict License 1.0.0](LICENSE)** ([polyformproject.org](https://polyformproject.org/licenses/strict/1.0.0)). Use is permitted for purposes covered by the license. Commercial use, software modification, and redistribution require separate authorization from the maintainer. Please refer to the repository's `LICENSE` file for the governing terms.

We will continue refining UXDA based on testing and community feedback, and may revisit its licensing and usage policies as the project matures.
