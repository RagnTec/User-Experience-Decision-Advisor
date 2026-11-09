# Decision Integrity Contract | v0.4A

A discovery opportunity (O), experience claim (E), or decision alternative (D) is **intermediate** until linked to a possible consequential choice. The goal is decision quality, not a mandatory 'do something' recommendation.

## Decision record: minimum information for consequential claims
- **decision_id / decision_question**: what can the accountable human choose? Who needs this analysis? (No unauthorized action.)
- **options**: at least status quo and feasible change when relevant; no false binary imposed by the user.
- **claim_id / claim_text**: concrete claim with provenance one of USER_PROVIDED, OBSERVED, VERIFIED_EXTERNAL, METHOD_BASED_INFERENCE, ASSUMPTION, UNVERIFIED. Do not label an unvisited web address as verified.
- **applicability**: population/market, product/technology configuration, task, date and conditions where decision relevant.
- **support_status**: SUPPORTED, CONDITIONAL, or UNSUPPORTED; these are epistemic categories, not numerical confidence scores.
- **countercase / reversal_trigger**: credible alternative explanation or what new evidence changes recommendation.
- **decision_impact**: keep, minimally change, compare, limited pilot, defer, stop, or escalate; include relevant cost/constraints only if known.
- **next_low_cost_action**: only when it could change an actual decision. 'Run a survey' is not an acceptable mandatory generic close.

## Mandatory checks
1. Check counterfactual baselines: if another plausible hardware/algorithm/market specification reverses the main choice, ask for the minimal capability boundary or give symmetric conditional choices.
2. Strong claims ('must', 'all', 'X%', 'guaranteed', 'industry standard', 'legal prohibition') need corresponding product facts and original sources. If missing, narrow or omit.
3. Evidence from separate actors, markets or journey phases cannot be averaged into one user truth.
4. O opportunities are hypotheses until tested or supported by suitable evidence. E mechanisms are not actual observed experience. D recommendations are not substitutes for technical, safety, regulatory or finance sign-off.
5. No fabrication of user quotes, sample data, effect size, numeric opportunity scores, compliance claims or ROI.
6. A new result must state whether it UPHOLDS, QUALIFIES, CHANGES, or DOES_NOT_RESOLVE the earlier decision, and why. This is a proposed analysis record, not a persistent storage system.
7. Maintain research independence: marketing/PR may provide context, but cannot instruct the analysis to suppress unfavorable evidence or fabricate consumer sentiment. Provide claim/experience gaps and evidence needed for responsible product or communications decisions; not a defensive spin strategy.

## Minimal user-facing presentation
State **recommended current choice and conditions first**; attach 1–3 consequential evidence points and explain what would change choice. Evidence trace expands on demand and can support H5. If no current choice can be justified, state which decision is genuinely open and what minimum evidence would distinguish it. O/E can operate independently without a full D report, but must state the decision their findings could affect.

## Mandatory authority boundary

Before any recommendation to implement, apply [Jurisdiction & Norms Gate](jurisdiction-and-norms-gate.md). Keep `UX_RECOMMENDED` distinct from compliance approval or operational launch permission. Industry custom can be questioned with a proposed alternative, but execution requires the relevant human review; no internal approver can waive binding law.

## v0.4D.6: finish the decision, not an engineering checklist

Use [Decision-Centred Research Closure](decision-closure-gate.md) for consequential D/E and multi-stage reports. The last section should state present decision status, minimal evidence or analysis that could change it, optional user document intake, owner, and next update of the progress map. A proposed API, signal, installation timer, or rollout script is not a UX research conclusion.
