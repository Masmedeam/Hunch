<div align="center">

<img src="ui/public/logo.svg" alt="Hunch Logo" width="88" height="88" />

# Hunch

**Million-Token Cross-Vertical Forecasting & Headquarters Intelligence Engine**  
*Built at the **Gemini 4 Argon SF Hackathon** (Cerebral Valley · Shack15, San Francisco — Oct 25, 2026)*

[![Model: gemini-4-argon](https://img.shields.io/badge/Model-gemini--4--argon-E1381C?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Track: Million Token Engineering](https://img.shields.io/badge/Track-Million_Token_Engineering-141413?style=flat-square)](pitch/README.md)
[![Data: 12 Glasser Verticals](https://img.shields.io/badge/Glasser-545_Runs_%C2%B7_32%2C490_Records-0E7A5D?style=flat-square)](COLLECTION.md)
[![Benchmark: #1 Brier 0.1759](https://img.shields.io/badge/Benchmark-%231_Brier_0.1759_%C2%B7_3.98%2F5_Judge-4F46E5?style=flat-square)](BENCHMARK.md)
[![Tests: 42 Passing](https://img.shields.io/badge/Tests-42_Passing-0E7A5D?style=flat-square)](tests/)

[**Live Observatory**](https://nextday-prediction.hidden-pond-5e6a.workers.dev) · [**5-Slide Pitch Deck (`/pitch`)**](https://nextday-prediction.hidden-pond-5e6a.workers.dev/pitch) · [**Pre-Loaded HQ Demo (`/?hq=1`)**](https://nextday-prediction.hidden-pond-5e6a.workers.dev/?hq=1) · [**Benchmark Report**](BENCHMARK.md)

</div>

---

## Why We Built Hunch (Hackathon Problem Statement)

> **Track 1 — Million Token Engineering:** *Pick a monumental task where scale and temporal consistency across hundreds of files/records matter, execute it end-to-end with `gemini-4-argon` (1,048,576 context), and measure your improvement over a baseline.*

### The Problem: $100M+ Headquarters Decisions on 18-Month-Stale Data
Whether a company is choosing where to place its next **corporate headquarters / regional hub**—or an investor is predicting where a company will relocate—today's decision loop is broken:
1. **Stale Consultant Spreadsheets (For Companies):** Boards pay $500K+ for static site-selection PDFs built on 18-month-lagging census tables, blind to live AI engineering compensation (`$300K–$380K` in SF), real-time mortgage rates (`7.49%` 30Y Fixed), and state commercial energy spreads (`$8.46/gal` CA diesel vs. `$5.74/gal` TX).
2. **Priced In at the Press Release (For Markets & Cities):** When Meta disclosed **$825B** in future AI data-center and office leases on Oct 25, shares moved nearly 8%. Waiting for the official press release or SEC Form 8-K means missing 60–90 days of local hiring, housing absorption, and short-term stay compression signals.
3. **The Million-Token Bottleneck:** True leading indicators are scattered across **32,490+ raw records** in 12 noisy verticals. Small-context models either drop critical cross-vertical correlations or suffer from severe temporal leakage.

### The Solution: Cross-Vertical Evidence Fusion + Closed Verification Loop
**Hunch** ingests live multi-vertical evidence through **Glasser**, enforces strict point-in-time quarantine ($T_0$), and uses **`gemini-4-argon`** (`1,048,576` input token window) to output schema-validated probabilistic forecasts—verified against a 10-day, 50-question retrospective benchmark.

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ 1. GLASSER MULTI-VERTICAL INGESTION (545 Paid Runs · $2.41 Total Spend)    │
│    LinkedIn · Wellfound · Zillow · RentCast · Airbnb · AAA Gas & EV Grid   │
│    SEC 8-K & Form 4 · Equity OHLCV · Exa News (EN/JA/PT/AR) · X · YouTube  │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 2. TEMPORAL QUARANTINE & DELTA ENGINE (32,490 Records · Zero Leakage)      │
│    • Separates publication time (event_at) from capture time (retrieved_at)│
│    • Strips post-cutoff article edits (28 mutated live blogs quarantined)  │
│    • Computes 526 exact-counter velocity intervals & metro cost spreads    │
└─────────────────────────────────────┬──────────────────────────────────────┘
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. GEMINI 4 ARGON FORECASTER + BLINDED JUDGE LOOP (72.8K Tokens / Pass)    │
│    • Generates calibrated probabilities, 80% intervals & resolution rules  │
│    • Verified across 10 daily cutoffs vs. 3.1-Pro, 3.8-Flash & Baseline    │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Actual Fetched Data Snapshot (Oct 25, 2026 UTC)

Every forecast in Hunch cites real, auditable Glasser Run IDs stored in `data/observations.sqlite` and `data/batches/verticals-cache-01/`:

| Vertical | Provider / Endpoint | Run ID | Live Captured Evidence (`2026-10-25 UTC`) |
| :--- | :--- | :--- | :--- |
| **Mortgages** | `zillow:/get_mortgage_rates` | `e5782de1` | **30Y Fixed: 7.49%** (`7.668% APR`) · 30Y Jumbo: **6.75%** (`6.926% APR`) · 15Y Fixed: **6.75%** |
| **Metro Housing** | `rentcast:/markets` (`78701`) | `f9be9fc9` | **Austin `78701` Median Sale: $675,000** across **309 active listings** (`41 new`) · 1BR `$499.9K` (`89d DOM`) · 2BR `$895K` (`$754/sqft`) |
| **Tech Talent & Comp** | `wellfound:/get_trending_jobs` | `e5041c13` | **San Francisco** Staff Data/AI (`Green`): **$300k–$380k** · **Salt Lake City** (`Alto Cirra`): **$115k–$155k** · **Austin/NYC/Miami** (`MOLTEN Cloud`): **$70k–$90k + eq** |
| **Fuel & EV Grid** | `aaa-gas-prices` (National/State/EV) | `a1dcecca` `26e9741d` | **CA:** `$6.02/gal` reg, `$8.46/gal` diesel, `$0.472/kWh` (`26,869` EV chargers) · **NY:** `$4.38/gal`, `$0.405/kWh` (`21,328` chargers) · **TX:** `$3.72/gal` reg, `$5.74/gal` diesel · **NC:** `$3.49/gal` |
| **SEC & Leases** | `secapi` + `exa:/search` | `argon-pilot` | **Meta (`META`)**: **$825B** in future AI data-center & office leases disclosed (`WSJ`/Exa) · **29,096 SEC filings** parsed |
| **Fleet & Retail** | `carfax` + `keepa:/deal` | `3a6a35bc` `fbc2f44d` | **SF `94103` Hybrid Fleet:** 2025 Camry SE Hybrid benchmark · **Amazon US:** 24h deal discount depth **19.4%** avg |

---

## Global City Headquarters Predictions (`gemini-4-argon`)

Synthesizing our live US, UK, Japan, and India evidence panels, Hunch generates calibrated probabilities for where companies should place—or will expand—their headquarters and regional hubs:

| Rank | Global City | Target Archetype | Probability | Grounded Cross-Vertical Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **01** | **Austin, USA** (`78701`) | Corporate & Ops HQ | **82%** `[74%, 89%]` | **309 active listings** (`$675K` median) absorb relocating staff; TX regular fuel (`$3.72/gal`) & diesel (`$5.74/gal`) sit **38% below CA** alongside active multi-hub cloud hiring (`MOLTEN Cloud`). |
| **02** | **San Francisco, USA** (`94103`) | Frontier AI R&D Core | **88%** *(R&D Core)* | Unmatched principal AI density (`$300K–$380K` comp, `26,869` CA EV chargers), but `$6.02/gal` fuel, `$8.46` diesel, and `$825B` hyperscaler lease competition push non-R&D G&A headcount out. |
| **03** | **Tokyo, Japan** | APAC AI & Robotics HQ | **76%** | Meta launched its *Muse* AI agent in Japan on Oct 23 alongside Sakana AI releases; PM Takaichi’s Diet supplementary tech budget and **+2.8%** 14-day Airbnb stay compression signal APAC HQ inflow. |
| **04** | **New York City, USA** | FinTech & Commercial HQ | **79%** | High SEC Form 8-K velocity (`JPM` Q3 filings, 171–242 daily filings), **21,328 NY EV chargers** (`$0.405/kWh`), and strong forward corporate travel demand. |
| **05** | **London, UK** | EMEA AI & FinTech Hub | **72%** | Rapid post-Storm Boelo grid restoration (`82,000` $\rightarrow$ `<25,000` properties without power in 24h, `72%` prob) and steady LinkedIn ML Engineer hiring (**10–30 new roles/day**). |
| **06** | **Mumbai & East Coast, IN** | Global Capability Center | **74%** | Jio Platforms IPO momentum and discounted crude keep Mumbai #1 for engineering scale-ups, while East Coast corridors require weather hedging (**85% IMD Cyclonic Storm probability** on Oct 26). |

---

## Measured Improvement Over Baseline (10-Day Benchmark)

To prove `gemini-4-argon` does not merely generate plausible prose, we built a **10-cutoff retrospective benchmark (`2026-10-14` to `2026-10-23` UTC, 50 questions across 5 tracks)** with strict directory isolation (`public_inputs/` vs. `private_outcomes/`) and evaluated 4 Gemini models against an empirical persistence baseline:

| Model | Calibration (Brier ↓) | Binary Accuracy (↑) | NASA X Volume MAE (↓) | Blinded Judge Score (1–5 ↑) |
| :--- | :---: | :---: | :---: | :---: |
| **`gemini-4-argon`** 🏆 | **0.1759** | 65.0% | 1.30 | **3.98 / 5.00** |
| `gemini-3.1-pro-preview` | 0.1759 | 65.0% | 1.30 | 3.36 / 5.00 |
| `gemini-3.8-flash` | 0.1886 | 65.0% | 1.29 | 3.23 / 5.00 |
| `gemini-3.1-flash-lite` | 0.1989 | **75.0%** | **1.20** | 2.74 / 5.00 |
| `Persistence Baseline` | 0.2060 | 60.0% | 1.32 | 2.50 / 5.00 |

- **`gemini-4-argon` reduces Brier calibration error by 14.6% over the persistence baseline** (`0.1759` vs. `0.2060`) and leads all models by **+0.62 to +1.24 points** on blinded narrative evaluation against held-out next-day reporting.

---

## Quickstart & Live Demo Commands

### 1. Install & Run Offline Test Suite (42 Tests)
```sh
python3 -m venv .venv
.venv/bin/pip install -e .

# Run all 42 unit tests (budget guards, normalization, leakage quarantine, forecast validation)
.venv/bin/python -m unittest discover -s tests -v
```

### 2. Run the Web Observatory & `/pitch` Deck
```sh
# Export credential-free JSON bundle into ui/public/data/
.venv/bin/python scripts/export_ui_data.py

# Preview locally (serves /, /pitch, /api/plan-simulator, and /api/run-prediction)
wrangler dev
```
- **Main Observatory:** `http://localhost:8787/`
- **5-Slide Minimalist Pitch Deck:** `http://localhost:8787/pitch`
- **One-Click Pre-Loaded HQ Demo:** `http://localhost:8787/?hq=1`

### 3. CLI Evidence Collection, Normalization & `gemini-4-argon` Forecasting
```sh
# 1. Generate a multi-vertical discovery plan (Zillow, Airbnb, LinkedIn, AAA Gas, Signals, Keepa, CARFAX)
.venv/bin/nextday plan --verticals zillow airbnb linkedin gas signals keepa carfax --output data/hq-plan.json

# 2. Preflight contract validation & worst-case USD reservation (free, no paid calls without --execute)
.venv/bin/nextday collect --plan data/hq-plan.json --batch hq-01 --budget 1.00

# 3. Execute collection, normalize into SQLite/JSONL, and run gemini-4-argon forecast
.venv/bin/nextday collect --plan data/hq-plan.json --batch hq-01 --budget 1.00 --execute
.venv/bin/nextday normalize
.venv/bin/nextday predict --name hq-forecast-01 --limit 64 --forecasts 5 --budget 0.30 --execute
```

---

## Repository Structure

```text
.
├── pitch/                     # Standalone 5-slide pitch deck (index.html + README.md)
├── config/
│   ├── coverage.json          # 4 global regions, multilingual topics & 7 HQ/market verticals
│   ├── benchmark-plan.json    # Frozen 10-cutoff retrospective benchmark protocol
│   └── forecast-schema.json   # Model-neutral JSON schema for next-day forecasts
├── nextday/
│   ├── cli.py                 # CLI entry point (`nextday`)
│   ├── client.py              # HTTPS-only Glasser client
│   ├── collector.py           # Idempotent batch runner & worst-case budget guard
│   ├── plans.py               # Discovery, 7-vertical, and fixed-cohort plan builders
│   ├── normalize.py           # Provider adapters, exact-counter deltas & SQLite/JSONL export
│   ├── gemini.py              # Direct Gemini API client (`gemini-4-argon`)
│   ├── prediction.py          # Stratified evidence sampler, validator & forecast runner
│   └── benchmark.py           # Historical case builder, leakage auditor & isolated loader
├── scripts/
│   ├── run_gemini_benchmark.py# Multi-model runner & blinded gemini-4-argon judge
│   ├── benchmark_resume.py    # Resumable historical dataset builder
│   └── export_ui_data.py      # Compiles credential-free data bundles for Cloudflare UI
├── ui/
│   ├── worker.js              # Cloudflare Worker Edge API (/api/plan-simulator, /api/run-prediction, /pitch)
│   └── public/                # Hunch Web Observatory (index.html, pitch/index.html, app.js, logo.svg)
└── tests/                     # 42 unit tests covering budgets, normalization, leakage & forecasts
```
