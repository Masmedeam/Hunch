# Hunch × Domino

**Next-day forecasting and headquarters intelligence on Gemini 4 Argon. Every prediction is grounded in live, auditable evidence and scored against what actually happened.**

*Gemini 4 Argon SF Hackathon (Cerebral Valley × Google DeepMind, SHACK15, 25 October 2026). Track 1: Million Token Engineering.*

**Live links:**
- [Observatory](https://nextday-prediction.hidden-pond-5e6a.workers.dev)
- [5-slide pitch](https://nextday-prediction.hidden-pond-5e6a.workers.dev/pitch/)
- [Pre-loaded HQ demo](https://nextday-prediction.hidden-pond-5e6a.workers.dev/?hq=1)
- [Domino 3D world model](https://nextday-prediction.hidden-pond-5e6a.workers.dev/domino/)
- [Real estate dashboard](https://nextday-prediction.hidden-pond-5e6a.workers.dev/realestate)
- Layout mocks: [V1](https://nextday-prediction.hidden-pond-5e6a.workers.dev/realestate/mock?v=1), [V2](https://nextday-prediction.hidden-pond-5e6a.workers.dev/realestate/mock?v=2), [V3](https://nextday-prediction.hidden-pond-5e6a.workers.dev/realestate/mock?v=3) (add `&theme=white` or `&theme=offwhite` for the white and off-white versions)
- [Repository](https://github.com/Masmedeam/Hunch)

## Inspiration

Companies decide where to put a headquarters, and investors bet on where companies will move, using data that is months old.
- Site-selection reports cost hundreds of thousands of dollars and rest on lagging census tables.
- By the time a lease disclosure reaches a press release or an SEC filing, the market has already moved.
- The true leading indicators are scattered across tens of thousands of noisy records: job posts, rents, mortgage quotes, fuel prices, filings, multilingual news and social chatter.

We wanted one system that reads all of it, predicts what happens next, and proves whether it was right.

## What it does

### Hunch: the forecasting and evidence engine

**Collection.** Hunch collects live evidence from 12 verticals through the Glasser API gateway: LinkedIn, Wellfound, Zillow, RentCast, Airbnb, AAA gas and EV charging, SEC 8-K and Form 4 filings, equity prices, Exa news in English, Japanese, Portuguese and Arabic, X and YouTube. That came to 545 paid runs and 32,490 records for $2.41.

**Temporal quarantine.** It separates when something was published from when it was captured, so no forecast can see the future. 28 live blogs edited after the cutoff were quarantined, and 526 exact-counter velocity intervals were computed.

**Forecasting.** Gemini 4 Argon (1,048,576-token context, about 72.8K tokens per pass) turns the evidence into:
- schema-validated probabilities with 80% intervals and resolution rules;
- next-day forecasts;
- a ranked list of headquarters cities.

Austin leads for a corporate and operations HQ at 82% [74%, 89%]. San Francisco leads for frontier AI R&D. New York, Tokyo, Mumbai and London follow for their archetypes.

**Benchmark.** A frozen 10-cutoff benchmark (14–23 Oct, 50 questions over 5 tracks) compares Argon with three Gemini models and a persistence baseline.
- Argon has the best calibration: Brier 0.1759 vs 0.2060, 14.6% lower error.
- It scored 3.98/5 from a blinded judge.

### Domino: the world model and the verification loop

Domino (`integrations/domino/`) sits on top of Hunch and asks three questions of every prediction.

**1. Did it come true?**
- Argon resolved all 199 narrative claims from the benchmark against held-out next-day evidence.
- The judge's scores did not track correctness (Spearman −0.05), but they did track how specific a claim sounded (+0.50). So Domino reports outcome metrics next to the judge.
- On the benchmark's yes/no questions, Argon fed Domino's evidence (SEC filing histories, earnings calendars) did best: Brier 0.192, vs 0.207 for Argon alone and 0.226 for the baseline. This is 10 cases and not yet significant.

**2. What is the first domino?**
- Every forecast comes with a causal chain, and each link is labelled measured, untested or anecdotal.
- Two chains are measured out of sample:
  - The 10-year Treasury leads mortgage rates by two weeks (Granger p = 3e-34). TimesFM cuts forecast error 26%.
  - Market rents lead official rent inflation by 13 months (r = 0.90), cutting 12-month-ahead error by 43%.

**3. Should you lease or buy?**
- A real estate screen covers nine markets: Dallas, Austin, Houston, San Antonio, Miami, Dubai, Abu Dhabi, Almaty and Astana.
- It combines Zillow, Realtor.com, RentCast, Airbnb and LinkedIn data with Argon research grounded in Google Search.
- Argon's ranking agrees with a transparent scoring model (Spearman 0.73).

**Combined with Hunch's HQ call, the result is concrete.** Austin ranks #1 for an operations HQ, but Domino says lease, don't buy:
- home values are still down 4.3% over the year;
- financing costs exceed rental yields in all nine markets.

**Pre-registration.** Forecasts are hashed before the outcome is known. Examples are the head-to-head on Hunch's five live pilot questions (resolving 27 Oct) and next week's mortgage rate.

### Visuals

**The Observatory** includes a 3D Hotspots tab with walkable World Labs office renders for Dallas, Astana and Salt Lake City.

**Domino adds:**
- a 3D globe and causal graph across nine dashboard profiles;
- a real estate dashboard;
- three simplified layouts (map-first, linked views, causal flow), each in dark, white and off-white.

## How we built it

**Pipeline:**

| Stage | What runs |
|---|---|
| Collection | An idempotent, budget-guarded Glasser collector (HTTPS only, worst-case fee reservation), with treg.to for dated news, LinkedIn job counts and social search |
| Normalization | Into SQLite and JSONL, with leakage auditing |
| Forecasting | Argon forecasts plus a blinded multi-model judge |
| Domino | Outcome resolution, statistical and TimesFM 3.0 models, Argon ensembles, dashboards |

**How we use Gemini 4 Argon:**
- **Settings:** thinking `high` and the Priority tier on every call since the rule took effect; structured JSON schemas; Google Search grounding for research.
- **Roles:** forecaster, evidence resolver, researcher, social analyst, investment committee, benchmark auditor and judge.
- **Ensembles:** 5-sample, pooled in log-odds.
- **Volume:** Domino alone made 226 logged Argon calls (924K input, 310K output and 505K thinking tokens; about 175 minutes; $10 at list price). Every call is cached and replayable.

**Stack:** Python (numpy, pandas, scipy, statsmodels), a Cloudflare Worker with GitHub Actions deploys, FastAPI, and Globe.gl with 3d-force-graph.

## Challenges

- **Temporal leakage.** Live blogs are edited after the fact, and social counters only ever go up, so keeping the future out of past forecasts took a dedicated quarantine layer.
- **Judging prose fairly.** A capable LLM judge rewarded specificity, not accuracy. We added outcome resolution so "sounds right" and "was right" are measured separately.
- **Scale and freshness.** Every source refreshes on a different clock: daily mortgage quotes, monthly rents, weekly job counts, minute-level social posts.
- **Live-demo reliability.** We used one WebGL context per page, drew land as vector paths and drew the causal graph in SVG, so the dashboards render on any laptop.

## Accomplishments

- A leakage-audited benchmark where Gemini 4 Argon has the best calibration among four Gemini models and a baseline.
- Two causal chains measured out of sample, which drive cost-of-living forecasts for any HQ city.
- Every Domino number traces to an evidence file, and every forecast is pre-registered, so the track record can be audited.
- A deployed Observatory that judges can open now, with the world-model dashboards integrated.

## What we learned

- Argon is strongest at reasoning over evidence: reading, resolving, researching and explaining.
- Simple statistics still win on clean numeric series, such as posting cadence and home-value momentum.
- The best results came from combining the two and showing them side by side.
- Outcome scoring changes the conclusions, and judge scores alone are not enough.

## What's next

- **Office data:** a licensed feed for office rents and vacancy, so lease-versus-buy uses office yields, not residential ones.
- **More inputs:** salary bands and flight connectivity.
- **HQ scorecard:** for each city, the three-year cost of a 200-person team and the odds of an overrun.
- **Continuous monitoring:** Argon Managed Agents that watch each city's first dominoes (rates, rents, currency, supply) and alert when one moves.
- **Track record:** score the pre-registered forecasts as they resolve, and publish the record.

## Built with

| Category | Tools |
|---|---|
| Models | Gemini 4 Argon; TimesFM 3.0 |
| Data gateways and collectors | Glasser; treg.to |
| Data sources | Exa; Zillow; RentCast; Realtor.com; BLS; Freddie Mac; SEC EDGAR; AAA |
| Infrastructure | Cloudflare Workers; GitHub Actions |
| Software | Python; FastAPI; Globe.gl; 3d-force-graph; World Labs |
