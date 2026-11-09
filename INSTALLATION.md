# UXDA Installation Guide

This guide covers installing and verifying the UXDA Public Core (`v0.1.0-beta.1`) skills across common AI coding assistant environments.

---

## Prerequisites

- **Python 3.9+** (Standard library only; zero mandatory third-party pip dependencies).
- Supported Agent Harness / IDE:
  - **Google Antigravity**
  - **Gemini CLI / Google Agent SDK**
  - **Claude Code**
  - **Cursor / Open-interpreter / Custom LLM tool-calling harnesses**

*Note: UXDA consists of portable markdown skills and Python scripts. Compatibility depends on the host platform's support for standard prompt-based skill discovery and filesystem read tools.*

---

**Access note:** While the repository is Private, GitHub access is required to clone it. When it becomes Public, the same URL will work without repository membership.

## Method 1: Global Installation (Recommended)

Following the standard multi-agent convention, reusable skills should be installed globally under `~/.agents/skills/`.

```bash
# 1. Clone repository
git clone https://github.com/RagnTec/User-Experience-Decision-Assistant.git /tmp/uxda-source

# 2. Copy the two public skills to the canonical shared directory
mkdir -p ~/.agents/skills
cp -R /tmp/uxda-source/skills/ux-decision-assistant-router ~/.agents/skills/
cp -R /tmp/uxda-source/skills/evidence-based-design-review ~/.agents/skills/

# 3. Clean up source checkout
rm -rf /tmp/uxda-source
```

### Discovery Link for Google Antigravity
If you use Google Antigravity, link the canonical directory to your Antigravity config:

```bash
mkdir -p ~/.gemini/config/skills
ln -sf ~/.agents/skills/ux-decision-assistant-router ~/.gemini/config/skills/ux-decision-assistant-router
ln -sf ~/.agents/skills/evidence-based-design-review ~/.gemini/config/skills/evidence-based-design-review
```

---

## Method 2: Project-Local Installation

If your team requires pinning skills within a specific repository root:

```bash
cd /path/to/your/project
mkdir -p .agents/skills
cp -R /path/to/uxda/skills/* .agents/skills/
```
Ensure your agent harness is configured to inspect `.agents/skills/` within the active workspace.

---

## Standalone Verification (No Extension Pack Required)

UXDA is designed to work in **Public Core mode** on user-provided in-context materials without requiring any private extension manager or database.

### Verification Checklist:
1. **Self-check Script**:
   Test that the internal python validation scripts run without errors:
   ```bash
   python3 ~/.agents/skills/ux-decision-assistant-router/scripts/response_preface_check.py --help
   python3 ~/.agents/skills/evidence-based-design-review/scripts/render_report.py --help
   ```
2. **Interactive Sanity Test**:
   Open a new session with your AI assistant and prompt:
   > "Use your installed UXDA skill to outline a research plan comparing two navigation bar layouts."
   
   **Expected Behavior**:
   - The agent reads `analytical-quality.md` and `evidence-boundaries.md` before substantive analysis;
   - The first output block presents a `业务推进图` (Business Progress Map);
   - The agent operates directly on the stated problem without attempting unauthorized background directory scans.
