# pilot_b_beta4.md

## Turn 1

### Current Judgment & Recommendation

**Conditional judgment (based strictly on 4 synthetic pilot excerpts; non-empirical):** Do not broadly enable or expand the current **Auto-Approve** feature, and do not leave the **"Confirm Batch"** action unchanged. While automation shows directional value in narrow, predictable workflows (recurring utility bills on a fixed vendor list), the current design carries two distinct blockers before wider pilot use:

1. **Governance / Compliance Blocker (Escalation Required):** The audit log reportedly failed to record *who* enabled Auto-Approve (`INT-03`), prompting compliance to instruct the team to disable it. Fixing UI usability alone will not unblock adoption until compliance, finance, and engineering owners confirm and implement required actor-attribution logging.
2. **Pre-Execution Visibility & Commitment Friction:** Users could not verify which vendor rules Auto-Approve matched before turning it on (`INT-01`), and a batch action labeled **"Confirm Batch"** committed approvals immediately instead of showing a preview (`INT-04`).

**Recommended direction:** Keep Auto-Approve disabled (or strictly paused) until compliance sign-off on audit-log attribution is obtained, and prioritize low-cost clarity fixes—showing matched vendor rules before Auto-Approve activation and separating batch preview from final approval commitment.

---

### 1. Qualitative Coding Summary

- **Corpus & Coding Unit:** 4 synthetic interview excerpts (`INT-01` to `INT-04`), coded at the **excerpt-per-participant** level ($N = 4$ synthetic participants across 4 distinct roles; $n = 1$ per role).
- **Important Epistemic Label:** All excerpts and embedded figures ("20 minutes", "12 invoices") are **synthetic inputs (`synthetic: true`)**, not empirical field measurements. Counts below summarize the provided corpus only and cannot be generalized to user populations or role prevalence.

| Excerpt ID | Role (Synthetic) | Grounded Excerpt Cue (Stated Fact) | Primary Codes (Inductive / UX Mechanism) | Inferred UX / Governance Mechanism (Conditional) |
|---|---|---|---|---|
| **INT-01** | Senior Buyer | Enabled "Auto-Approve" toggle once, then turned it off because matched vendor rules were not visible. | `RULE_OPACITY`, `FEATURE_ABANDONMENT`, `TRUST_CALIBRATION_GAP` | **Lack of rule/system visibility:** Unable to inspect which vendors/rules the toggle governed, the buyer disabled automation to avoid unverified approvals. |
| **INT-02** | AP Clerk | Reported Auto-Approve saved 20 minutes on recurring utility bills; never checked rules because vendor list is fixed. | `EFFICIENCY_GAIN_REPORTED`, `FIXED_SCOPE_PREDICTABILITY`, `LOW_VERIFICATION_NEED` | **Qualifying condition (bounded predictability):** When task scope is repetitive and the vendor set is known and static, explicit rule inspection was not perceived as necessary. |
| **INT-03** | Controller | Audit log did not show who enabled Auto-Approve; compliance instructed the team to disable it. | `AUDIT_ATTRIBUTION_MISSING`, `COMPLIANCE_BLOCKER`, `FORCED_DISABLEMENT` | **Governance & accountability gap:** Missing actor attribution in system logs violated internal audit expectations, triggering organizational disablement regardless of end-user convenience. |
| **INT-04** | Junior Buyer | Clicked "Confirm Batch" expecting a preview; system actually approved 12 invoices. | `LABEL_MENTAL_MODEL_MISMATCH`, `PREMATURE_COMMITMENT`, `MISSING_PREVIEW_STEP` | **Action-consequence ambiguity:** Button copy ("Confirm Batch") did not communicate irreversible/immediate approval execution, leading to an unintended batch commit (a *mistake* in mental model rather than a motor slip). |

#### Code Frequency Snapshot (Synthetic Corpus Only, $N = 4$)

| Theme / Code Cluster | Excerpts Coded ($n / 4$) | Excerpt IDs | Synthetic Corpus Note |
|---|---|---|---|
| Pre-execution / rule & state opacity | 2 of 4 | `INT-01`, `INT-04` | Different UI triggers (toggle vs. batch button), shared lack of preview/visibility before commitment. |
| Unintended or halted adoption | 3 of 4 | `INT-01`, `INT-03`, `INT-04` | Two halted/disabled (`INT-01`, `INT-03`); one unintended execution (`INT-04`). |
| Governance / auditability blocker | 1 of 4 | `INT-03` | Organizational-level blocker; cannot be resolved by UI copy alone. |
| Fixed-scope efficiency benefit (Qualifying) | 1 of 4 | `INT-02` | Positive outcome under fixed-vendor, recurring-bill conditions. |

---

### 2. Key Themes, UX Mechanisms & Competing Hypotheses

1. **Theme 1 — Pre-Execution Opacity Erodes Control & Trust (`INT-01`, `INT-04`)**
   - **UX Mechanism:** Both excerpts point to a gap between initiating an action and seeing its exact scope/consequence. In `INT-01`, toggling Auto-Approve exposed no preview of matched vendor rules, prompting defensive abandonment. In `INT-04`, clicking **"Confirm Batch"** triggered immediate approval of 12 invoices when the user expected a review/preview step.
   - **Competing Hypotheses:**
     - *H1a (UI Visibility / Copy Defect):* The toggle lacks a rule-match summary, and "Confirm Batch" ambiguously conflates "confirm selection to review" with "execute approval."
     - *H1b (Training / Onboarding or Permission Gap):* Buyers may not have been briefed on rule configuration or batch-approval finality, or Junior Buyers (`INT-04`) may have approval permissions without workflow safeguards (e.g., dual review or dry-run mode).

2. **Theme 2 — Governance & Audit Attribution as a Non-UX Gate (`INT-03`)**
   - **UX / Socio-Technical Mechanism:** Financial approval features operate under organizational accountability controls. Even if end users understand the UI, an audit log that omits actor attribution ("who enabled Auto-Approve") removes traceability and forces compliance intervention.
   - **Competing Hypotheses:**
     - *H2a (Missing Audit Schema / Logging Bug):* The system records toggle state changes without `actor_id` / timestamp metadata.
     - *H2b (Shared Account or Log Access Misalignment):* Actor data may exist in a separate admin log inaccessible to Controllers, or multiple users share a service/role context. *(Requires engineering/compliance log inspection rather than user interviews.)*

3. **Theme 3 — Predictable, Bounded Scope Enables Automation Adoption (`INT-02`)**
   - **UX Mechanism:** When the underlying domain is deterministic and familiar (recurring utility bills with a fixed vendor list), the user already holds an accurate mental model of what Auto-Approve covers and experiences time savings without needing per-run rule verification.

---

### 3. Negative & Qualifying Cases

- **Primary Qualifying Case — `INT-02` (AP Clerk) vs. `INT-01` (Senior Buyer):**
  `INT-02` directly qualifies any blanket conclusion that "Auto-Approve is unusable or untrusted." Under fixed-vendor, recurring-bill conditions, `INT-02` experienced clear perceived efficiency (reported 20 minutes saved) and did not need rule inspection. The contrast with `INT-01` suggests adoption may be **task- and vendor-volatility-dependent**: opaque automation is rejected when buyers must verify variable or high-judgment vendor rules (`INT-01`), whereas fixed-list recurring payables tolerate—and benefit from—low-friction automation (`INT-02`).
- **Organizational Override vs. Individual Friction — `INT-03` vs. `INT-02`:**
  Even though `INT-02` represents a successful individual workflow, `INT-03` acts as a system-wide override: an internal compliance directive to disable Auto-Approve blocks *all* users, including `INT-02`'s beneficial use case, until audit attribution is resolved.
- **Scope Distinction — `INT-04` (Batch Execution) vs. `INT-01`/`INT-02`/`INT-03` (Auto-Approve Toggle):**
  `INT-04` describes an unintended manual batch commitment via **"Confirm Batch"**, rather than the Auto-Approve toggle itself. Treating `INT-04` as "an Auto-Approve bug" would misdiagnose the surface component; however, keeping it linked at the **mechanism level** reveals a shared pattern across the pilot: high-consequence approval actions lack a clear pre-commit preview and unambiguous action labeling.

---

### 4. Methodological & Evidence Limitations

1. **Synthetic Data (`synthetic: true`):** These 4 excerpts are synthetic test inputs, not empirical data from real B2B buyers, clerks, or controllers. Reported figures ("20 minutes", "12 invoices") are fictional prompt elements and must not be cited as measured time savings or error rates.
2. **No Population Prevalence or Quantitative Inference:** With $N = 4$ single-sentence excerpts ($n = 1$ per role), frequencies cannot be converted into percentages (e.g., never "25% of users" or "50% of buyers") or used to rank problem severity by frequency.
3. **Role-Task Confounding:** Because each role appears once, role differences (Senior Buyer vs. AP Clerk vs. Junior Buyer vs. Controller) are completely confounded with task type (variable procurement vs. fixed utility bills vs. batch review vs. audit oversight).
4. **Missing System & Recovery Context:** No UI screenshots, rule-matching logic, button placement, undo/reversal capabilities (whether the 12 approved invoices in `INT-04` could be recalled), or actual audit-log schemas were supplied.
5. **Self-Report vs. Behavioral Observation:** Excerpts reflect brief retrospective statements (`INT-02`'s "saved me 20 minutes" is unverified self-report; `INT-01` and `INT-04` lack screen/log traces confirming exact UI states).
6. **Compliance & Authority Boundary:** `INT-03` reflects an internal compliance instruction. UX analysis cannot determine applicable statutory, SOX, or financial-audit requirements or certify compliance; authoritative review belongs to compliance, finance, and engineering owners. (No external standards or regulations were retrieved in this offline analysis.)

---

### 5. Business Impact & Smallest Next Steps

- **Business Impact:** Leaving Auto-Approve disabled protects auditability (`INT-03`) but forfeits potential recurring-task efficiency (`INT-02`). Conversely, leaving **"Confirm Batch"** ambiguous creates ongoing risk of unintended financial commitments (`INT-04`) even with Auto-Approve turned off.
- **Smallest Next Checks (Low-Cost, Sequenced Before Any Large Study):**
  1. **Zero-Recruitment Artifact & Log Check (Product + Compliance + Engineering):** Inspect (a) what fields the audit log currently captures when Auto-Approve is toggled (`INT-03`), (b) whether a preview/dry-run state or reversal path exists for "Confirm Batch" (`INT-04`), and (c) whether Auto-Approve rules can be displayed inline or restricted to approved fixed vendor lists (`INT-01`, `INT-02`).
  2. **Targeted Comprehension Check (3–5 Representative Users across Buyer & AP Clerk Roles, if pilot resumes):** Present revised prototypes/copy and test two concrete tasks without hinting: *(i)* ask users to name which vendors Auto-Approve will affect before enabling it, and *(ii)* ask what clicking **"Preview Batch"** / **"Approve Batch"** will immediately do.
- **Reversal / Update Conditions:**
  - *Re-enable bounded Auto-Approve pilot* only if compliance confirms required actor-attribution logging is live **and** rule-scope visibility passes comprehension checks (or scope is explicitly restricted to pre-approved fixed vendor lists with visible rule summaries).
  - *Escalate or redesign batch flow* if log inspection shows `INT-04`-style batch approvals are irreversible without finance intervention.

---

### 6. Machine-Checkable Evidence JSON Record (`synthetic: true`)

**Schema & Validator Support in UXDA (`v0.1.0-beta.4`):**
- **Supported & Machine-Checkable:** `assets/evidence-session-schema.md` + `scripts/evidence_session_audit.py` provides an offline structural validator checking `network_mode`, `external_search_performed`, `user_forbids_network`, `sources`, `claims`, and `interaction`. It accepts additional top-level metadata such as `"synthetic": true` (note: the script audits the core session fields and ignores custom metadata keys like `"synthetic"`).
- **Schema Notes for Other UXDA Formats:** `assets/fusion-trace-schema.md` defines `"synthetic": true` natively, **but** its validator (`fusion_trace_check.py`) is explicitly not included in `v0.1.0-beta.4`. Meanwhile, `scripts/render_report.py` validates `validation.evidence_origin: "synthetic"`, and `scripts/spiral_audit.py` validates `data_origin: "synthetic"`.

Below is a valid **Evidence Session JSON record** (verified structurally against `scripts/evidence_session_audit.py` logic with `ok: true, issues: []`) carrying `"synthetic": true`:

```json
{
  "synthetic": true,
  "record_type": "evidence_session",
  "schema_ref": "assets/evidence-session-schema.md",
  "network_mode": "OFFLINE",
  "external_search_performed": false,
  "user_forbids_network": false,
  "sources": [
    {
      "id": "INT-01",
      "kind": "LOCAL_DOCUMENT",
      "locator": "prompt-excerpts#INT-01",
      "version": "synthetic-v1",
      "scope": "synthetic Senior Buyer excerpt; non-empirical"
    },
    {
      "id": "INT-02",
      "kind": "LOCAL_DOCUMENT",
      "locator": "prompt-excerpts#INT-02",
      "version": "synthetic-v1",
      "scope": "synthetic AP Clerk excerpt; non-empirical"
    },
    {
      "id": "INT-03",
      "kind": "LOCAL_DOCUMENT",
      "locator": "prompt-excerpts#INT-03",
      "version": "synthetic-v1",
      "scope": "synthetic Controller excerpt; non-empirical"
    },
    {
      "id": "INT-04",
      "kind": "LOCAL_DOCUMENT",
      "locator": "prompt-excerpts#INT-04",
      "version": "synthetic-v1",
      "scope": "synthetic Junior Buyer excerpt; non-empirical"
    }
  ],
  "claims": [
    {
      "id": "C1",
      "claim_type": "SYNTHETIC_EXCERPT_OBSERVATION",
      "status": "LOCAL_DOCUMENT",
      "source_refs": ["INT-01"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; Senior Buyer (n=1); B2B invoice approval pilot; non-empirical",
      "summary": "Senior Buyer enabled Auto-Approve once and turned it off because matched vendor rules were not visible."
    },
    {
      "id": "C2",
      "claim_type": "QUALIFYING_CASE_OBSERVATION",
      "status": "LOCAL_DOCUMENT",
      "source_refs": ["INT-02"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; AP Clerk (n=1); recurring utility bills with fixed vendor list; non-empirical",
      "summary": "AP Clerk reported saving 20 minutes on recurring utility bills without checking rules because the vendor list is fixed."
    },
    {
      "id": "C3",
      "claim_type": "GOVERNANCE_OBSERVATION",
      "status": "LOCAL_DOCUMENT",
      "source_refs": ["INT-03"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; Controller (n=1); audit log / compliance boundary; non-empirical",
      "summary": "Controller reported audit log did not show who enabled Auto-Approve, leading compliance to instruct team to disable it."
    },
    {
      "id": "C4",
      "claim_type": "SYNTHETIC_EXCERPT_OBSERVATION",
      "status": "LOCAL_DOCUMENT",
      "source_refs": ["INT-04"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; Junior Buyer (n=1); batch confirmation action; non-empirical",
      "summary": "Junior Buyer clicked Confirm Batch expecting a preview; system instead approved 12 invoices."
    },
    {
      "id": "C5",
      "claim_type": "UX_MECHANISM",
      "status": "METHODOLOGICAL_INFERENCE",
      "source_refs": ["INT-01", "INT-04"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; candidate mechanism across rule-matching opacity and batch-commit label ambiguity; requires empirical verification",
      "summary": "Invisible rule matching (INT-01) and preview-vs-commit label mismatch (INT-04) point to low action predictability and pre-execution state visibility."
    },
    {
      "id": "C6",
      "claim_type": "QUALIFYING_BOUNDARY",
      "status": "HYPOTHESIS",
      "source_refs": ["INT-01", "INT-02"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; confounded by single-participant-per-role design; requires task-stratified check",
      "summary": "Auto-Approve acceptance may depend on whether vendor scope is fixed and recurring (INT-02) versus dynamic or opaque (INT-01)."
    },
    {
      "id": "C7",
      "claim_type": "COMPLIANCE_ESCALATION",
      "status": "METHODOLOGICAL_INFERENCE",
      "source_refs": ["INT-03"],
      "decision_strength": "PROVISIONAL",
      "applicability": "synthetic: true; internal governance blocker; applicable financial/audit rules unverified",
      "summary": "Lack of actor attribution in audit logs blocks feature enablement at the governance layer and requires compliance/engineering owner resolution."
    }
  ],
  "interaction": {
    "intent": "PRACTICE_OR_EXAMPLE",
    "project_event": "NONE",
    "explicit_user_authorization": false
  }
}
```

*Can expand upon request: a focused 3–5 participant comprehension test protocol for Auto-Approve rule preview and batch confirmation, or a report-data JSON payload compatible with `scripts/render_report.py`.*