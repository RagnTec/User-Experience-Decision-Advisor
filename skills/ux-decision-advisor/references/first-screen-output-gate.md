# First-screen Output Gate | v0.4D.4

Applies to Router, O, E/D, V and direct Specialist calls. **Professional correctness is mandatory; chart-first order is not.** This pilot replaces the legacy order rule for user-visible first-screen output.

## Default first screen: UX research/business judgment first

1. **Current supported conclusion or choice:** clarify the user problem, likely UX/human-factors mechanism, and its provisional status.
2. **Decisive basis and countercase:** state 1–3 relevant supplied facts or supportable professional inferences, critical unknowns, and what could reverse the current reading.
3. **Actionable next step or stopping condition:** give the smallest useful decision or verification step; do not default to surveys or engineering implementation.
4. **Optional depth:** theoretical explanation, methods, study materials, calculations, audit/status history and project flow on demand. If a critical legal/safety issue exists, state it immediately, not in a hidden appendix.

For explicit project workflow or multi-stage milestone requests, a small progress map may be useful. Do not show O/E/D/V labels, stage status enums or JSON by default. Substantive method/data provenance must remain reconstructible, with the summary limits readable. [Business-Facing Output Contract](business-facing-output-contract.md) governs this presentation order.

## Initial preset (not a fixed mandatory pipeline)

* Goal and decision boundary (known from user input, not implicitly approved).
* Jurisdiction/legal/platform applicability (unchecked until market, channel, implementation and current rules are verified).
* Human factors / industry norms applicability (cognitive HF may apply even without physical HF; distinguish binding norms vs practices).
* Consumer / target market, relevant task and pre/post-use lifecycle.
* Experience mechanism, choice alternatives, consequences, evidence gaps.
* User may **opt in** to VOC, existing document intake, interviews/survey/task tests and analysis return **after** explicit route choice; none is a preset step.
* Conditional decision / ownership and, if relevant, pilot and monitoring.

Only include relevant steps. Do not label preliminary legal triage as formal compliance approval, or mark industry/HF as "not applicable" before considering cognitive mechanisms. An opt-out design is not inherently a lawful or ethical choice, and a recommended alternative does not have measured effectiveness until supported by evidence.

## Preflight self-check (must happen before reply)

- Does the first user-visible paragraph answer the UX/business question with a clear conditional judgment (rather than mandating a business-progress map)?
- Are `已完成/已确认` supported by user-supplied state and referenced deliverables? If not, show `待核实/建议/候选`.
- If a map was requested, does it correctly distinguish confirmed from candidate stages? In all modes, is the decisive blocker visible?
- Does the UX research judgment still include the necessary evidence limits, credible countercase, relevant methodological boundary and decision reversal conditions?

A lightweight local check `scripts/response_preface_check.py` may lint a saved Markdown response; the lint cannot prove UX or legal correctness. The optional `workflow_map.py preset` command creates a versioned, editable default route, not a completed project record.

Routing-specific rule: inspect [Router Scope Contract](router-scope-contract.md) before any analytic handoff.
