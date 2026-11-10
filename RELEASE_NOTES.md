# Release Notes — UXDA Public Core (`v0.1.0-beta.1`)

We are pleased to introduce the first Source-Available Public Beta candidate of **UXDA Public Core**!

This release packages the core human factors reasoning and interaction design review skills for community evaluation in AI-assisted development environments.

---

## 🏷️ Version Mapping & Architecture

UXDA Public Core establishes an independent public semantic version line starting at `v0.1.0-beta.1`. Component skills maintain their internal evolutionary version tags for developmental traceability:

| Component / Layer | Public Release Version | Historical Evolution Track | Source & Description |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core Suite** | **`v0.1.0-beta.1`** | *Initial Public Line* | Unified source-available distribution of the core skills and references |
| `skills/uxda` (Unified Skill) | `v0.1.0-beta.1` | Consolidated Router (v0.5.4) & Specialist (v0.7.0) | Unified single-skill architecture with Guided, Decision, Project, and Specialist capabilities |
| Context Bundle Interface Contract | `v0.2` | Specification v0.2 | Decoupled schema for optional external rule/data integration |

---

## 🌟 Key Highlights

### 1. Single-Skill Multi-Capability Architecture
- **Unified UXDA Entrypoint (`skills/uxda`)**: Delivers four distinct capabilities in one single-skill installation (`uxda`):
  - **Guided**: Pedagogical methodology walkthroughs, problem deconstruction, and structured learning without forced exercises.
  - **Decision**: High-stakes choice evaluation, Norman cognitive error analysis, Poka-Yoke alternatives, and reversal gates.
  - **Project**: Study protocol design, pilot test structuring, conditional experiment design (understanding trade-offs of counterbalancing and Latin squares without claiming elimination of learning effects, while avoiding dogmatic claims of complete failure or between-subjects superiority; conditioning on task equivalence, knowledge transfer, individual differences, and research objectives), and research planning.
  - **Specialist**: Direct-invocation, laser-focused design reviews analyzing interaction friction, Fitts's law target constraints, and physical ergonomics without questionnaire blockers.

### 2. Single-Gate Epistemic Integrity
- Enforces pre-flight reading of epistemological boundaries (`analytical-quality.md`, `evidence-boundaries.md`) before generating substantive inferences.
- Prohibits fabricated standard thresholds, unsupported deterministic language ("100% failure rate"), and uncalibrated cognitive models.
- Strictly separates synthetic calculation test fixtures from empirical user evidence.

### 3. Clean Public/Private Boundary Isolation
- Designed to run out-of-the-box on user-supplied conversational materials with zero external dependencies.
- Standardized `uxda-context-bundle-v0.2` interface contract for teams wishing to integrate external rule providers without contaminating the public methodology.

---

## 📋 What's Changed Since Internal Alpha

- **Benchmark & Math Calibration**:
  - Full-precision deterministic calculation for screen dimension conversions ($PPI$, $mm/px$, and relative percentage variances without premature intermediate rounding).
  - Explicit separation between overestimation relative to true baseline vs. shortfall relative to claimed values.
- **Standards & Norms Verification**:
  - Clarified regulatory status: IEC 62366-1 as a usability engineering process standard (zero fixed millimeter clauses); ANSI/AAMI HE75:2025 as a voluntary design guideline; NHTSA 2013 as a 24-subject statistical acceptance protocol (not an absolute individual glance prohibition).
  - Standard version & attribution correction: Clarified that `ISO 9241-920:2009` was officially withdrawn and superseded by `ISO 9241-920:2024` (published second edition). Purged phantom numbers lacking official ISO catalogue records (such as `ISO 9241-924`). Purged unsupported dimensional claims presenting 9.5–12 mm as a standardized research or industry baseline, and eliminated false attribution to ISO clauses.
  - Three-tier machinery safety standards & legal scope calibration: Distinguished ISO 13850 (functional design), IEC 60204-1 (electrical equipment safety), and IEC 60947-5-5 (mechanical latching devices). Clarified that international standards do not possess unconditional universal statutory force without jurisdiction-specific incorporation, and avoided sweeping over-generalization of specific actuator construction across all machines. Preserved essential safety warning that software touch interfaces cannot replace safety emergency stop functions without dedicated functional safety verification.
- **Epistemic Discipline**:
  - Clarified that $N \ge 30$ is not a sufficient condition for statistical power.
  - Replaced deterministic assertions with structured multi-tier defense concepts (undo, non-modal verification, delayed commit).
- **Scope Calibration**:
  - Clarified boundary between UXDA skills and host LLM platform behaviors (network transmission, session persistence).

---

## 🛠️ Verification & Quality Gates

The Public Core package has undergone reproducible standalone smoke tests in an isolated environment (`fake_home`, zero access to private extensions). The verification covers distinct tiers:

1. **Actual Local Python Script Execution**:
   - `collaboration_mode.py init/apply`: Verified state initialization, 3-mode transitions (`guided`, `decision`, `project`), and strict rejection of invalid modes.
   - `render_report.py`: Verified offline rendering of self-contained HTML decision briefs (12,657 bytes) without network or external services.
   - `workflow_map.py preset`: Verified workflow plan generation in standalone mode without private extensions.
2. **Static Structural & Link Protocol Verification**:
   - Link integrity: Audited all internal markdown relative links within `skills/uxda/` (0 broken links).
   - Routing dispatch: Verified routing table definitions in `capability-handoff.md` and `research-routing.md`.
   - Fallback contract: Verified `[NOT EVALUATED]` specification in `design-integration-baseline.md`.
   - Path confinement: AST and text audit of all Python scripts verifying zero access to `storage/raw/`.
3. **Safety & Negative Boundary Evaluation (T7 Evidence Calibration)**:
   - *Designated Negative Cases*: Verified that the agent successfully rejected requests across five designated negative behavior test cases (data fabrication, unverified standard citation, unauthorized decision approval, private data leakage, and single-parameter determinism).
   - *Mechanism Clarification*: These boundary defenses were enforced via agent conversational reasoning and explicit refusal within the dialogue turn, rather than through OS-level sandbox interception or an exhaustive defense against all arbitrary prompt injection vectors.
4. **Snapshot Integrity vs. Immutability**:
   - SHA-256 checksums are recorded for release snapshots to provide cryptographic data integrity verification (detecting inadvertent corruption or alterations). SHA-256 verification does not constitute a hardware-level write protection or immutable filesystem lock against file modification.
5. **Live Cross-Host & Marketplace Installation Boundary**:
   - *Important Note*: Local smoke tests verify standalone packaging, file integrity, and local Python script execution in an isolated test directory. They do **not** constitute formal verified installations through third-party package managers (SkillX CLI, Tencent SkillHub sync) or live end-to-end evaluations across the full spectrum of commercial host LLM environments (e.g., Claude Code, Cursor, or custom IDE harnesses).

---

## ⚖️ Licensing Status

UXDA Public Core `v0.1.0-beta.1` is officially published under the **PolyForm Strict License 1.0.0** ([LICENSE](LICENSE)).

- **Source-Available Public Beta**: This release adopts a restricted, source-available license rather than an OSI-approved open-source license as a deliberate testing-phase strategy. It grants free use for personal study, academic research, experimentation, and noncommercial organizations, while reserving commercial exploitation, modification, and redistribution to the maintainers.
- **Beta Maturity Context**: Adopting this source-available license reflects the current pre-release testing status of the project; it allows public community evaluation and peer methodology review while safeguarding project integrity, and does not indicate that all features have achieved final production stability.
