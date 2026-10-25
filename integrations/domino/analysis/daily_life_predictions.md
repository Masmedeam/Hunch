# Beyond pizza: predictions that matter in daily life

- **Date:** 2026-10-25.
- **Reproduce:** `.venv/bin/python -m domino.daily_life`, then `tools/argon_daily_life.py`.
- **Results:** `runs/daily_life_results.json`.
- **Argon reasoning:** `analysis/argon_daily_life.json` (gemini-4-argon, thinking high, priority tier, 134 s).

## 1. Why this extension

The pizza chain is a great hook but anecdotal. What people feel is the end of the chain: what they pay at the pump, what their mortgage costs, whether flu is coming. We tested whether the Domino world model forecasts those, one week ahead, with the same rigor as before:
- rolling one-step-ahead forecasts on an expanding window, with no look-ahead;
- block-bootstrap 95% CIs and Diebold–Mariano tests;
- a separate autoregression-only comparison, to isolate what the leading driver (the domino) adds.

## 2. Measured results

| Next-week target | Data | Test weeks | Error vs. "no change" | vs. autoregression only | Direction right | First domino (Granger) | Next-week forecast |
|---|---|---|---|---|---|---|---|
| **Gasoline at the pump** ($/gal) | FRED GASREGW; RBOB futures | 564 (2016–2026) | **−33.6%**, CI [−0.018, −0.012] $/gal, p = 3e-17 | **−19.4%**, p = 4e-11 | **80%** | RBOB futures → pump, p = 2e-15, lag 1 week | **$4.27** (from $4.284 on Oct 19) |
| **30-year mortgage rate** (%) | FRED MORTGAGE30US; 10-year Treasury | 565 | **−13.5%**, p = 3e-6 | **−12.5%**, p = 7e-6 | 66% | 10-year Treasury → mortgage, p = 3e-34, lag 2 weeks | **7.30%** (from 7.32% on Oct 22) |
| **Flu activity** (CDC weighted ILI) | Delphi FluView; Wikipedia "Influenza" | 146 | **−28.3%**, p = 4e-5 | 0.0%, p = 0.98 | 80% | attention → ILI, p = 0.03 (weak) | **2.36%** (from 2.20%, week 41) |
| Initial jobless claims | FRED ICSA; Wikipedia "Unemployment", "Layoff" | 146 | +0.9%, p = 0.77 | −11.6%, p = 0.007 | 54% | not significant | about 193k (from 194k) |
| Egg prices (monthly) | FRED APU0000708111; Wikipedia "Avian influenza" | 6 | −18%, p = 0.53 | — | — | too few months | $2.32 (from $2.27) |
| Air quality, next day (PM2.5, Sacramento; added 12:33) | Open-Meteo / CAMS hourly; Wikipedia "Wildfire" | 1,027 days | −5.8% (log), CI [−0.029, −0.004], p = 0.008 | — | — | wildfire attention → PM2.5, p = 0.07 (not significant) | 4.1 µg/m³ on Oct 24 (clean) |

**Reading the table:**
- **Gas and mortgage are real, strong, next-week predictions.** The leading market (RBOB futures, the 10-year Treasury) is the measured first domino, and it adds value beyond autoregression.
- **Flu is predictable from its own momentum.** Public attention adds nothing beyond that (vs. autoregression: 0.0%). Honest result: Wikipedia is not the first domino for flu.
- **Claims and eggs are not ready.** Claims show no gain over "no change". Eggs have too short an attention history; our Wikipedia cache starts in June 2023.

## 3. The pizza-to-pump chain, with each link labelled

| Link | Evidence | Status |
|---|---|---|
| Pentagon pizza busyness → strike within hours | Press reports for June 12 and 21, 2025, plus 2026 cases. A LessWrong backtest of 648 Pizza Report posts found no signal. Google exposes no busyness for these shops today (litescrape, SerpApi, and pizzint.watch all show null). | **Anecdotal** |
| Escalation / Hormuz tanker attacks → Brent | Brent at $111.70 on Oct 23 amid tanker attacks. Wikipedia attention does not lead Brent (0 of 60 pairs significant). | **Contemporaneous, not leading** |
| Brent → RBOB gasoline futures | Same-day market linkage | Measured (standard) |
| **RBOB futures → your pump price next week** | Granger p = 2e-15; −33.6% forecast error; 80% direction accuracy over 564 weeks | **Measured and strong** |

**Argon's 60-word version:** "Pentagon pizza spikes before the June 2025 Israeli and US strikes remain anecdotal… However, downstream links are measured: … RBOB futures strongly predict US pump prices (Granger p=2e-15, −33.6% MAE, 80.5% direction-hit across 564 weeks)."

**Editor's note:** Argon wrote "tanker attacks pushed Brent to $111.70". That is a causal claim we have not tested, so we say "amid".

## 4. Week-ahead forecasts (plain English, from the latest data)

- **Gas:** about $4.27 a gallon next week, down about 1.4¢ from $4.284. Futures lead the pump by about a week.
- **Mortgages:** the 30-year fixed rate eases to about 7.30% from 7.32%, following the 10-year Treasury with a two-week lag.
- **Flu:** national influenza-like illness rises to about 2.36% of outpatient visits from 2.20%, which is typical late-October momentum.
- **Jobless claims:** flat at about 193k. The model has no edge here.

## 5. Next daily-life tests (proposed by Argon)

| Candidate | First domino | Free data | treg / Glasser data | Expected predictability (Argon) |
|---|---|---|---|---|
| Wildfire smoke and PM2.5 hazard days | Upwind satellite fire radiative power | NASA FIRMS, Open-Meteo air quality | treg news, Trends (local) | 8.9 / 10 |
| Next-day electricity prices and demand | Grid-weighted 72-hour temperature anomaly, wind | Open-Meteo, EIA, ISO data | treg news (outages) | 8.8 |
| Respiratory ER surges | Municipal wastewater viral load | CDC NWSS | treg Trends ("fever", "urgent care") | 8.6 |
| Egg and poultry shelf prices | Weekly commercial bird depopulation counts | USDA APHIS | Glasser Keepa (Amazon prices) | 8.4 |
| Used-vehicle prices | Wholesale auction conversion rates | Manheim index (public releases) | Glasser listings | 8.3 |
| Home listings cutting prices | Weekly mortgage-rate changes plus MBA applications | FRED, Redfin data center | Glasser RentCast | 8.1 |
| Morning commute delays | 05:30 local precipitation and temperature composite | NWS / Open-Meteo | treg Maps (traffic), news | 7.9 |
| Jobless claims, revisited | State WARN Act layoff notices | State WARN databases | treg Reddit (r/layoffs), Trends ("severance") | 7.6 |

The predictability scores are Argon's priors, not measurements. Each needs the same rolling, baseline-relative test as §2 before it goes on stage.

## 6. Caveats

- One-step-ahead skill on weekly price series reflects well-known pass-through (futures → retail, Treasuries → mortgages). It is real and useful, but not secret alpha. The value Domino adds is chaining these measured links, at different speeds, into one live world model and explaining them.
- Flu and claims use attention series that start in 2023, so they have shorter samples.
- Forecasts are statistical, not financial or medical advice.


## 7. Against the state of the art: Google TimesFM 3.0 (added 12:45)

We ran TimesFM 3.0 (`google/timesfm-3.0-pytorch`, 330M parameters, zero-shot, released 2026-08-31) on the same test weeks with the same information: the target's own history (up to 512 points) plus the leading driver as a covariate known at forecast time. Weights are licensed non-commercial; this is a hackathon demo. It ran on the Mac's GPU (MPS) in under 2 s per target.

Files: `domino/sota_timesfm.py`, `runs/sota_timesfm.json`.

| Next-week target | TimesFM 3.0 vs no-change | Our regression vs TimesFM | TimesFM direction right | TimesFM 80% coverage |
|---|---|---|---|---|
| Gas at the pump (564 weeks) | −34.8% | +1.7% (p = 0.67): **tie** | 78% | 0.78 |
| 30-year mortgage (565 weeks) | −26.1% | **+17% worse** (p = 3e-6) | 72% | 0.86 |
| Flu ILI (146 weeks) | −36.7% | **+13% worse** (p = 0.002) | 83% | 0.81 |

For the Brent next-day distribution (last 260 days, 3-quantile pinball loss), our HMM/Student-t mixture scores 0.785 against TimesFM's 0.811, so ours is about 3% better, with equal 80% coverage (0.79). TimesFM's 9-quantile coverage over 592 days is 0.81.

**Decision: Domino picks the backtest-best numeric model per target.**
- TimesFM 3.0 for the week-ahead daily-life series.
- The regime mixture for daily markets.
- Gemini 4 Argon for events, data choice, recursion, and explanation.

That is an all-Google stack with a measured reason for every component.

**TimesFM's next-week forecasts** (`runs/timesfm_week_ahead.json`):

| Target | Forecast | 80% band | Last value |
|---|---|---|---|
| Gas | $4.23 / gal | 4.15–4.31 | $4.284 on Oct 19 |
| Mortgage | 7.28% | 7.15–7.40 | 7.32% |
| Flu | 2.28% | 2.13–2.46 | 2.20% |
