# Domino · Real estate: what moves housing next, and what does not

Built 2026-10-25, 14:05–14:30 PDT. Code: `domino/realestate.py` (stats · argon · timesfm). Results: `runs/realestate_results.json`, `runs/realestate_argon.json`, `runs/realestate_timesfm.json`. Demo visual: `?profile=real-estate` (screenshot `runs/screens/1427/ui_real-estate.png`).

## 0. Bottom line

1. **Treasury → mortgage rates is the first domino, and it is fast.**
   - Weekly 10-year Treasury changes Granger-cause the Freddie Mac 30-year survey rate at a 2-week lag (p = 3e-34, 565 weeks).
   - TimesFM 3.0 with the Treasury as a covariate cuts error 26% vs no-change.
   - Thursday 29 Oct: **7.28% [7.15, 7.40]** vs 7.32% last week. Domino stats P(lower) 0.62; Argon 0.65.
2. **Market rents → CPI rent is the second domino, and it is slow.**
   - Zillow's market rents (ZORI) lead the official CPI rent of primary residence by **13 months** (corr 0.90, vs 0.13 with no lag; Granger p = 0.005).
   - A 12-month-ahead model using market rents beats CPI's own history by 43% (DM p = 0.04), and persistence by 27% (p = 0.19, overlapping windows).
   - Your rent inflation in Sep 2027: **2.9% [2.2, 3.5]**, down from 3.0%.
3. **Home values follow their own momentum; neither mortgage rates nor price cuts add next-month skill.**
   - Adding rate changes makes the pooled 36-metro model 8% *worse* out of sample (DM p = 0.04).
   - Adding rates at 6 months: +1.8% (p = 0.90). Adding Realtor.com price cuts: +0.4% (p = 0.40).
   - TimesFM 3.0 is 170% worse than simple momentum on Zillow's smoothed home-value series.
   - We report these as findings, not failures.
4. **October calls:**
   - US home values +0.10% m/m. P(fall) 0.13 from stats; Argon says 0.21.
   - Likeliest decliners: Charlotte (P 0.90), Baltimore (0.89), San Antonio (0.77), Las Vegas (0.75).
   - Strongest: San Francisco +0.65%, Chicago +0.49%, San Jose +0.48%.

## 1. Data (all free; downloaded files treated as data, read under `python -I`)

| Source | Series | Through | Notes |
|---|---|---|---|
| Freddie Mac PMMS history CSV | 30-year fixed, weekly since 1971 | 2026-10-22 (7.32%) | plus the FRED copy already in `data/` |
| yfinance `^TNX` | 10-year Treasury, daily | 2026-10-23 (4.99%, −11 bp on week) | |
| Zillow research CSVs | ZHVI (home values, smoothed, seasonally adjusted, mid-tier) and ZORI (market rents), 36 largest metros + US | 2026-09 | ZHVI is a 3-month smoothed series (see caveats) |
| Realtor.com research CSV | Metro inventory, days on market, price-cut share | 2024-02..2026-09 | short history (32 months) |
| BLS API v1 (no key) | CPI rent of primary residence `CUSR0000SEHA`, shelter `CUSR0000SAH1` | 2026-09 | v1 caps requests at 10 years; two requests merged |
| treg news (free) | 3 queries: mortgage rates, housing market, rent / CPI shelter | live, 25 Oct | context for Argon only |
| Hunch verticals (Glasser) | Zillow lender quotes, RentCast Austin 78701 | 2026-10-25 snapshot | one snapshot: illustrative, not backtestable |

Gaps:
- **FRED was unreachable all afternoon** (HTTP/2 stream errors, then 150-second timeouts on HTTP/1.1, 3 retries per series).
- That cost two series: S&P Case-Shiller (national, released Tue 27 Oct) and the Optimal Blue daily mortgage index. The daily index would have allowed a true next-day mortgage forecast.
- Both are one rerun away when FRED returns: `data/realestate/fred/`, fetcher at `scratchpad/fred_get.sh`.

## 2. Domino 1 — 10-year Treasury → mortgage rate (weekly)

Measured in `domino/daily_life.py`; reused here with fresh data.

| Model (next week's 30-year rate) | Error vs no-change | DM p | n |
|---|---|---|---|
| TimesFM 3.0 + Treasury covariate | **−26.1%** | — | 565 weeks |
| Treasury regression (Domino) | −13.5% | 3e-6 | 565 weeks |

Further context:
- **Granger:** 10-year weekly change → PMMS change, best lag 2 weeks, p = 2.9e-34.
- **Spread:** PMMS minus the 10-year is 2.37 pp, vs a 2.29 average since 2024 (z = +0.31). That is slightly wide, so there is mild room to compress.
- **This week:** the 10-year fell 11 bp last week and Thursday's survey should follow. TimesFM puts it at **7.28% [7.15, 7.40]**, so P(below 7.32%) = 0.62.
- **Argon's 5-sample ensemble** (live news, thinking high, priority tier) agrees: 7.27% [7.15, 7.39], P = 0.65.

## 3. Domino 2 — market rents → CPI rent (monthly, 13-month lead)

**Why the lead exists:** CPI measures the rent every tenant pays, and most leases reprice only once a year. ZORI measures asking rents on new leases. Today's new leases become the CPI average over the next year.

| Test | Result |
|---|---|
| Cross-correlation, ZORI y/y vs CPI rent y/y | peak at a **13-month** lead: 0.90; contemporaneous 0.13 |
| Granger, ZORI y/y change → CPI rent y/y change | p = 0.005 (lag 3) |
| 12-month-ahead CPI rent y/y, rolling origin 2019-01..2025-08 (n = 80) | market-rent model MAE 1.42 pp vs CPI-only AR 2.49 (**−43%, DM p = 0.04**) vs persistence 1.94 (−27%, p = 0.19) |
| Next monthly print, last 36 months | AR + market rents a year earlier: MAE 0.063 pp vs no-change 0.074 (−15%) |
| Same, TimesFM 3.0 | −20% vs momentum (p = 0.11) |

Forecasts:
- **CPI rent m/m for October** (BLS, mid-November): 0.225% [0.10, 0.35], after 0.246%. P(below 0.30%) = 0.79 from stats; Argon says 0.80.
- **CPI rent y/y for Sep 2027:** 2.91% [2.19, 3.46], from 3.00% now. Market rents are at +2.70% y/y, so official rent inflation keeps drifting down. Argon says 2.80%.
- **US market rent for October** (TimesFM 3.0, which beats momentum by 52% on ZORI): $1,932 [$1,930, $1,934].

## 4. Home values — momentum, and two honest negatives

**Setup:**
- Pooled panel of the 36 largest metros, monthly ZHVI % change.
- Rolling origin over the last 48 months: 2022-10..2026-09, 1,725 metro-months.
- Features known at forecast time only.

| Model (next month's home-value change) | MAE (pp) | vs comparison | DM p |
|---|---|---|---|
| Zero change | 0.335 | — | — |
| Naive momentum (repeat last month) | 0.127 | — | — |
| **AR(2) momentum, pooled** | **0.101** | −20% vs naive momentum | — |
| AR(2) + mortgage-rate changes | 0.109 | **+8.0% vs AR (worse)** | 0.04 |
| AR(2) + price cuts (Realtor.com; 2025-10..2026-09) | 0.061 vs 0.061 | +0.4% vs AR | 0.40 |
| 6-month horizon: momentum + rate change | 2.44 vs 2.40 | +1.8% vs momentum model | 0.90 |
| TimesFM 3.0, US series (36 months) | 714 $ vs 265 $ | +170% vs momentum | 1e-4 |

**Why rates don't help here:**
- The full-sample rate coefficients have the expected sign: −0.035 pp of monthly growth per +1 pp three-month rate rise (p = 0.09), and −1.5 pp of six-month growth per +1 pp (in sample).
- Out of sample, though, the effect is already inside the momentum terms: rates moved first in 2022, and prices have been adjusting slowly ever since.
- At these horizons, the trend you can see this month is the forecast.

**Price cuts:**
- The coefficient is +0.12 pp per share-point, the wrong sign for a distress signal.
- Argon's reading is that sellers cut in seasonally slow months that the model already knows about. That is a hypothesis, not tested.

**October 2026 by metro** (pooled AR momentum; P(fall) uses each metro's own backtest error):

| Metro | ZHVI y/y | Oct forecast | P(fall) | Price-cut share | Days on market | +1 pp rate → 24 months (in sample) |
|---|---|---|---|---|---|---|
| Charlotte | −0.8% | −0.13% | 0.90 | 26% | 64 | −0.6% |
| Baltimore | +0.4% | −0.12% | 0.89 | 22% | 46 | +0.1% |
| San Antonio | −1.9% | −0.07% | 0.77 | 25% | 71 | −3.5% |
| Las Vegas | −2.6% | −0.05% | 0.75 | 25% | 58 | −3.7% |
| Phoenix | −1.1% | −0.02% | 0.58 | 29% | 62 | −1.5% |
| Austin | −4.3% | +0.31% | low | 27% | 80 | — |
| Chicago | +5.0% | +0.49% | 0.00 | 16% | 36 | −0.2% |
| San Jose | +0.2% | +0.48% | 0.04 | 16% | 35 | −1.8% |
| San Francisco | +3.1% | +0.65% | 0.00 | 13% | 37 | −0.7% |
| **US** | **+1.2%** | **+0.10%** | **0.13** | 22% (median metro) | 54 (median) | — |

The 24-month rate-sensitivity column comes from in-sample metro regressions. It ranks metros by how much their prices moved with past rate cycles: Las Vegas and San Antonio most, Baltimore least. It is not an out-of-sample forecast.

**Austin 78701** (RentCast via Glasser, 25 Oct): 306 sale listings, 25 new, 117.75 average days on market, median $657k ($755/sq ft).

Argon's reading: a luxury-skewed downtown condo market that lags the metro's tentative turn. The metro's ZHVI is still −4.3% y/y but positive m/m since the summer, and downtown listings sit about 38 days longer than the metro's 80. That is anecdotal, one ZIP on one day.

## 5. Argon (Gemini 4 Argon, thinking high, priority tier)

The run made six calls: a 5-sample ensemble on the forecasts below, then one metro brief. Inputs were live news, our stats, and Hunch's Zillow and RentCast snapshots. The ensemble is pooled in log-odds.

| Question (pre-registered) | Domino stats | Argon ensemble | Resolves |
|---|---|---|---|
| Freddie 30-year below 7.32% on Thu 29 Oct | 0.62 | 0.65 | Freddie Mac, Thu 29 Oct |
| Freddie 30-year, median [p10, p90] | 7.28 [7.15, 7.40] | 7.27 [7.15, 7.39] | same |
| US home values fall in October (ZHVI m/m < 0) | 0.13 | **0.21** | Zillow, mid-November |
| CPI rent October m/m < 0.30% | 0.79 | 0.80 | BLS, mid-November |
| CPI rent y/y, Sep 2027 | 2.91% | 2.80% | BLS, Oct 2027 |

- **Hash:** `edff892394c3da9f96b92e8b21612265abeb7a7b6a1e8fe19d77edcb1171b0c5` (stats and Argon numbers, `runs/realestate_argon.json`).
- **The one disagreement** is home values. Argon reads the Charlotte, Las Vegas and Baltimore softness, and the 22% price-cut share, as more downside than momentum allows. Momentum won the backtest.
- **Correction, logged:** the first run of the stats side gave P(fall) = 0.002 from an ad-hoc national error scale. It was replaced with a proper national backtest (48 months, MAE 0.077 pp), giving 0.13. Both runs were re-registered; the hash above is the corrected one.

**From Argon's brief** (`runs/realestate_argon.json`; narrative, checked against our numbers):
- **Zillow quote vs Freddie survey** (7.49% vs 7.32%): the gap comes from three structural differences.
  - Timing: Freddie Mac's survey is a weekly average that lags bond moves, while Zillow reprices daily.
  - Points and APR: Zillow's 7.49% quote carries 1.716 points (APR 7.668%).
  - Product mix.
- **What we cannot predict** (Argon's own list matches our negatives): next-month metro prices from price cuts (p = 0.40), and from recent rate changes alone.
- **Chain story** (Argon): "When the 10-year Treasury yield jumps, the first domino falls within two weeks… Sidelined buyers crowd into rentals, lifting ZORI market rents, which lead CPI rent by 13 months (r = 0.90) and reset a renter's lease."
  - Treasury → PMMS and ZORI → CPI rent are measured.
  - "Sidelined buyers crowd into rentals" is the untested link.

## 6. Demo visual: `?profile=real-estate` (key 9 in the switcher)

| Area | What it shows |
|---|---|
| Globe | 12 metros with their October forecast and P(fall), national nodes (10-year, Freddie, spread, momentum, price cuts, CPI rent), Austin 78701 |
| Causal graph | Near-solid edges for measured links: Treasury → PMMS, ZORI → CPI rent → your rent, momentum → metros. Dashed for mechanisms without measured skill: rates → momentum, price cuts → momentum. Fine dashes for anecdotal: Austin 78701 |
| This week · housing | Freddie Thursday and CPI rent October, with 80% bands and the Argon ensemble line |
| Odds | Three head-to-heads, Domino stats vs Argon |
| Price cuts by metro | Realtor.com, Sep 2026 |
| Listings right now | Days on market, cut share, Austin 78701 |
| Your housing ahead | Mortgage next week, rent inflation in Sep 2027, US home value in October |
| Leaderboard | 11 rows of what works and what doesn't |
| Backtest chart | CPI rent y/y vs the market-rent forecast made 12 months earlier |

## 7. Reproduce

```bash
.venv/bin/python -I domino/realestate.py stats      # ~20 s
.venv/bin/python -I domino/realestate.py argon      # 6 Argon calls, ~3 min
<research venv>/bin/python -I domino/realestate.py timesfm --weights <timesfm-3.0 dir>
.venv/bin/python -I domino/profiles_build.py        # all profiles incl. real-estate
```

## 8. Caveats

- **ZHVI smoothing:** ZHVI is a smoothed series, so part of next month's value is already in this month's data. Momentum's edge partly reflects that. The fair claim is "predictable print", not "predictable market".
- **Overlapping windows:** the 12-month-ahead tests overlap. DM uses Newey-West with 12 lags, so p-values are conservative and the persistence comparison is not significant.
- **Short price-cut history:** Realtor.com covers only 32 months, so the price-cut test has 12 test months.
- **Rate sensitivity:** in sample only.
- **Approximations:** P(fall) uses a normal approximation to backtest errors. The national value is backtested directly (48 months).
- **FRED outage:** no Case-Shiller (this week's release) and no daily mortgage index.
