# Domino · Where to invest in real estate (Dallas, Austin, Houston, San Antonio, Miami, Dubai, Abu Dhabi, Almaty, Astana)

Built 2026-10-25, 14:40–15:15 PDT, for a USD-based buy-to-let investor over a 12-month horizon.
- **Code:** `domino/realestate_invest.py` (collect · glasser · research · social) and `domino/realestate_invest_rank.py` (zips · rank).
- **Dashboard:** `http://127.0.0.1:8100/?profile=real-estate`, which redirects to `/realestate`. Add `&classic=1` for the full Domino view.
- **Screenshot:** `runs/screens/151505/ui_realestate.png`.
- **Pre-registered hash:** `703fedfc2aee903bc5d7d07e2e7c5c2810a9cc254b7a2879528bb464cfd80f2c` (`runs/re_invest_rank.json`).
- **Disclaimer:** this is research, not investment advice.

## 0. Bottom line

| # | Market | Gross yield | Net yield | Prices 12 m | Model 12 m (USD) | Argon 12 m [p10, p90] | Argon verdict (votes) |
|---|---|---|---|---|---|---|---|
| 1 | **Abu Dhabi** | 6.9% | 4.3% | +24.1% | +15.3% | **+9.2% [1.5, 16]** | **buy** (5/5) |
| 2 | Astana | 10.3% | 7.7% | +9.7% | +11.9% | +3.2% [−12, 14.5] | hold (4/5) |
| 3 | Almaty | 8.7% | 6.4% | +7.9% | +9.5% | +1.4% [−13.5, 11.5] | avoid (3/5) |
| 4 | Miami | 6.7% | 0.5% | +0.3% | −0.2% | −2.4% [−9, 4.5] | hold (3/5) |
| 5 | Dubai | 6.7% | 4.0% | −4.5% | 0.0% | −2.6% [−11.5, 5] | avoid (3/5) |
| 6 | **Dallas–Fort Worth** | 5.6% | −0.1% | −2.0% | −1.9% (metro) | **+1.8% [−6, 6.5]** | **accumulate** (5/5): selected ZIPs, all cash |
| 7 | Austin | 4.6% | −0.2% | −4.3% | −2.2% | −4.2% [−11, 2] | avoid (5/5) |
| 8 | Houston | 6.5% | 0.2% | −1.8% | −2.0% | −2.1% [−8.5, 3] | avoid (4/5) |
| 9 | San Antonio | 6.2% | 0.5% | −1.9% | −2.1% | −3.5% [−10, 2] | avoid (5/5) |

**How the two sides compare.** The transparent model and Argon's 5-sample ranking agree well on the order: Spearman 0.73, p = 0.025.

Where Argon disagrees, it says why:
- **Abu Dhabi:** Argon haircuts the model's +15% to +9%. Half of a +24% trailing year is too much to extrapolate.
- **Dallas:** Argon goes *up* from the metro average. The metro is a mix, and the high-yield Fort Worth and East Dallas ZIPs clear the roughly 4.5% Texas tax and insurance drag.
- **Kazakhstan:** Argon goes sharply down, for three reasons:
  - **Ownership rules:** its sources say non-resident foreigners need a permanent residence permit to register an apartment.
  - **Mortgages:** loans cost 19.5%.
  - **Currency:** the tenge moved 13% against the dollar in a year.
- **Austin:** Argon goes down further. It argues, fairly, that the model annualises a one-month bounce.

**Argon's pick** (from the ensemble):
- **Abu Dhabi:** completed, prime freehold units in designated Investment Zones.
- **Fort Worth ZIP 76164:** selective all-cash accumulation.
  - 11.2% gross yield on Zillow, 9.7% on RentCast.
  - $208k median price.
  - Rentals lease in a median 4 days (RentCast).
- **No debt anywhere:** leverage is negative in all 9 markets. Mortgage rates exceed net yields: UAE 5.25%, US 7.3%, Kazakhstan 19.5%.

## 1. Data: every collector Hunch configures, pointed at these markets

**The Hunch bundle.** The live bundle was re-downloaded at 14:40 to `external/hunch_live/20261025_144017/bundle.json`. It is byte-identical to our copy (SHA-256 `e7f116cf…`).
- It holds social and news data: X, TikTok and YouTube search, trends and details, plus news text.
- It holds 10 cached verticals: AAA gas and EV charging, Zillow lender quotes, RentCast Austin 78701, insider ratios, premarket movers, Wellfound, Keepa and Carfax.
- It holds the benchmark's price bars, SEC filings and Exa articles.
- Its Zillow, Airbnb and LinkedIn verticals are *configured but disabled* (`enabled: false`), so it contains no LinkedIn or Airbnb data. We ran those collectors ourselves:

| Hunch collector (provider:endpoint in `ui/worker.js`) | How we ran it | What came back |
|---|---|---|
| LinkedIn jobs (`apify /harvestapi/linkedin-job-search`) | treg `harvestapi.linkedin.search.jobs` (same actor), 4 queries per market | jobs posted this week: Dallas 59,911 · Houston 49,596 · Austin 45,830 · Miami 42,923 · San Antonio 39,116 · Dubai 5,881 · Abu Dhabi 3,307 · Almaty 236 · Astana 114 (LinkedIn is little used in Kazakhstan, so compare within a country) |
| LinkedIn company (`scrapecreators /v1/linkedin/company`) | Glasser `tikhub …/get_company_profile`, with HQ-checked slugs | Emaar 1,701,426 followers, 16,691 staff on LinkedIn · Aldar 536,454 / 9,889 · Invitation Homes 50,012 / 1,447. BI Group and D.R. Horton did not resolve to the right company and were dropped |
| Airbnb (`apify /tri_angle/airbnb-scraper`) | Glasser, with Hunch's settings (check-in +14 days, 3 nights, 2 adults, USD) | 20 listings per market. Median effective nightly rate: Dallas $123 · Austin $143 · Houston $146 · San Antonio $144 · Miami $175 · Dubai $175 · Abu Dhabi $180 · Almaty $50 · Astana $48 |
| Zillow (`/get_mortgage_rates`, `/search_agents`) | Glasser | 9 lender quotes; agents for Dallas and Austin |
| RentCast (Hunch's `rentcast_market`) | Glasser `market_data` → `market_stats` | 76164: median sale $208k, rent $1,677, rentals lease in 4 days (median) · 78731: $970k vs $1,495 rent (1.8% gross) · 78734: $600k, 495 listings, 98 days on market (median) |
| Wellfound (`/get_trending_jobs`) | Glasser | 5 trending startup roles |
| X, TikTok, YouTube, news | treg (`anyapi`, `crawl4ai`, dated news) | 543 posts and videos, 100 headlines; Argon read them for froth (§3) |
| Markets | yfinance | Emaar −22% over 1 year · D.R. Horton −6% · Invitation Homes flat · Kaspi +31% · USD/KZT −13% (tenge stronger) · AED pegged |
| AAA gas, insider ratios, premarket movers, Keepa, Carfax | Hunch's cache | not used for housing (Carfax and Keepa are irrelevant here) |

Other sources:
- **Zillow and Realtor.com research data** (free downloads), covering metros and ZIPs; Freddie Mac; BLS.
- **Gemini 4 Argon grounded research** (Google Search tool, thinking high, priority tier): one call per market, with dated sources, covering:
  - yield, price and rent trends, mortgage rates;
  - foreign-buyer rules, transaction and holding costs;
  - supply, short-term-rental occupancy and daily rates.

**Spend:**
- Glasser $0.73; balance $0.27 left from $1.00. A RentCast re-run was billed again, so later runs read RentCast from the cassette.
- treg about $0.08.

## 2. Method

**Transparent model** (each input is visible in `runs/re_invest_rank.json`):
- *net yield* = gross yield × (1 − 20% vacancy, management and maintenance) − annual holding costs (Argon-sourced: Texas about 4–5% including insurance, UAE 1.2–1.35%, Kazakhstan 0.55%).
- *appreciation* = half of recent momentum. US: 50/50 of the last 12 months and our next-month forecast annualised. Abroad: the reported last 12 months.
- *FX* = 0 expected (currencies are close to a random walk); the size of last year's swing counts as risk.
- *entry and exit* = round-trip transaction costs ÷ 5 (a 5-year hold).
- *risk* (0–1) = mean of: P(prices fall next month) and the share of listings with price cuts (US); Argon's social hype score; the FX swing; supply and red flags.
- *risk-adjusted* = expected − 4 × risk.

**Argon** saw the same table plus every collector's output and returned these for each market:
- expected 12-month USD return with p10 and p90, risk, and a verdict;
- what it is best for, the first domino, and what would change its mind.

It ran as 5 samples; numbers were pooled by median and verdicts by majority.

**Two corrections made during the run** (logged here for transparency):
1. The first model carried half of the tenge's +13% year against the dollar forward as an expected gain of +6.6 pp. Currencies don't trend reliably, so the expectation is now 0 with the swing counted as risk.
2. The ranking prompt was cut at 30k characters, which dropped Houston and San Antonio. It now uses an explicit market key and trimmed text.

## 3. What the collectors say, market by market

- **Abu Dhabi:**
  - +24.1% prices and +4.7% rents over 12 months (ValuStrat, Savills, ADREC; dated Q2–Q3 2026).
  - Foreign freehold is allowed in 50 Investment Zones, up 8 in 2026. Loans cost 5.25%.
  - Airbnb median $180 a night. Argon's sourced figures (61% occupancy) imply about 12.6% gross short-term-rental yield before fees.
  - Social hype 0.62 with sentiment +0.78, the most bullish chatter. Aldar has 536k LinkedIn followers.
  - Risk: a hot market priced on momentum.
- **Dubai:**
  - Prices −4.5% and rents −6.8% (ValuStrat, REIDIN, Property Monitor); Emaar's shares are −22% over the year.
  - Hype is the highest of the 9 markets (0.72): broker promotion against growing macro skepticism.
  - The supply pipeline is the risk. Argon: avoid for new entries.
- **Almaty and Astana:**
  - The highest yields: 8.7% and 10.3% gross. Rents +17% and +21%, prices +8% and +10% (BNS, Krisha.kz, Halyk Finance).
  - **But** mortgages cost 19.5%, and the tenge swung 13% against the dollar in a year.
  - **Ownership rules:** Argon's grounded sources say a non-resident foreigner needs a Kazakh permanent residence permit (VNZh) to register an apartment. This is *Argon-sourced*; verify with local counsel before acting.
  - LinkedIn barely covers Kazakhstan's job market, so it is no signal there. Airbnb is about $50 a night.
- **Dallas–Fort Worth:**
  - Metro gross yield 5.6% (Zillow). The roughly 4.5% Texas tax and insurance drag makes the metro-wide net yield about zero.
  - It is a mixed market. The best ZIPs clear 9–11% gross:

    | ZIP | Gross yield | Prices 12 m | Model 12 m |
    |---|---|---|---|
    | 76164 Fort Worth | 11.2% | +0.3% | +6.1% |
    | 75223 East Dallas | 10.1% | −0.1% | +5.4% |
    | 76104 Fort Worth | 9.8% | +0.1% | +5.0% |
    | 76114 River Oaks | 9.1% | +0.7% | +3.9% |

  - RentCast confirms 76164: rentals lease in a median 4 days, a sign of real tenant demand.
  - Dallas also has the most new LinkedIn jobs of the 9 markets (59.9k this week).
- **Austin:**
  - Prices −4.3%, yields 4.6%. No ZIP's model return clears 1%.
  - RentCast 78734: 495 listings sitting a median 98 days.
  - Hype is the lowest (0.35, "no speculative froth"). That is a sign of a working-through market, not a bargain yet. Argon: avoid; patient capital waits 6–12 months.
- **Houston and San Antonio:** decent gross yields (6.2–6.5%), but falling prices. San Antonio has the highest risk score (0.73) and the only negative US rents (−0.7%). Avoid.
- **Miami:** thin net yield (0.5%) after Florida tax and insurance; the market is split. Hold.

## 4. Caveats

**Data quality:**
- **Where the numbers come from:** US figures are measured (Zillow ZIP and metro data, Realtor.com, RentCast). Abroad, they are Argon-grounded published figures; each market's sources are in `runs/re_invest_research.json`.
- **ZIP yields:** Zillow's home-value and rent series cover different housing stock, so ZIP yields are noisy. We keep ZIPs with 3–12% gross yields and home values ≥ $150k, and cross-checked the top picks with RentCast.
- **Airbnb sample:** 20 listings, a 3-night stay two weeks out. Treat it as a rate check, not occupancy. Argon's sourced daily rates match ours for Dubai and Kazakhstan; US sources run higher (larger homes, cleaning fees).
- **LinkedIn counts:** these are LinkedIn's own approximate totals, and LinkedIn's reach differs by country.

**Modeling choices:**
- **Momentum:** annualising a one-month momentum forecast overstates rebounds, as Argon noted for Austin. A 12-step decaying forecast would be the better next version.
- **Taxes:** simplified. Texas non-homestead property tax is about 2–2.5%, and insurance is high on the Gulf coast.

## 5. Reproduce

```bash
.venv/bin/python -I domino/realestate_invest.py collect     # treg + Glasser collectors (~$0.4 Glasser at today's prices)
.venv/bin/python -I domino/realestate_invest.py glasser     # re-poll Glasser Runs (idempotent: no second charge)
.venv/bin/python -I domino/realestate_invest.py research    # 9 grounded Argon calls (Google Search)
.venv/bin/python -I domino/realestate_invest.py social      # 9 Argon social readings
.venv/bin/python -I domino/realestate_invest.py zips        # Zillow ZIP screen + RentCast (cassette first)
.venv/bin/python -I domino/realestate_invest.py rank        # model + 5-sample Argon ranking + hash
.venv/bin/python -I domino/profiles_build.py                # rebuilds every profile and profiles/real-estate/dashboard.json
```
