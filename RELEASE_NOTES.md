# Release Notes — UXDA Public Core (`v0.1.0-beta.3`)

**Product:** User Experience Decision Advisor (UXDA) / 用户体验决策顾问  
**Skill ID:** `ux-decision-advisor`  
**Canonical path:** `skills/ux-decision-advisor/`

## Changes in v0.1.0-beta.3

- Rename the public-facing product from **User Experience Decision Assistant** to **User Experience Decision Advisor**; keep the UXDA abbreviation.
- Replace the Skill identifier `uxda` with `ux-decision-advisor` and move all core files to the matching skill directory.
- Refresh bilingual documentation, installation paths, and Skill discovery metadata; keep historical component IDs and the original repository URL unchanged.
- Include the unchanged PolyForm Strict 1.0.0 LICENSE inside the Skill directory so direct Skill installations carry their license notice.
- No planned changes to the four capability contracts, offline research assets, Python script logic, or evaluation methodology.

## Installation and migration

New installations should use `npx skills add RagnTec/User-Experience-Decision-Assistant --skill ux-decision-advisor` once this version is on the default branch. Earlier `uxda` installations are not automatically migrated or removed. Keep `v0.1.0-beta.2` as the immutable historical release. The GitHub repository name intentionally remains unchanged.

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
