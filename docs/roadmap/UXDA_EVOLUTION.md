# UXDA Evolution Roadmap

**Current Public Beta:** `v0.1.0-beta.5`  
**Status Taxonomy:** `Closed / Completed` | `Active Next` | `Planned` | `Unvalidated Assumption`

---

## Phased Lifecycle & Current Status

| Phase | Status | Scope, Evidence & Boundary |
|---|---|---|
| **Stage 0 — Mainline Integration** | **Closed / Completed** | Merged Beta.4 (`1c2def9`) and Qoder Pilot.3 (`0.1.0-qoder-research-pilot.3`): task-first entry, 4 silent lenses, 3-layer delivery, rule precedence, UXRR upstream boundary, `Evidence-to-Outcome Guardrail`, `uxda-evidence-v1` + 3 consistency guards, dual `render_report.py` dispatch, `render_markdown_report.py`, and 61/61 engineering unit tests. |
| **Stage 1A — Synthetic Workflow Pilot** | **Closed / Completed** | Executed independent isolated-ZIP Pilots A–C (`EXPLICIT_LOAD`, `research` / Flash) with Beta.4 baseline comparison, `validate_evidence.py` check on Pilot B JSON, and `render_markdown_report.py` H5 generation on Pilot C. Native `/skills reload` auto-discovery (`NATIVE_SKILL`) remains `NOT_RUN` without modifying global Beta.4. |
| **Beta.5 — Public Beta Release** | **Active (`v0.1.0-beta.5`)** | Public Beta release consolidating the integrated research workflow, qualitative coding, descriptive analysis, evidence contract, and Markdown→H5 reporting. Validation checks structure and links, not source truth or scientific efficacy. |
| **Stage 1B — Authorized Real-World Workflow Pilot** | **Active Next** | Prepare and record real-world authorized feedback (2–3 tasks: workflow friction/time, avoidable rework, evidence gaps, decision consequences) and build a held-out methodology evaluation set separate from tuning cases. **No new feature development is triggered automatically.** |
| **Stage 2 — Qualitative Depth, Schema Migration & Minimal Research Ops** | **Planned** | Deepen qualitative coding vertical slice; extend `uxda-evidence-v1` only after Stage 1B real-task gaps are observed (including **decoupling per-evidence conflict relations from overall claim support degree**, source version/authorization/retention, decision linkage, denominator/missingness fields) via explicit versioned migration; add minimal Research Ops handoff (screener, consent, scheduling, data management). |
| **Stage 3 — Bounded Quantitative Design & Specialist Slices** | **Planned** | One bounded quantitative design module (power, sample size, or equivalence) driven by validated task need (not an omnibus stats engine), plus targeted human-factors and accessibility slices with traceable primary standards. |
| **Stage 4 — Conditional Interoperability Adapters** | **Planned (Conditional)** | Only if Stage 1B–2 workflows demonstrate need: specify common adapter contract and threat model (permissions, consent, retention, prompt injection, provenance, deletion, vendor policy), starting with one local import or authorized read-only adapter. |
| **Stage 5 — Optional Scale-Out** | **Planned (Optional)** | Cross-project evidence browser, reusable decision history, selected domain packs, and marketplace expansion, prioritized by real demand and quality data. |

---

## Market Research Caveat

`MARKET_UX_UXR_SKILLS_2026.md` (retained in Qoder pilot development archives) is dated exploratory evidence (2026-11-25/26). Installation counts, provider product descriptions, pricing, and reported market gaps are not independently verified facts in this release; recheck primary sources before letting any market claim drive a decision.
