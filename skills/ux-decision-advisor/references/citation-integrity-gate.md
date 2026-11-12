# Citation Integrity Gate | v0.4D.9 (ALL O/E/D/V outputs)

**No source fabrication, dead citations or empty references.** A URL is a locator, NOT proof that the page loaded, was read, is the named document, or supports the claim. This gate covers conversation replies, private Markdown/H5 reports, decision records, user-provided local knowledge, methodology teaching, technical standards and legal/regulatory claims. It applies to direct professional Skill calls as well as Router calls.

## Minimal research-grade reference

Every consequential externally sourced statement must let a reviewer recover the **exact supporting material**:

- **Academic literature:** real authors, full title, year, journal/book/conference or publisher, DOI or authentic publisher/permalink URL, relevant page/section or identifiable abstract, and what the reviewed content actually supports. DOI validity does not prove that full text was accessed. Don't invent DOI, article metadata, sample size or effect size; abstracts support only abstract-level claims.
- **Web pages / official product docs:** page title, issuing organization, direct canonical HTTPS URL, access date, relevant heading/paragraph, page reachability and the precise claim supported. Homepages/search result snippets alone do not establish product features or technical details. A screenshot, retrieval record or accessible excerpt should permit review.
- **Law, policy, platform rules, standards:** correct issuer, title, number if independently confirmed, jurisdiction, version/effective date, **specific operative article/clause and applicability to this product and operation**, official link or exact location in user-provided authorized text. Official title/summary can support metadata, NOT unseen binding provisions. No broad legal prohibition from an unrelated sector standard.
- **User/local/private documents:** title, file version/date, section/page/row/line, source ID and private file hash or user-upload reference. Citation is private-safe: do not publish filesystem paths, raw VOC or proprietary fragments into GitHub or public search queries. Supplied company rules are NOT automatically current law or confirmed technical reality.
- **Computed numbers:** exact input dataset/version, units, analysis method/formula, filter, denominator, missingness and executable reproduction; do not invent external source for deterministic calculations. **Expert mechanism / analogy / hypotheses** are labeled as professional inference and must not masquerade as cited empirical findings.

## Three hard gates before making a claim

1. **IDENTITY:** source actually exists, bibliographic metadata matches the accessed item; URL is a direct document/page or honest DOI reference, not placeholder/homepage/redirect to unrelated content.
2. **ACCESS & CONTENT:** a real retrieval/check occurred this turn or a previously archived authorized original can be located. Page is not 404, blank, robot challenge or access-denied. PDF/paywall/blocked pages are `NOT_CONTENT_VERIFIED` unless the relevant page was truly inspected in an authorized local copy. Confirm quoted/referenced passage exists. Web links may change; record check time and destination.
3. **SUPPORT & APPLICABILITY:** quoted paragraph actually supports the exact level of conclusion; check geographic/market/version/product applicability, method/sample limitations and independent contradiction where consequential. One article may support a **general mechanism** while not supporting a *specific product's risk rate*, regulatory mandate or implementation threshold.

## Decision and interaction behavior

- **No verifiable source?** DO NOT fill the gap with an invented title, URL, DOI, clause, statistic or user quotation. State `未核实`, omit the particular external claim or make the judgment explicitly conditional; still provide valid UX reasoning and the smallest source needed to decide. Do not fabricate an 'alternative link'.
- **Offline:** source may be user's local document with exact anchor and hash, or general methodology/inference as such. Do not claim the latest public rule, current market or checked web page. Later user-provided files or authorized browsing can upgrade only the affected claim.
- **Online:** use actual host browser/search tools; record inspected page or publication ID, exact URL, access date and matching passage. Distinguish unavailable/limited/full text. Check independently where the claim materially changes the decision. No automatic broad crawling. Link is not 'verified' because it is in an installed reference list.
- **Teaching track:** illustrative questions, examples and explanations must be distinguished from consulted real publications; do not use synthesized sources as educational citations.
- **Output:** keep the main executive summary readable; evidence details may be collapsed but must exist and be accessible. Strong conclusions cannot depend entirely on hidden `未核实` entries. For formal private files use explicit `[SRC:S01]` markers and claim ledger; chat with host-native citations may use actual host citations instead. Never display raw private file paths publicly.

## Offline tooling, limitations and release boundary

- `scripts/citation_integrity.py --report /private/report.md --ledger /private/ledger.json --private-root /private` performs strict **offline structural and local-file** checks, including source IDs, document hash/line anchoring, metadata, placeholder URLs, references and decision strength. It never accesses the network and cannot independently authenticate an Agent's alleged browser trace or determine whether a legal/empirical claim is true.
- Online link and source text verification relies on host-native search/browsing tools under explicit user authorization. UXDA Public Core scripts run strictly offline and do not initiate outbound network requests. Unverified or unreachable sources remain unverified.
- For authoritative claims, human/host-run review of retrieval trace, actual operative clause, study findings, changing versions and contradictions remains mandatory. Place claim ledger/snapshots/actual reports only in authorized private project folders; public source tree contains generic code/tests only.

**Fail closed on invalid references, not on legitimate offline UX analysis.** User review and manual correction may change claims but never manufacture source access or approval.
