# UXDA Installation & Peer Review Setup Guide

This guide covers installing and verifying the UXDA Public Core across common AI coding assistant environments, distinguishing the **official stable baseline (`v0.1.0-beta.3`)** from the **active Peer Review Candidate (`v0.1.0-beta.4-rc.2`)**.

---

## 📌 Version Overview

| Release Track | Version | Git Branch / Tag | Description |
| :--- | :--- | :--- | :--- |
| **Stable Baseline** | `v0.1.0-beta.3` | `main` | Current official public release on GitHub `main`. |
| **Historical RC** | `v0.1.0-beta.4-rc.1` | `tag: v0.1.0-beta.4-rc.1` | First peer review candidate (archived). |
| **Current RC (Peer Review)** | `v0.1.0-beta.4-rc.2` | `branch: release/beta4-rc1`<br>`tag: v0.1.0-beta.4-rc.2` | Active Release Candidate for peer trial (PR #5 unmerged). |

> **Note**: Default commands targeting `main` (such as `git clone` without branch flags or basic `npx skills add`) check out the stable `v0.1.0-beta.3` release. Follow the specific instructions below to test the Release Candidate.

---

## Prerequisites

- **Python 3.9+** (Standard library only; zero mandatory third-party pip dependencies).
- Supported Agent Harness / IDE:
  - **Google Antigravity** (Verified in local sandboxed environment)
  - **Gemini CLI / Google Agent SDK**
  - **Claude Code**
  - **Cursor / Open-interpreter / Custom LLM tool-calling harnesses**

*Compatibility Notice: UXDA consists of local Markdown skill specifications and Python standard library scripts. Runtime behavior depends on the host platform's prompt-based skill discovery and filesystem read capabilities. Cross-platform compatibility across all proprietary commercial harnesses has not been certified.*

---

## Method 1: Direct Release ZIP Installation (Recommended for Peer Review)

To evaluate the exact packaged candidate without cloning Git history:

1. **Download the Release Candidate ZIP**:
   Download `ux-decision-advisor-v0.1.0-beta.4-rc.2.zip` from the [GitHub Pre-release page](https://github.com/RagnTec/User-Experience-Decision-Advisor/releases/tag/v0.1.0-beta.4-rc.2).

2. **Verify SHA-256 Checksum**:
   ```bash
   shasum -a 256 ux-decision-advisor-v0.1.0-beta.4-rc.2.zip
   # Verify that the output matches the published checksum in the Release Notes
   ```

3. **Extract into the Canonical Skills Directory**:
   ```bash
   # Check if a previous installation already exists to avoid accidental overwrite
   if [ -d "$HOME/.agents/skills/ux-decision-advisor" ]; then
     echo "Notice: An existing installation was found at ~/.agents/skills/ux-decision-advisor."
     echo "Please back up or rename the existing directory before unzipping."
   fi

   mkdir -p ~/.agents/skills
   unzip -q ux-decision-advisor-v0.1.0-beta.4-rc.2.zip -d ~/.agents/skills/
   ```
   *The ZIP unpacks directly as `~/.agents/skills/ux-decision-advisor/` containing `SKILL.md`, `references/`, `assets/`, `scripts/`, and `LICENSE` (total 92 files).*

4. **Discovery Link for Google Antigravity (Optional)**:
   ```bash
   mkdir -p ~/.gemini/config/skills
   # Review existing destination before creating symlink (use -s to prevent unintended overwrite)
   ln -s ~/.agents/skills/ux-decision-advisor ~/.gemini/config/skills/ux-decision-advisor
   ```

---

## Method 2: Git Clone Installation

### To install the Stable Baseline (`v0.1.0-beta.3`):
```bash
git clone https://github.com/RagnTec/User-Experience-Decision-Advisor.git /tmp/uxda-source
mkdir -p ~/.agents/skills
cp -R /tmp/uxda-source/skills/ux-decision-advisor ~/.agents/skills/
rm -rf /tmp/uxda-source
```

### To install the Peer Review Candidate (`v0.1.0-beta.4-rc.2`):
```bash
# Clone specifying the release candidate branch or tag
git clone --branch release/beta4-rc1 https://github.com/RagnTec/User-Experience-Decision-Advisor.git /tmp/uxda-source
mkdir -p ~/.agents/skills
cp -R /tmp/uxda-source/skills/ux-decision-advisor ~/.agents/skills/
rm -rf /tmp/uxda-source
```

---

## Method 3: Third-Party CLI / Skill Manager (Project-Local)

When using CLI skill managers (requires Node.js 22.20+ and a compatible agent host per [Vercel Skills CLI specification](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)):

```bash
# Install stable baseline from default branch (main):
npx skills add RagnTec/User-Experience-Decision-Advisor --skill ux-decision-advisor

# Or install the Release Candidate by specifying the release tag in the repository URI:
npx skills add RagnTec/User-Experience-Decision-Advisor@v0.1.0-beta.4-rc.2 --skill ux-decision-advisor
```

> **Migration from legacy `uxda`**: The canonical skill directory and identifier is `ux-decision-advisor`. Legacy installations named `uxda` will not be overwritten automatically; review and migrate them according to your host environment.

---

## Standalone Verification (No Extension Pack Required)

UXDA is designed to work in **Public Core mode** on user-provided in-context materials without requiring any private extension manager or external database.

### Verification Checklist:
1. **Self-check Scripts**:
   Test that internal validation scripts run cleanly with Python standard library:
   ```bash
   python3 ~/.agents/skills/ux-decision-advisor/scripts/response_preface_check.py --help
   python3 ~/.agents/skills/ux-decision-advisor/scripts/render_report.py --help
   ```
2. **Interactive Sanity Test**:
   Open a new session with your AI assistant and prompt:
   > "Use your installed ux-decision-advisor skill to evaluate whether a 15% increase in feature CTR warrants immediate full rollout despite user complaints about interface friction."
   
   **Expected Behavior (Beta.4 Business-First Protocol)**:
   - The agent reads `analytical-quality.md` and `evidence-boundaries.md` before substantive analysis;
   - The default output directly provides the **professional judgment, key evidence, underlying UX friction mechanism, and actionable next steps**;
   - Deep statistical proofs, theoretical constructs, or comprehensive business progress maps are available **on demand**, rather than forced as rigid first-screen barriers.

---

## Verification Boundaries & Known Limitations

- **Isolated Sandbox Verification**: The package structure, internal relative links, and standalone offline Python scripts have passed smoke tests in an isolated local directory.
- **Unverified Scope (Pre-Release Beta)**:
  - Automated formal installation through external marketplace package registries (e.g. `skillx install`, Tencent SkillHub repository synchronization) has **not yet been verified** and is pending marketplace developer authorization and onboarding.
  - End-to-end runtime behavior across all third-party commercial host LLM environments (Claude Code, Cursor, Codex, Gemini CLI, etc.) has not been universally certified.
  - Snapshot SHA-256 checksums provide cryptographic data integrity verification (detecting inadvertent file corruption or tampering); they do not constitute an immutable hardware lock preventing files on disk from being modified.
