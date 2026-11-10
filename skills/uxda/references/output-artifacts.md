# Robust presentation and optional portable deliverables

Load when presenting dense structured data, diagrams or mathematical results; when the user explicitly requests Markdown/H5; or when a meaningful research/project milestone makes a shareable deliverable useful. This file is not a requirement to offer a document in every turn.

## Presentation correctness and Markdown reliability

- **Safe range formatting**: In Markdown text, avoid raw tilde combinations like `60~70` or `2~3` which easily trigger accidental strikethrough (strikethrough syntax `~~` or parser variance). Prefer clean en-dash, hyphen, or explicit language (e.g., `60–70`, `2-3`, or "从 2 到 3").
- **Reliable structured layout**: Choose the least complex form that preserves data-to-label associations: ordinary prose, clean Markdown table, or grouped cards.
  - Never fake columns with spaces, tabs, or monospaced arrow alignment in code fences.
  - Do not use wide character / monospace alignment art as default process visualization. Mermaid is acceptable only where supported, and must be accompanied by a readable text/list fallback.
  - Verify that labels, field names, and data values remain aligned across desktop and mobile viewing contexts.
- **Table readability**: For wide tables prefer shorter columns or stacked cards. For generated HTML use responsive viewport/layout, readable type, semantic headings/tables, meaningful alternatives, keyboard accessibility and checks for overflow at narrow widths.
- **Deliverable self-explanatory capability**:
  - Independent deliverables (such as Markdown summaries, standalone HTML reports, executive memos, or handover cards) must possess contextual self-explanation for substantial content.
  - Substantive metrics, models, or acronyms that directly impact stakeholder comprehension, methodological reproducibility, or decision-making must include necessary operational definitions, parameters, and task context within the document itself, rather than forcing readers to cross-reference conversational history. Avoid mechanical glossaries that unpack every common abbreviation without analytical purpose.
  - **Standalone verification**: Independent deliverables must re-verify their evidence chain; do not uncritically carry over unverified inferences or exploratory assumptions from earlier conversation turns into the final deliverable as confirmed facts.
- **Epistemic fidelity**: Preserve numerator/denominator, evidence status, citations, constraints and differences between observed result and unconfirmed candidate plan. Attractive visuals never strengthen weak evidence.

## Portable outputs

- At an actual checkpoint, a **single brief optional** suggestion of `.md` for editable review or a self-contained `.html` for cross-device presentation is appropriate. Continue project work without waiting for user selection. Do not repeat an identical offer every turn.
- If explicitly asked for an artifact, generate the real file when the host has the necessary tools; verify file existence and basic correctness. Where available render-test representative desktop/mobile viewports, otherwise state clearly that only static checks were possible.
- Separate `created locally`, `shared internally`, and `published externally`. No share, upload, repository push, or public publishing occurs without its own authorization.
- Avoid external scripts, trackers, private fonts, and remote dependencies for standalone offline HTML where practical; escaping/sanitization is required when user data appear in HTML.
