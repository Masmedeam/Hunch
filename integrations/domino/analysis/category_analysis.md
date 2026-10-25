# Where the Argon predictive world model works: category analysis and first dominoes

- **Date:** 2026-10-25, 12:06 PDT.
- **Reproduce:** `.venv/bin/python -m domino.categories`, `-m domino.first_domino`, `tools/argon_categories.py hypothesize|interpret`.
- **Raw results:** `runs/category_results.json`, `runs/first_domino_results.json`.
- **Argon reasoning:** `analysis/argon_category_hypotheses.json` (before the data), `analysis/argon_category_interpretation.json` (after). Both ran on `gemini-4-argon` at thinking high, priority tier.

## 1. Question

Which topics can our Argon world model predict *tomorrow*, and what is the first domino of each causal chain? The first domino is the earliest measurable signal that moves before the rest.

## 2. Method

**Data (free, daily, 2023-06 → 2026-10-24):**
- 47 English-Wikipedia attention series in 8 categories (pageviews, z-scored against a trailing 60-day window).
- 31 market series (yfinance).

**Tests (all out of sample, rolling refits every 21 days, strict lag).** Strict lag means the attention used is complete before the forecast interval starts.

1. **Market forecasts.**
   - Model: 2-state HMM "tension" plus a Student-t regime mixture.
   - Baseline: EWMA Student-t.
   - Scores: CRPS, log score, 80% interval coverage, and Brier score for |return| > 2.5%.
   - Statistics: block-bootstrap 95% CIs and Diebold–Mariano tests.
2. **Attention forecasts** (social-engagement proxy). Next-day category attention, AR(1) vs. persistence, scored by MAE.
3. **First domino.** Granger tests from attention to next-day |return| and in reverse (lags 1–3), Holm-corrected within each category. A first domino leads markets without being led by them.
4. **First-domino model.** EWMA volatility scaled by exp(β·z) of the leading article; does using it improve forecasts?
5. **Argon.**
   - Before the data: proposes chains, first dominoes, and the treg / Glasser endpoint that could measure each.
   - After the data: ranks categories on the measured evidence.

## 3. Results

| Category | Next-day attention forecast (MAE vs. persistence) | Market return forecasts (best target, CRPS diff, DM p) | Attention leads markets (Holm, sig/pairs) | Markets lead attention | First domino (Granger) |
|---|---|---|---|---|---|
| Macro stress | **−0.035, p = 4e-8** | gold −0.002, p = 0.49 | 3 / 30 | 1 | **"Recession" → VIX (lag 1, p = 7.6e-6), S&P 500 (lag 1, p = 2e-4)** |
| China–Taiwan / trade | **−0.029, p = 7e-4** | semis −0.002, p = 0.69 | 1 / 15 | 0 | **"US–China trade war" → FXI (lag 1, p = 2e-4)** |
| Weather / disasters | **−0.035, p = 1e-11** | insurers −0.002, p = 0.55 | 0 / 15 | 0 | none |
| AI / tech | **−0.027, p = 2e-8** | semis −0.005, p = 0.49 | 0 / 24 | 0 | none |
| Health / outbreaks | **−0.025, p = 8e-6** | biotech 0.000, p = 0.99 | 0 / 15 | 0 | none |
| Crypto | **−0.014, p = 0.03** | BTC **+0.009 (worse), p = 0.03** | 3 / 15 | **4** | feedback loop (Ethereum → BTC, lag 2, p = 0.04) |
| Geopolitics → energy | −0.008, p = 0.26 | WTI −0.007, p = 0.12 | 0 / 60 | 0 | none (markets react same day) |
| Russia–Ukraine | +0.017 (worse), p = 0.09 | natgas −0.002, p = 0.80 | 1 / 20 | 0 | invasion article → ITA (lag 1, p = 0.01) |

**First-domino volatility models** (strict lag; positive log-score difference = better):

| First domino → target | β (last fit) | CRPS change | Log-score diff [95% CI] | Verdict |
|---|---|---|---|---|
| "Recession" → S&P 500 | +0.121 | −0.52% (DM p = 0.12) | **+0.018 [+0.004, +0.036]** | **Confirmed**: the only CI that excludes zero |
| "Recession" → VIX | +0.106 | −0.20% (p = 0.52) | +0.011 [−0.001, +0.024] | Borderline |
| "US–China trade war" → FXI | +0.071 | −0.34% (p = 0.25) | +0.005 [−0.006, +0.016] | Suggestive |
| "Russian invasion of Ukraine" → ITA | −0.071 | +0.02% | +0.002 [−0.012, +0.014] | Sign flips out of sample: not real |
| "Ethereum" → BTC | +0.059 | 0.00% | +0.002 [−0.003, +0.007] | None |

**Calibration.** Across most targets, the world model's 80% intervals cover about 0.80 of outcomes, where the EWMA baseline covers about 0.77. The world model fixes the baseline's chronic under-coverage of tail risk even when point accuracy ties.

## 4. Top 5 categories

**Argon's ranking, made after it saw the evidence:**

| # | Category | Score |
|---|---|---|
| 1 | Macro stress | 7.8 |
| 2 | China–US trade | 6.5 |
| 3 | Weather / disasters | 5.6 |
| 4 | AI / tech | 5.0 |
| 5 | Crypto | 3.0, kept as the "radical honesty" example |

**Recommended top 5 for the demo** (evidence first, then stage value):

1. **Macro stress: "Recession" attention → tomorrow's S&P 500 and VIX volatility.** Our only statistically confirmed first domino that also improves a forecast. Demo: volatility bands widen the day after recession attention spikes.
2. **Next-day social attention (engagement) across topics.** This beats persistence at p < 0.001 in five categories: weather 1e-11, AI 2e-8, macro 4e-8, health 8e-6, China 7e-4. This is the cleanest "predict tomorrow" claim we can make. Demo: forecast tomorrow's attention wave for the live crisis topics.
3. **China–US trade → China equities (FXI) volatility.** Granger-significant (p = 2e-4), with no reverse lead and a small, not-yet-significant forecast gain. Next data: native-language Google Trends through treg.
4. **Geopolitics → energy: the live scenario (Iran / Strait of Hormuz, Brent $111.70).** Not a leading indicator in our data, because oil reprices the same day, faster than Wikipedia. The world model still gives calibrated intervals (coverage 0.80 vs. 0.77). This is the hero visual and the live pre-registered forecast. The pizza signal is the hook, clearly labelled anecdotal.
5. **Weather / disasters.** Attention is the most predictable of all (p = 1e-11), but markets have already priced the event by the time Wikipedia moves. Demo: the honest contrast between predicting attention and predicting markets.

## 5. Getting to the first domino

**Finding:** mainstream attention is rarely the first domino. Only 8 of 194 attention→market pairs survive multiple-testing correction, against 5 that run the other way. Crypto prices lead crypto attention, and energy markets move the same day as the news. The true first dominoes sit upstream of Wikipedia, in signals that move hours earlier and that treg / Glasser can buy now.

| Category | Candidate first domino (Argon) | How to measure it now | Price | Lead (Argon estimate) |
|---|---|---|---|---|
| Macro stress | Layoff leaks, WARN notices, "severance" searches | treg Google Trends + Reddit r/layoffs search | $0.0012 + $0.0009–0.0019 | about 14 h |
| China / trade | Mandarin / Traditional-Chinese tariff and export-control searches; local news | treg Trends (geo, language); GDELT; Polymarket tariff markets | $0.0012; free | about 6–12 h, US–Asia offset |
| Geopolitics | Pentagon-area late-night activity (pizza busyness); tanker AIS gaps; Gulf local news | treg Maps popular times (null today); treg news (free) | $0.00015 | hours (anecdotal) |
| Weather | Regional outage / flood searches; port truck-stop busyness | treg Trends (geo-fenced); Maps popular times | $0.0012; $0.00015 | about 10 h |
| AI / tech | Sysadmin error-code chatter before status pages | treg Reddit r/sysadmin, r/devops; Trends "[vendor] down" | about $0.001 | about 1–3 h |

This is where RPWM's expected-free-energy data acquisition matters. The live pipeline (`domino/live.py`) already lets Argon choose the next purchase from a priced menu by expected information gain per dollar. In today's live run it bought the Gulf-tanker and shipping-insurance news; recursion then stopped by the relative-ΔF rule.

## 6. Honest caveats

- **No CRPS improvement reaches p < 0.05.** Across all 31 market targets and 5 first-domino models, the measured gains are in calibration (coverage) and one log-score CI. Point accuracy is not significantly better.
- **Multiple testing.** Granger results are Holm-corrected within each category but not across categories. With 194 pairs, a few false leads are expected; the Russia–Ukraine sign flip is likely one.
- **Habituation.** Trailing-window z-scores detect shocks, not sustained regimes. Today, with Brent at $111.70, the attention z is −0.77. A long-window baseline is the next fix.
- **Timing.** Daily UTC pageviews overlap the US session, so we use strict lags. The June 13, 2025 early warning appears only without the strict lag, so we do not claim it. Hourly per-article pageviews are not available.
- **Pizza index.** Google exposes no busyness for Pentagon-area pizza shops today (litescrape and SerpApi both returned null). The pizza signal is shown as an anecdotal hook, never as evidence.
- **Argon reading errors.** Argon's interpretation described the big-move threshold as ">1.5σ"; we used an absolute 2.5% threshold. Argon's "7 of 8 categories" means 7 negative point estimates, of which 6 are significant.


## 7. Argon as a forecaster: a leak-free check (added 12:26)

Is Gemini 4 Argon itself a good next-session forecaster?
- **Days:** the 17 Brent trading days after Argon's release (2026-09-30 → 10-22), when it cannot have memorized the outcomes.
- **Inputs:** headlines dated the previous day (treg dated news search) plus closes through that day.
- **Settings:** thinking high, priority tier.
- **Comparison:** the strict-lag statistical model.

`runs/argon_forecast_eval.json`, `domino/argon_forecast_eval.py`

| Metric | Argon | Statistical model | Climatology (hindsight base rate 0.18) |
|---|---|---|---|
| Brier score, P(\|move\| > 2.5%) | 0.165 [0.077, 0.246] | 0.163 | 0.145 |
| Log loss | 0.532 | 0.513 | — |
| 80% interval coverage | 0.82 | 0.82 | — |
| Pinball loss (P10 / P50 / P90) | 0.473 | 0.476 | — |
| Direction hit rate | 0.47 | — | — |

**Verdict:** with only 17 days, the confidence intervals are wide. Argon matches the statistical model's calibration but does not beat it, and neither beats the hindsight base rate on big moves. Direction is a coin flip. This agrees with the literature on LLM forecasting of liquid markets. Argon earns its place in the world model by reading events, choosing data, and explaining, not as a market oracle. The daily-life targets in `analysis/daily_life_predictions.md` are where next-period skill is strong and significant.
