# Decision and business output

Use for recommendations, trade-offs, research findings, product/design briefs, or meeting materials. Presentation must not create evidence or authority.

## 1. Lead with the decision

State the current judgment and its conditions first. If no defensible choice exists, name the open decision and the minimum evidence that would resolve it.

A useful default is:

**judgment → decisive evidence and user-task mechanism → business consequence → smallest next step → reversal condition.**

This is a logical flow, not a mandatory four-box template.

### Layered delivery

| Layer | Trigger | Content | Limit |
|---|---|---|---|
| Direct answer | default | judgment, decisive boundary, next action | one short expansion cue at most |
| Explanation | user asks why or to expand | only the relevant mechanism, method trade-off, or evidence audit | do not repeat the direct answer |
| Artifact | user asks for a plan, instrument, review, record, or report | usable deliverable with fields and checks | no surrounding essay or blank template |

Do not announce layers, create a menu of internal modes, or preload every optional section. In Chinese, use a natural cue such as “可展开：方法选择 / 执行方案 / 证据审计”; in English, use “Optional detail: method / protocol / evidence audit.” Remove the cue when nothing material remains.

## 2. Make the recommendation conditional

Include:

- affected users, tasks, product/version, and context;
- options, including status quo when relevant;
- benefits, costs, risks, and dependencies;
- strongest countercase;
- evidence status and important unknowns;
- what new observation would change the recommendation;
- owner and authorization boundary.

Avoid false binaries. Do not impose a single option when several are feasible.

Do not relabel a pre-specified decision branch as a reversal condition. “If evidence points to value, study value” is a branch; “a reproducible target-user study shows the entry is discovered and understood without assistance” is new evidence that could reverse an entry-first recommendation.

## 3. Translate without distorting

For product and design partners, use task behavior and decision language. Explain a technical term only when it changes interpretation. For researchers, retain methodological precision. For learners, add one concrete example.

Do not use “proven,” “guaranteed,” “industry standard,” “compliant,” or a precise uplift without supporting evidence. Do not turn a pilot into a population claim.

## 4. Keep process internal

Do not expose routing logic, internal IDs, audit logs, raw JSON schemas, or status codes by default. Show them only when the user requests traceability or they materially help a handoff.

Translate status into ordinary language:

- “现有证据不足以支持直接上线” rather than an opaque hold code;
- “可先做低成本、可逆的修补并观察” rather than a launch instruction;
- “需要授权负责人确认” rather than implying approval.

## 5. Evidence-to-outcome discipline

Do not state improvement, deterioration, equivalence, or direction unless the data support it. If only one condition or aggregate result is available, describe exactly that and identify the missing comparison.

Do not fabricate paired participant outcomes from group aggregates. Do not create before/after narratives for synthetic cases unless explicitly labeled.

## 6. Decision brief

A concise decision brief may include:

| Field | Content |
|---|---|
| Decision | accountable choice and timing |
| Recommendation | conditional current choice |
| Why | decisive evidence and mechanism |
| Alternatives | serious options and status quo |
| Countercase | strongest argument against the recommendation |
| Evidence gap | unknown that matters |
| Next action | feasible owner and step |
| Reversal condition | observation that changes the choice |
| Boundary | research, legal, safety, or launch authority not granted |

### Evidence and decision record

Use `assets/uxda-evidence-v1.schema.json` when the user needs traceability, reuse, or handoff. Keep it minimal: study, evidence, claim, and decision objects with stable IDs and explicit references. Validate with `scripts/validate_evidence.py`; validation checks structure and links, not whether a source is true.

A decision-ledger entry adds only what the brief lacks:

- decision owner and review date;
- supporting and opposing claim IDs;
- implementation status and actual result when known;
- result source references and any evidence that was overturned.

Do not create a second requirement-review graph. UXRR may supply the upstream requirement claim and evidence request; UXDA records how research evidence changed the decision and what happened afterward.

## 7. Final quality check

- Is the first sentence useful to the decision-maker?
- Are evidence and inference distinguishable?
- Does the recommendation fit actual resources?
- Is the next step tied to a real uncertainty?
- Is the countercase credible?
- Are limitations proportionate rather than boilerplate?
- Have unauthorized implementation or approval claims been avoided?
