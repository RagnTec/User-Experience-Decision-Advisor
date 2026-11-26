# pilot_a_integrated.md

## Turn 1

With **4 weeks and 2 researchers**, you can execute a focused **two-phase mixed-method plan**: **Weeks 1–2** for existing evidence triage and event-anchored qualitative discovery to pinpoint *why* approvals feel slow and risky, followed by **Weeks 3–4** for targeted quantitative validation (either a **comparative task-based prototype benchmark** if a redesign prototype is ready, or a **production log audit + structured approver survey** if the redesign is still being scoped).

**Key feasibility boundary:** In B2B finance, 4 weeks end-to-end cannot support both open-ended discovery and a statistically powered production A/B test on actual financial error or fraud rates. Within 4 weeks, you can establish **causal task-level friction mechanisms, step-level bottlenecks, and controlled prototype time/error differences** (or structured self-reported prevalence), while real-world cycle-time lift and payout error rates must be verified after launch.

**Smallest next step (Days 1–2):** Confirm four prerequisites before launching recruitment or data pulls (`to confirm`):
1. **Open product choices:** Which redesign levers are still undecided (e.g., batch approvals, risk-tier routing, inline PO/receipt matching, audit-trail cues) vs. fixed by policy/ERP constraints?
2. **Existing data access:** Do approval audit logs or telemetry already link `invoice_id`, `approver_id`, submission time, and approval/rejection timestamps?
3. **Prototype readiness:** Will an interactive redesign prototype with realistic invoice states be ready by the end of Week 2?
4. **B2B recruitment & compliance:** How long does customer/finance-manager scheduling take, and are NDAs or synthetic test invoices required?

---

### 1. Decision Frame & Competing Hypotheses

**Supplied context:** Finance managers complain that B2B invoice approvals *"take too long and feel risky."* You have 4 weeks and 2 researchers to inform a flow redesign.

**Core design tension:** Faster approval flows (e.g., fewer clicks, batch approval, auto-defaults) can inadvertently increase actual or perceived financial liability; adding verification steps can reduce anxiety while worsening cycle time. Before redesigning UI screens, research must separate UI friction from upstream data/policy bottlenecks.

These explanations are **not mutually exclusive** and should be tested together:

| Candidate Explanation | Mechanism | Observable Prediction | Observation That Weakens It | Lowest-Cost Check |
|---|---|---|---|---|
| **Cross-system information hunting** | Approvers leave the flow to verify POs, contracts, or tax details in ERP/email. | High tab/window switching, long dwell time before clicking approve, copy-paste workarounds. | All required match data is visible on-screen, yet approvers still hesitate or delay. | Audit logs + live invoice walkthroughs |
| **Routine vs. exception mixing** | Low-risk recurring invoices follow the same heavy path as high-value or mismatched ones. | Bulk of approval time spent reviewing routine, error-free invoices. | Delays concentrate almost entirely on flagged exceptions/discrepancies. | Approval log stratification + interviews |
| **Missing provenance & accountability cues** | UI hides *what* changed, *who* validated line items, or *why* an invoice was flagged. | Approvers re-check already-verified fields because they distrust or cannot trace system checks. | Approvers understand all checks clearly but still delay due to external sign-offs. | Event-anchored interviews |
| **Irreversibility & escalation fear** | Unclear undo window, post-approval recall rules, or personal liability on final click. | Hesitation at final confirmation; managers message submitters off-platform before clicking. | Approvers click immediately once data matches, with no confirmation hesitation. | Walkthroughs + usability tasks |
| **Non-UI / upstream & policy delays** | Delays stem from missing submitter attachments, multi-tier approver queues, or ERP sync lag. | Long idle time *between* assignment and opening the invoice, rather than *during* active review. | Active in-screen review duration drives most total approval cycle time. | Existing timestamp logs (`to confirm`) |

---

### 2. Four-Week, Two-Researcher Execution Plan

#### Week 1: Alignment, Existing Evidence Audit & Recruitment Launch
* **Day 1–2 — Scope, Ethics & Existing Data Triage (Researcher A + B):**
  * Confirm open redesign decisions, stakeholder decision owner, and data-access authorization.
  * **Existing evidence check first:** Audit historical approval timestamps (time-in-queue vs. active review time, if logged), rejection/return reasons, and support tickets. Check denominators, missing IDs, and whether pre-submission abandonments or off-platform approvals are unlogged.
  * Prepare **synthetic/redacted invoice stimuli** (never use live vendor bank details or confidential pricing in recorded sessions).
* **Day 2–5 — Recruitment & Protocol Prep (Researcher A: Quant/Ops lead; Researcher B: Qual lead):**
  * Launch B2B recruitment immediately (target **10–12 finance managers** for Week 2 interviews to buffer against no-shows and yield **8–10 completed sessions**, segmented across routine high-volume approvers vs. exception/multi-tier approvers). Screen on actual recent invoice volume and ERP/role exposure—never on desired opinions—and pilot the screener.
  * Pilot the interview guide with 1–2 internal finance/ops proxies (treat strictly as instrument rehearsal, not target-user evidence).

#### Week 2: Qualitative Discovery & Quantitative Instrument Setup
* **Day 6–9 — Event-Anchored Contextual Interviews (Researcher A + B, 4–5 sessions each):**
  * 45–60 min sessions anchored on **two concrete recent invoices** per participant: (1) a routine approval that felt slow, and (2) an invoice that felt risky or was held/rejected.
  * Reconstruct exact action sequence, cross-referenced artifacts (PO, email, ERP), hesitation points, and workarounds *before* asking for subjective explanations (treat user self-diagnosis as a hypothesis, not proven root cause).
* **Day 7–10 — Disciplined Qualitative Synthesis (Researcher A + B):**
  * Fix coding unit as the **invoice-approval episode** (so repeated quotes from one manager are not counted as independent confirmation).
  * Build a **versioned codebook** with inclusion/exclusion rules; both researchers **independently double-code a planned 25–30% subset**, adjudicate disagreements while preserving original codes, and explicitly retain **negative/disconfirming cases**.
  * *Boundary:* Qualitative counts identify mechanisms and failure modes; never report "6 of 9 managers cited X" as population prevalence.
* **Day 9–10 — Lock & Pilot Quantitative Validation Track:**
  * **Select Track A or Track B** based on Week 2 prototype readiness and recruitment capacity:
    * **Track A (if interactive prototype is ready):** Finalize task cards (realistic goals without leaking UI button labels), equivalent invoice datasets (routine vs. hidden-anomaly), success/error anchors, and pilot with 2 participants.
    * **Track B (if prototype is not ready / scoping stage):** Finalize a **5–7 item structured approver survey** (anchoring recent 7-day recall, separating frequency of specific delay sources from perceived risk triggers, closed skip-logic, explicit "not applicable / don't know" options) + production log query plan.

#### Week 3: Quantitative Validation Fieldwork
* **Option A — Comparative Task-Based Benchmark (Researcher A + B):**
  * **Sample & design:** Target **$n = 16\text{–}24$ finance managers** (between-subjects if customer pool permits; if B2B access is tight, **within-subjects $n = 12\text{–}16$** comparing Current vs. Redesign using matched-difficulty invoice sets and counterbalanced order). Note explicitly that counterbalancing reduces but does not guarantee elimination of learning/carryover effects, and non-probability B2B convenience samples do not automatically generalize to all customer tiers.
  * **Tasks:** Give realistic approval goals containing a mix of clean invoices and planted anomalies (e.g., PO quantity mismatch, duplicate line item, missing tax ID) to test the **speed–risk trade-off** directly—not just click speed.
  * **Pre-specified metrics:** Task completion rate, **anomaly detection / false-approval rate**, active review duration (**median and IQR**, keeping incomplete/failed tasks separate from successful-task times), unassisted recovery from errors, and single-item post-task perceived confidence/risk (kept distinct from observed behavior).
* **Option B — Production Log Funnel + Structured Approver Survey (if no prototype):**
  * **Production logs:** Stratify cycle time into *assignment-to-first-open* vs. *first-open-to-decision* (`[Proposed event]` schema required if not yet instrumented).
  * **Survey:** Field to **$\ge 60\text{–}100$ active approvers** (if accessible via in-app intercept or customer panel) to estimate frequency of specific delay and risk triggers across company sizes/approval tiers. Monitor nonresponse and self-selection bias; report branch denominators for every item.
* *Note on statistical power:* Do not claim a sample is "powered" or "underpowered" without specifying baseline variance and minimum practically important effect size from Week 1 logs. For small comparative samples ($n = 12\text{–}24$), prioritize **effect estimates, uncertainty intervals, and transparent descriptive counts** over binary p-value claims.

#### Week 4: Reproducible Analysis, Triangulation & Decision Readout
* **Day 16–18 — Data Cleaning & Analysis (Researcher A leads Quant; Researcher B leads Integration):**
  * Preserve raw data; document exclusions, timeouts, retries, and missingness.
  * Report **complete-pair results separately from all-started tasks**; run sensitivity checks showing results with and without flagged outliers (never silently drop difficult/slow cases).
  * Never claim $p > 0.05$ proves old and new flows are "equally safe" or "equally fast." Distinguish relative % change from percentage-point or absolute-minute differences.
* **Day 18–20 — Triangulation & Decision Brief:**
  * Integrate qualitative mechanisms with quantitative metrics as **complementary evidence** (mechanisms explain *why* quantitative bottlenecks or errors occur; if both draw from the same customer cohort, label shared sampling bias explicitly rather than calling it independent replication).
  * Deliver concise Decision Brief with design recommendations, strongest countercase, and post-launch instrumentation requirements.

---

### 3. Measurement & Privacy Guardrails

* **Unit of analysis discipline:** Never mix *invoices*, *approval sessions*, and *approvers* in the same denominator. When one manager evaluates multiple invoices, analyze using participant-level aggregates or paired/clustered methods.
* **Telemetry definition (`[Proposed event]` if unverified):** Any proposed production tracking (e.g., `invoice_review_opened`, `po_detail_expanded`, `invoice_approved_submitted`) must define numerator, denominator, time window, linking keys (`invoice_id`, `approval_attempt_id`), deduplication by unique event/request ID (not naive fixed-second intervals), and unlinked/abandoned records.
* **Privacy & worksite ethics:** Obtain explicit customer/employer authorization before pulling audit logs or recruiting client finance staff. Ensure sessions are **voluntary and unobserved by managers/supervisors** so participants do not hide informal workarounds or risk anxieties. Mask or replace real financial/PII data before recording.

---

### 4. Contingency Downgrades & Decision Link

**If constraints slip:**
* **Slow B2B recruitment** → Run 5–6 external manager interviews + internal finance/ops structural walkthrough; narrow conclusions to *structural friction discovery* (no population prevalence or superiority claims).
* **Prototype delayed past Week 2** → Switch Week 3 to **Track B (log analysis + survey)** or static-prototype cognitive walkthrough; do not claim validated speed or error reduction.
* **Missing invoice-level logs** → Rely on Week 3 comparative usability/survey and deliver a `[Proposed event]` logging plan as a prerequisite before full rollout.

**How evidence maps to the redesign decision:**

| Evidence Pattern | Decision Consequence | Stop / Reversal Condition |
|---|---|---|
| Logs/interviews show most delay is **idle queue time or missing upstream data**, not UI review | **Pause UI-only speedup.** Prioritize pre-submission validation, routing SLAs, or ERP sync fixes first. | Reverses if Week 3 logs/observations show active in-screen review drives the majority of delay. |
| Risk anxiety traces to **hidden PO/variance provenance** and unclear undo/audit trail | **Prioritize inline verification cues & clear reversibility** before adding batch/auto-approve shortcuts. | Reverses if approvers miss planted anomalies *because* of visual clutter rather than missing data. |
| Redesign speeds up routine tasks **without increasing false-approval rate** on planted anomalies | **Proceed to staged rollout** with post-launch guardrail monitoring on error/return rates. | **Stop / revise** if anomaly miss rate rises or uncertainty intervals cannot rule out unacceptable financial error risk. |
| Survey/interviews show routine vs. exception workflows need **fundamentally different flows** | **Split approval paths by risk tier** rather than forcing one UI for all invoices. | Reverses if exception volume or rules vary too unpredictably across B2B tenants to classify reliably. |

*Optional detail: interview guide / 5–7 item survey draft / usability task protocol & metrics / qualitative coding worksheet.*

---

## Turn 2

With **5 working days**, **no external customer recruitment**, **6 internal finance ops specialists**, and the **last 30 days of approval logs**, you should shift from a discovery-plus-external-validation plan to a **5-day Bottleneck Audit & Structural Risk Triage** led by your 2 researchers.

**What stays valid vs. what changes:**
* **Unchanged:** The core decision trade-off (speeding up approvals vs. raising financial/compliance error risk), the five competing hypotheses (cross-system hunting, routine/exception mixing, missing provenance, irreversibility fear, and upstream/ERP latency), and your **decision criteria and reversal conditions**.
* **Downgraded / narrowed:** You can no longer measure external B2B finance managers' subjective risk perception, customer-segment prevalence, or redesigned prototype performance with target buyers. The **30-day logs** remain real production evidence (subject to data-quality checks), while the **6 internal finance ops specialists** are an **internal proxy perspective**—useful for exposing structural friction, missing data cues, and workarounds, but carrying shared organizational knowledge bias.
* **Decision implication:** Use this 5-day sprint to fix **low-cost, reversible structural blockers** (e.g., surfacing missing PO/variance context inline) and isolate **non-UI queue delays**. **Hold or gate high-risk, hard-to-reverse changes** (e.g., removing verification steps, auto-approving, or batch-approving high-value invoices) until external customer validation or closely monitored staged-rollout verification is possible.

**Smallest next step (Day 1 morning):** Obtain log-access authorization, pull a 30-day schema sample to verify whether timestamps distinguish *assignment-to-open* from *open-to-decision* (`to confirm`), and schedule the 6 internal specialists without their direct managers observing.

---

### 1. Revised 5-Day, 2-Researcher Schedule

| Day | Researcher A (30-Day Logs Lead) | Researcher B (Internal Ops Sessions Lead) | Output / Gate |
|---|---|---|---|
| **Day 1** | **Log audit & denominator check:** Verify authorization, inspect `invoice_id` / `approval_attempt_id` / `approver_id` linking, check missing/orphan events, retries, and whether active review time is separable from idle queue time. | **Stimulus & guide prep:** Prepare 3–4 realistic redacted/synthetic invoice cases (clean routine, PO mismatch, duplicate/tax anomaly) and an event-anchored walkthrough guide. | Clean log schema verified; 6 sessions scheduled (voluntary, 1:1). |
| **Day 2** | **Quant bottleneck stratification:** Compute approval duration (**medians & IQR**), rejection/return rates, and escalation counts across routine vs. exception invoices, value tiers, and approval stages. | **Sessions 1–3 (45–60 min each):** Reconstruct each specialist's recent slow/risky approvals first, then walk through the current flow on the synthetic test cases (capture hesitations, off-platform checks, and workarounds). | First-pass log cut; initial friction & workaround notes. |
| **Day 3** | **Outlier & sensitivity checks:** Inspect long-tail delays, incomplete/abandoned attempts, and multi-tier handoffs; test whether delays cluster by specific tenants, ERPs, or exception types. | **Sessions 4–6 (45–60 min each):** Complete remaining internal sessions (split 1–2 with Researcher A if needed to keep pace); capture disconfirming cases where routine approvals are already fast or risk feels low. | All 6 internal sessions complete; log anomaly checks done. |
| **Day 4** | **Reproducible quant summary + double-coding:** Lock descriptive log tables (with raw counts, denominators, and missingness). Both researchers **independently double-code 2 of the 6 sessions** using a compact codebook (unit: *invoice-approval episode*), adjudicating disagreements without erasing original codes. | **Mechanism mapping:** Link internal task blockers and risk-cue gaps to the specific steps/segments showing high delay or rejection in the 30-day logs; retain negative cases. | Coded episode table + verified log tables. |
| **Day 5** | **Joint Decision Readout:** Deliver Decision Brief separating (1) observed production log patterns, (2) internal proxy mechanisms, (3) reversible quick wins vs. high-risk changes requiring external follow-up, and (4) `[Proposed event]` logging gaps if timestamps are incomplete. | | Stakeholder decision review & follow-up plan. |

---

### 2. Preserved Decision Criteria (Adapted to 5-Day Evidence Boundaries)

Your decision criteria remain intact; only **evidence authority** is calibrated to what 30-day logs + 6 internal specialists can support:

| Evidence Pattern (30-Day Logs + 6 Internal Ops) | Decision Consequence | Immediate Action vs. External Gate | Stop / Reversal Condition |
|---|---|---|---|
| **Logs show most cycle time is idle queue / upstream wait** (e.g., assignment-to-open, missing submitter docs, ERP sync lag) rather than active review | **Do not invest in UI-only speedup** as the primary fix. | Redirect engineering/ops to pre-submission validation, routing SLAs, or ERP sync fixes. | **Reverses** if log breakdown (once active review timestamps are confirmed) or follow-up observation shows active in-screen checking dominates delay. |
| **Logs show long active review / high back-and-forth AND internal ops pinpoint missing PO/variance provenance or unclear undo/audit trail** | **Prioritize inline verification cues & explicit reversibility** before introducing shortcuts. | **Proceed minimally** on low-cost, reversible UI clarity fixes (e.g., surfacing existing match data/audit status inline). | **Reverses** if internal walkthroughs show match data is already visible and hesitation comes from visual overload rather than missing context. |
| **Logs show routine clean invoices consume bulk of total review volume/time** and internal ops use repetitive checks solely due to unseparated paths | **Split routine vs. exception routing criteria** in the redesign scope. | Design the split concept now, but **gate one-click/batch approval or auto-routing** behind external customer validation or controlled staged rollout with error guardrails. | **Stop / revise** if historical rejection/return logs show subtle errors slipping through ostensibly "routine" low-value invoices. |
| **30-day logs lack linking IDs or active-review timestamps** (`to confirm`) | **Cannot quantify where time is lost inside the UI.** | Restrict conclusions to internal structural defect discovery + rejection counts; ship `[Proposed event]` instrumentation as a prerequisite before evaluating redesign impact. | **Reverses** once clean session/attempt timestamps are verified in production logs. |

---

### 3. Explicit Evidence & Ethics Boundaries for This 5-Day Sprint

* **Do not treat internal ops as external customers:** Never state *"67% of finance managers feel X"* or *"the redesign is validated"* from 6 internal specialists. Report them strictly as **internal structural mechanisms and proxy observations** that identify candidate UI/data gaps and inform what must later be tested with external buyers.
* **Do not conflate log duration with user effort:** Unless logs separate screen-open from idle assignment time, a 48-hour approval duration can reflect calendar/queue delay, not 48 hours of UI friction. Report **medians, IQR, denominators, and missingness** explicitly, and never drop failed/cancelled approvals from duration reporting.
* **Worksite & data privacy:** Ensure the 6 internal specialists participate voluntarily without manager presence (so compliance workarounds are surfaced honestly), and verify authorization before querying 30-day production invoice logs.

*Optional detail: 30-day log audit checklist / 6-session internal walkthrough guide / episode coding sheet.*