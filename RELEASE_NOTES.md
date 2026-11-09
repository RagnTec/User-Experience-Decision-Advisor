# Release Notes — UXDA Public Core (`v0.1.0-beta.1`)

We are pleased to introduce the first Source-Available Public Beta candidate of **UXDA Public Core**!

This release packages the core human factors reasoning and interaction design review skills for community evaluation in AI-assisted development environments.

---

## 🏷️ Version Mapping & Architecture

UXDA Public Core establishes an independent public semantic version line starting at `v0.1.0-beta.1`. Component skills maintain their internal evolutionary version tags for developmental traceability:

| Component / Layer | Public Release Version | Historical Evolution Track | Source & Description |
| :--- | :---: | :---: | :--- |
| **UXDA Public Core Suite** | **`v0.1.0-beta.1`** | *Initial Public Line* | Unified source-available distribution of the core skills and references |
| `skills/ux-decision-assistant-router` | `v0.5.4-beta.1` | v0.1.0 → v0.5.4-beta.1 | Workflow entry point, multi-mode routing, & progress mapping |
| `skills/evidence-based-design-review` | `v0.7.0-beta.1` | v0.1.0 → v0.7.0-beta.1 | Standalone interaction friction & cognitive failure mode review |
| Context Bundle Interface Contract | `v0.2` | Specification v0.2 | Decoupled schema for optional external rule/data integration |

---

## 🌟 Key Highlights

### 1. Dual-Skill Architecture
- **UXDA Router (`v0.5.4-beta.1`)**: Classifies user inquiries into `guided` (pedagogical), `decision` (executive choice), and `project` (ongoing study review). Enforces the **Business Progress Map** (`业务推进图`) at the very top of every response.
- **Evidence-Based Design Review Specialist (`v0.7.0-beta.1`)**: Provides direct-invocation, laser-focused design reviews analyzing interaction friction, Norman cognitive action slips, Fitts's law target constraints, and Poka-Yoke error prevention.

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
  - Purged phantom standard numbers (e.g., corrected ISO 9241-920:2024 tactile standard).
- **Epistemic Discipline**:
  - Clarified that $N \ge 30$ is not a sufficient condition for statistical power.
  - Replaced deterministic assertions with structured multi-tier defense concepts (undo, non-modal verification, delayed commit).
- **Scope Calibration**:
  - Clarified boundary between UXDA skills and host LLM platform behaviors (network transmission, session persistence).

---

## 🛠️ Verification & Quality Gates

The Public Core package has undergone reproducible standalone smoke tests in an isolated environment (`fake_home`, zero access to private extensions). The verification covers three distinct tiers:

1. **Actual Local Python Script Execution**:
   - `collaboration_mode.py init/apply`: Verified state initialization, 3-mode transitions (`guided`, `decision`, `project`), and strict rejection of invalid modes.
   - `render_report.py`: Verified offline rendering of self-contained HTML decision briefs (12,657 bytes) without network or external services.
   - `workflow_map.py preset`: Verified workflow plan generation in standalone mode without private extensions.
2. **Static Structural & Link Protocol Verification**:
   - Link integrity: Audited all 93 internal markdown relative links across Router and Specialist (0 broken links).
   - Routing dispatch: Verified routing table definitions in `capability-handoff.md` and `research-routing.md`.
   - Fallback contract: Verified `[NOT EVALUATED]` specification in `design-integration-baseline.md`.
   - Path confinement: AST and text audit of all Python scripts verifying zero access to `storage/raw/`.
3. **Live Cross-Host Agent Evaluation Boundary**:
   - *Important Note*: Local smoke tests verify standalone packaging, file integrity, and local Python script execution in an isolated sandbox. They do **not** constitute live end-to-end evaluations across diverse commercial LLM platforms (e.g., Claude Code, Cursor, or custom IDE harnesses), which require live inference and host-specific tool execution.

---

## ⚖️ Licensing Status

UXDA Public Core `v0.1.0-beta.1` is officially published under the **PolyForm Strict License 1.0.0** ([LICENSE](LICENSE)).

- **Source-Available Public Beta**: This release adopts a restricted, source-available license rather than an OSI-approved open-source license as a deliberate testing-phase strategy. It grants free use for personal study, academic research, experimentation, and noncommercial organizations, while reserving commercial exploitation, modification, and redistribution to the maintainers.
- **Beta Maturity Context**: Adopting this source-available license reflects the current pre-release testing status of the project; it allows public community evaluation and peer methodology review while safeguarding project integrity, and does not indicate that all features have achieved final production stability.
