# User Experience Decision Advisor (UXDA) — Quick Start Guide

Get up and running with UXDA in 5 minutes using simple, synthetic scenarios.

---

## 1. Four Core Capabilities

The unified UXDA skill supports four core capabilities, selectable directly through natural language in conversation:

| Capability | Trigger Phrasing | Primary Purpose | Key Output Component |
| :--- | :--- | :--- | :--- |
| **`guided`** | "Teach me how to...", "Where should we start research on..." | Pedagogical walkthrough & structured methodology learning | Foundational concepts, methodology trade-offs, & practice exercises |
| **`decision`** | "Help us decide...", "Review the trade-offs of..." | High-stakes choice evaluation and error-mode analysis | Executive decision brief, competing hypotheses, & reversal gates |
| **`project`** | "We have an ongoing study on...", "Help us audit this test data..." | Research execution templates, study design, logging sanity checks, and review | Survey/interview/usability/telemetry templates (`research-execution-templates.md`), milestone review, & data verification |
| **`specialist`** | "Evaluate touch button size for...", "Review UI friction on..." | Laser-focused physical ergonomics and interface review | Quantitative physical math, touch hitbox bounds, & heuristic audit |

---

## 2. Interactive Walkthrough: Reviewing a Destructive Action Pattern

### Scenario:
A product team is debating whether to remove a confirmation modal on a batch-delete action to make bulk cleanup faster.

### Prompt:
```text
We are reviewing a proposed change to our media library management tool:
Currently, deleting a batch of 50 items displays a modal dialog: "Are you sure? This cannot be undone."
The product manager proposes removing this modal to save 1.5 seconds per batch.
Evaluate this change using human factors principles. What failure modes could occur, 
and what alternatives balance speed with safety?
```

### What UXDA Does:
1. **Business Progress Map**: Starts with a single-line navigation track:
   `[Confirmed] Speed vs. Safety Trade-off -> [Active] Cognitive Failure Mode Audit -> [Candidate] Poka-Yoke & Undo Alternatives`
2. **Failure Mode Analysis**:
   - Identifies **Action Slips (Norman Capture Slip)**: Repetitive keyboard selection can cause muscle memory to trigger delete automatically.
   - Identifies **Habituation**: Confirms that modals alone often fail because users click through reflexively (habitual blind-tapping).
3. **Evidence-Based Trade-off**:
   - Explains why removing the modal without a replacement reduces error tolerance to zero.
   - Refuses to invent arbitrary time metrics (e.g., does not claim users will waste "exactly 12 minutes").
4. **Actionable Poka-Yoke Alternative**:
   - Proposes **Optimistic Delete with a 10-second Floating Undo Snackbar** (asynchronous safety buffer).
   - Proposes a **Trash Bin / Soft-Delete lifecycle** before permanent destruction.

---

## 3. Working Directly with the Specialist Capability

You can invoke the **Specialist (Ergonomics & Design Review)** capability directly for detailed technical reviews without answering preliminary questionnaires:

### Prompt:
```text
Conduct a focused human factors design review on an industrial touch screen interface:
Display: 10.1-inch 1280x800 resolution (approx. 149 PPI).
Environment: Cold storage warehouse, operators wearing thick thermal insulated gloves.
Proposed touch buttons: 36px x 36px (approx. 6.1mm physical size).
Identify the physical ergonomics risks and propose a compliant layout baseline.
```

### Expected Specialist Response:
- **Reproducible Physical Math (under 100% display scaling and 1:1 physical pixel mapping)**:
  - 10.1-inch diagonal at 16:10 aspect ratio ($1280 \times 800$) yields $\approx 149.45\text{ PPI}$ and a pixel pitch of $\approx 0.170\text{ mm/px}$.
  - $36 \times 36\text{ px}$ corresponds to $\approx 6.12 \times 6.12\text{ mm}$ physical rendered footprint on this panel.
- **Five Critical Distinctions & Unknowns**:
  1. *Known Screen Parameters*: $149.45\text{ PPI}$ and $\approx 6.12\text{ mm}$ are reproducible physical calculations under 1:1 unscaled pixel assumptions.
  2. *Unknown Touch Hitbox*: $36\text{px}$ describes the rendered icon/visual graphic; whether software provides invisible touch padding (hitbox expansion) remains an unverified implementation detail.
  3. *Unknown Glove & Task Conditions*: Gloved contact area, seam thickness, padding deformation, and tactile feedback depend on specific glove models and cold-storage working postures; avoid citing unverified 15–20mm contact estimates as established facts.
  4. *Advisory Ergonomics vs. Machinery Emergency Safety Standards*: Specific millimeter button proposals require explicit task context, experimental measurement, and citation provenance; they must not be presented as standardized baselines or attributed to ISO 9241 clauses. ISO 9241 standards (e.g. current second edition `ISO 9241-920:2024` on tactile/haptic interactions, replacing the withdrawn 2009 edition) offer voluntary ergonomic guidance without prescribing fixed millimeter button dimensions; phantom numbers like `ISO 9241-924` lack official ISO records and must not be cited. Furthermore, ordinary touch screen buttons must be distinguished from machinery emergency stop standards across three tiers: ISO 13850 (emergency stop function principles), IEC 60204-1 (electrical equipment safety), and IEC 60947-5-5 (mechanical latching switchgear). ISO/IEC standards do not possess universal unconditional legal force unless incorporated by specific legislation; however, an ordinary touch screen interface cannot be treated as an emergency stop device without dedicated functional safety verification under applicable machinery risk assessments.
  5. *Empirical Verification Requirement*: Whether target expansion or spacing adjustments prevent adjacent miss-taps requires real in-situ usability testing with representative operators.
- **Beta Boundary Reminder**: Specific standard clauses and numerical thresholds are advisory; critical industrial safety judgments require human engineering review.
