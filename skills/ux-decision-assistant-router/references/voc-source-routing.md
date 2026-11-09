# Optional VOC source routing | v0.4B.1

VOC is **optional decision evidence**, not a mandatory project step. Do **not** directly crawl/scrape review sites, social media, marketplaces or support systems as the default behavior of this Skill. If the user asks how to obtain data, suggest their authorized internal export, an official documented API, a licensed research provider, or a permitted external collection workflow. Explain that a third-party collection tool's own permissions and data provenance still need checking. Never propose bypassing access controls, platform limits, CAPTCHAs, login walls, or privacy protections.

## When to offer
Only if feedback evidence could plausibly alter a decision (e.g. recurring failure, expectations gap, severity, after-sales friction). Give the preliminary O/E/D conclusion first, and invite **one** relevant source rather than presenting a long list. Offer `existing VOC/export`, `authorized external collection then upload`, `continue without VOC`, and `describe a different source` as natural-language alternatives. Do not insist if the user declines.

## Data intake and provenance
When VOC arrives, ask only for essential missing collection context, preferably as a user-provided source note or private `voc_source_manifest.json`:
- `platform_or_channel`, `product_or_service_scope`, `market`, `language`, `collection_window`, `collection_method`, `query_or_inclusion_rule`, `unit_of_record`, `known_coverage_limits`, `rights_and_privacy_status`, `collection_date`.
- For crawled material additionally consider relevance ranking, missing/deleted reviews, fake/incentivized reviews, popularity bias, and platform recommendation filters; identify whether the view contains negative-only/complaint-only content.
- Keep source files and metadata private. Do not print, commit, package or send raw content to public Skill repo; prefer de-identified and minimum necessary columns. Respect copyright, privacy and platform terms.
- Each excerpt must retain a stable local source row or reference ID, not reveal the author's identity. Automated 'sentiment' is a model interpretation, not the customer's confirmed emotion; negate/sarcasm/multilingual quality require manual review.

## Analytic units & claims
Distinguish records, mentions, unique contributors (if ethically/pseudonymously supported), issues and affected tasks. Deduplicate with documented key (the same cross-post may appear on multiple channels). Never turn complaint share into incidence, public comment frequency into market prevalence, star-rating distribution into causes, or negative comments into population sampling without defensible denominators and selection process.

Outputs should include (a) themes with original row citations, (b) rival explanations and limitations, (c) precise decision link and what could reverse it. If only theme-coded feedback is available, route to V's existing `coded_feedback.csv` path. The shipped V analyzer **does not** automatically crawl sites, perform arbitrary text classification, or calculate population rates from VOC.

References to review per case: ICC/ESOMAR Social Media Research guidance; Brown et al. (2025), *Web scraping for research: Legal, ethical, institutional, and scientific considerations*, DOI 10.1177/20539517251381686. Do not treat this guide as permission to collect any particular source.
