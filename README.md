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

## 🚀 Install, Invoke, and Explore

### 1. Install the two skills (macOS / Linux)

UXDA is an **agent skill package, not a standalone app**. You need an AI agent that can read local skill files. The commands below install both public skills; they do not install an LLM, run a service, or guarantee that every host will discover the skills automatically.

```bash
git clone https://github.com/RagnTec/User-Experience-Decision-Assistant.git
cd User-Experience-Decision-Assistant
mkdir -p ~/.agents/skills
cp -R skills/ux-decision-assistant-router ~/.agents/skills/
cp -R skills/evidence-based-design-review ~/.agents/skills/

# Verify the two entry files exist
test -f ~/.agents/skills/ux-decision-assistant-router/SKILL.md
test -f ~/.agents/skills/evidence-based-design-review/SKILL.md
```

**Google Antigravity (optional discovery links, if required by your setup):**

```bash
mkdir -p ~/.gemini/config/skills
ln -s ~/.agents/skills/ux-decision-assistant-router ~/.gemini/config/skills/ux-decision-assistant-router
ln -s ~/.agents/skills/evidence-based-design-review ~/.gemini/config/skills/evidence-based-design-review
```

Check for an existing link or folder before running `ln -s` again. This is a setup example from the tested environment, **not a universal installation path** for Gemini CLI, Claude Code, Cursor, or every agent host. Consult [INSTALLATION.md](INSTALLATION.md) and your host's skill-discovery settings. **While this repository is Private, cloning requires GitHub access to it.**

### 2. Invoke a skill in your agent chat

There is **no UXDA-specific slash command or hosted API** in this beta. In a compatible agent session, use an explicit natural-language prompt. Skill discovery and actual tool/file access depend on your host.

**Router (guided learning / decision support / project work)**

```text
Use the installed ux-decision-assistant-router skill for this task.
Choose decision mode. Compare two ways of handling an accidental bulk-delete:
(a) a confirmation dialog; (b) reversible deletion with Undo.
Explain the trade-offs, assumptions, and what evidence would change the recommendation.
If the skill is not accessible, tell me instead of pretending it was loaded.
```

**Direct Specialist (focused design review, without starting the Router workflow)**

```text
Use the installed evidence-based-design-review skill directly.
Evaluate the interaction risks of these two interface variants for the
specified task. Separate observable design facts, human-factors inference,
and unknown conditions. Recommend only actionable next steps.
If you cannot access the skill, report that limitation.
```

If your host cannot auto-discover a skill, point it to the corresponding `SKILL.md` in the installed folder **only if the host supports reading local files**. You can also paste a sanitized design description directly; no private extension or company project data is required.

### 3. What can I try? Four short, generic demonstrations

These are **synthetic, illustrative walkthroughs, not captured model sessions or measured UX outcomes**. The excerpts show the *type* of result UXDA is intended to support, not a guaranteed verbatim response. Outputs will differ with the host model, input evidence, and requested scope.

<details>
<summary><strong>A · Guided learning (Router): choose an appropriate UX research method</strong></summary>

**Try this prompt:**

```text
Use ux-decision-assistant-router in guided mode.
In a generic shopping app, we suspect people have trouble locating filters.
Teach me how to decide between interviews, task-based usability testing,
and a survey. Give a minimal pilot plan and explain what each method cannot prove.
No real participant data is available yet.
```

**Illustrative result excerpt:**

```text
Research question: Can people find and use the filter during a product task?
Suggested first step: Observe a small task-based pilot before measuring prevalence.
What to record: task success, navigation detours, hesitation, and participant comments.
Evidence boundary: The difficulty is a hypothesis; no failure rate can be reported yet.
Next decision: Use pilot observations to refine the problem and the later survey.
```

</details>

<details>
<summary><strong>B · Decision support (Router): speed versus error recovery</strong></summary>

**Try this prompt:**

```text
Use ux-decision-assistant-router in decision mode.
A media manager proposes removing the confirmation dialog before deleting
several files. Compare keeping the dialog with a reversible delete + Undo.
Consider accidental actions, habituation, irreversibility and effort.
Recommend a conditional choice; do not invent completion-time improvements.
```

**Illustrative result excerpt:**

```text
Current recommendation: Compare Undo + recoverable deletion when recovery is
reliable; retain stronger confirmation before irreversible deletion.
Counterexample: If the platform cannot guarantee recovery, Undo is not equivalent.
Still unknown: actual deletion reversibility, usage frequency, and error reports.
Decision gate: Do not approve a final design without confirming those conditions.
```

</details>

<details>
<summary><strong>C · Project work (Router): plan a low-cost pilot, not fictional results</strong></summary>

**Try this prompt:**

```text
Use ux-decision-assistant-router in project mode.
Help plan a small usability pilot for two navigation layouts in a generic
task manager. Define tasks, observations, possible order effects, a simple
recording table and the decision this pilot can inform.
This is a plan only; no sessions have been run.
```

**Illustrative result excerpt:**

```text
Pilot goal: Identify major findability problems, not estimate population effects.
Design: Counterbalance layout order where feasible; use the same goal-driven tasks.
Record: layout, sequence, task completion, assistance, detours, qualitative notes.
Next step: Run the pilot, inspect conflicting cases, then decide whether to scale.
Not evaluated: Any observed advantage, significance test, or user preference rate.
```

</details>

<details>
<summary><strong>D · Direct Specialist: physical touch target and context review</strong></summary>

**Try this prompt:**

```text
Use evidence-based-design-review directly, without Router mode selection.
A 10.1-inch 1280×800 industrial touch display uses 36×36 px controls.
Operators may wear insulated gloves. Estimate the displayed control size
from the supplied screen dimensions, identify interaction risks, and propose
what physical measurements or user trials are still needed.
Do not invent a mandatory ISO minimum.
```

**Illustrative result excerpt:**

```text
Calculated estimate: ~149.5 PPI; 36 px corresponds to ~6.1 mm on the display.
Potential issue: the visible graphic, actual touch hitbox and gloved fingertip
contact area may be different. A pixel count alone cannot establish usability.
Recommendation: Verify effective hitbox geometry and test realistic gloves/tasks.
Boundary: No compliance certification or observed mis-touch rate is implied.
```

</details>

**Want a visual report?** If your host allows local file writing, you may additionally ask: `After the review, offer an HTML/H5 summary. Create it only after I approve the format.` This is an optional presentation workflow, not a guaranteed built-in GUI. Short real-session screenshots can be added later; the previews above deliberately avoid fabricated screenshots or success metrics.

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
