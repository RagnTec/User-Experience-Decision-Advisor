# Methodology Boundaries & System Limitations

To prevent over-reliance and unwarranted certainty, this document outlines the fundamental epistemological, operational, and architectural limitations of UXDA Public Core.

---

## 1. Epistemological & Evidentiary Boundaries

1. **No Automated Hallucination Elimination**:
   - While UXDA's Single-Gate enforces pre-flight verification and structured reasoning steps, **it cannot guarantee that an underlying LLM will never hallucinate or misapply a principle**.
   - All analytical conclusions and design recommendations remain **conditional proposals for discussion (拟议审议建议)** that require human verification.

2. **Synthetic Data Has Zero Population Generalizability**:
   - Synthetic fixtures, mock datasets, and developmental pilots are strictly intended for testing software pipelines and analytical logic.
   - **Synthetic data cannot serve as empirical evidence for real user behavior, market demand, or production safety.**

3. **Sample Size & Statistical Power ($N \ge 30$ is NOT sufficient)**:
   - Small qualitative studies ($N = 5 \text{ to } 12$) identify cognitive mechanisms, mental models, and severe usability obstacles. They **cannot establish population incidence, market prevalence, or precise effect sizes**.
   - The common heuristic "$N \ge 30$" is merely a rule-of-thumb for the Central Limit Theorem approximating normal distributions. It is **NOT** a sufficient condition for statistical power. Statistical power ($1 - \beta$) requires formal *a priori* power analysis based on expected effect size (Cohen's $d$), alpha level, and variance.

4. **Methodological Silos**:
   - **Usability Testing**: Measures behavioral task friction and cognitive blockages; cannot forecast commercial demand or conversion willingness.
   - **Surveys**: Capture self-reported perceptions and attitudes; cannot accurately measure micro-interaction times or actual behavioral slips.
   - **Telemetry & Server Logs**: Record observed click frequencies and abandonment points; cannot explain subjective intent or cognitive rationale without qualitative triangulation.

5. **Cognitive Modeling Calibration (KLM/GOMS)**:
   - Uncalibrated keystroke-level models (e.g., standard desktop constants like $M = 1.35\text{s}$ or $K = 0.2\text{s}$) must never be treated as empirical measurements on touchscreen tablets, automotive cockpits, or medical hardware without dedicated environmental calibration.

---

## 2. Professional Authority & Regulatory Boundaries

1. **Proposals vs. Business Decisions**:
   - UXDA outputs are structured decision-support materials, never approved engineering change orders, corporate resolutions, or product sign-offs.
   - Final decisions on product releases, budget allocations, and risk acceptances reside exclusively with authorized human decision-makers.

2. **Standards vs. Statutory Regulations & Safety Distinctions**:
   - UXDA differentiates mandatory statutory laws (e.g., EU MDR, FAA regulations, machinery safety directives) from voluntary consensus guidelines (e.g., ANSI/AAMI HE75, ISO 9241).
   - **Verification, Standard Status & Phantom Standards**: If a standard's official text has not been directly verified, specific citations must be labeled as `[NOT VERIFIED]`. Unverified citations must never be mechanically substituted with another standard. Standards must cite current official editions (e.g., `ISO 9241-920:2024`, noting the 2009 edition was officially withdrawn); hallucinated numbers without official ISO records (such as `ISO 9241-924`) are strictly prohibited. Specific dimensional recommendations (such as informal heuristics like 9.5–12 mm) lack universal empirical justification across all task contexts and must never be falsely presented as standardized research or industry baselines, nor attributed to ISO clauses.
   - **Machinery Safety Standards & Touch Screen Boundaries**: Voluntary international standards (ISO/IEC) do not have unconditional universal statutory legal force across all jurisdictions. Distinguish the three tiers of machinery safety standards: ISO 13850 (emergency stop function design), IEC 60204-1 (machine electrical equipment safety), and IEC 60947-5-5 (mechanical latching emergency stop devices). Construction requirements for specific actuators must not be generalized universally to all machines without applicable risk assessments. However, an ordinary software touch screen interface cannot, without dedicated functional safety verification (e.g. ISO 13849-1 / IEC 62061) and formal risk assessments, be used as an emergency stop safety device.

3. **Engineering & Physical Safety Separation**:
   - Software temperature setpoints ($\Delta T$) represent operational modes, not measured surface contact temperatures or heat fluxes.
   - UXDA evaluates user behavioral slips and mode confusion; it does **not** evaluate electrical insulation, flammability ratings, structural fatigue, or thermodynamic heat dissipation.

---

## 3. Operational & Platform Limitations

1. **Host Platform Dependent Tool-Calling**:
   - UXDA relies on the host agent harness to execute `read_file` and `run_command`. The effectiveness of Single-Gate depends on the host LLM adhering to tool-invocation instructions.
2. **Deterministic Calculations Require Calibrated Inputs**:
   - Physical millimeter conversions assume 1:1 unscaled square native pixels on a calibrated display panel. Deviations in OS display scaling (DPI scaling factors), aspect ratios, or viewport zoom must be explicitly calibrated by the user.
3. **No Database Persistence Guarantees**:
   - The presence of an interactive UI element (such as a save button) does not prove that backend database persistence, transactional rollbacks, or offline caching are functioning correctly.
4. **Unverified Scope: Formal Package Installation & Cross-Host Runtime Compatibility**:
   - Testing in the current beta was conducted in an isolated local filesystem sandbox and the development harness.
   - Formal automated installation through external package manager registries (e.g., SkillX CLI, Tencent SkillHub repository sync) and live runtime compatibility across the full diversity of commercial host LLM environments (such as Claude Code, Cursor, Codex, Gemini CLI, or diverse operating systems) have **not** been certified.
   - Users and platform operators must perform independent verification in their target deployment environments.
