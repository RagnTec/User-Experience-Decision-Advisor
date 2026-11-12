# Jurisdiction, binding requirements and industry norms gate | shared O/E/D/V

**Always run a short applicability triage before advocating a new need, feature, design change, research protocol or launch decision.** The purpose is to keep UX decisions inside applicable requirements, not to impersonate lawyers, certify products or demand an exhaustive legal review for an early idea.

## 1. Establish the narrow context
- Identify **where** the product/service is offered or used (country and, where material, state/province, channel), **what** product category and audience (including minors/other vulnerable users), **which lifecycle action** (research/data collection, concept, design, trial, marketing claim, deployment), and **when** the decision would take effect. Cross-border data flows may involve more than one jurisdiction.
- If unknown, label jurisdiction or product scope **UNRESOLVED**. Ask the single most consequential question if a binding compliance decision depends on it; otherwise continue a bounded UX/experience exploration with no legality claim.
- Existing company policies, legal notes and standards provided by a user are **project evidence**, not automatically up-to-date controlling law. Note version, provenance, owner and any conflicts; never send private materials to public search or other systems without authorization.

## 2. Distinguish authority and purpose (do not collapse categories)
1. `BINDING_LAW`: statutes, regulations and legally binding regulator requirements.
2. `MANDATORY_STANDARD`: technically mandatory requirements in the applicable jurisdiction, or otherwise incorporated into binding regulation or contract. A standard's prefix/name alone does not establish applicability or legal force.
3. `VOLUNTARY_STANDARD`: guidelines or voluntary standards; not necessarily legally binding, but may provide a recognized conformity path, and can become contractually binding by incorporation.
4. `CONTRACT_OR_PLATFORM`: contracts, platform terms, procurement commitments and certification-scheme conditions; check enforceability and responsible owner. Not automatically mere convention.
5. `INDUSTRY_CONVENTION`: customary practice, accepted pattern or de facto norm without a demonstrated binding source. It may be suboptimal, context-dependent, contestable or misleading.
6. `ORGANIZATION_RULE`: organizational policies, brand/design systems, internal operating rules and governance; may have internal approval or legal implications. No internal rule overrides binding external law.

Important: classify the **specific requirement**, not its document title. A generally voluntary standard may contain provisions incorporated into an enforceable contract or regulation; confirm the exact context.
- **Touch Screen Usability vs. Machinery Emergency Stop Safety**:
  - **Ergonomic Standards Status & Threshold Calibration**: Note that `ISO 9241-920:2009` has been officially withdrawn and superseded by `ISO 9241-920:2024` (published second edition, Guidance on tactile and haptic interactions). ISO 9241 series standards provide voluntary ergonomic guidance and conceptual frameworks; they do NOT prescribe fixed millimeter button thresholds. Purge any claims presenting unsourced dimensional heuristics (such as 9.5–12 mm) as standardized research or industry baselines, and eliminate any attribution to ISO standards. Non-existent identifiers without official ISO catalogue records (such as `ISO 9241-924`) must NOT be cited as valid standards.
  - **Three Tiers of Machinery Emergency Stop Standards**:
    1. *ISO 13850*: Specifies functional design principles and requirements for the emergency stop function of machinery;
    2. *IEC 60204-1*: Specifies safety requirements for electrical equipment of machines, including stop categories (0, 1, 2);
    3. *IEC 60947-5-5*: Specifies electromechanical requirements for emergency stop devices with mechanical latching functions.
  - **Legal Force & Scope Calibration**: ISO and IEC standards are voluntary international consensus standards by default; they do not have unconditional universal statutory legal force across all machines and jurisdictions unless formally incorporated by applicable legislation, directives, or contractual specifications. Do not generalize the specific mechanical actuator construction requirements of IEC 60947-5-5 universally to all machinery without reference to applicable risk assessments.
  - **Functional Safety Warning**: An ordinary software touch screen interface cannot, without dedicated functional safety verification (e.g. ISO 13849-1 / IEC 62061) and appropriate machinery risk assessment, be used as an emergency stop device. Any specific claim must cite verifiable clauses and product context rather than sweeping assertions.

## 3. Evidence and verification
For every decision-relevant rule, capture: category, affected action, jurisdiction and product population, identifier/title, authority, source/version/effective date, applicability reasoning, verification status (official source verified / user-provided document only / unverified), possible conflicts, responsible reviewer, and current evidence gaps. Prefer competent authorities' **official current** texts over third-party summaries. The latest retrieval date is not necessarily the legal effective date.

- **Offline**: read authorized local standards/policies as a preliminary source. State that legal currency and applicability have **not** been externally verified. Do not invent thresholds, certifications, exemptions or rulings. Offline operation must not prevent bounded UX analysis.
- **Online**: verify only material legal/standards issues with competent official sources, jurisdiction/version/effective date and current applicability. Source links do not imply the product passed compliance assessment.
- **Contradictions**: original binding sources prevail over heuristics/marketing descriptions; unresolved discrepancies go to compliance/legal/standards owner.

## 4. Decision and authority gates
- `BINDING_LAW` and applicable `MANDATORY_STANDARD`: never recommend implementation known to violate them; stop or redesign that branch and route uncertain/high-impact issues to qualified legal/compliance/safety review. General stakeholder approval **cannot waive the law**. Do not mark `compliance approved` merely from this Skill.
- `CONTRACT_OR_PLATFORM` / `ORGANIZATION_RULE`: identify contractual/internal authority and approval path. Do not label exceptions as adopted until the authorized owner approves; an internal exception never makes an external legal conflict lawful.
- `VOLUNTARY_STANDARD`: may recommend an alternative technical approach **only as a proposal**, explaining equivalent protection, associated verification burden and owner sign-off. In some contexts a standard provides a recognized compliance route: a change may increase conformity-assessment obligations.
- `INDUSTRY_CONVENTION`: the Agent **may challenge or propose breaking** a convention with user-value rationale, trade-offs, counterexamples, accessibility, interoperability and consumer-expectation risk. Explicitly tag `DEVIATION_PROPOSAL`, request review from a named human role, and do **not** implement, approve a rollout or claim a sanctioned exception without the user's responsible human decision. Propose ordinary conforming options alongside novel ones where feasible.
- Where a legal status is uncertain and material, use `HOLD_FOR_SPECIALIST` for the affected deployment/commitment, **not** a blanket halt to all O/E/V exploratory analysis.

## 5. Output and iteration
Normal short tasks: one concise preflight sentence (`target jurisdiction, potential binding or customary constraints, verification status`) or no visible section when none is consequential, while still applying the triage. High-stakes cases: a compact **Constraint Ledger** with rule/source/version, binding tier, product applicability, proposed exception, owner, and decision status. Distinguish `UX_RECOMMENDED` from `IMPLEMENTATION_AUTHORIZED`; the latter must not be awarded by the agent.

Reopen the gate if the target market, product category, user group, rollout channel, material function, law/standard version, or data-processing behavior changes. Record which recommendation is affected, not automatically invalidate every UX insight. For an optional private machine-readable structural check, see [Constraint Gate Record](../assets/jurisdiction-gate-schema.md) and `scripts/jurisdiction_gate_audit.py`. **Passing code checks do not establish legality or legal advice.**

## Public reference anchors (not a preloaded regulation database)
- PRC *Standardization Law*: https://www.samr.gov.cn/zw/zfxxgk/fdzdgknr/fgs/art/2023/art_d7040b9f1d0f4980a0e55089a57bf37d.html — mandatory standards must be implemented; recommended standards encouraged.
- European Commission, *Harmonised standards*: https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards_en — harmonised standards generally voluntary, alternative technical compliance routes possible under applicable laws.
- EU *Regulation 2023/988*: https://eur-lex.europa.eu/eli/reg/2023/988/oj/eng — **this session encountered a robot verification page, operative text NOT inspected**; illustrative locator only, not an applicable-clause citation for any product.

Never copy protected standards' full text into the public Skill. References do not replace jurisdiction-specific professional review.

## v0.4D.6: provenance is not optional

Before giving a specific local standard identifier, its alleged mandatory clause or compliance judgement, apply [Claim Provenance Gate](source-provenance-gate.md). A statement in model training memory is not `VERIFIED_OFFICIAL`; tool availability or a provided link alone does not prove a search occurred. For product-level App updates, do not silently substitute vehicle-level OTA rules. When documents are not accessible, give a bounded preliminary constraint triage and specify source requirements rather than an unverified legal ban.
