# Hunch (NEXTDAY) × Domino: ingest, review, and benchmark analysis

- **Date:** 2026-10-25.
- **Subject:** [github.com/Masmedeam/Hunch](https://github.com/Masmedeam/Hunch) at commit `8252d4cc` (2026-10-25 13:03 PDT). Its public data bundle comes from the live observatory (`/data/bundle.json`, generated 18:37 UTC).
- **Handling:** the repo and bundle are treated as untrusted data. They are cloned to `external/` and read only; none of their code was executed.
- **Visual demo:** `http://127.0.0.1:8100/?profile=hunch`. Same layout as the Domino demo, with Hunch data.

## 1. What Hunch is

"NEXTDAY // Temporal Evidence & Next-Day Forecasting Observatory".

**Pipeline:**
- **Evidence:** Glasser multi-vertical evidence collection: news and social, equities and SEC, Zillow, Airbnb, LinkedIn, plus AAA, RentCast, Keepa, and Carfax caches.
- **Leakage control:** a temporal quarantine separates `event_at` from `retrieved_at`, strips current social counters, excludes post-cutoff edits, and keeps public inputs and private outcomes in separate directories.
- **Forecasting:** Gemini 4 Argon forecasts against a model-neutral JSON schema.
- **Judging:** Argon also acts as a blinded narrative judge.
- **UI:** a Cloudflare Workers observatory.

**Benchmark `retrospective-v0`:**
- 10 daily cutoffs (Oct 14–23), 5 questions each.
- 357 Glasser Runs, $1.78 of data.

| Question | What it asks |
|---|---|
| Q1 | Ticker direction (a weekend count control on weekends) |
| Q2 | Any 8-K accepted from a 10-company cohort |
| Q3 | NASA X post count |
| Q4 | World developments (judged) |
| Q5 | Social developments (judged) |

## 2. Argon's review of the repo

Argon read every repo file (with `app.js` truncated) plus the slimmed bundle in one long-context call: 279k input tokens, thinking high, priority tier, `analysis/argon_hunch_review.json`.

**Strengths (Argon, and we agree):**
- exemplary temporal hygiene;
- point-in-time price bars;
- contract-inspected, idempotent paid calls with worst-case budget reservation;
- schema and provenance validation of forecasts;
- honest accounting for unresolved outcomes.

**Gaps:**

| Severity | Issue (Argon) | Our verification |
|---|---|---|
| Critical | The judge's held-out reference is filtered to articles and social posts, then sliced `[:65]` with no stratification, so social posts may never reach the Q5 judge | **Code confirmed** (`scripts/run_gemini_benchmark.py`, `run_judge_for_case`). Impact is plausible: the bundle's reference samples are 100% articles. Fully confirming it needs their private outcomes. |
| High | 87% of Argon's Brier gain over the baseline is a weekend-calendar artifact on Q2 | **Confirmed.** Q2 Brier on weekdays: Argon 0.252 vs baseline 0.261. On weekends: 0.0025 vs 0.090, because the baseline uses a fixed 0.30 when EDGAR is closed. Q1 weekdays: 0.249 vs 0.250. |
| High | Blind IDs are fixed per model, and Argon judges itself, against the repo's own judge policy | Code confirmed (model order is fixed) |
| High | Pure LLM prompting on raw price/count arrays, with no statistical time-series models | Confirmed by design. §3 shows what adding them does. |
| Medium | Four new verticals lack normalization adapters; a paid Gemini route is unprotected | Not re-verified |

## 3. Domino applied to the NEXTDAY benchmark

**Entries added.** Every input is computed only from data before each cutoff (`domino/hunch_analysis.py`, `domino/hunch_timesfm.py`):

- **Domino-stats:**
  - Q1: EWMA Student-t with a 1-year drift.
  - **Q2: SEC EDGAR submission histories for the 10 CIKs.** Each company's 8-K hazard is multiplied by whether it filed in the same week last year (the earnings calendar, which is the first domino). Weekends get 0.01.
  - Q3 and the weekend Q1 count: Poisson by day type, from the prior week.
- **Domino-TimesFM (Q1 only):** P(close up) from TimesFM 3.0 quantiles.
- **Domino-Argon:** Gemini 4 Argon (high, priority) per case. It is given the statistical priors and the case's history summary, starts from the priors, and is asked to name the domino behind any move.

**Results, rescored on the objective tracks** (17 binary forecasts: Q1 weekday + Q2; numeric: Q3 + weekend Q1):

| Entry | Brier (Q1+Q2) | 95% CI | Brier Q1 | Brier Q2 | MAE Q3 | Δ Brier vs baseline |
|---|---|---|---|---|---|---|
| **Domino-Argon** | **0.192** | [0.139, 0.243] | 0.249 | **0.153** | 1.06 | −0.034 |
| **Domino-stats** | 0.194 | [0.141, 0.244] | 0.249 | 0.155 | **0.99** | −0.033 |
| gemini-3.1-pro-preview | 0.206 | [0.139, 0.273] | 0.255 | 0.173 | 1.30 | −0.020 |
| gemini-4-argon (Hunch) | 0.207 | [0.127, 0.289] | 0.249 | 0.177 | 1.30 | −0.020 |
| gemini-3.8-flash | 0.221 | [0.142, 0.304] | 0.255 | 0.198 | 1.29 | −0.005 |
| baseline | 0.226 | [0.161, 0.297] | 0.250 | 0.210 | 1.32 | — |
| gemini-3.1-flash-lite | 0.232 | [0.130, 0.345] | 0.238 | 0.228 | 1.20 | +0.006 |
| Domino-TimesFM (Q1 only) | — | — | **0.239** | — | — | — |

**Reading it honestly:**
- **The gain is the first domino, not better prompting.** Q2 improves because the earnings calendar drives 8-K filings. Q3 improves because NASA posts on a weekday cadence. Domino-Argon adds almost nothing over Domino-stats: Argon mostly kept the statistical priors.
- **Q1 (stock direction) is a coin flip for everyone.** All entries sit around 0.24–0.25. TimesFM is marginally best.
- **Not significant yet.** n = 17 binary forecasts. A sign-flip permutation test of Domino-Argon against the baseline gives p = 0.18, and the CIs overlap.
- **Why our numbers differ from Hunch's leaderboard.** Hunch reports Argon at 0.1759 and baseline at 0.2060. That is a per-day mean in which weekend days (Q2 only, trivially near zero) weigh as much as weekdays. Our 0.207 vs 0.226 pools all binary forecasts equally.

## 4. Tomorrow (Monday 26 October) through Domino

- **Any cohort 8-K accepted:** **P = 0.80.** Late October is earnings week. The largest per-company probabilities come from last year's same-week filings: AMZN 0.25, GOOGL 0.23, XOM 0.21. Hunch's fixed baseline would say 0.30.
- **NASA X posts:** about 1.6 expected, 80% band [0, 3] (Poisson, weekday).
- **Daily life, from Hunch's own verticals:**

  | Item | Hunch vertical today | Domino next week |
  |---|---|---|
  | Gas (AAA regular) | $4.289; week ago $4.299 | TimesFM 3.0 **$4.23** [4.15, 4.31] (EIA weekly series; backtest −35% error vs no-change) |
  | Diesel (AAA) | $6.347; +74% year over year | — |
  | 30-year mortgage | Zillow lender quote 7.49% (APR 7.67%, includes points) | Freddie Mac survey 7.32% → **7.28%** next week (TimesFM, 10-year Treasury covariate) |

- **Hunch's own Argon pilot forecasts for Oct 26** are shown as gauges, unresolved:
  - IMD cyclone classification, 0.85;
  - UK power restoration, 0.72;
  - US diplomatic/military development, 0.78;
  - YouTube view count, 0.78.

## 5. Recommendations for Hunch

1. Make the baseline calendar-aware: Q2 at 0.01 on weekends and a rolling pre-cutoff weekday rate. Report weekday and weekend tracks separately.
2. Add the SEC first-domino prior (submission histories × last-year earnings timing) and a Poisson cadence prior to the forecaster prompt. In this rescoring, that alone moves Q2 Brier from 0.177 to 0.155.
3. Stratify the judge's reference evidence by kind before slicing. Randomize blind IDs per case (seeded), and add a judge from another model family.
4. Use TimesFM 3.0 for numeric tracks and for the AAA and mortgage verticals. In our backtests it beats or ties regression on gas (−35%), mortgage (−26%), and flu (−37%) against no-change.
5. Grow the sample. 50 questions show the pipeline works but cannot rank models: our best entry's advantage has p = 0.18.

## 6. Files

| Path | Contents |
|---|---|
| `external/Hunch/` | The cloned repo |
| `external/hunch_live/bundle.json` | Their public data bundle |
| `analysis/argon_hunch_review.json` | Argon's review |
| `runs/hunch_analysis.json` | Every score and our entries |
| `runs/hunch_argon_entry.json` | Domino-Argon forecasts with their rationales and dominoes |
| `runs/hunch_timesfm.json` | TimesFM Q1 probabilities |
| `domino/static/profiles/hunch/*.json` | Visual-demo fixtures |
| `domino/hunch_profile.py` | The fixture builder |


## 7. Expanded: Q4 world and Q5 social claims, resolved on outcomes (added 14:05)

Hunch's own benchmark doc says the primary score should be "outcomes, not an LLM's impression". Its narrative tracks are scored only by an Argon judge, so we resolved every claim instead (`domino/hunch_extended.py resolve`):
- **Claims:** all 199 of the four LLMs' Q4 and Q5 claims.
- **Resolver:** Gemini 4 Argon (thinking high, priority tier), one call per case.
- **Evidence:** the held-out next-day reference articles (24 per case), the benchmark judge's day summary, and NASA's actual X post count.
- **Rule:** a claim is NO only if contradicted; unmentioned is UNRESOLVED, which is Hunch's own rule.

Results: `runs/hunch_claims.json`, `runs/hunch_claim_scores.json`.

| Model | Claims | Resolved | YES rate (resolved) | Mean stated p | Claim Brier (resolved) | Q4 Brier | Q5 resolved | Specificity (1–5) |
|---|---|---|---|---|---|---|---|---|
| gemini-4-argon | 60 | 29 (48%) | 0.90 | 0.69 | **0.144** | 0.138 | 5 / 30 | 3.3 |
| gemini-3.1-pro-preview | 59 | 18 (31%) | 0.83 | 0.72 | 0.148 | 0.158 | 2 / 30 | 3.4 |
| gemini-3.8-flash | 40 | 17 (42%) | 0.82 | 0.81 | 0.155 | **0.125** | 6 / 20 | 3.0 |
| gemini-3.1-flash-lite | 40 | 16 (40%) | 0.56 | 0.72 | 0.244 | 0.198 | 5 / 20 | 3.0 |

Totals: 64 YES, 16 NO, 119 UNRESOLVED. Most Q5 claims cannot be resolved because the public bundle holds no held-out social posts. That is the same gap Argon found in their judge (§2).

**Finding 1: the judge does not reward being right.** Across 53 model-days:
- Hunch's judge score vs. outcome Brier: Spearman **−0.05 (p = 0.72)**, no relation.
- Judge score vs. claim specificity: **+0.50 (p = 0.0002)**.

The judge rewards specific-sounding claims, not correct ones. That is exactly the failure mode Hunch's own doc warns against ("an elegant explanation must not outrank a better-calibrated forecast").

**Finding 2: models forecast continuations, not news.** Of 199 claims:

| Claim type | Count | Came true (resolved) |
|---|---|---|
| Continuations of already-running stories | 85 | 87% |
| Scheduled events | 22 | 86% |
| Posting-cadence claims | 89 | 56% |
| Genuinely new events | **1** | — |

Their Q4/Q5 hit rates mostly measure "tomorrow resembles today". A Domino-style first-domino prior (calendars, ongoing stories) would score just as well with no LLM, so the honest question for Q4 is whether a model ever calls a new event.

## 8. Pilot head-to-head for Monday 26 October (pre-registered)

Domino re-forecast Hunch's five Argon pilot forecasts (`domino/hunch_extended.py pilot`, `runs/hunch_pilot_domino.json`, hash `a5118015…`).
- **Live data:** treg news for the cyclone, UK outages and embassies; treg YouTube statistics for the video.
- **Models:** a Student-t volatility model for META.
- **Argon:** a 5-sample ensemble (thinking high, priority tier), pooled in log-odds.

| Pilot forecast | Hunch (Argon) | Domino | Basis |
|---|---|---|---|
| fc-1 · IMD upgrades the Bay of Bengal system to Cyclonic Storm | 0.85 | 0.86 (±0.02) | live news + Argon ensemble |
| fc-2 · UK homes without power < 25,000 by Oct 27 | 0.72 (0.72 / 0.23 / 0.05) | 0.73 (0.73 / 0.23 / 0.04) | live news + Argon ensemble |
| fc-3 · META Monday: down > 1.5% / within ±1.5% / up > 1.5% | 0.35 / 0.45 / 0.20 | 0.28 / 0.45 / 0.28 | Student-t on EWMA volatility (no drift) |
| fc-4 · no US embassy departure order **and** no US strike inside Iran | 0.78 | **0.89** (±0.01) | live news + Domino's live strike odds (0.12) + Argon |
| fc-5 · K/DA "FIRESTARTER" ≥ 26.85M views by Oct 27 00:00 UTC | 0.78; estimate 27.05M [26.78M, 27.6M] | **0.99**; median **29.08M** [28.34M, 30.27M] | measured velocity (below) |

**The YouTube call is the clearest difference.**
- The view counter went from 26,661,415 at 17:36 UTC (Hunch's own snapshot) to 26,991,503 at 21:01 UTC (treg, $0.001). That is about **97,000 views per hour**, and the threshold is already passed.
- Domino extrapolates with a decaying velocity: lognormal multiplier, median 0.8, log-sd 0.35, plus a 1% audit-deduction risk.
- Hunch's 80% interval tops out at 27.6M, below Domino's 10th percentile.

The pre-registered numbers settle this tomorrow.

## 9. Social data audit and the verticals (Argon, `runs/hunch_verticals_argon.json`)

**Social data:**
- **Freshness:** 70% of 1,838 observations are within 7 days, 10% older, and 19% of unknown recency. All 462 TikTok trend points are older than 7 days.
- **Coverage:** skewed to single-page TikTok and YouTube search samples. Regions (US, GB, IN, JP) are requested, not verified audience geography.
- **Counters:** 99% are exact integers, but they are lifetime totals with sparse repeat observations (526 growth intervals). Tomorrow's engagement can be forecast only for items that are re-observed. The K/DA forecast works because we took a second snapshot.

**Verticals (today, and what it means for daily life):**

| Vertical | Today | First domino | Next-day prediction idea |
|---|---|---|---|
| AAA gas, national | regular $4.289, easing for a week | RBOB / ULSD futures | AAA regular ticks down 0.5–1.2¢ tomorrow; Domino's TimesFM sees $4.23 next week |
| AAA gas, 20 states | CA–GA spread $2.37 | PADD refinery outages | spread narrows or widens by more than 1¢ |
| AAA EV charging | $0.34–0.6/kWh by state | utility TOU tariffs, wholesale power | net new public chargers per day |
| Zillow mortgage | 30-yr quote 7.49% (APR 7.67%) | 10-year Treasury and MBS coupons | the next quote follows the Treasury (Domino: Freddie 7.28% next week) |
| RentCast (Austin 78701) | median sale $657k, 118 days on market | lease expirations, return-to-office | days on market stays above 118 |
| Insider ratios | sell / buy about 4 : 1 | 10b5-1 plan executions | sell / buy stays above 2.2 : 1 |
| Keepa (Amazon) | 6 of 10 items unchanged | inventory and freight (diesel) | at least 8 of 10 within ±1% |
| Carfax used Camrys | $24k–$30k | Manheim wholesale lanes | no list-price markdowns in 24 h |

**Argon's cross-vertical story:** "Households in late October 2026 are locked in a defensive crouch. Even as regular gas eases toward our $4.23/gal forecast, $6.35/gal diesel and 7.67% mortgage APRs freeze big-ticket mobility…"

**Editor's note:** that is narrative, not measurement. The measured parts are the gas and mortgage forecasts.

## 10. Demo visuals (one per analysis, same layout as `runs/ui_live3.png`)

Open `http://127.0.0.1:8100/?profile=<id>`. The header switcher lists all of them, from `profiles/index.json`.

| Profile | What it shows |
|---|---|
| `hunch` | Overview: Hunch's world as dominoes, the rescored benchmark leaderboard, Monday's forecasts, AAA gas by state |
| `hunch-world` | Q4: outcome-resolved claims, claim types, judge vs. outcome, the Monday world head-to-head |
| `hunch-social` | Q3 + Q5 + YouTube: posting cadence, the view-velocity forecast vs. Hunch, the social data audit |
| `hunch-markets` | Q1 + Q2 + META: per-company 8-K odds on the globe (earnings week), the META bracket head-to-head |
| `hunch-life` | Verticals: pump prices by state, EV, mortgage, rent, cars, insiders; your week ahead |
| `daily-life` | Our gas / mortgage / flu week-ahead backtests (Domino and TimesFM vs. no-change) |
| `categories` | Our 8-category sweep: attention predictability, first dominoes, Argon's ranking |
| `real-estate` | Treasury → mortgage (weekly), market rents → CPI rent (13-month lead), metro home values (momentum; rates and price cuts add no skill); Argon vs stats head-to-heads. Doc: `analysis/real_estate_analysis.md` |

Screenshots of all nine (1920×1080) and a contact sheet: `runs/screens/1427/` (`contact_sheet.png`).
