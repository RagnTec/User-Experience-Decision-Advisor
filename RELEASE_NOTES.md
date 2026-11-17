# Release Notes — UXDA Public Core (`v0.1.0-beta.4`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`  
**Release Phase:** Official Public Beta (`v0.1.0-beta.4`)

## Changes in v0.1.0-beta.4

### 1. Official Public Beta Release Consolidation
- **Full Main Branch Baseline**: Merged the bilingual core architecture and peer review improvements into `main` (merging PR #5).
- **Package Integrity & Verification**: Finalized release package `ux-decision-advisor-v0.1.0-beta.4.zip` (92 files, SHA-256: `30e82bd01c27a26a71456efedac41371426e9687634dfcbd50e4b92d4d5ccb2e`), passing all structural, static, and runtime safety verifications.

### 2. Methodological & Statistical Precision Refinements
- **Non-Significance Epistemic Guardrail**: Refined statistical reporting discipline in `business-facing-output-contract.md`: Failure to reject the null hypothesis ($p > 0.05$) does not establish equivalence. Ruling out practically meaningful effects requires examining effect estimates, uncertainty intervals, and a justified practical importance threshold. Prohibits asserting insufficient statistical power without supporting analysis.
- **Directional Hypothesis & Tail Alignment**: Enforces that one-tailed test outcomes match directional hypotheses without probability misalignments.

### 3. Native Bilingual Core Architecture & Language Auto-Adaptation
- **English-First Marketplace Presentation with Full Chinese Parity**: Re-architected `SKILL.md` to present clean English-first documentation for international skill registries while preserving complete, professional Chinese rules.
- **Dynamic Language Adaptation**: Responds automatically in English when queried in English, and in Chinese when queried in Chinese, without unprompted dual-language mixing.
- **16 Standard Scientific Constructs**: Systematically mapped foundational concepts across Usability, Epistemology, Inference Boundaries, and Problem Framing.

### 4. Defensive Non-Destructive Installation
- **Strict Overwrite Protection**: Provided automated install routines that halt (`exit 1`) if the destination directory or symlink exists.
- **Pre-Extraction Hash Validation**: Guarantees archive integrity prior to unpacking.
- **Standardized Vercel Skills CLI Syntax**: Verified `npx skills add RagnTec/User-Experience-Decision-Advisor@v0.1.0-beta.4 --skill ux-decision-advisor`.

---

## Historical Release Notes — v0.1.0-beta.4-rc.3

# Release Notes — UXDA Public Core (`v0.1.0-beta.4-rc.3`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`  
**Release Phase:** Release Candidate 3 for Bilingual Peer Review (双语同行评审候选版本 3)

## Changes in v0.1.0-beta.4-rc.3

### 1. Native Bilingual Core Architecture (`SKILL.md`)
- **English-First Presentation with Chinese Parity**: Re-architected the main `SKILL.md` entrypoint to prioritize international English display (compatible with LobeHub Marketplace and global agent environments) while retaining full professional and semantic Chinese equivalence.
- **Language Adaptation Policy**: Explicitly defined rules for input language matching: English input yields English output; Chinese input yields Chinese output; user overrides are respected; never provides unprompted dual-language responses; language choice never alters evidence thresholds, risk tiers, or research conclusions.
- **16 Key Scientific Terminology Equivalences**: Aligned core constructs (Usability/可用性, Effectiveness/有效性, Efficiency/效率, Satisfaction/满意度, Human Factors/人因工程, Construct Validity/构念效度, Evidence/证据, Hypothesis/假设, Association/关联, Causation/因果关系, Statistical Significance/统计显著性, Practical Significance/实际意义, User-perceived Problem/用户感知问题, Technical Root Cause/技术根因, Design Recommendation/设计建议, Compliance Requirement/合规要求).

### 2. Strict Installation Overwrite Safety
- **Defensive Extraction Script**: Updated `INSTALLATION.md` and documentation with a non-destructive installation sequence that halts immediately (`exit 1`) if the target destination folder or symlink (including broken symlinks) already exists.
- **Isolated Staging Validation**: Enforced extracting to an isolated temporary directory first, validating archive structure (`SKILL.md` and `LICENSE`), and performing an atomic directory move to prevent corrupt or partial installations.
- **CLI Risk Disclosure**: Noted that Vercel Skills CLI may update in-place without prompting, recommending project-local installations or guarded ZIP extraction where strict non-destructive isolation is required.

### 3. Marketplace Synchronization Delineation
- **Index Origin Clarification**: Documented that community marketplaces (including LobeHub) bind to the repository default branch (`main`, currently locked at `v0.1.0-beta.3`). Candidate releases (`v0.1.0-beta.4-rc.3`) are installed directly via GitHub Release ZIP or Vercel Skills CLI with `@v0.1.0-beta.4-rc.3`.

---

## Historical Release Notes — v0.1.0-beta.4-rc.2

# Release Notes — UXDA Public Core (`v0.1.0-beta.4-rc.2`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`  
**Release Phase:** Release Candidate 2 for Peer Review (线上同行评审候选版本 2)

## Changes in v0.1.0-beta.4-rc.2

### 1. Agent Skills Frontmatter Specification Compatibility
- **String-to-String Metadata Mapping**: Replaced the YAML list in `metadata.historical_components` with a specification-compliant string (`"ux-decision-assistant-router, evidence-based-design-review"`), adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).
- **Body Lineage Documentation**: Documented historical component evolution explicitly in the markdown body of `SKILL.md`.

### 2. Multi-Track Versioning & Documentation Synchronization
- **Unambiguous Version Delineation**: Synchronized version mappings across `README.md`, `README.zh-CN.md`, `INSTALLATION.md`, `RELEASE_NOTES.md`, and `SECURITY.md`.
  - Main Branch Stable Baseline: `v0.1.0-beta.3`
  - Historical RC 1: `v0.1.0-beta.4-rc.1`
  - Active Peer Review Candidate: `v0.1.0-beta.4-rc.2` (PR #5 unmerged, branch `release/beta4-rc1`)
- **Installation Method Clarification**: Delineated the three distinct installation pathways: Release ZIP extraction, Git branch/tag clone, and CLI package managers. Explicitly noted that default installations from `main` fetch `v0.1.0-beta.3`. For Vercel Skills CLI, verified the official tag syntax:
  ```bash
  npx skills add RagnTec/User-Experience-Decision-Advisor@v0.1.0-beta.4-rc.2 --skill ux-decision-advisor
  ```
- **Verified Package Composition (92 Files Total)**: Verified through Git tree inspection at tag `v0.1.0-beta.4-rc.2`:
  - `references/`: 59 files
  - `assets/`: 16 files
  - `scripts/`: 15 files
  - `SKILL.md`: 1 file
  - `LICENSE`: 1 file
  Total: 92 files (packaged in `ux-decision-advisor-v0.1.0-beta.4-rc.2.zip`, SHA-256: `c2aa7a0c5b0c0122d94064957b1cc88c589baf50d2bd0c971ed73dc417bb7cff`).

### 3. Representative Workflow Showcase (`DEMO-02`)
- **Real Business-First Workflow**: Added `DEMO-02` (Game Lag vs. Render Frame Hitching under 2-person, 5-day constraints) to demonstrate the refined business-first interaction protocol:
  - Immediate identification of authentic user experience friction and disrupted control;
  - Bounded multi-hypothesis framing (network jitter, frame hitching, streaming IO, HUD desync);
  - High-leverage 2-person, 5-day triage plan with clear research vs. engineering boundaries;
  - On-demand progressive expansion into deep theoretical, algorithmic, and telemetry details.
- **Historical Baseline Preservation**: Preserved `DEMO-01` (Proactive Schedule Recommendation Card) as the historical `v0.1.0-beta.2` reference baseline.

### 4. Statistical Data Consistency
- **Contingency Parameter Clarification**: Re-verified Fisher exact test parameters in the formative usability test case:
  - Baseline group (Group A): 7/8 completed (87.5%), 1/8 incomplete;
  - Variant group (Group B): 5/8 completed (62.5%), 3/8 incomplete;
  - Fisher exact two-sided $p \approx 0.5692$ (directional one-sided $p \approx 0.2846$);
  - Clarified that `5/8 vs 3/8` describes successful vs. unsuccessful participants within the new variant group, distinct from group-to-group completion rate comparisons (`7/8 vs 5/8`).

---

## Historical Release Notes — v0.1.0-beta.4-rc.1

# Release Notes — UXDA Public Core (`v0.1.0-beta.4-rc.1`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`  
**Release Phase:** Release Candidate 1 for Peer Review (线上同行评审候选版本)

## Changes in v0.1.0-beta.4-rc.1

### 1. Scientific Core & Inference Rigor
- **ISO 9241-11:2018 Conceptual Alignment**: Faithfully represent ISO 9241-11:2018 as a conceptual usability framework (effectiveness, efficiency, satisfaction in context of use). Eliminate ad-hoc composite ratios and false universal prerequisite claims. Strictly distinguish conceptual definitions, operational metrics, custom analyst constructs, and context-dependent task costs.
- **Statistical Inference Discipline**: Prohibit equating $p > 0.05$ with "proven equality" or "no difference"; enforce directional hypothesis tail alignment in exact tests; treat survivor bias / censoring as methodological risks rather than verified empirical facts; explicitly bound small-sample formative tests ($N \le 8$) against population effect-size claims.
- **Metric Operationalization**: Accurately define CTR (clicks ÷ impressions) as a behavioral traffic routing ratio under specific exposure, rather than visual attention, comprehension, or satisfaction. Explicitly distinguish relative change (+15%) from percentage point change (+15pp).

### 2. UX Reasoning & User Encounter Focus
- **Grounding in User Encounters**: Start problem analysis from real user tasks, observable interaction friction, and disruption of user control, rather than premature engineering architecture.
- **Authentic Feedback & Competing Hypotheses**: Respect user descriptions (e.g. "网卡/卡顿") as authentic subjective experience cues rather than patronizingly dismissing them as "self-serving bias" or "fake issues". Systematically formulate and discriminate competing hypotheses (real network jitter, rendering frame hitching, streaming IO contention, HUD display desync) with evidence.
- **Realistic Resource Calibration**: Explicitly structure research plans within stated resource boundaries (e.g. 2 researchers in 5 days) using high-discrimination triage rather than bloated multi-month discovery suites.

### 3. Business-Facing Presentation Contract (`references/business-facing-output-contract.md`)
- **Actionable Conclusion First**: Default chat outputs follow the natural logical flow: *Current judgment → Key evidence & UX mechanism → Business impact & smallest next step*.
- **Internal Machinery Kept Internal**: Keep internal planning identifiers (O/E/D/V, S1–S7, status enums, compulsory menus) internal by default, avoiding robotic software acceptance tone.
- **Collaborative Implementation Boundaries**: UX research proposes candidate decision conditions, guardrail metric frameworks, and risk factors; research does not arbitrarily dictate fixed rollout percentages (e.g. 20%→50%→100%), fixed monitoring durations (e.g. 48-72h), or unverified engineering fixes without stakeholder agreement.
- **Progressive Depth on Demand**: Provide deep professional explanations of theoretical models, measurement constructs, and statistical details when explicitly requested.

### 4. Peer Review Readiness
- Added bilingual Peer Review Trial Guide and concise feedback template.
- License remains PolyForm Strict 1.0.0 (Non-commercial source-available, not OSI-approved open source).

---

## Historical Release Notes — v0.1.0-beta.3

# Release Notes — UXDA Public Core (`v0.1.0-beta.3`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`

## Changes in v0.1.0-beta.3

- Rename the public-facing product from **User Experience Decision Assistant** to **User Experience Decision Advisor**; keep the UXDA abbreviation.
- Replace the Skill identifier `uxda` with `ux-decision-advisor` and move all core files to the matching skill directory.
- Refresh bilingual documentation, installation paths, and Skill discovery metadata; preserve historical component IDs and Beta tags. The GitHub repository was renamed from `RagnTec/User-Experience-Decision-Assistant` to `RagnTec/User-Experience-Decision-Advisor`.
- Include the unchanged PolyForm Strict 1.0.0 LICENSE inside the Skill directory so direct Skill installations carry their license notice.
- No planned changes to the four capability contracts, offline research assets, Python script logic, or evaluation methodology.
- Correct a pre-existing documentation example that called an unbundled `fusion_trace_check.py` script; no validator is added or claimed.

## Installation and migration

New installations should use `npx skills add RagnTec/User-Experience-Decision-Advisor --skill ux-decision-advisor` once this version is on the default branch. Earlier `uxda` installations are not automatically migrated or removed. Keep `v0.1.0-beta.2` as the immutable historical release. The GitHub repository is now `RagnTec/User-Experience-Decision-Advisor` (renamed from `RagnTec/User-Experience-Decision-Assistant`). GitHub preserves historical tags; update local Git remotes and installation commands to the canonical URL.

## Verification status

This document records the intended release delta, not a claim of independent cross-agent or marketplace validation. Verify post-merge file inventory, GitHub Tag release, project-local installation, and channel indexing separately.

---

## Historical Release Notes — v0.1.0-beta.2

# Release Notes — UXDA Public Core (`v0.1.0-beta.2`)

UXDA (User Experience Decision Assistant) Public Core (`v0.1.0-beta.2`) extends the unified single-skill Beta architecture (`skills/uxda`) with ready-to-adapt research execution templates and methodological safeguards hardened through local pilot evaluations.

---

## 1. Version Mapping & Release Identity

UXDA Public Core maintains an independent public semantic version line starting at `v0.1.0-beta.1`. Component skills retain their internal developmental histories for traceability:

| Distribution Component | Public Version | Internal Component Track | Notes |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core Suite** | **`v0.1.0-beta.2`** | *Source-Available Public Beta* | Unified source-available distribution with research execution enablement |
| `skills/uxda` (Unified Skill) | `v0.1.0-beta.2` | Consolidated Router (v0.5.4) & Specialist (v0.7.0) | Single entrypoint delivering Guided, Decision, Project, and Specialist capabilities |
| External Context Bundle Contract | `v0.2` | Specification v0.2 | Generic public JSON interchange specification for optional private extensions |

---

## 2. What's New in `v0.1.0-beta.2`

### Research Execution Templates (`skills/uxda/references/research-execution-templates.md`)
Added progressive-disclosure execution templates (`Template 1–5`) built on top of Adaptive Research Strategy so UXDA can deliver modifiable study instruments with explicit research rationale, applicability criteria, adjustable parameters, evidence boundaries, and decision linkages:
- **Template 1 — Structured Survey**: Instrument design distinguishing co-occurring behaviors (`contact`, `adoption`, `dismissal`, `opt-out`) from mutually exclusive choices, non-probability sampling vs. statistical testing boundaries, and subjective preference vs. effectiveness validation.
- **Template 2 — Qualitative Interview**: Semi-structured interview guides and probing sequences with safeguards against extrapolating exploratory candidate mechanisms into population-level cause rankings.
- **Template 3 — Usability Testing**: Task scenarios, observation prompts, completion/error rubrics, and small-sample qualitative bottleneck discovery limits.
- **Template 4 — Behavioral Telemetry & Bottleneck Analysis**: Event-chain definitions, shared-menu denominator validation, explicit separation of entry CTR / result CTR / search task success rate / satisfaction, observability tiers, missing `session_id`/`search_id` guards, and prohibition of mechanical 1–3s interval deduplication (prioritizing `event_id`, `request_id`, interaction semantics, and duplicate-reporting causes).
- **Template 5 — Mixed-Method & Constrained Pilot**: Combined evidence framing calibrated to decision risk, cost, reversibility, method complementarity, shared bias, and independent replication.

### Methodological Hardening
- **Fact vs. Assumption Separation**: Requires separating confirmed product facts, testable hypotheses, and unknowns before locking study objects or conclusions (`SKILL.md`, `research-project-coproduction.md`, `research-execution-templates.md`).
- **Proportionate Evidence Gating**: Updated `research-evidence.md` and templates to avoid mechanically requiring two independent evidence types for low-risk, easily reversible fixes.
- **4-Capability Architecture Preserved**: Retained the single `skills/uxda/SKILL.md` entrypoint, single-gate pre-flight sequence, and direct `Specialist` review path without introducing multi-skill fragmentation.

---

## 3. Verification & Quality Scope

- **Static & Structural Integrity**: Verified Agent Skills YAML frontmatter (`name`, `description`, `metadata.version`), relative Markdown link integrity across all documents, 8-field completeness across all 5 execution templates, and Python standard-library compatibility (`py_compile` and `--help` across all 15 scripts in `skills/uxda/scripts/`).
- **Isolated Installation & Smoke Checks**: Verified clean-home installation per [INSTALLATION.md](INSTALLATION.md), Antigravity discovery/metadata loading (`v0.1.0-beta.2`), and minimal functional smoke tests for `Project` execution template generation and `Specialist` direct ergonomic review.
- **Local Pilot Regression Coverage**: Pre-release pilot cases (`TC-01` through `TC-06`) verified Guided, Decision, Project, and Specialist workflows along with targeted methodological fixes in survey design and behavioral telemetry prior to final release-doc wrapping.

---

## 4. Known Beta Limitations & Baseline History

- **Known Non-Blocking Beta Boundaries**: UXDA Public Core runs offline without GUI tooling, automated hosting telemetry, or bundled external Python dependencies; optional context bundle integration (`uxda-context-bundle-v0.2`) provides a generic specification only. Cross-host installation paths outside standard `~/.agents/skills/` and tested Antigravity symlinks may require host-specific skill path configuration (see [LIMITATIONS.md](LIMITATIONS.md) and [INSTALLATION.md](INSTALLATION.md)).
- **`v0.1.0-beta.1` Baseline**: Initial source-available public beta introducing the consolidated single-skill architecture (`skills/uxda`), offline local-knowledge evidence scripts (`local_evidence.py`), epistemic boundary protocols, and English/Chinese documentation demos.

---

## 5. Licensing

UXDA Public Core `v0.1.0-beta.2` is published under the **PolyForm Strict License 1.0.0** ([LICENSE](LICENSE)).
