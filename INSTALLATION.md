# UXDA Installation Guide

This guide covers installing and verifying the UXDA Public Core (`v0.1.0-beta.3`) skills across common AI coding assistant environments.

---

## Recommended CLI Installation (Project-Local)

Install the public Skill by its stable identifier (requires Node.js 22.20+ and a compatible agent host):

```bash
npx skills add RagnTec/User-Experience-Decision-Advisor --skill ux-decision-advisor --agent codex
```

This is a project-local install unless you explicitly add `--global`. Check the CLI result and inspect the installed `SKILL.md` before use. Use the GitHub Release Tag to pin a historical version if needed.

**Migration from `uxda`:** the renamed Skill has a different install identifier. Existing `uxda` installations will not be silently replaced or removed. Review the old installation before removing it; users on `v0.1.0-beta.2` can keep that version.

## Prerequisites

- **Python 3.9+** (Standard library only; zero mandatory third-party pip dependencies).
- Supported Agent Harness / IDE:
  - **Google Antigravity**
  - **Gemini CLI / Google Agent SDK**
  - **Claude Code**
  - **Cursor / Open-interpreter / Custom LLM tool-calling harnesses**

*Note: UXDA consists of portable markdown skills and Python scripts. Compatibility depends on the host platform's support for standard prompt-based skill discovery and filesystem read tools.*

---

**Access note:** This GitHub repository is public and can be cloned over HTTPS without repository membership.

## Method 1: Global Installation (Recommended)

Following the standard multi-agent convention, reusable skills should be installed globally under `~/.agents/skills/`.

```bash
# 1. Clone repository
git clone https://github.com/RagnTec/User-Experience-Decision-Advisor.git /tmp/uxda-source

# 2. Copy the unified UXDA skill to the canonical shared directory
mkdir -p ~/.agents/skills
cp -R /tmp/uxda-source/skills/ux-decision-advisor ~/.agents/skills/

# 3. Clean up source checkout
rm -rf /tmp/uxda-source
```

### Discovery Link for Google Antigravity
If you use Google Antigravity, link the canonical directory to your Antigravity config:

```bash
mkdir -p ~/.gemini/config/skills
ln -sf ~/.agents/skills/ux-decision-advisor ~/.gemini/config/skills/ux-decision-advisor
```

---

## Method 2: Project-Local Installation

If your team requires pinning skills within a specific repository root:

```bash
cd /path/to/your/project
mkdir -p .agents/skills
cp -R /path/to/uxda/skills/ux-decision-advisor .agents/skills/
```
Ensure your agent harness is configured to inspect `.agents/skills/` within the active workspace.

---

## Standalone Verification (No Extension Pack Required)

UXDA is designed to work in **Public Core mode** on user-provided in-context materials without requiring any private extension manager or database.

### Verification Checklist:
1. **Self-check Script**:
   Test that the internal python validation scripts run without errors:
   ```bash
   python3 ~/.agents/skills/ux-decision-advisor/scripts/response_preface_check.py --help
   python3 ~/.agents/skills/ux-decision-advisor/scripts/render_report.py --help
   ```
2. **Interactive Sanity Test**:
   Open a new session with your AI assistant and prompt:
   > "Use your installed UXDA skill to outline a research plan comparing two navigation bar layouts."
   
   **Expected Behavior**:
   - The agent reads `analytical-quality.md` and `evidence-boundaries.md` before substantive analysis;
   - The first output block presents a `业务推进图` (Business Progress Map);
   - The agent operates directly on the stated problem without attempting unauthorized background directory scans.

---

## Verification Boundaries & Known Unverified Scope

- **Isolated Sandbox Verification**: The Public Core package structure, internal relative links, and standalone offline Python scripts have passed smoke tests in an isolated local directory.
- **Unverified Scope (Pre-Release Beta)**:
  - Automated formal installation through external marketplace package registries (e.g. `skillx install`, Tencent SkillHub repository synchronization) has **not yet been verified** and is pending marketplace developer authorization and onboarding.
  - End-to-end runtime behavior across all third-party commercial host LLM environments (Claude Code, Cursor, Codex, Gemini CLI, etc.) has not been universally certified.
  - Snapshot SHA-256 checksums provide cryptographic data integrity verification (detecting inadvertent file corruption or tampering); they do not constitute an immutable hardware lock preventing files on disk from being modified.
