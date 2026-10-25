# NEXTDAY // Temporal Evidence & Next-Day Forecasting Observatory

A data-first probabilistic forecasting and multi-model benchmarking pipeline powered by **Glasser** (multi-vertical evidence ingestion) and **Gemini 4 Argon (`gemini-4-argon`)** (forecasting engine and blinded judge), paired with a Cloudflare Workers web observatory.

- **Live Observatory UI:** **[https://nextday-prediction.hidden-pond-5e6a.workers.dev](https://nextday-prediction.hidden-pond-5e6a.workers.dev)**
- **Detailed Reports:** [COLLECTION.md](COLLECTION.md) · [PREDICTION.md](PREDICTION.md) · [BENCHMARK.md](BENCHMARK.md) · [BENCHMARK_PROGRESS.md](BENCHMARK_PROGRESS.md)

---

## Core Architecture

`nextday` separates **evidence acquisition**, **temporal quarantine**, **forecast generation**, and **evaluation** into auditable stages:

1. **Multi-Vertical Evidence Ingestion (`nextday/collector.py`, `nextday/plans.py`):**
   - Validates every job against its inspected Glasser endpoint contract (`data/contracts/*.json`) and reserves worst-case charges (including empty/error fee clauses) *before* any paid call.
   - Persists UUID idempotency keys to `manifest.json` prior to submission so transport retries never double-charge.
   - Supports **5 configurable data verticals**:
     - **News & Social Attention:** Date-bounded Exa news bodies, Serper news, X trends & search (`tikhub`), TikTok trending feeds, keyword searches & hashtag curves (`scrapecreators`, `tikhub`), and YouTube weekly searches & Shorts (`scrapecreators`).
     - **Equities & SEC Filings:** Daily OHLCV price bars and company facts (`financialdatasets`), SEC EDGAR daily acceptance logs, fixed-cohort 8-K searches, and full archive filing documents (`secapi`).
     - **Zillow (Real Estate & Mortgages):** National mortgage rates (`zillow:/get_mortgage_rates`), property details & Zestimates (`brightdata:/datasets/v3/zillow-properties`), open houses (`zillow:/get_open_houses`), and metro agent directories (`zillow:/search_agents`).
     - **Airbnb (Hospitality & Short-Term Stays):** Forward booking window pricing and supply snapshots across global cities (`apify:/tri_angle/airbnb-scraper`).
     - **LinkedIn (Job Market & Hiring Velocity):** Active job searches by role/city (`apify:/harvestapi/linkedin-job-search`), company headcount & profiles (`scrapecreators:/v1/linkedin/company`), hiring discourse (`scrapecreators:/v1/linkedin/search/posts`), and startup job trends (`wellfound:/get_trending_jobs`).

2. **Temporal Quarantine & Provenance (`nextday/normalize.py`, `nextday/benchmark.py`):**
   - **Capture time $\neq$ publication time:** Historical backfills preserve both `event_at` and actual `retrieved_at`.
   - **Zero current social counters in retrospective history:** `FORBIDDEN_HISTORY_KEYS` strips `views`, `likes`, `comments`, `followers`, and `statistics` from historical case inputs so today's viral counters never leak into past context.
   - **Post-cutoff edit exclusion:** Automatically quarantines mutable live blogs and articles carrying `modifiedDate` / inline `Updated:` timestamps at or after the cutoff wall $T_0$.
   - **Strict directory isolation:** Forecasters read only `public_inputs/<case_id>/` via `load_public_case()`. Next-day outcomes and reference corpora remain sealed in `private_outcomes/<case_id>/resolution.json`.

3. **Probabilistic Forecasting & Blinded Judging (`nextday/prediction.py`, `nextday/gemini.py`):**
   - Uses a provider-neutral JSON contract (`config/forecast-schema.json`) supporting binary probabilities, numeric point estimates with prediction intervals, and mutually exclusive categorical distributions, plus explicit abstentions and disconfirmation signals.
   - Two-phase execution (`countTokens` + budget check $\rightarrow$ `--execute`) with no automatic paid retries.

---

## Repository Structure

```text
.
├── config/
│   ├── coverage.json          # Regions, multilingual topics, and Zillow/Airbnb/LinkedIn verticals
│   ├── benchmark-plan.json    # Frozen 10-cutoff retrospective benchmark protocol & policies
│   └── forecast-schema.json   # Model-neutral JSON schema for next-day forecasts
├── nextday/
│   ├── cli.py                 # CLI entry point (`nextday`)
│   ├── client.py              # HTTPS-only Glasser client (no redirect credential forwarding)
│   ├── collector.py           # Idempotent batch runner & worst-case budget reservation guard
│   ├── plans.py               # Discovery, vertical, and fixed-cohort refresh plan builders
│   ├── normalize.py           # Provider adapters, exact-counter growth deltas & SQLite/JSONL export
│   ├── gemini.py              # Direct Gemini API client (`gemini-4-argon`)
│   ├── prediction.py          # Stratified evidence sampler, schema validator & forecast runner
│   ├── benchmark.py           # Historical case builder, leakage auditor & isolated public loader
│   └── checkpoint.py          # Credential-free status checkpoint generator
├── scripts/
│   ├── benchmark_resume.py    # Resumable historical scrape & dataset builder
│   └── export_ui_data.py      # Compiles credential-free data bundles for the Cloudflare UI
├── ui/
│   ├── worker.js              # Cloudflare Worker Edge API (/api/plan-simulator, /api/validate-forecast)
│   └── public/                # Static Observatory SPA (index.html, styles.css, app.js, data/)
├── tests/                     # 42 unit tests covering budgets, normalization, leakage & forecasts
├── wrangler.jsonc             # Cloudflare Workers configuration
└── pyproject.toml             # Python package definition (`nextday-data`)
```

---

## Quickstart

### 1. Python Environment & Credentials

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
```

Create a local `.env` file (excluded from Git):

```ini
GLASSER_API_KEY=your_glasser_key
GEMINI_API_KEY=your_gemini_key
```

Run the offline unit test suite (42 tests):

```sh
.venv/bin/python -m unittest discover -s tests -v
```

### 2. Prospective Discovery & Next-Day Prediction

```sh
# 1. Free authentication & catalog download
.venv/bin/nextday catalog

# 2. Generate a frozen discovery plan (optionally including Zillow, Airbnb, LinkedIn verticals)
.venv/bin/nextday plan --verticals zillow airbnb linkedin --output data/discovery-plan.json

# 3. Free preflight: inspect contracts, validate schemas, and reserve worst-case prices
.venv/bin/nextday collect --plan data/discovery-plan.json --batch discovery --budget 1.00

# 4. Paid execution & offline normalization
.venv/bin/nextday collect --plan data/discovery-plan.json --batch discovery --budget 1.00 --execute
.venv/bin/nextday normalize

# 5. Prepare & execute a Gemini 4 Argon next-day forecast
.venv/bin/nextday predict --name experiment-01 --limit 64 --forecasts 5 --budget 0.30
.venv/bin/nextday predict --name experiment-01 --limit 64 --forecasts 5 --budget 0.30 --execute
```

### 3. Retrospective Benchmark (`retrospective-v0`)

The v0 retrospective benchmark covers **10 daily cutoffs (`2026-10-14` to `2026-10-23` UTC)** and **50 shared questions** across 5 tracks (Market Direction / Registry Count, Corporate 8-K Events, NASA X Publication Count, World Developments, and Social Cohort Developments), collected across 357 Glasser Runs ($1.78072 total spend):

```sh
# Refresh local checkpoint status (offline, no API calls)
.venv/bin/python scripts/benchmark_resume.py

# Rebuild isolated public_inputs/<case_id>/ and private_outcomes/<case_id>/ offline
.venv/bin/nextday benchmark-build --root data/benchmarks/retrospective-v0
```

### 4. Cloudflare Workers Observatory UI

```sh
# Export credential-free JSON bundle from local data into ui/public/data/
.venv/bin/python scripts/export_ui_data.py

# Preview locally or deploy to Cloudflare Workers
wrangler dev
wrangler deploy
```

---

## Safety & Data Hygiene Guarantees

- **No silent paid calls:** Search, contract inspection, and plan generation are free; paid Glasser Runs and Gemini generations require `--execute`.
- **Untrusted evidence boundary:** Scraped articles, social captions, and job descriptions are treated strictly as untrusted data, never instructions.
- **No fabricated metrics:** Missing counters remain `null` (never `0`); rounded display labels (e.g., `31K`) are excluded from exact-counter growth math; incomplete outcome coverage resolves to `unresolved` rather than `NO`.
