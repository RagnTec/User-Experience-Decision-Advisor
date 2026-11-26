# pilot_a_beta4.md

## Turn 1

### Recommendation & Scope Judgment

With **4 weeks and 2 researchers**, you can run a high-signal **qualitative discovery phase (Weeks 1–2)** and a **pre-launch quantitative validation phase (Weeks 3–4)**—provided you calibrate what "quantitative validation" means inside a 4-week window.

Specifically, 4 weeks with 2 researchers is sufficient to:
1. Diagnose **where** time and confidence break down (via existing approval logs + 6–8 behavioral walkthrough interviews), and
2. Quantitatively test whether a redesigned prototype improves **task completion, discrepancy-detection accuracy, active review time, and perceived confidence** before engineering builds it (via a structured benchmark usability study + a brief targeted survey).

However, 4 weeks is **not** enough to measure post-launch production cycle-time reduction or long-term error rates in live B2B traffic unless engineering already has an instrumentation pipeline and live traffic ready to test immediately. Framing Weeks 3–4 as **pre-build quantitative validation (prototype benchmark + targeted survey)** plus **production guardrail definition** keeps the plan realistic and prevents false certainty.

---

### Separating Facts, Missing Context, and Working Assumptions

Before locking instruments, separate what we know from what still needs confirmation:

- **Known facts**: You are redesigning a B2B invoice approval flow; finance managers report that "approvals take too long and feel risky"; the goal covers qualitative discovery and quantitative validation with 2 researchers over 4 weeks.
- **Missing context (To Confirm in Days 1–2)**:
  1. *Baseline data access*: Do approval timestamps, rejection/escalation logs, or ERP audit trails already exist and can researchers inspect them in Week 1?
  2. *Workflow & policy constraints*: Is this single-approver or multi-tier routing (e.g., PO-matched vs. non-PO invoices, dollar thresholds), and which verification steps are mandatory compliance/audit controls?
  3. *Prototype & recruitment readiness*: Will design have clickable prototypes ready by the start of Week 3, and how quickly can you recruit internal/customer finance managers?
- **`[Working Assumptions]`**: This plan assumes (a) Week 3–4 validation targets a pre-engineering or staging prototype rather than a live A/B release, and (b) at least basic approval logs or finance ops ticket records exist to inspect in Week 1.

---

### Competing Hypotheses & Core UX Mechanisms

Treat *"takes too long"* and *"feels risky"* as authentic experiential cues—and keep **speed** and **risk calibration** together. Cutting confirmation steps to make approvals faster can *increase* perceived risk—or worse, increase rubber-stamping of bad invoices.

| Complaint Cue | Competing UX / Product Hypotheses | Alternative (Non-UI) Hypotheses to Rule Out |
| :--- | :--- | :--- |
| **"Takes too long"** | • **Cross-screen scavenging**: Managers switch across invoice PDFs, POs, receipts, and budget trackers to verify details.<br>• **Manual exception handling**: Unclear mismatch explanations force off-system Slack/email follow-ups. | • **Routing / SLA wait time**: Total approval time is dominated by multi-tier queue waits or ERP sync latency rather than UI interaction time.<br>• **Policy friction**: Mandatory threshold rules require secondary sign-off regardless of UI. |
| **"Feels risky"** | • **Opaque system checks**: Users cannot see whether PO/tax/duplicate checks already ran or passed.<br>• **Unclear accountability & reversibility**: Users do not know what happens after clicking *Approve* (can it be recalled? who is liable if an error slips through?). | • **Legitimate high-stakes consequence**: Recent audit findings, vendor fraud incidents, or unclear corporate approval policies drive caution outside the interface. |

---

### 4-Week Research Plan (2 Researchers)

#### Week 1: Baseline Log Audit, Compliance Guardrails & Recruitment (Parallel Tracks)
*Goal: Locate bottlenecks in existing data and secure Week 2–3 participants before writing new UI.*

- **Researcher A — Existing Evidence & Event Audit**:
  - Inspect historical approval logs, rejection reasons, and support/ops tickets (check denominators, missing records, and whether "approval duration" mixes *active screen review time* with *idle queue wait time*).
  - If telemetry is incomplete, align with engineering on one minimal funnel chain (marking unverified events as `[Suggested Event]`):
    - `view_invoice_approval_detail` → `open_supporting_evidence` (PO / receipt / audit log; isolate sub-tabs with `selected_tab`) → `submit_approval_decision` (`decision=approve|reject|escalate`)
    - **Five-element metric rule** (example for supporting-doc check rate): *Numerator*: distinct `attempt_id` triggering `open_supporting_evidence`; *Denominator*: distinct `attempt_id` triggering `view_invoice_approval_detail`; *Time window*: single review session (e.g., ≤ 30 min); *Deduplication unit*: `attempt_id` / `invoice_id` (not crude 1–3 second time-window stripping); *Broken-link handling*: bucket orphaned downstream events separately for logging QA rather than forcing them into conversion rates. Note that front-end submission (`approval_triggered`) does not guarantee downstream ERP settlement succeeded.
- **Researcher B — Compliance Framing & Participant Recruitment**:
  - Align with Finance/Compliance owners on non-negotiable audit requirements (UX research identifies friction and verification gaps; Compliance/Finance owns legal and audit sign-off).
  - Recruit **6–8 finance managers** for Week 2 discovery and **12–16** (minimum **10–12** if recruitment is tight) for Week 3–4 benchmark testing, stratified by invoice complexity/approval tier (e.g., SMB vs. enterprise or high-volume vs. high-value approvers).

#### Week 2: Qualitative Discovery (Mechanisms & Mental Models)
*Goal: Understand how finance managers actually verify invoices and what creates confidence vs. hesitation.*

- **Method**: **6–8 Contextual Inquiry / Behavioral Retrospective Interviews** (40–45 min each; 3–4 per researcher), anchored on a recent invoice the participant actually approved, rejected, or delayed.
- **Core Inquiry Structure (Facts Before Opinions)**:
  1. *Recent episode walk-through (Behavior)*: "Walk me through the last invoice that felt slow or made you hesitate—what did you open first, and where did you pause?"
  2. *Verification & evidence check (Behavior)*: "In that specific case, what information did you check before deciding, and did you leave this tool (e.g., ERP, spreadsheets, Slack/email) to verify anything?"
  3. *Action & reversibility model (Mental Model)*: "Right before clicking Approve/Reject, what did you expect would happen next, and what did you think would happen if a mistake was caught afterward?"
  4. *Subjective attribution (Opinion — logged separately from observed facts)*: "Looking back, which part felt riskiest or most time-consuming?" *(Treat self-diagnoses as cues to test, not proven root causes.)*
- **Method Boundary**: Qualitative interviews reveal **mechanisms, verification vocabulary, and hidden workarounds**. Do **not** rank population causes by small-sample counts (e.g., "4 of 6 managers said X" does not mean 67% of all managers experience X).
- **End-of-Week-2 Checkpoint**: Deliver a concise mechanism map to Product/Design. If discovery shows the delay is mostly off-system SLA/ERP latency rather than UI, flag that immediately before prototyping begins.

#### Week 3: Quantitative Validation Setup & Targeted Micro-Survey
*Goal: Prepare unbiased benchmark tasks and quantify self-reported friction prevalence across a wider sample.*

- **Track A — Benchmark Usability Protocol Prep & Pilot (Prototype)**:
  - Design **2–3 realistic approval tasks** comparing Current vs. Redesign (or testing Redesign against baseline criteria), ensuring at least one **clean match** and one **subtle discrepancy/exception** (e.g., quantity mismatch or duplicate invoice).
  - **Order & learning control**: If using a within-subject comparison (A/B), counterbalance task order with equivalent-complexity invoice pairs—while noting that order balancing reduces but does not guarantee elimination of learning carryover.
  - Pilot the protocol with 2 internal/non-team reviewers to verify prototype error states, timing capture, and realistic financial figures.
- **Track B — Targeted Micro-Survey (3–4 Questions, In-App or Email to Broader Approver Pool)**:
  - Suitable for estimating **self-reported** friction patterns and perceived risk drivers across roles/tiers (not actual task speed or error rates).
  - Keep items single-construct, mutually exclusive, with complete branching and "cannot recall / N/A" exits:
    - *Q1 (Recent workflow routing)*: In your last 7 days of invoice approvals, which situation happened most recently when an approval stalled? (`A. Had to cross-check PO/receipt/contract outside the tool` / `B. Unsure if automated checks or prior approvals were complete` / `C. Waited on another person/department` / `D. No stalls in the last 7 days` / `E. Cannot recall`) → *Route D/E to end; A/B/C to Q2.*
    - *Q2 (Perceived risk driver, branched for A/B/C)*: What most increased your sense of risk in that approval? (Rotate options covering missing mismatch detail, unclear reversibility/recall, unclear liability/audit trail, or Other.)
    - *Q3 (Perceived confidence rating)*: Symmetrical 5-point scale on confidence that approved invoices are error-free (+ independent "Unable to judge" option).

#### Week 4: Quantitative Benchmark Execution, Triangulation & Decision Handoff
*Goal: Test whether the redesign improves efficiency without sacrificing accuracy or safety.*

- **Execute Benchmark Testing ($N=10–16$, 30–40 min each, ~5–8 sessions per researcher)**:
  - **Core Metrics (Separating Effectiveness, Efficiency, and Perceived Confidence)**:
    1. *Discrepancy-detection accuracy* (Effectiveness): % of participants who catch the planted error without prompting. **Critical guardrail**: faster approvals caused by missing discrepancies represent failure, not improvement.
    2. *Task completion & active decision time* (Efficiency): Record successful-task time separately from failed/abandoned attempts so survivor bias does not disguise difficult failures as speedups.
    3. *Perceived ease & approval confidence* (Satisfaction/Confidence): Single Ease Question (SEQ) + post-task risk/confidence rating. (Keep SEQ distinct from actual error-detection accuracy.)
- **Inference & Triangulation Discipline**:
  - Use **method complementarity**: logs locate *where* steps drop off, interviews explain *why* hesitation occurs, and benchmark testing verifies *whether* the new interaction resolves the friction while preserving error detection.
  - Avoid **shared-bias claims**: if survey respondents and interviewees come from the same small group of vocal complainers, treat findings as directional rather than independent population replication.
  - When reporting comparative benchmark results, report point estimates, uncertainty intervals, and exact denominators. If a difference is statistically non-significant ($p > 0.05$), never claim the two flows are "equivalent"—state the uncertainty and practical magnitude instead.

---

### Decision Conditions & Contingency Plan

- **Conditional Criteria to Recommend Engineering Build / Limited Pilot**:
  - The redesign removes cross-screen verification friction (shorter observed active review time or fewer external-tool switches in benchmark tasks) **AND** discrepancy-detection accuracy is maintained or improved **AND** Finance/Compliance confirms required audit cues remain intact.
  - *Post-launch production guardrails* (for Product/Engineering/Finance owners to calibrate): track post-approval reversal/dispute rate, discrepancy catch rate, and active review time vs. queue wait time in a staged release.
- **Trigger to Pause / Rework**:
  - Speed improves only because users miss planted discrepancies (rubber-stamping risk), or discovery shows >50% of delay is backend routing/policy latency that UI changes will not fix.
- **Fallback if Constraints Slip**:
  - *If external finance manager recruitment takes >1 week*: Start Week 2 with internal finance/accounting staff who handle real approvals (clearly labeled as internal proxy sample—useful for structural workflow defects, not representative of external customer variance).
  - *If clickable exception states are not ready by Week 3*: Run a static cognitive walkthrough focused on information hierarchy and risk cues, and explicitly defer quantitative speed/accuracy validation until an interactive build is ready.

---

### Smallest Next Step (Days 1–2)

Before kicking off recruitment or drafting full scripts:
1. **Confirm log & SLA breakdown**: Ask Data/Engineering whether existing logs separate *active review duration* from *multi-tier waiting time* and record rejection/escalation reasons.
2. **Confirm compliance non-negotiables**: Ask Finance/Compliance what verification evidence must stay mandatory on-screen.
3. **Lock the Week 2–4 participant pool**: Confirm whether 15–20 customer or internal finance managers can be scheduled starting next week.

*On-demand expansion available*: I can expand the full Week 2 behavioral interview guide, the complete benchmark task cards with planted discrepancy scenarios, or the formal telemetry event specification once you confirm prototype and data availability.

---

## Turn 2

### Revised Judgment & Claim Boundaries (5 Working Days)

You can still execute a high-value **5-day diagnostic and risk-triage sprint** without compromising your decision criteria—provided you **narrow what the 5 days claim to prove** and scale the release decision to match the weaker sample.

Specifically, **30 days of approval logs + 6 internal finance ops specialists** can reliably establish:
1. **Where time actually goes** in production (active review friction vs. multi-tier queue/ERP wait time, from the 30-day logs), and
2. **Deterministic usability and risk defects** in the current flow and candidate redesign (missing verification cues, confusing mismatch states, or rubber-stamping hazards).

What this 5-day sprint **cannot** establish is external customer prevalence, generalizable task-duration lift, or statistical equivalence. Internal finance ops specialists share company-specific terminology, ERP familiarity, and policy priors—so they are an **internal proxy sample**, not independent external validation, and small-sample counts cannot be extrapolated to external finance managers.

---

### Updated Scope: Knowns, Gaps, and Working Assumptions

- **Updated facts**: 5 working days; external customer recruitment is unavailable; **6 internal finance ops specialists** and **the last 30 days of approval logs** are available.
- **Working assumptions**: `[Working Assumption]` 2 researchers remain assigned; a static or clickable redesign candidate will be available by Day 3 for Day 4 testing.
- **Confirm on Day 1 morning (`To Confirm`)**:
  1. Do the 30-day logs separate **active screen review duration** from **end-to-end routing/queue wait time**, and do they include a single-attempt identifier (`attempt_id` or `session_id`) alongside `invoice_id`?
  2. Which compliance/audit verification checks are legally or policy-mandatory (owned by Finance/Compliance)?
  3. Will Day 4 test an interactive prototype or static screens? *(Static mocks can check comprehension and risk cues, not click speed or error recovery.)*

---

### Revised 5-Day Plan (2 Researchers)

To avoid contaminating Day 4 prototype error-catching with Day 2 exposure, **split the 6 internal specialists into two cohorts of 3** (3 for current-flow diagnosis on Day 2; 3 unexposed specialists for prototype task checks on Day 4).

#### Day 1: 30-Day Log Audit Setup, Compliance Guardrails & Scheduling
- **Researcher A (Log Analysis)**:
  - Pull the last 30 days of invoice approval records with explicit denominators (total submitted invoices, approved, rejected, escalated, and post-approval reversals/disputes).
  - Separate **active review time** (if session logs exist) from **queue/SLA wait time** across approver tiers. If `session_id`/`attempt_id` is missing, document that step-by-step UI funnel reconstruction is not reliable and restrict quantitative claims to invoice-level state transitions and cycle times.
- **Researcher B (Compliance & Participant Prep)**:
  - Lock non-negotiable audit cues with Finance/Compliance owners.
  - Schedule the 6 internal specialists: **Cohort 1 (3 specialists)** on Day 2 for recent-invoice behavioral walkthroughs; **Cohort 2 (3 unexposed specialists)** on Day 4 for prototype task testing.

#### Day 2: Log Deep-Dive + Current-Flow Behavioral Walkthroughs (Cohort 1, $n=3$)
- **Researcher A**: Slice 30-day logs by invoice type (PO-matched vs. non-PO), dollar threshold, and rejection/reversal outliers to identify where delays and errors cluster.
- **Researcher B**: Run three 35-minute behavioral walkthroughs anchored on **actual delayed or flagged invoices** from the last 30 days:
  1. *Exact sequence*: Which screens, tabs, or external tools (ERP, spreadsheets, Slack/email) did they open to verify this invoice?
  2. *Risk trigger*: Where did they pause, and what check did they feel was missing or unconfirmed?
  3. *Reversibility mental model*: What did they believe would happen if they approved an error?
- **End-of-Day-2 Gate**: Check the competing hypotheses. If 30-day logs show most of the delay is multi-tier queue waiting or ERP sync latency rather than active review time, flag immediately that **UI redesign alone will not fix total cycle time**, though surfacing pre-checks can still reduce perceived risk.

#### Day 3: Synthesis & Prototype / Discrepancy-Task Preparation
- **Both Researchers**: Map log bottlenecks against Day 2 verification friction and review the candidate redesign with Design/PM.
- Prepare **2 core benchmark scenarios** for Day 4:
  - *Task 1*: Clean PO-matched invoice (tests baseline verification speed and confidence).
  - *Task 2*: Subtle discrepancy invoice (e.g., unit-price/quantity mismatch or duplicate—tests **error-detection accuracy** so speed gains do not come from blind approval).
- Pilot the tasks internally (1 dry run) to verify prototype error states and timing capture.

#### Day 4: Controlled Prototype Task & Risk Check (Cohort 2, $n=3$ unexposed)
- **Both Researchers**: Run three 35–40 minute moderated sessions (counterbalancing Task 1 / Task 2 order where possible, noting that small-sample balancing does not eliminate learning carryover).
- Record three distinct dimensions (without merging them into a single score):
  1. **Discrepancy catch/miss** (Effectiveness / safety check)
  2. **Active verification steps & completion time** (logging incomplete or failed tasks separately from completed ones)
  3. **Perceived ease (SEQ) and approval confidence/risk rating** (explicitly kept separate from actual error-catch accuracy)
- *(Note: If you must test all 6 specialists on Day 4 instead of splitting 3+3, track Cohort 1 vs. Cohort 2 separately so prior Day 2 exposure does not mask learnability issues.)*

#### Day 5: Triangulation & Decision Handoff
- Combine 30-day production log patterns with the 6 internal sessions into a concise decision memo—explicitly marking findings as **production log baseline + internal proxy evaluation**, not external customer validation.

---

### Preserved Decision Criteria (Scaled to 5-Day Evidence Strength)

Your core decision criteria stay intact, while the **scope of action** scales proportionally to cost, reversibility, and evidence limits:

1. **Proceed with Low-Cost, Reversible UI Improvements**
   - *Criteria*: 30-day logs confirm active review friction or repeated verification steps **AND** Day 4 proxy tasks show zero increase in missed discrepancies **AND** Finance/Compliance confirms required audit cues are present.
   - *Examples*: Surfacing existing automated match status, clarifying post-approval audit trail / recall rules, consolidating existing fields on one screen.
2. **Hold High-Cost or Low-Reversibility Workflow Changes**
   - *Criteria*: Changes that alter approval thresholds, remove confirmation/secondary sign-off gates, or require heavy engineering/ERP rework.
   - *Why*: 6 internal specialists with shared company priors cannot verify how external finance managers comprehend risk or handle edge-case exceptions. Gate these behind external customer validation or a controlled production pilot.
3. **Pause / Rework Triggers (Unchanged)**
   - **Rubber-stamping risk**: Any faster completion in Day 4 is accompanied by missed discrepancies or lower risk awareness.
   - **Wrong bottleneck**: 30-day logs prove >50% of approval delay sits in off-screen routing queues or backend ERP sync rather than active review UX.
   - **Broken instrumentation**: 30-day logs lack reliable timestamps or denominators to separate active review from waiting.
4. **Production Guardrails for Subsequent Rollout (Owned by Product / Engineering / Finance)**
   - Before any live release of approved changes, agree with Engineering and Finance on guardrail tracking: post-approval reversal/dispute rate, discrepancy catch rate, and active review time vs. queue wait time (with specific rollout thresholds and monitoring windows calibrated by Product/Engineering/Finance owners rather than fixed arbitrarily by UX).

---

### Smallest Next Step (Day 1, Hour 1)

1. Pull a quick schema check of the **30-day approval logs** to confirm whether `active review timestamps` and `rejection/reversal reasons` exist.
2. Confirm with Finance/Compliance which verification fields are mandatory on-screen.
3. Book **3 internal specialists for Day 2** and **3 separate internal specialists for Day 4**.

*On-demand expansion available*: I can immediately generate the Day 1 30-day log audit checklist (exact fields and denominator splits) or the Day 2 / Day 4 35-minute session guides.