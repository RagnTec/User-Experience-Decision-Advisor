# UXDA — User Experience Decision Assistant (Public Core v0.1.0-beta.1)

English | [简体中文](README.zh-CN.md)

[![License: PolyForm Strict 1.0.0](https://img.shields.io/badge/License-PolyForm_Strict_1.0.0-blue.svg)](#license)
[![Status: Source-Available Public Beta](https://img.shields.io/badge/Release-v0.1.0--beta.1_(Source--Available_Beta)-orange.svg)](#version-mapping--release-identity)
[![Architecture: Public Core](https://img.shields.io/badge/Architecture-Public_Core-green.svg)](#architecture--clean-separation)

**UXDA (User Experience Decision Assistant)** is a source-available, evidence-based Human Factors (HF) and interaction design reasoning skill suite designed for AI pair-programming and tool-calling agent environments (including Google Antigravity, Gemini CLI, Claude Code, Cursor, and custom agent harnesses).

It provides structured decision frameworks, cognitive failure mode audits (e.g., Norman action slips, motor chunking, habituation), ergonomic dimensional conversions, and methodology gating to help AI coding assistants produce defensible, verifiable, and context-aware UX recommendations.

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
+-------------------------------------------------------------------------+
|                        UXDA PUBLIC CORE (This Repo)                     |
|                                                                         |
|  [Router Skill: ux-decision-assistant-router (v0.5.4-beta.1)]             |
|   - Task classification (Guided Learning / Decision / Project Review)   |
|   - Single-Gate pre-flight verification & Business Progress Mapping     |
|   - Evidence taxonomy & methodology boundary enforcement                |
|                                                                         |
|  [Specialist Skill: evidence-based-design-review (v0.7.0-beta.1)]          |
|   - Independent direct-invocation design review                         |
|   - Human factors failure modes (Norman Action Slips, Fitts's Law)      |
|   - Trade-off analysis, competing hypotheses, & Poka-Yoke alternatives  |
|                                                                         |
|  [Public Methodology References & Generic Knowledge Models]             |
|   - ISO 9241, KLM/GOMS calibration rules, cognitive heuristics          |
+-------------------------------------------------------------------------+
                                    │
                                    │ (Optional Context Bundle v0.2 Contract)
                                    ▼
+-------------------------------------------------------------------------+
|                    PRIVATE EXTENSIONS (User-Maintained)                 |
|                                                                         |
|  - Proprietary company rules & internal design systems                  |
|  - Private project registries, document storage, & bindings             |
|  - Confidential telemetry, internal user research records, & approvals  |
|                                                                         |
|  *Note: Public Core operates standalone on user-provided context.       |
+-------------------------------------------------------------------------+
```

---

<a id="version-mapping--release-identity"></a>
<a id="versioning"></a>
## 🏷️ Version Mapping & Release Identity

UXDA Public Core begins its public semantic versioning lifecycle at `v0.1.0-beta.1` (Source-Available Public Beta), while individual modular skills preserve their internal component development version histories:

| Component / Distribution Layer | Public Release Version | Component Evolution Track | Role & Purpose |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core Suite** | **`v0.1.0-beta.1`** | *Source-Available Public Beta* | Unified source-available distribution of the UXDA agent skills |
| `skills/ux-decision-assistant-router` | `v0.5.4-beta.1` | v0.1.0 → v0.5.4-beta.1 | Workflow entry point, task routing, & progress visualization |
| `skills/evidence-based-design-review` | `v0.7.0-beta.1` | v0.1.0 → v0.7.0-beta.1 | Standalone interaction & ergonomic design review specialist |
| External Context Bundle Contract | `v0.2` | Specification v0.2 | Decoupled JSON data exchange schema for optional extensions |

---

## 📦 What's Included in the Public Beta

| Component | Path | Description |
| :--- | :--- | :--- |
| **Router Skill** | `skills/ux-decision-assistant-router` | Main conversational entrypoint. Gathers problem framing, maps business stages, enforces evidence boundaries, and guides O/E/D/V research routes. |
| **Specialist Skill** | `skills/evidence-based-design-review` | Focused design reviewer. Evaluates wireframes, UI changes, hardware panels, and workflows against cognitive and physical ergonomics. |
| **Single-Gate References** | `skills/*/references/` | Core epistemological guides: `analytical-quality.md`, `evidence-boundaries.md`, `design-integration-baseline.md`. |
| **Documentation & Guides** | Root (`*.md`) | Standalone setup guides, synthetic walk-throughs, and methodology boundary definitions. |

---

## 🚀 Quick Start

### 1. Installation
Clone or copy the skills into your agent's shared skills directory (defaults to `~/.agents/skills/`):

```bash
# Clone the repository
git clone https://github.com/<org>/uxda.git

# Copy skills to shared agent directory
mkdir -p ~/.agents/skills
cp -r uxda/skills/ux-decision-assistant-router ~/.agents/skills/
cp -r uxda/skills/evidence-based-design-review ~/.agents/skills/

# (Optional) Link to Antigravity global configuration
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/ux-decision-assistant-router ~/.gemini/config/skills/
ln -s ~/.agents/skills/evidence-based-design-review ~/.gemini/config/skills/
```
See [INSTALLATION.md](INSTALLATION.md) for detailed platform-specific steps and caveats.

### 2. Basic Invocation
Ask your AI assistant using natural prompt phrasing:

```text
"Review this proposed checkout redesign: The product team wants to remove the 
final confirmation screen to increase conversion speed. Evaluate the cognitive failure 
modes, error tolerance risks, and recommend defensible alternatives."
```

UXDA will guide the agent to:
1. Initialize the **Single-Gate pre-flight audit** (verifying evidence limits);
2. Render a top-of-screen **Business Progress Map** (`业务推进图`);
3. Formulate structured **Competing Hypotheses** (e.g., habituation slips vs. feedback latency);
4. Provide actionable, decoupled trade-off recommendations without unsupported claims of zero risk.

---

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

We welcome individuals, researchers, and eligible organizations to explore UXDA's potential in human factors, user experience research, and interaction design review, and to share their experiences, issues, and suggestions through [GitHub Issues](https://github.com/your-org/uxda/issues).

As the project is still under active development and validation, some methodological rules, analytical capabilities, and cross-platform integrations have not yet been sufficiently validated in real-world use. **At this stage, UXDA is best suited for learning, research, evaluation, and experimentation. Direct production deployment is not recommended, nor should its outputs serve as the sole basis for critical business, safety, or compliance decisions.**

UXDA is distributed as **source-available software under the [PolyForm Strict License 1.0.0](LICENSE)** ([polyformproject.org](https://polyformproject.org/licenses/strict/1.0.0)). Use is permitted for purposes covered by the license. Commercial use, software modification, and redistribution require separate authorization from the maintainer. Please refer to the repository's `LICENSE` file for the governing terms.

We will continue refining UXDA based on testing and community feedback, and may revisit its licensing and usage policies as the project matures.
