# O/E Research Scope Integrity and Evidence-Calibrated Handoff | v0.4D.8

For O-only, E-only or combined O+E, retain the user's explicit research scope. A previous D **brief** is an evaluated proposal, not an approved product direction unless an explicit user/owner approval is actually present in the project record. On scope switch D → O+E, preserve D as `PREVIOUS_ANALYSIS_NOT_APPROVAL`; do not mark `decision complete`, `roadmap fixed`, `approved`, or `D complete` as business authorization.

## Reframe before exploring

- Distinguish **request (a phone-based experience)**, **user outcome (simple, predictable travel preparation)**, **capability baseline (what is technically verified)**, and **actual vehicle/system states**. Examples of important distinctions: a remote comfort request is not the same as propulsion-ready authorization; access credentials are not the same as an HMI button; unlocking is not equivalent to shift/drive authorization. Do not silently merge separate mechanisms into a single "start" or assume an EV, ICE, UWB, BLE, NFC, cloud link, failsafe, authenticated user, etc.
- Use a minimal actor/task context: driver, household co-user, passenger, valet/maintenance operator, nearby persons; phases before arrival, approach, driving readiness, departure and failure/recovery, but ONLY the phases pertinent to this decision. Do not fabricate a complete journey map.
- Cite only **observed** competitors. Direct/indirect product analogies can suggest better questions (handoff, transparency, account delegation, progressive automation), not establish product fact, user acceptance or implementation authorization. Every transferable mechanism needs a material mismatch/countercase.

## O opportunity quality: what O may / may not conclude

- For 1–3 best opportunities use: **user/trigger and actual task → latent psychological need as HYPOTHESIS → observable benefit and friction → alternative explanation → evidence to discriminate → implication for later product choice**.
- Prefer useful problem reframing and missed edge cases to feature brainstorming. The opportunity's **importance is not known** until supported by adequate user or product evidence. Without a real sample, no popularity, adoption, preference rates, ROI or priority claims.
- Do not create `P0/P1/P2`, mandatory hardware/software architecture, feature acceptance decisions or roadmaps unless the user separately asks for a planning/decision exercise and authorizes the D scope. `Potentially high consequence` ≠ `validated high priority`.

## E evaluation quality: task-oriented, not safety-system engineering

- Assess the behavior/status displayed to users, mental model, uncertainty, perceived control, interruption and recoverability across relevant normal + failure cases. Include positives and tradeoffs, not only catastrophic hypotheticals.
- Separate USER EXPERIENCE HAZARD (e.g. unclear readiness, lack of recovery guidance) from SYSTEM ENGINEERING SAFETY REQUIREMENT (e.g. powertrain interlock, digital-key localization, safety state machine). UX can identify safety-sensitive user tasks and recommend owner review; it does NOT invent a mandatory hardware AND gate, numeric safety threshold, cybersecurity design, or certification sign-off.
- Specific quantities, ranges, labels `hard requirement`, compliance prohibitions, and claims of complete reliability must have traceable applicable evidence. Otherwise omit the number or explicitly label it a placeholder awaiting engineering or empirical confirmation. General method knowledge does not verify product-specific limits.
- Test alternative explanations; an ambiguous user experience is a **risk hypothesis**, not proof of anxiety, errors, injury, or complaint frequency. Never promise a universal fail-safe or `zero-risk` experience.

## O/E closing contract (even when no new research is authorized)

1. **Research interpretation**: 1–3 grounded opportunity hypotheses and 1–3 primary user experience mechanisms/risks, distinguishing verified current product facts from conditional inference and missing material facts.
2. **Decision linkage WITHOUT decision usurpation**: which decision would be influenced if evidence supports or refutes the hypotheses; what is *not* ready to decide. Label `DECISION_NOT_YET_AUTHORIZED` or `CONDITIONAL_RESEARCH_INPUT`, not an approved design choice.
3. **Most useful next step in confirmed scope**: a bounded clarification, comparison or analysis of existing materials. Invite up to three **optional** user sources with the precise question each source would resolve; allow continued conditional O/E work without them. Asking permission for V is allowed, starting a study is not.
4. **Return choice**: continue O/E with additional detail, re-open D to make a choice, optionally authorize V, or stop with a bounded provisional conclusion. These are offers, not pre-enabled branches. Explicitly show how current workflow status changes and what evidence would reverse the hypothesis.
5. **Ownership**: UX defines evidence/experience risk and decision implication; product owner decides roadmap, engineering/safety/security assesses systems and thresholds, legal/compliance determines jurisdictional applicability. Do not end with a hardware/API task list.

## Research learning (optional)

When asked *why/how* a method was chosen, demonstrate **business question → user-task construct → competing hypotheses → candidate method and its limitations → possible result → decision change**, without mutating O/E/D/V scope or pretending a teaching example is actual research.

## Minimal first screen

`业务推进图 rN｜需求明确 → 法规与系统边界：待核实 → O/E：当前 → 现有证据复核：可选 → D 决策或停止：待用户选择`

`分析范围：O+E 已确认；历史 D：仅完成分析输出，未见方案批准。`

Then short main finding and end with bounded, decision-linked continuation. The map is an informational snapshot, not an auto-approved project plan.
