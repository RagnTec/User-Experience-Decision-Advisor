# UXDA Workflow Pilot — Tasks A–C & Execution Recording Template

> **Status:** Prepared for Stage 1 Workflow Pilot (`0.1.0-beta.5-integration.1`).  
> **Data Provenance Notice:** All three tasks below use **explicitly labeled synthetic / desensitized scenarios** because no user-authorized private study dataset was provided. Do NOT extrapolate synthetic pilot outcomes into real business efficiency or user efficacy claims.

---

## Task A — Multi-Turn Research Plan Co-Creation & Resource Constraint Change

- **Data Origin:** `SYNTHETIC`
- **Objective:** Verify task-first plan drafting, multi-turn constraint downgrade (4-week full study → 5-day, 2-researcher pilot), preservation of still-valid hypotheses/metrics, and explicit narrowing of conclusions.
- **Turn 1 Input (Initial Request):**  
  "We are redesigning our B2B invoice approval flow because finance managers complain 'approvals take too long and feel risky.' We want a research plan covering qualitative discovery and quantitative validation. Assume 4 weeks and 2 researchers."
- **Turn 2 Input (Constraint Change):**  
  "Update: leadership cut the timeline to 5 working days and we cannot recruit external customers yet—only 6 internal finance ops specialists and last 30 days of approval logs are available. Please revise the plan without losing the decision criteria."
- **Expected Pass Criteria:**
  1. Turn 1 avoids mandatory O/E/D/V gates and frames competing hypotheses + feasible plan.
  2. Turn 2 revises only affected parts (recruitment, sample, method downgrade, narrowed claim) rather than rewriting from scratch, and explicitly marks internal ops != external customer generalization.

---

## Task B — Qualitative Coding, Thematic Analysis, Negative Cases & Evidence Traceability

- **Data Origin:** `SYNTHETIC` (desensitized synthetic interview excerpts)
- **Objective:** Verify `qualitative-coding.md` workflow, versioned codebook, unit/source IDs, negative cases, accountable single-reviewer limitation disclosure, and valid `uxda-evidence-v1` JSON output checked by `scripts/validate_evidence.py`.
- **Input Material (Synthetic Excerpts):**
  - `INT-01` (Senior Buyer): "I saw the new 'Auto-Approve' toggle, turned it on once, then turned it off because I couldn't see which vendor rules it matched."
  - `INT-02` (AP Clerk): "Auto-Approve saved me 20 minutes on recurring utility bills; I never had to check rules because the vendor list is fixed." *(Negative / qualifying case)*
  - `INT-03` (Controller): "Our audit log didn't show who enabled Auto-Approve, so compliance told our team to disable it."
  - `INT-04` (Junior Buyer): "I clicked 'Confirm Batch' thinking it only previewed; it actually approved 12 invoices."
- **Expected Pass Criteria:**
  1. Produces a versioned codebook (`codebook_version`), unit/source IDs (`INT-01`..`INT-04`), negative/qualifying case (`INT-02`), competing explanations, and explicit single-reviewer limitation (no fake inter-rater kappa or population prevalence).
  2. Produces a `uxda-evidence-v1` JSON artifact (keeping `synthetic: true`) that passes `scripts/validate_evidence.py` with `truth_verification=not_performed`.

---

## Task C — Experience & Human-Factors Review + Markdown / Offline H5 Deliverable

- **Data Origin:** `SYNTHETIC`
- **Objective:** Verify Specialist human-factors bounds (no invented compliance thresholds), safety/standard separation, localized Chinese Markdown with Mermaid flowchart + text fallback, and offline H5 rendering via `scripts/render_markdown_report.py`.
- **Input Prompt:**  
  "单手握持工业手持平板、佩戴厚防护手套时，8mm×8mm 紧急确认按钮与取消按钮边缘间距 2mm。请给出人因评估与决策边界，并输出可直接转换为离线 H5 的中文 Markdown 报告（含 Mermaid 流程图及文本回退）。"
- **Expected Pass Criteria:**
  1. Separates visual target from hitbox, flags 10mm pitch vs gloved contact risk as expert hypothesis requiring physical measurement, separates ISO 9241 conceptual/voluntary guidance from mandatory machinery E-stop standards (`ISO 13850` / `IEC 60204-1` / `IEC 60947-5-5`).
  2. Markdown converts cleanly via `scripts/render_markdown_report.py --language zh` to a self-contained offline H5 with rendered SVG flowchart, text fallback, and zero remote assets.

---

## Pilot Execution & Recording Template (For Real Runs)

| Field | Task A | Task B | Task C |
|---|---|---|---|
| **Task ID & Data Origin** | `PILOT-A` (`[SYNTHETIC / AUTHORIZED]`) | `PILOT-B` (`[SYNTHETIC / AUTHORIZED]`) | `PILOT-C` (`[SYNTHETIC / AUTHORIZED]`) |
| **Input Summary** | | | |
| **Actual Skill Load Path** | | | |
| **Host & Model** | | | |
| **Raw Output Location** | | | |
| **Human Intervention / Edits** | | | |
| **Rework Count & Cause** | | | |
| **Scientific / Boundary Errors** | | | |
| **Deliverable Status** | | | |
| **Time Spent (min)** | | | |
