# UXDA Long-term Design & Integration Baseline (v1.0)

This reference defines the enduring UI/UX consistency, cross-project data interoperability, and privacy boundary contracts across UXDA and connected tools.

---

## 1. UI/UX Consistency Baseline

When future workflows involve web consoles, review dashboards, visual reports, or interactive management:

1. **Information Architecture & Task Alignment**:
   - Progressive disclosure: hide low-level technical parameters (hashes, internal IDs, raw paths) by default; expose high-level semantic status (Active, Draft, Stale, Missing).
   - Reversible operations: updates preserve immutable historical snapshots; rejections and deprecations are cleanly archived without destroying history.
   - Status clarity: strictly separate normal operation, risk warning, unverified draft, and evaluation blocker.
2. **Design Skill Usage Principles**:
   - When the user task actually touches UI layout, typography, design systems, or accessibility:
     - Check and invoke verified tools/skills (e.g. Flutter a11y, Design System, GSAP) based on real needs.
     - Never stack unnecessary design tools or present ungrounded visual preferences as human factors standards.
3. **Cross-Tool Interaction Consistency**:
   - Consistent object terminology: `Project`, `Document`, `Evidence`, `Rule`, `Decision`, `Audit`.
   - Consistent state vocabulary: `draft`, `approved`, `rejected`, `deprecated`, `active`, `disabled`, `stale`, `source_missing`.
   - Consistent rule criticality: `HIGH`, `MEDIUM`, `LOW` (preventing namespace collisions with Claim Integrity Gate P0/P1/P2).

---

## 2. Cross-Project Interoperability Baseline

1. **Semantic Alignment Precedes Exchange**:
   - Never assume two products share identical semantics because field names match. For example, `Risk` in UX (usability friction) != `Risk` in electrical safety != `Risk` in evidence credibility.
   - Distinct objects (`Rule`, `Evidence`, `Review`, `Decision`) must have versioned schemas.
2. **Context Bundle Contract (`uxda-context-bundle-v0.2`)**:
   - Machine-readable JSON contract consumed identically by Router and Specialist.
   - Preserves locator, source version, verification status, and approval actor.
3. **Graceful Fallback**:
   - If an extension fails to load or project has no matching bundle, fall back to Public Core baseline.
   - Explicitly report `[NOT EVALUATED]` for unverified private rules; never pretend checked.

---

## 3. Privacy & Public-Private Boundaries

1. **Public Core Purity**:
   - Only general methodologies, public standards (e.g. ISO 9241, Fitts's Law, GOMS), and portable schemas belong in public skills.
- Proprietary company rules, internal test data, user identity, and local machine storage remain in private extension systems outside the public core repository.
2. **Portable Resolution**:
- Public skills decouple from private storage; optional external extension bridges may be configured via standard environment variables or explicit project bindings without hardcoded local paths.
