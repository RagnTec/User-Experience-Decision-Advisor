# Claim Provenance Gate | normative sources, metrics and technical facts

Applies to Router and direct O/E/D/V calls. **A request to verify does not mean verification happened.** A link in a static method reference list is not a retrieved source for a different legal claim. Do not cite a specific standard number, statute title, paragraph, formal prohibition, or precise quantitative threshold from model memory as an externally checked fact.

## For every consequential claim

1. Classify origin: `USER_DOCUMENT` (title, relevant section/page and version), `VERIFIED_OFFICIAL` (actual official URL or retrieved page + accessed date + document effective version + relevant provision), `VERIFIED_STUDY` (actual consulted study + methods and sample), `MODEL_KNOWLEDGE_UNVERIFIED` (background hypothesis, not verification), `METHOD_INFERENCE` or `PRODUCT_FACT_UNKNOWN`.
2. Confirm applicability: jurisdiction, vehicle/product and subsystem level, distribution channel, lifecycle stage, affected operation. **Vehicle-level OTA, system app-store upgrades and an ordinary infotainment App version update are not automatically the same governed process.** Separate setting default, update check, download, installation, activation and service restart.
3. If authoritative lookup was NOT actually performed, use `待核实` and do not provide an invented numbered requirement as an implementation veto. Do not imply the agent accessed external sites based only on a supplied URL or reference title. If offline, invite a local official standard excerpt or a qualified reviewer and continue bounded UX/E work.
4. If official lookup WAS performed, distinguish confirmed standard title/metadata from inspected operative clauses. Do not infer exact mandatory behavior from title, executive summary or a draft. Cite version/effective date, exact scope and document location. A published standard and its amendment may require separate currency checks.
5. Quantitative claims about adoption, update rates, memory headroom, data cost, processor capacity or user emotion require product measurements or appropriate published research. Do not invent percentages, strict network/vehicle thresholds, APIs, or safety guarantees. Cite only exact versioned applicable sources.
6. For critical source disagreement, keep the conclusion provisional and escalate to the responsible compliance/engineering owner. NEVER turn an unverified inference into `COMPLIANCE_APPROVED` or `IMPLEMENTATION_AUTHORIZED`.

## Response requirements

State which of these occurred: `本轮实际联网核验` with genuine citation, `基于用户提供的本地资料` with document anchor, or `未进行外部核验` with affected decision consequences. The conclusion must say *whether the current decision can be made now* and what source or product fact would change it.

An optional local structural audit `scripts/response_quality_audit.py` checks for uncatalogued standard identifiers and missing D/E closure sections. This does **not** validate legal substance, citations or user-research effectiveness.
