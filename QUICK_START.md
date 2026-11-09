# UXDA Quick Start Guide

Get up and running with UXDA in 5 minutes using simple, synthetic scenarios.

---

## 1. Core Operating Modes

UXDA Router supports three main operational modes, selectable directly in conversation:

| Mode | Trigger Phrasing | Primary Purpose | Key Output Component |
| :--- | :--- | :--- | :--- |
| **`decision`** *(Default)* | "Help us decide...", "Review the trade-offs of..." | High-stakes choice evaluation and error-mode analysis | Executive decision brief, competing hypotheses, & reversal gates |
| **`guided`** | "Explain the human factors principles of...", "Teach me how to..." | Pedagogical walkthrough & structured learning | Foundational concepts, methodology trade-offs, & practice exercises |
| **`project`** | "We have an ongoing study on...", "Help us audit this test data..." | Research design, logging sanity checks, and review | Milestone review, data verification, & task decomposition |

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

## 3. Working Directly with the Specialist

You can invoke the **Evidence-Based Design Review Specialist** directly for detailed technical reviews:

### Prompt:
```text
Conduct a focused human factors design review on an industrial touch screen interface:
Display: 10.1-inch 1280x800 resolution (approx. 149 PPI).
Environment: Cold storage warehouse, operators wearing thick thermal insulated gloves.
Proposed touch buttons: 36px x 36px (approx. 6.1mm physical size).
Identify the physical ergonomics risks and propose a compliant layout baseline.
```

### Expected Specialist Response:
- Derives physical millimeter dimension: $149\text{ PPI} \implies 0.170\text{ mm/px} \implies 36\text{px} \approx 6.1\text{mm}$.
- Contrasts 6.1mm with adult glove contact dimensions (15–20mm contact footprint).
- Cites ISO 9241 physical input baselines (noting specific clauses are guidelines, not statutory laws).
- Separates visual graphic bounds from touch hitboxes ($\ge 48\text{px}$ or $\ge 12\text{mm}$ hitbox padding).
- Clarifies that final operating sign-off belongs to industrial safety engineers.
