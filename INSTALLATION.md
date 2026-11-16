# UXDA Installation & Peer Review Setup Guide

This guide covers installing and verifying the UXDA Public Core across common AI coding assistant environments, distinguishing the **official stable baseline (`v0.1.0-beta.3`)** from the **active Peer Review Candidate (`v0.1.0-beta.4-rc.3`)**.

---

## 📌 Version Overview

| Release Track | Version | Git Branch / Tag | Description |
| :--- | :--- | :--- | :--- |
| **Stable Baseline** | `v0.1.0-beta.3` | `main` | Current official public release on GitHub `main`. |
| **Historical RCs** | `v0.1.0-beta.4-rc.1`<br>`v0.1.0-beta.4-rc.2` | `tag: v0.1.0-beta.4-rc.1`<br>`tag: v0.1.0-beta.4-rc.2` | Archived peer review candidates. |
| **Active RC (Peer Review)** | `v0.1.0-beta.4-rc.3` | `branch: release/beta4-rc1`<br>`tag: v0.1.0-beta.4-rc.3` | Current Release Candidate for bilingual peer trial (PR #5 unmerged). |

> **Note**: Default commands targeting `main` (such as `git clone` without branch flags or basic `npx skills add` without a tag) check out the stable `v0.1.0-beta.3` release. Follow the specific instructions below to test the Release Candidate.

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

To evaluate the exact packaged candidate with **strict overwrite protection**:

1. **Download the Release Candidate ZIP**:
   Download `ux-decision-advisor-v0.1.0-beta.4-rc.3.zip` from the [GitHub Pre-release page](https://github.com/RagnTec/User-Experience-Decision-Advisor/releases/tag/v0.1.0-beta.4-rc.3).

2. **Verify SHA-256 Checksum**:
   ```bash
   shasum -a 256 ux-decision-advisor-v0.1.0-beta.4-rc.3.zip
   # Verify that the output matches the published checksum in the Release Notes
   ```

3. **Safe Non-Destructive Extraction Script**:
   Execute the following bash sequence, which guarantees existing installations or symlinks are never overwritten:
   ```bash
   TARGET_DIR="$HOME/.agents/skills/ux-decision-advisor"
   ZIP_FILE="ux-decision-advisor-v0.1.0-beta.4-rc.3.zip"

   # 1. Strict guard: halt immediately if destination exists (folder or symlink)
   if [ -e "$TARGET_DIR" ] || [ -L "$TARGET_DIR" ]; then
     echo "❌ Error: Installation halted. Target path already exists: $TARGET_DIR" >&2
     echo "   To prevent accidental loss, please backup or remove the old installation manually." >&2
     exit 1
   fi

   # 2. Extract into isolated temporary directory first
   TMP_EXTRACT=$(mktemp -d /tmp/uxda_install_XXXXXX)
   trap 'rm -rf "$TMP_EXTRACT"' EXIT
   unzip -q "$ZIP_FILE" -d "$TMP_EXTRACT"

   # 3. Validate archive structure before touching user skills directory
   if [ ! -f "$TMP_EXTRACT/ux-decision-advisor/SKILL.md" ] || [ ! -f "$TMP_EXTRACT/ux-decision-advisor/LICENSE" ]; then
     echo "❌ Error: Archive validation failed (required files missing). Installation aborted." >&2
     exit 1
   fi

   # 4. Atomic move to final destination
   mkdir -p "$HOME/.agents/skills"
   mv "$TMP_EXTRACT/ux-decision-advisor" "$TARGET_DIR"
   echo "✅ Successfully installed UXDA to $TARGET_DIR"
   ```

4. **Discovery Link for Google Antigravity (Optional)**:
   ```bash
   ANTIGRAVITY_LINK="$HOME/.gemini/config/skills/ux-decision-advisor"
   if [ -e "$ANTIGRAVITY_LINK" ] || [ -L "$ANTIGRAVITY_LINK" ]; then
     echo "⚠️ Notice: Antigravity link already exists: $ANTIGRAVITY_LINK (preserved, not overwritten)."
   else
     mkdir -p "$HOME/.gemini/config/skills"
     ln -s "$TARGET_DIR" "$ANTIGRAVITY_LINK"
     echo "✅ Linked to Antigravity discovery: $ANTIGRAVITY_LINK"
   fi
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

### To install the Peer Review Candidate (`v0.1.0-beta.4-rc.3`):
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
npx skills add RagnTec/User-Experience-Decision-Advisor@v0.1.0-beta.4-rc.3 --skill ux-decision-advisor
```

> **Notice on CLI Overwrite Behavior**: Unlike the safe shell script in Method 1, third-party CLI tools may update in-place or overwrite files without prompting. For production environments, recommend project-local installations or Method 1.

---

## 🌐 Marketplace Synchronization Note (LobeHub, SkillHub, etc.)

- **Repository Binding**: Marketplaces like LobeHub index directly from the repository's **default branch (`main`)**.
- **Version Propagation**: While Release Candidates are being evaluated on `release/beta4-rc1` (PR #5), `main` remains locked at `v0.1.0-beta.3`. Therefore, public marketplace catalog views reflect the stable `main` version.
- **Testing RC Releases**: To test `v0.1.0-beta.4-rc.3`, use Method 1 (Direct ZIP) or Method 3 (Vercel Skills CLI with `@v0.1.0-beta.4-rc.3`).

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
   Open a new session with your AI assistant and prompt (in English or Chinese):
   > "Use your installed ux-decision-advisor skill to evaluate whether a 15% increase in feature CTR warrants immediate full rollout despite user complaints about interface friction."
   
   **Expected Behavior (Bilingual Business-First Protocol)**:
   - The agent reads `analytical-quality.md` and `evidence-boundaries.md` before substantive analysis;
   - Output automatically matches your prompt language (English for English, Chinese for Chinese);
   - The default output directly provides the **professional judgment, key evidence, underlying UX friction mechanism, and actionable next steps**;
   - Deep statistical proofs, theoretical constructs, or comprehensive business progress maps are available **on demand**, rather than forced as rigid first-screen barriers.
