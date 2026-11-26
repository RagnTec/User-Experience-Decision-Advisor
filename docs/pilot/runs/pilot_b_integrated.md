# pilot_b_integrated.md

## Turn 1

# Synthetic Pilot Analysis: B2B Invoice Approval (`synthetic: true`, N = 4)

> **Synthetic Data & Authority Notice:** All four excerpts analyzed below are **synthetic** (`n = 4`, 1 excerpt per role). They illustrate qualitative coding structure, competing hypotheses, and decision boundaries; they **cannot** support population prevalence estimates, net time-savings claims, compliance sign-off, or production rollout authorization.

---

## Executive Decision Summary

**Current judgment (Decision Status: Open — Hold Broad Rollout):** These 4 synthetic excerpts do not support scaling either **Auto-Approve** or the current **Confirm Batch** flow. While one role (`INT-02`, AP Clerk) reports saving 20 minutes on fixed-vendor recurring utility bills, three distinct operational and governance blockers appear in the other three roles: rule-matching opacity causing immediate abandonment (`INT-01`), missing actor attribution in audit logs triggering compliance disablement (`INT-03`), and an ambiguous `"Confirm Batch"` label causing unintended approval of 12 invoices (`INT-04`).

- **Strongest qualifying countercase:** Blanket rejection of Auto-Approve ignores `INT-02`, where a bounded, fixed vendor list (recurring utility bills) reportedly delivered time savings without requiring per-invoice rule inspection—suggesting that **scope predictability** may moderate whether users demand inline rule visibility.
- **Smallest next step:** Before any further pilot expansion, (1) inspect the audit log schema with Finance/Compliance to verify actor attribution for toggle changes, (2) inspect the `"Confirm Batch"` UI flow and separate preview from commit (plus verify whether an undo/rollback path exists), and (3) pair any fixed-vendor allowlist test with real telemetry and task-based usability checks.
- **Reversal condition:** Verified actor-level audit logging accepted by Compliance, plus task-based usability and pilot telemetry on real users demonstrating accurate rule-match comprehension (for variable vendors) and zero unintended batch approvals.

---

## 1. Qualitative Coding Summary

### 1.1 Study Frame
- **Study ID / Decision ID:** `STUDY-B2B-INVOICE-PILOT-SYN-01` / `DEC-B2B-AUTOAPPROVE-PILOT-01`
- **Research question:** What rule-visibility, auditability, and batch-commit usability risks or scope qualifiers emerge from the four synthetic pilot role excerpts?
- **Source type & authorization:** Prompt-supplied synthetic interview excerpts (`evidence_status: supplied`, `access_class: internal`, `authorized_for_use: true` for this analysis).
- **Coding unit:** Single participant interview excerpt (1 excerpt per role; `N = 4` independent synthetic roles).
- **Independent-source rule:** Each excerpt (`INT-01`–`INT-04`) counts as at most 1 independent source; repeated references within an explanation never count as additional confirmation.
- **Codebook version & review status:** `codebook-v1.0` — **single-reviewer AI initial coding** (no second independent coder or human adjudication performed yet; double-coding on real field transcripts is required before finalizing claims).

### 1.2 Codebook (`codebook-v1.0`)

| Code | Definition | Include | Exclude / Near Neighbor | Example Locator |
|---|---|---|---|---|
| `RULE-OPACITY` | User cannot inspect or verify which vendor/invoice rules an automated approval setting applies or matched. | Turning off, hesitating, or distrusting automation because matched vendor rules are unseen. | `AUDIT-GAP` (post-hoc actor logging of setting changes); `FIXED-SCOPE-TRUST` (trust derived from a static vendor list). | `INT-01` |
| `FIXED-SCOPE-TRUST` | Self-reported time savings and bypassed rule checking when automation operates on a narrow, recurring, fixed vendor list. | Reported efficiency gain or low verification need explicitly attributed to a fixed/predictable vendor scope. | `RULE-OPACITY` (dynamic/uncertain rule sets where opacity causes abandonment). | `INT-02` |
| `AUDIT-GAP` | Missing actor attribution or traceability in audit logs for automation configuration/enablement, triggering compliance intervention. | Absent "who enabled" records or compliance-directed feature disablement due to non-traceability. | `RULE-OPACITY` (in-task visibility of vendor rules); `COMMIT-AMBIGUITY` (batch UI action mismatch). | `INT-03` |
| `COMMIT-AMBIGUITY` | User mistakes a state-changing batch commit control for a read-only preview step, causing unintended approvals. | Unintended multi-invoice approval driven by ambiguous button wording (`"Confirm Batch"`) or missing preview step. | `RULE-OPACITY` (uncertainty over Auto-Approve toggle rules rather than explicit batch execution). | `INT-04` |

### 1.3 Coded Evidence (Raw Observation vs. Interpretation)

| Evidence ID | Source / Role | Raw Observation | Code | Interpretation | Alternative Explanation | Resolution |
|---|---|---|---|---|---|---|
| `EV-INT-01` | `INT-01` (Senior Buyer) | Turned `'Auto-Approve'` on once, then turned it off because they could not see which vendor rules it matched. | `RULE-OPACITY` | Inability to verify matched vendor rules undermined trust/control and led directly to self-initiated abandonment. | Rule-matching details may exist in a separate settings view that `INT-01` missed, or `INT-01` handles non-standard vendors requiring manual verification. | Single-reviewer code (`v1.0`); needs UI inspection & double-coding. |
| `EV-INT-02` | `INT-02` (AP Clerk) | Reported `'Auto-Approve'` saved 20 minutes on recurring utility bills and stated they never had to check rules because the vendor list is fixed. | `FIXED-SCOPE-TRUST` | Static, recurring vendor scope eliminated perceived rule-checking overhead and produced self-reported time savings. | 20-minute estimate is unverified recall; skipping rule checks could hide silent misrouting if the vendor list or invoice amounts drift. | Single-reviewer code (`v1.0`); retained as qualifying case (`CLM-02`). |
| `EV-INT-03` | `INT-03` (Controller) | Reported the audit log did not show who enabled `Auto-Approve`, so compliance instructed the team to disable it. | `AUDIT-GAP` | Lack of actor-level audit attribution created a hard governance/compliance blocker independent of end-user convenience. | Attribution may exist in an admin-only log outside the Controller's view, or compliance policy disallows role-level self-enablement altogether. | Single-reviewer code (`v1.0`); verify against log schema & policy. |
| `EV-INT-04` | `INT-04` (Junior Buyer) | Clicked `'Confirm Batch'` expecting only a preview; the action actually approved 12 invoices. | `COMMIT-AMBIGUITY` | Label-to-outcome mismatch (expecting preview vs. executing irreversible/batch commit) caused unintended batch approval of 12 invoices. | Junior Buyer onboarding gap or missing secondary confirmation/undo guard in the batch review flow. | Single-reviewer code (`v1.0`); separate mechanism from toggle; inspect UI flow. |

---

## 2. Themes & Claim Synthesis

*(Counts indicate how many of the `N = 4` synthetic excerpts speak to each claim—never population prevalence.)*

| Claim ID | Theme & Claim Statement | Supporting Sources | Qualifying / Contradicting Sources | Evidence Status | Decision Implication |
|---|---|---|---|---|---|
| `CLM-01` | **Theme 1 — Conditional Trust & Rule Visibility:** In non-fixed or high-scrutiny buyer workflows, inability to inspect which vendor rules `Auto-Approve` matches can drive immediate abandonment after first use. | `1/4` (`EV-INT-01`, Senior Buyer) | Qualified by `1/4` (`EV-INT-02`, AP Clerk; `CLM-02`) | `contested` (`supplied`) | Do not treat `Auto-Approve` as self-explanatory; expose matched vendor rules inline before/during activation for buyer workflows. |
| `CLM-02` | **Theme 1 Qualifier — Scope Predictability:** In narrow, recurring workflows with a fixed vendor list (recurring utility bills), `Auto-Approve` can yield self-reported time savings without rule inspection, qualifying a blanket rule-opacity claim. | `1/4` (`EV-INT-02`, AP Clerk) | Creates governance tension with `EV-INT-03` (`CLM-03`) if unmonitored | `supported` as a scope qualifier (`supplied`) | Evaluate restricting initial `Auto-Approve` pilots to audited, fixed-vendor allowlists rather than open-ended vendor catalogs. |
| `CLM-03` | **Theme 2 — Governance & Auditability Blocker:** Missing actor attribution in the audit log for enabling `Auto-Approve` creates an organizational compliance blocker capable of forcing team-wide disablement. | `1/4` (`EV-INT-03`, Controller) | `0/4` | `supported` (`supplied`) | Treat actor-level audit logging (who enabled/changed rules, timestamp, scope) as a hard prerequisite before re-enabling `Auto-Approve`. |
| `CLM-04` | **Theme 3 — Batch Commit Affordance Hazard:** Ambiguous action labeling (`'Confirm Batch'` interpreted as a preview) can cause unintended immediate approval of multiple invoices, posing a distinct safety defect outside the `Auto-Approve` toggle. | `1/4` (`EV-INT-04`, Junior Buyer) | `0/4` | `supported` (`supplied`) | Audit and decouple `"Preview"` vs. `"Approve/Commit Batch"` actions immediately; check whether an approval reversal/undo workflow exists. |

---

## 3. Negative & Qualifying Cases

1. **Qualifying Case on Rule Opacity (`INT-02` vs. `INT-01`):** `INT-02` directly qualifies a universal claim that *"users cannot or will not use Auto-Approve without seeing matched rules."* When the vendor set is fixed and recurring (utility bills), the AP Clerk bypassed rule inspection entirely and reported a 20-minute time gain. However, this qualifier also exposes a **secondary risk**: `"I never had to check rules"` combined with `INT-03`'s audit gap creates silent financial exposure if a vendor list ever changes or an anomalous bill enters the queue.
2. **Scope-Boundary Case (`INT-04` vs. `INT-01`–`INT-03`):** `INT-04` does **not** describe the `Auto-Approve` toggle at all; it describes an explicit batch-review button (`'Confirm Batch'`). Treating all four excerpts as a single `"Auto-Approve failure"` would misdiagnose the defect and leave the batch-commit affordance unfixed even if `Auto-Approve` remained disabled.

---

## 4. Limitations

- **Synthetic data (`n = 4`):** Constructed excerpts (1 per role) cannot establish real-world prevalence, role-wide consensus, or net ROI.
- **Unverified self-reports:** `INT-02`'s `"saved me 20 minutes"` has no baseline duration, task denominator, or invoice error rate; `INT-03`'s log gap and `INT-04`'s batch-commit behavior have not been verified against actual system logs or UI screens.
- **Single-reviewer coding (`codebook-v1.0`):** No independent second coder or disagreement adjudication was performed.
- **No saturation:** With 1 short excerpt per role across 4 distinct roles, thematic saturation is not reached; each theme rests on `n = 1` excerpt.
- **Missing contextual variables:** Invoice dollar thresholds, segregation-of-duties rules, rollback/cancellation mechanics for the 12 approved invoices in `INT-04`, and role permissions are unknown.

---

## 5. Machine-Checkable `uxda-evidence-v1` JSON Record

*(Validated against `assets/uxda-evidence-v1.schema.json` using `scripts/validate_evidence.py`: structure and within-study references pass; validation does not verify external truth or grant decision approval.)*

```json
{
  "schema_version": "uxda-evidence-v1",
  "synthetic": true,
  "studies": [
    {
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "decision_id": "DEC-B2B-AUTOAPPROVE-PILOT-01",
      "title": "B2B Invoice Approval Pilot - Synthetic Qualitative Excerpt Analysis",
      "question": "What rule-visibility, auditability, and batch-commit usability risks or scope qualifiers emerge from four synthetic pilot role excerpts?",
      "method": "interview",
      "sample_frame": "4 synthetic role-based interview excerpts (Senior Buyer, AP Clerk, Controller, Junior Buyer) from a B2B invoice approval pilot",
      "analysis_unit": "Single participant interview excerpt (1 excerpt per role/participant)",
      "status": "completed",
      "limitations": [
        "Synthetic data (n=4, 1 excerpt per role); cannot support population prevalence, effect sizes, or production launch claims.",
        "Single-reviewer AI coding (codebook v1.0); not double-coded or adjudicated by human researchers.",
        "Self-reported excerpts only; unverified against system telemetry, UI screens, audit logs, or compliance policy.",
        "Saturation not reached; missing baseline time-on-task, invoice error rates, role denominators, and undo/rollback behavior."
      ]
    }
  ],
  "evidence": [
    {
      "evidence_id": "EV-INT-01",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "source_type": "interview",
      "source_locator": "Prompt synthetic excerpt INT-01 (Senior Buyer)",
      "evidence_status": "supplied",
      "access_class": "internal",
      "authorized_for_use": true,
      "participant_pseudonym": "INT-01",
      "version": "codebook-v1.0",
      "note": "Role: Senior Buyer. Verbatim excerpt: \"I saw the new 'Auto-Approve' toggle, turned it on once, then turned it off because I couldn't see which vendor rules it matched.\" Code: RULE-OPACITY."
    },
    {
      "evidence_id": "EV-INT-02",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "source_type": "interview",
      "source_locator": "Prompt synthetic excerpt INT-02 (AP Clerk)",
      "evidence_status": "supplied",
      "access_class": "internal",
      "authorized_for_use": true,
      "participant_pseudonym": "INT-02",
      "version": "codebook-v1.0",
      "note": "Role: AP Clerk. Verbatim excerpt: \"Auto-Approve saved me 20 minutes on recurring utility bills; I never had to check rules because the vendor list is fixed.\" Code: FIXED-SCOPE-TRUST."
    },
    {
      "evidence_id": "EV-INT-03",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "source_type": "interview",
      "source_locator": "Prompt synthetic excerpt INT-03 (Controller)",
      "evidence_status": "supplied",
      "access_class": "internal",
      "authorized_for_use": true,
      "participant_pseudonym": "INT-03",
      "version": "codebook-v1.0",
      "note": "Role: Controller. Verbatim excerpt: \"Our audit log didn't show who enabled Auto-Approve, so compliance told our team to disable it.\" Code: AUDIT-GAP."
    },
    {
      "evidence_id": "EV-INT-04",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "source_type": "interview",
      "source_locator": "Prompt synthetic excerpt INT-04 (Junior Buyer)",
      "evidence_status": "supplied",
      "access_class": "internal",
      "authorized_for_use": true,
      "participant_pseudonym": "INT-04",
      "version": "codebook-v1.0",
      "note": "Role: Junior Buyer. Verbatim excerpt: \"I clicked 'Confirm Batch' thinking it only previewed; it actually approved 12 invoices.\" Code: COMMIT-AMBIGUITY."
    }
  ],
  "claims": [
    {
      "claim_id": "CLM-01",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "statement": "In non-fixed or high-scrutiny buyer workflows, inability to inspect which vendor rules Auto-Approve matches can lead users to disable the feature after initial trial.",
      "support_type": "supports",
      "evidence_refs": ["EV-INT-01"],
      "conflict_refs": ["CLM-02"],
      "status": "contested",
      "boundary": "Synthetic n=1 (Senior Buyer); rule-visibility UI and underlying rule accuracy were not independently inspected."
    },
    {
      "claim_id": "CLM-02",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "statement": "In narrow, recurring workflows with a fixed vendor list (recurring utility bills), Auto-Approve can yield self-reported time savings without rule inspection, qualifying any blanket assumption that rule visibility blocks all users.",
      "support_type": "qualifies",
      "evidence_refs": ["EV-INT-02"],
      "conflict_refs": ["CLM-01"],
      "status": "supported",
      "boundary": "Synthetic n=1 (AP Clerk); self-reported 20-minute saving is unverified against baseline telemetry or exception/error rates, and skipping rule checks remains vulnerable if the vendor list changes."
    },
    {
      "claim_id": "CLM-03",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "statement": "Missing actor attribution in the audit log when Auto-Approve is enabled creates an organizational compliance blocker that can force team-wide disablement.",
      "support_type": "supports",
      "evidence_refs": ["EV-INT-03"],
      "status": "supported",
      "boundary": "Synthetic n=1 (Controller); actual audit log schema and written compliance requirements were not inspected."
    },
    {
      "claim_id": "CLM-04",
      "study_id": "STUDY-B2B-INVOICE-PILOT-SYN-01",
      "statement": "Ambiguous batch action labeling ('Confirm Batch' interpreted as a preview) can cause unintended immediate approval of multiple invoices, representing a distinct workflow safety defect outside the Auto-Approve toggle.",
      "support_type": "supports",
      "evidence_refs": ["EV-INT-04"],
      "status": "supported",
      "boundary": "Synthetic n=1 (Junior Buyer); distinct UI flow from Auto-Approve toggle; true misclick rate and reversal/undo controls are unknown."
    }
  ],
  "decisions": [
    {
      "decision_id": "DEC-B2B-AUTOAPPROVE-PILOT-01",
      "owner": "Unassigned Product and Finance Compliance Owner",
      "review_date": "2026-12-10",
      "recommendation": "Do not scale Auto-Approve or unguarded batch confirmation based on current synthetic pilot excerpts; hold broad rollout until (1) actor-level audit logging for Auto-Approve changes is verified with compliance, (2) matched vendor rules are surfaced before/during toggle use (or restricted to audited fixed-vendor allowlists), and (3) 'Confirm Batch' separates preview from explicit irreversible commit.",
      "reversal_condition": "Verified actor-level audit logs accepted by compliance plus a task-based usability and telemetry check on real pilot users demonstrating accurate rule comprehension and zero unintended batch approvals across both fixed and variable vendor workflows.",
      "claim_refs": ["CLM-01", "CLM-02", "CLM-03", "CLM-04"],
      "status": "open",
      "authorization_boundary": "Synthetic pilot evidence only (n=4); does not authorize production rollout, compliance sign-off, or net time-savings claims."
    }
  ]
}
```