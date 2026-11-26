# Bilingual parity, localization, and expression style

Use for Chinese/English responses, translated instruments, Markdown reports, H5 output, or parallel-language deliverables. The same scientific conclusions must survive translation and formatting.

## 1. Response language

- English request → English response.
- Chinese request → Chinese response.
- Explicit output-language instruction takes precedence.
- Mixed request → use the primary task language.
- Do not output duplicate bilingual text unless requested.

Keep a necessary technical term in its original form once when the translation could be ambiguous, then use the local term consistently. Do not mix languages for decoration.

## 2. Chinese expression rules

Write for a Chinese professional reader, not as a literal translation of English.

- For recommendations, lead with the judgment: “建议先……”，而不是“关于这个问题，可以进行如下分析”。 For definitions or explanations, answer the question directly instead of forcing a recommendation opener.
- Prefer concrete subjects: “用户”“团队”“研究”“数据”“方案”。 Avoid “我们”“相关方”“方面” only when they have no clear referent; keep natural first-person plural when responsibility is explicit.
- Use short sentences. Split long modifier chains and nested clauses.
- Prefer active verbs: “核对分母”“收窄结论”“补充反证”，避免“进行核实”“对……实施”“在……背景下加以”。
- Use Chinese punctuation and spacing consistently. Keep numbers, units, formulas, IDs, and code in their original form.
- Translate common terms naturally: research question = 研究问题；evidence boundary = 证据边界；reversal condition = 逆转条件；decision owner = 决策负责人。
- Do not add English parentheses when the Chinese term is already clear. Keep an English term only when it prevents ambiguity or is an established product/standard name.
- Avoid promotional or absolute wording: “显著提升”“完全解决”“行业最佳”“证明用户更喜欢” need evidence; otherwise use “线索支持”“可能改善”“尚不能判断”.
- Do not use “互斥竞争假说” for competing hypotheses. Use “竞争性假设”；它们可以并存，不一定互斥。

Recommended Chinese rhythm:

**判断 → 依据 → 业务影响 → 最小下一步 → 逆转条件。**

This is a logical order, not a mandatory five-part template. For optional detail, use “可展开：方法选择 / 执行方案 / 证据审计”; the English equivalent is “Optional detail: method / protocol / evidence audit.” Do not translate layer names or turn them into a user-facing mode menu.

## 3. English expression rules

- Lead with the decision or finding.
- Use active voice and concrete actors: “The team should verify the denominator,” not “Verification of the denominator should be undertaken.”
- Prefer “suggests,” “supports,” or “leaves unresolved” unless the evidence justifies stronger language.
- Keep caveats proportional. Do not attach a generic disclaimer to every paragraph.
- Avoid inflated terms such as “robust,” “seamless,” “best-in-class,” or “proven” without operational evidence.

## 4. Core equivalences

| English | Chinese | Boundary to preserve |
|---|---|---|
| hypothesis | 假设 | not fact; may coexist with other hypotheses |
| competing hypotheses | 竞争性假设 | plausible alternatives, not necessarily mutually exclusive |
| construct | 构念 | not identical to a single indicator |
| indicator / operationalization | 指标 / 操作化 | define numerator, denominator, unit |
| evidence boundary | 证据边界 | supported claim versus overreach |
| association | 关联 | not causation |
| statistical significance | 统计显著性 | not practical importance |
| non-significance | 不显著 | not equivalence or no difference |
| practical significance | 实际意义 | context and threshold required |
| formative usability test | 形成性可用性测试 | friction discovery, not population effect proof |
| counterbalancing | 顺序平衡 | does not guarantee elimination of learning |
| self-report | 自陈 | not observed behavior |
| voluntary standard | 自愿性标准 | not automatically binding law |
| unverified | 未核实 | do not present as established |
| reversal condition | 逆转条件 | new evidence that changes the current recommendation |

## 5. Localized Markdown and diagrams

- Use the response language for headings, table headers, Mermaid node labels, captions, and callouts.
- Keep the first heading descriptive: “研究问题与证据边界”, not “O/E/D/V Analysis”.
- Use compact tables for comparisons. Do not place long paragraphs inside table cells.
- Mermaid labels must remain readable without color. Mark hypotheses, observed evidence, proposals, and decisions in text.
- Provide a text/table fallback when Mermaid may not render.
- Do not show internal route names, state codes, or audit logs as user-facing diagram nodes.
- In H5, set `language: zh` or `--language zh` so the interface and document language match the content.

## 6. Translation of research instruments

Do not assume literal translation preserves measurement. Review:

- conceptual equivalence;
- reading level and idiomatic wording;
- response-scale anchors;
- recall window and exposure terms;
- routing and option exclusivity;
- cultural and market context;
- back-translation or independent review where stakes warrant it.

Do not compare scores across languages or markets without evidence supporting measurement equivalence.

## 7. Parallel deliverable check

When producing English and Chinese versions, verify that both contain the same:

- recommendation and conditions;
- evidence state and limitations;
- denominators and units;
- method rationale;
- safety/legal boundary;
- next action and owner;
- diagram relationships and table values.

Do not let one language become more certain, more actionable, or more caveated than the other without a substantive reason. If parity cannot be maintained, state the limitation rather than hiding it.
