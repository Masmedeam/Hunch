# Historical benchmark — resume checkpoint

Updated: **2026-10-25T18:52:11.167180Z**. Directory: `/Users/salim/Hack/nextday-prediction`.

## User objective and authorization

Create a retrospective forecasting dataset: seven days of news/social context, a hidden next 24 hours, common questions for comparing models, then blinded model judging plus objective outcome scores.

- User explicitly approved **$10 maximum for scraping only**. Model inference/judging has a separate budget, but **no evaluation or judge calls have been made during this phase**.
- Preserve the earlier collection/predictions. `.env` contains local Glasser and Gemini credentials; do not print or copy them into prompts/checkpoints.
- Benchmark approval: `data/benchmarks/retrospective-v0/private_raw/approval.json`. The earlier `data/approval.json` remains the old separate $1 allowance.

## Progress snapshot

- **357 terminal Glasser Runs; $1.78072 charged so far** for this benchmark scrape.
- $4.33222 is the sum of inspected maximum reservations for currently materialized batches, **not actual spend**. Remaining planned pagination may add small reservations, within the root $10 cap.
- Parsed raw records (duplicates/out-of-window items still included): {'price_bar': 125, 'filing': 29096, 'social_post': 1560, 'article': 1700, 'filing_document': 9}.
- Raw social platform counts: {'x': 1410, 'tiktok': 60, 'youtube': 90}. Quarantined during basic parsing: 0.
- Built 10 cases / 50 questions. Resolution statuses: {'resolved': 20, 'resolved_search_relative': 10, 'reference_ready': 20}. Check report timestamp against current raw batches before treating it as final.

| Batch | Planned calls | Current states | Recorded charge |
| --- | ---: | --- | ---: |
| audit | 8 | COMPLETED: 8 | $0.05936 |
| cik-verify | 1 | COMPLETED: 1 | $0.0005 |
| core | 90 | COMPLETED: 90 | $0.44736 |
| filing-documents | 9 | COMPLETED: 9 | $0.0045 |
| news | 100 | COMPLETED: 100 | $0.700 |
| pagination-01 | 54 | COMPLETED: 54 | $0.06174 |
| pagination-02 | 27 | COMPLETED: 27 | $0.03126 |
| regional | 68 | COMPLETED: 68 | $0.476 |

**This is a point-in-time checkpoint.** Refresh it with the status-only command below. Last recorded worker status: `completed; 10 case packs and hidden resolutions built and verified`.

## Frozen protocol

- Protocol: `data/benchmarks/retrospective-v0/protocol.json`.
- Ten cutoff dates: **14–23 October 2026 UTC**. Each case's target is the following UTC calendar day.
- Context dates across the collection: **8–24 October 2026** (extra preceding SEC day for Eastern/UTC boundaries).
- Five shared questions per case, **50 planned questions**:
  1. Market direction for a predetermined ticker; weekend fallback is a registry count control.
  2. An original 8-K acceptance in a fixed ten-company CIK cohort.
  3. NASA X publication count under the frozen retrieval protocol (experimental/search-relative, not complete platform truth).
  4. Up to three next-day world developments (held-out news references; judge/semantic review needed).
  5. Up to three next-day social publication/topic developments (not historical views/comments gained).
- Dates/cohorts/templates were frozen before bulk retrieval. Acquisition amendments document date-boundary fixes and uniform regional coverage; question templates did not change.

## Sources and integrity decisions

- Exa daily news bodies: six global subject panels plus uniform Japan/Japanese, India/English, Brazil/Portuguese and Middle East/Arabic supplements.
- Financial Datasets daily OHLCV plus company CIK verification. Do not expose current company financial metrics.
- SEC daily acceptance logs, fixed-cohort filing search and original archived filing/exhibit documents.
- X: fixed NASA/WHO/BBCWorld accounts, buffered date queries with strict local UTC filtering and bounded pagination.
- TikTok: fixed bbcnews/dwnews profile publication records, sorted latest rather than today's popularity.
- YouTube: fixed NASA/BBCNews video publication records. Prefer exact `publishDate`; relative estimates alone are quarantined or need details.
- **All current social views, likes, comments, followers and statistics are omitted from historical inputs.**
- X returned out-of-range posts in the audit; enforce actual timestamps, never trust the query filter alone.
- SEC daily logs omitted CIK/company fields; use a separate verified cohort search. Never derive issuer CIK from accession prefixes.
- News/post text is a **reconstructed current version**, not necessarily the original as-of text. Detectable later updates/live blogs are excluded, but latent training contamination and undetectable edits remain limitations.

## Active worker context

Two workers were launched earlier:

- Historical pagination worker: bounded rounds `pagination-01` through `pagination-12`, then any missing exact YouTube publication-date details. Original harness shell ID: `sh_1744357d1001WTrZQxdOam06SL`.
- Regional supplement collector: `regional`, 68 calls. Original harness shell ID: `sh_1744815700013u3jW7f9f8sMxJ`.

Check their completion notifications/logs before launching a second resume worker. Do not start duplicate collectors or use new batch names to retry. Existing batch manifests hold persisted idempotency keys and final/pending Run IDs.

Recorded handoff notes: Benchmark scrape and dataset build completed at $1.78072 across 357 Glasser Runs (under $10 cap). All 10 cases and 50 questions are built and verified (20 resolved, 10 resolved_search_relative, 20 reference_ready, 0 unresolved).

Known pagination blocker: a YouTube continuation token returned by the provider exceeded Glasser's inspected 2,048-character input limit. Do **not** truncate opaque tokens. The original rejected `pagination-02.json` plan is preserved; `pagination-02-compatible.json` quarantines the unsupported token and retains the other valid continuation jobs. The rejected batch admitted no Runs. The resume script prefers the compatible plan, reuses accepted batch names/keys, and keeps that YouTube tail marked incomplete.

## Exact resume commands

Run from the project root; `.venv` is already installed.

```sh
# Local status only: update this file without API calls
.venv/bin/python scripts/benchmark_resume.py

# After prior workers have finished or been explicitly stopped:
# resume frozen acquisition plans with existing keys, bounded pagination,
# then build the dataset. This CAN spend the remaining scraping allowance.
.venv/bin/python scripts/benchmark_resume.py --execute

# Offline validation/build only, once acquisition is finished
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/nextday benchmark-build --root data/benchmarks/retrospective-v0
```

The resume script does **not** run model forecasts or judging. Unknown outcomes remain unresolved. Completed batches replay locally/skip; ambiguous network submissions reuse their saved idempotency key.

## Expected final artifacts

- `data/benchmarks/retrospective-v0/public_inputs/<case_id>/history.json`: complete allowlisted pre-cutoff history.
- `data/benchmarks/retrospective-v0/public_inputs/<case_id>/history.compact.json`: deterministic common profile, up to 200 records and 1,500 text characters per item; full data retained.
- `data/benchmarks/retrospective-v0/public_inputs/<case_id>/questions.json`: common frozen questions/rules, no labels.
- `data/benchmarks/retrospective-v0/private_outcomes/<case_id>/resolution.json`: hidden labels and next-day reference evidence.
- `data/benchmarks/retrospective-v0/private_outcomes/source_audit.json`: private raw provenance.
- `data/benchmarks/retrospective-v0/integrity_report.json`: spending, coverage, unresolved rates and leakage-check status.
- `data/benchmarks/retrospective-v0/private_raw/`: frozen plans, contracts, Run manifests, raw results and collector logs.

**Evaluate each case in a fresh stateless model call. Never combine all histories in one prompt:** a later case's history can contain an earlier case's hidden next day. `load_public_case()` reads only explicit public files for one case and never loads private outcomes.

## Code added / unfinished verification

- `nextday/benchmark.py`: protocol freeze, acquisition plans, continuations, allowlisted parsers, common-question/case builder, compact profile, leakage audits and safe public loader.
- `scripts/benchmark_resume.py`: reproducible resume/status entry point.
- `nextday/checkpoint.py`: this local checkpoint generator.
- `tests/test_benchmark.py`: boundary, engagement stripping, hidden-answer isolation, verified-CIK and outcome-independent-question tests.
- CLI: `benchmark-plan`, `benchmark-build`.
- **40 tests passed** including filing-document/compact-profile and cursor-compatibility checks; re-run the suite before the final build.

Next tasks: finish existing scraping workers; validate original filing bodies and pagination completeness; build/audit all case packs; inspect unresolved/low-entropy questions and news leakage flags; write the final data summary. Only then implement/run the separate retrospective multi-model runner and blinded judge. Keep objective, search-relative and narrative scores separate.
