# UXDA Evolution Roadmap

**Current Integrated Baseline:** `0.1.0-beta.5-integration.1` (local integration of `v0.1.0-beta.4` + `0.1.0-qoder-research-pilot.3`)  
**Status Taxonomy:** `Implemented` | `Partially Implemented` | `Planned` | `Unvalidated Assumption`

---

## Current State Summary

| Area | Status | Notes & Evidence Boundary |
|---|---|---|
| Task-first entry, silent 4 lenses, 3-layer delivery | **Implemented** | `SKILL.md`, `core-reasoning.md`, `decision-and-business-output.md`; verified via 60 unit tests & prompt checks |
| Bilingual parity & localized Markdown/H5 reports | **Implemented** | `bilingual-parity.md`, `render_markdown_report.py`, dual `render_report.py` dispatch |
| Evidence-to-outcome & non-significance guardrails | **Implemented** | `business-facing-output-contract.md`, `core-reasoning.md` |
| Minimal evidence contract (`uxda-evidence-v1`) + 3 consistency guards | **Implemented** | `validate_evidence.py` (structural & within-study reference checks only; not truth verification) |
| Qualitative coding worksheet & bounded descriptive script | **Implemented** | `assets/qualitative-coding.md`, `scripts/analyze_synthetic.py` (no causal/power certification) |
| Real-workflow validation & held-out evaluation set | **Planned** | Synthetic/prompt checks exist; real authorized task validation not yet collected |
| Cross-study evidence graph & Research Ops handoff | **Planned** | Explicitly deferred to Stage 2 after Stage 1 real-task evidence |
| Quantitative design module (power / equivalence) | **Planned** | Deferred to Stage 3; no omnibus stats engine |
| External tool connectors / read-only adapters | **Planned (Conditional)** | Deferred to Stage 4; requires threat model, privacy review, and separate authorization |

---

## Phased Evolution Plan

### Stage 1 — Real Workflow Pilot & Held-Out Evaluation (Post-Integration)
- **Scope & Owner**: UXDA maintainer + 1–2 internal UXR partners.
- **Activities**:
  - Run a small real workflow pilot (2–3 authorized tasks), collecting current workflow friction/time, avoidable rework, evidence gaps, and decision consequences.
  - Establish a small held-out methodology evaluation set separate from tuning cases (covering Chinese and English).
  - Conduct proportionate risk-based review; use independent expert review and inter-rater agreement where feasible, otherwise explicitly record single-reviewer limits.
- **Acceptance Evidence**: Written pilot log distinguishing real-task outcomes from synthetic checks; held-out pass/fail ledger.
- **Boundary**: Does not gate initial local integration.

### Stage 2 — Qualitative Depth, Schema Migration & Minimal Research Ops Handoff
- **Dependencies**: Observed real-task gaps from Stage 1.
- **Activities**:
  - Deepen the existing qualitative coding vertical slice first.
  - Extend `uxda-evidence-v1` only after real-task gaps are observed (e.g., per-evidence support links, source version/authorization/retention, decision linkage, denominator/missingness fields) under one authoritative schema/registry with explicit versioned migration before cross-study/cross-project reuse.
  - Introduce decision follow-up and observed outcomes, then a minimal Research Ops execution handoff (recruitment brief, screener, consent, scheduling/roles, data management).
- **Boundary**: No fake evidence or pseudo-precision.

### Stage 3 — Bounded Quantitative Design & Specialist Slices
- **Dependencies**: Validated task need from Stages 1–2.
- **Activities**:
  - Add one bounded quantitative design module (power, sample size, or equivalence) driven by validated task need — not an omnibus statistics engine.
  - Improve human factors and accessibility research as targeted specialist slices, prioritizing traceable methods, primary standards, and verified applicability.
- **Boundary**: No automatic standards or accessibility certification.

### Stage 4 — Conditional Interoperability Adapters
- **Dependencies**: Demonstrated workflow need + completed threat model & privacy review.
- **Activities**:
  - Specify common adapter contract and threat model (permissions, authorization/consent, retention, prompt injection, provenance, read/write capabilities, deletion, vendor policies).
  - Start with one local import or authorized read-only adapter; external connectors require separate approval.
- **Boundary**: No automated recruiting, payment, external publishing, or unauthorized write-back. Treat other UX tools as interoperability peers rather than re-implementing them inside UXDA.

### Stage 5 — Optional Scale-Out
- **Activities**: Cross-project evidence browser, reusable decision history, selected domain packs, and marketplace expansion, prioritized strictly by real demand and quality data.
- **Boundary**: No autonomous research platform, hosted repository, or new identity system by default.

---

## Market Research Caveat

`docs/qoder-local-pilot/MARKET_UX_UXR_SKILLS_2026.md` (if referenced) is retained only as dated exploratory evidence (2026-11-25/26). Installation counts, provider product descriptions, pricing, and reported market gaps are not independently verified facts in this release; recheck primary sources before letting any market claim drive a product decision.
