# Contributing to UXDA

Thank you for your interest in improving UXDA!

UXDA is currently in a **Source-Available Public Beta** under the [PolyForm Strict License 1.0.0](LICENSE). During this public testing phase, community participation is primarily organized around **feedback, evaluation, and issue reporting**.

---

## 1. Primary Contribution Channels (Feedback & Issues)

We actively welcome community feedback via [GitHub Issues](https://github.com/RagnTec/User-Experience-Decision-Advisor/issues):

1. **Bug Reports**:
   - Report script runtime failures, argument parsing errors, formatting anomalies, or compatibility problems across supported agent harnesses using the **Bug Report** template.
2. **Methodology & Evidence Feedback**:
   - Point out inaccurate cognitive mechanism claims (e.g., misattributed action slips), incorrect statistical assumptions, or erroneous standard citations using the **Methodology Feedback** template.
3. **Feature Requests & Knowledge Card Proposals**:
   - Suggest generic ergonomics frameworks, public domain cognitive heuristics, or workflow enhancements using the **Feature Request** template.

---

## 2. Code Contributions & Licensing Boundaries

Under the **PolyForm Strict License 1.0.0**:
- **Modification and Redistribution Restrictions**: Direct modification of the software and distributing modified versions or derived forks are not granted by default under this license.
- **No Unsolicited Code Pull Requests**: Because code contribution agreements and copyright assignment workflows have not yet been formalized for this beta release, unsolicited pull requests containing core code modifications or derived branches cannot be merged at this stage.
- **Future Contribution Framework**: If the project transitions to accepting community code contributions in future phases, explicit contributor agreements (e.g., Developer Certificate of Origin or Contributor License Agreement) and updated licensing policies will be established prior to accepting code patches.

---

## 3. Guiding Principles for Feedback & Proposals

When proposing methodology additions or reporting errors, please ensure your suggestions adhere to UXDA's core tenets:

1. **Strict Public Core Separation**:
   - Never include company-specific rules, internal project codes (e.g., `PROJ-***`), proprietary guidelines, or confidential user telemetry.
   - Do not propose hardcoded absolute local machine file paths (`/Users/...`, `/home/...`).
2. **Epistemic Rigor**:
   - Distinguish empirical research facts from design hypotheses.
   - Avoid deterministic buzzwords ("this will 100% prevent errors", "users inevitably fail").
   - Ensure all statistical claims specify sample constraints, *a priori* power considerations, and context boundaries.
3. **Zero External Dependencies**:
   - All public audit scripts in `scripts/` must strictly use the Python standard library. Propose no external pip dependencies.

