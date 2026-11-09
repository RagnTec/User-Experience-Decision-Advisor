# Security & Privacy Policy

UXDA Public Core is architected to minimize operational dependencies and maintain clear data boundaries.

---

## 1. Scope Distinction: UXDA Skills vs. Host Agent Platforms

To accurately evaluate the privacy and security profile of your deployment, it is vital to distinguish the **UXDA Skill Package** from the **Host Agent Platform**:

| Dimension | UXDA Skill Package (This Repository) | Host Agent Platform (e.g., Antigravity, Claude, Gemini CLI, Cursor) |
| :--- | :--- | :--- |
| **Network Transmission** | **Zero Network Calls**: UXDA contains only local markdown files and Python standard library scripts. It does not initiate HTTP requests, phoning-home, or third-party telemetry. | **Host Dependent**: The host agent platform transmits prompts and tool outputs over the network to LLM API endpoints according to that platform's terms and privacy policies. |
| **Session & Context Persistence** | **Stateless Skills**: UXDA skills do not maintain persistent databases or hidden local cache files. | **Host Dependent**: Session memory, context caching, and multi-turn message history are stored and managed by the host platform. |
| **File Access Execution** | **Confined Scripts**: UXDA verification scripts inspect only files passed via standard command-line flags. | **Host Dependent**: Tool permissions (e.g., `read_file`, `run_command`) and sandbox restrictions are enforced by the host runtime environment. |

---

## 2. Public Core Privacy & Boundary Principles

1. **No Proprietary Data in Public Distribution**:
   - The UXDA Public Core repository contains no enterprise-specific rules, internal project registries, or confidential research telemetry.
2. **No Unconstrained Filesystem Scavenging**:
   - UXDA guidelines explicitly instruct agents to analyze only user-provided in-context documents or explicitly bound inputs.
   - Agents are prohibited from performing unprompted directory discovery (such as scanning unlinked raw storage paths) to invent missing context.
3. **Transparent Uncertainty**:
   - Unknown technical parameters and unverified standards are explicitly labeled as `[NOT VERIFIED]` rather than hallucinated or borrowed from external domains.

---

## 3. Supported Versions

Security and boundary updates are provided for active beta versions:

| Version | Supported | Notes |
| :--- | :--- | :--- |
| `0.5.4-beta.1` | :white_check_mark: | Current Public Beta Candidate |
| `< 0.5.0` | :x: | Deprecated developmental prototypes |

---

## 4. Reporting a Vulnerability or Boundary Failure

If you observe an instruction bypass, an unintended information leak, or a security issue in UXDA's scripts or prompt structures:

1. **Do not open a public GitHub Issue.**
2. Submit a confidential advisory through GitHub's Private Vulnerability Reporting feature or email the maintainers directly.
3. Please provide:
   - Host platform and environment versions;
   - Full prompt and tool-invocation sequence;
   - The observed behavior and the expected isolation boundary.

We acknowledge receipt within 48 hours and coordinate a public release fix.
