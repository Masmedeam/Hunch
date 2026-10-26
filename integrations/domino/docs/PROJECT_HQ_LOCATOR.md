# Domino HQ: predicting the best market to lease or build a new headquarters

**Domino HQ uses Gemini 4 Argon as a prediction engine to rank cities for a new headquarters.** It ranks them on what the next three years will cost and deliver, not on last year's reports, and it shows the evidence and odds behind every call.

## The problem

Choosing a headquarters city is a multi-year, multi-million-dollar bet. Companies usually make it from consultant reports that are months old.

Yet the things that decide whether the bet pays off move every month:
- office and housing costs;
- hiring competition;
- financing rates;
- currencies, regulation and supply.

A city that looked cheap in last spring's report can be the expensive choice by the time the lease is signed.

## What it does

For each candidate city, Domino HQ forecasts the next 12 to 36 months on five questions:

1. **Talent:** can we hire here? Job-posting volume and trend on LinkedIn and Wellfound show the talent pool and how hard competitors are hiring.
2. **People cost:** what will employees pay to live here? It forecasts market rents, home values and mortgage rates.
3. **Space cost:** what will the office cost to lease or to buy? It uses Argon-researched office rents and vacancy with dated sources, plus local financing costs, to frame lease versus buy.
4. **Cost of doing business:** travel and running costs. Airbnb nightly rates stand in for business-travel cost, alongside property taxes, insurance and transaction costs.
5. **Risk:** currency swings, regulation, foreign-ownership rules, construction waves, and froth in public chatter.

The output is a ranked shortlist. Each city gets:
- a probability band;
- a verdict: lease now, buy, wait or avoid;
- the causal chain behind it. For example: *10-year Treasury → mortgage rates (two-week lead) → employee housing costs*, and *market rents → official rent inflation (13-month lead)*.

## How Argon makes the predictions

Argon is the reasoning layer. Statistics and Google's TimesFM 3.0 handle the numeric series, and every Argon output is checked against them.

| Role | What Argon does |
|---|---|
| Researcher | Uses Google Search with dated sources for what no data feed covers: office vacancy, incentives, foreign-ownership rules, supply pipelines |
| Forecaster | Runs 5-sample ensembles pooled in log-odds for questions like "Will market rents rise more than 5% in 12 months?", shown next to a statistical model of the same question |
| Causal mapper | Proposes how drivers flow through channels to outcomes. Statistics test each link, which is then labelled measured, untested or anecdotal |
| Analyst | Reads job postings, X, TikTok, YouTube and news for demand signals and froth |
| Committee | Ranks cities from the same evidence as a transparent scoring model, and explains every disagreement |

**How the calls run:**
- Every call uses thinking `high` on the Priority tier, and is cached and logged.
- Forecasts are hashed before outcomes are known (pre-registered), then scored as data arrives.
- At list price an Argon call costs about $0.044. A full pass for one city costs roughly $0.35: grounded research, a social read, a 5-sample ensemble, and its share of the ranking.

## What already works (built at the hackathon)

**Collectors live for nine markets.** Dallas–Fort Worth, Austin, Houston, San Antonio, Miami, Dubai, Abu Dhabi, Almaty and Astana are fed through Hunch's collector stack on treg.to and Glasser:
- LinkedIn jobs, Airbnb, Zillow, RentCast, Wellfound;
- X, TikTok, YouTube and news;
- Zillow, Realtor.com, BLS and Freddie Mac data.

**Measured, out-of-sample chains:**
- **Treasury → mortgage rates:** Granger p = 3e-34 at a two-week lead. TimesFM cuts forecast error 26% against no-change.
- **Market rents → official rent inflation:** a 13-month lead with r = 0.90. Forecast error 12 months ahead is 43% lower than using the series' own history.

**The ranking engine.** The Argon committee agrees with the transparent scoring model (Spearman 0.73, p = 0.025). Behind it sit nine grounded research calls and nine social readings. All 226 Argon calls are documented in `docs/ARGON_USAGE.md`.

**Dashboards.** A globe with causal links and three layouts, each in dark, white and off-white, merged into the Hunch repository.

## Today's signals (live run, 25 October 2026)

| City | LinkedIn postings this week | Airbnb median night | Rents, 12 m | Home values, 12 m | Local mortgage rate | Watch |
|---|---|---|---|---|---|---|
| Dallas–Fort Worth | 59,911 | $123 | +0.7% | −2.0% | 7.3% | Largest talent signal, cheapest travel; Texas property tax and insurance ≈ 4.5% a year |
| Houston | 49,596 | $146 | +0.1% | −1.8% | 7.3% | Flat rents |
| Austin | 45,830 | $143 | +0.7% | −4.3% | 7.3% | Home values still falling |
| Miami | 42,923 | $175 | +1.8% | +0.3% | 7.3% | High insurance and tax drag |
| San Antonio | 39,116 | $144 | −0.7% | −1.9% | 7.3% | Only US market with falling rents |
| Dubai | 5,881 | $175 | −6.8% | −4.5% | 5.25% | Largest housing delivery wave in a decade |
| Abu Dhabi | 3,307 | $180 | +4.7% | +24.1% | 5.25% | Fastest price growth; more freehold zones open to foreign buyers |
| Almaty | 236 | $50 | +17.3% | +7.9% | 19.5% | Thin LinkedIn coverage; 13% currency swing in a year |
| Astana | 114 | $48 | +21.4% | +9.7% | 19.5% | As Almaty; foreign-ownership rules flagged for legal review |

**How to read the table:**
- LinkedIn counts are LinkedIn's own approximate totals, and coverage varies by country (it is thin in Kazakhstan).
- US rents and home values are measured from Zillow.
- Rents and prices outside the US are published figures that Argon sourced, each with its date and source.

**One signal already stands out.** In all nine markets, local mortgage rates exceed net residential rental yields. That points to leasing rather than buying an HQ building today, unless paying cash. Office yields will replace the residential proxy once office data is connected.

## Honest limits

- **Office data:** office-lease rents and vacancy are not yet a live feed. Argon researches them with sources today, and a licensed feed is next.
- **Missing inputs:** salary bands and flight connectivity are not collected yet.
- **Track record:** it starts now. Forecasts are pre-registered and scored as outcomes arrive.
- **Legal and tax rules:** these come from Argon (for example, foreign ownership in Kazakhstan) and are flagged for verification by counsel.
- **Not advice:** this is a research tool, not investment, legal or tax advice.

## What's next

**More data and candidates:**
- Office listings and vacancy, salary bands, flights, and tax incentives.
- More candidate cities. Hunch's 3D Hotspots tab already shows walkable office renders for Dallas, Astana and Salt Lake City; Domino HQ adds the prediction behind which one to pick.

**An HQ scorecard for each city:**
- lease versus buy;
- the three-year cost of a 200-person team;
- the probability of a cost overrun.

**Continuous monitoring.** Argon Managed Agents watch each city's first dominoes (rates, rents, currency, supply) and alert when one moves.

## Built with

| Layer | Tools |
|---|---|
| Models | Gemini 4 Argon (thinking `high`, Priority tier, Google Search grounding); TimesFM 3.0 |
| Data | Hunch's collectors via treg.to and Glasser; Zillow, Realtor.com, BLS and Freddie Mac data |
| Software | Python (numpy, pandas, scipy, statsmodels); FastAPI; Globe.gl |
