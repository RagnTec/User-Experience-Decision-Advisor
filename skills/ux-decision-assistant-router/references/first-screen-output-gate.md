# First-screen Output Gate | v0.4D.4

Applies to Router, O, E/D and V, including direct professional-Skill calls, initial turns, mid-project turns, and private H5 exports. **Output order is a hard contract**, not an optional stylistic choice.

## Output order

1. **业务推进图** — first non-whitespace content in a substantive project response. Initially propose a context-sensitive stage route. In follow-ups refresh only affected nodes. Compact text arrow route suffices; expanded Mermaid when the user requests project workflow or milestone review. The graph is a decision/project plan, NOT the consumer journey.
2. **分析范围 O/E/D/V** — distinct `已识别/待确认` from `用户已确认`; only explicitly selected tracks may run; never preset VOC/访谈/问卷 branches.
3. **当前研究判断及证据边界** — decision question, experience or cognition mechanism, current supported vs hypothetical claims, blocking regulatory/technical unknowns.
4. **Professional O/E/D/V analysis** — task and audience, options, evidence, countercase, real decision consequences; natural paragraphs with meaningful headings.
5. **Action and user checkpoint** — next recommended preparation/optional study/decision handoff. User can explicitly change or reopen any prior node; do not assert business approval without authorized evidence.

Do not let an individual report template, short-brief target length, or H5 detail folding override this order. Include the flowchart in **D, E, O, V and research/decision updates**. A one-line route is enough for routine updates. Do not block emergency/safety advice to draw a diagram first.

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

- Is the **first** user-visible component the `业务推进图` stage route, before report title or conclusion?
- Are `已完成/已确认` supported by user-supplied state and referenced deliverables? If not, show `待核实/建议/候选`.
- Does the path identify current core stage and 1–3 possible next steps **without activating any unconfirmed branch**? Is a key blocker visible?
- Does D/E/O/V still include enough research substance, alternatives and decision reversal conditions?

A lightweight local check `scripts/response_preface_check.py` may lint a saved Markdown response; the lint cannot prove UX or legal correctness. The optional `workflow_map.py preset` command creates a versioned, editable default route, not a completed project record.

Routing-specific rule: inspect [Router Scope Contract](router-scope-contract.md) before any analytic handoff.
