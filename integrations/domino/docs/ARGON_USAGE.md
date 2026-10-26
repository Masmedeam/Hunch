# Gemini 4 Argon usage: Domino, a next-day world model

Generated 2026-10-25 16:15 PDT by `tools/argon_usage_report.py` from the project's own logs. Re-run it any time to refresh.

## For judges and investors: how Domino uses Argon

Domino predicts what happens next: tomorrow's events, next week's mortgage rate, next month's rents, where to buy property. Gemini 4 Argon is its reasoning layer. Argon reads the evidence, proposes causal links (the "first dominoes"), researches markets that have no data feed, decides whether past predictions came true, and gives calibrated probabilities as 5-sample ensembles. Statistics and Google's TimesFM handle the numeric series. Every Argon output is either scored on outcomes or pre-registered with a hash before the outcome is known.

| At a glance | |
|---|---|
| Live Argon calls | **226** |
| At thinking `high` | 150 (66%) |
| On the Priority tier | 143 (63%) |
| Tokens in / out / thinking | 924,214 / 310,255 / 505,115 |
| Argon time | 175 min, 46 s per call on average (ensembles run in parallel) |
| List-price equivalent | $10.00, about $0.044 per call (hackathon credits) |

### What Argon delivered, measured

| Use | What Argon does | Result | Evidence |
|---|---|---|---|
| Next-day forecasting on Hunch's NEXTDAY benchmark | Reasons over Domino's evidence (SEC filing histories, earnings calendars, posting cadence) and returns calibrated probabilities | Brier 0.192, the best of all entries (Argon alone 0.207, Hunch baseline 0.226); 8-K question 0.153. 10 cases, not yet significant | `runs/hunch_analysis.json` |
| Outcome resolution | Resolved every model's narrative claims against held-out next-day evidence (unmentioned counts as unresolved, not false) | 199 claims (64 yes / 16 no / 119 unresolved). Showed the benchmark's judge does not track correctness: Spearman -0.05 (p = 0.72) | `runs/hunch_claim_scores.json` |
| Benchmark audit | Read Hunch's code, data contracts and results | 6 issues found, e.g. the judge never sees held-out social posts on Q5; deterministic blind IDs with same-model judging; 87% of raw Argon's Brier gain over the baseline is a weekend-calendar artifact on the 8-K question | `analysis/argon_hunch_review.json` |
| Live head-to-head | 5-sample ensemble on live news for Hunch's five pilot questions (cyclone, UK outages, embassies/strikes); statistics for META and YouTube | Pre-registered before the outcome, hash a5118015…; resolves 27 Oct 00:00 UTC | `runs/hunch_pilot_domino.json` |
| Live Domino page | 5-sample ensemble on next-day geopolitical and market events, with the spread shown as uncertainty | 3 live event odds, e.g. US or Israeli strike on Iran, or Iranian strike on US/Israel…: 16% (spread 0.017) | `runs/forecast_latest.json` |
| Housing forecasts | 5-sample ensemble next to the statistical models, on the same questions | P(Freddie 30-yr below last on Thu) 0.65 vs statistics 0.62; P(US home values fall) 0.21 vs 0.13. Pre-registered, hash edff8923… | `runs/realestate_argon.json` |
| Grounded research | Google Search–grounded research with dated sources, for markets that have no data feed | 9 markets researched (incl. Dubai, Abu Dhabi, Almaty, Astana): yields, price and rent trends, financing, foreign-buyer rules, costs, supply | `runs/re_invest_research.json` |
| Social read | Read each market's X, TikTok and YouTube posts and headlines for froth, red flags and demand signals | 9 markets scored for hype and sentiment | `runs/re_invest_social.json` |
| Investment committee | 5-sample ranking from the same evidence as a transparent model, with disagreements explained | Agrees with the transparent model (Spearman 0.73, p = 0.025); top pick Abu Dhabi, verdict buy 5/5. Hash 703fedfc… | `runs/re_invest_rank.json` |
| Where prediction works | Ranked 8 domains by measured next-day predictability and named the first domino in each | #1 macro_stress (score 7.8/10) | `analysis/argon_category_interpretation.json` |

### How we keep Argon honest

- **Scored on outcomes, not impressions.** Brier and MAE on resolved questions; claims checked against held-out evidence.
- **Pre-registered.** Forecasts are hashed before the outcome is known; the hashes are in the result files and on the dashboards.
- **Head-to-head with statistics.** Every Argon probability is shown next to a statistical model on the same question.
- **Evidence labels on every causal link.** Measured (out-of-sample test), mechanism (Argon prior, untested) or anecdotal; links tested without skill are shown as such.
- **Reproducible.** Every call is cached and logged in `runs/argon_ledger.jsonl`, so every number replays offline.

### Where Argon did not beat simple models (reported, not hidden)

- Attention data did not predict next-day market returns, and Argon found no market edge there.
- Daily posting counts: a Poisson model on last week's cadence beat Argon (MAE 0.99 vs 1.30).
- Home values month to month: momentum beats every adjustment; Argon's higher odds of a fall (21% vs 13%) are untested until Zillow's October print.
- Argon-sourced legal claims (e.g. Kazakhstan's title rule for foreign buyers) are flagged for verification, not used as fact.

### Why it matters

- The same loop (collect, reason with Argon, score on outcomes) runs on any domain that has data collectors; Hunch's collectors already cover news, social, markets, housing, jobs and prices.
- Every prediction carries its evidence class and a pre-registration hash, so accuracy can be audited after the fact.
- Cost scales with calls: about $0.044 per Argon call at list price, so a 5-sample ensemble costs about $0.22.

## Rule

Every model call made by this project's code uses `gemini-4-argon`.

Since about 11:50 PDT, every call also runs at the most performant settings available: `thinking_level: high` and the Priority inference tier (`service_tier: priority`, billed at 75-100% above standard). These are the defaults in `rpwm/argon.py`; there is no economizing.

- Code audit: `grep -rE 'gemini-[0-9a-z.-]+' --include='*.py'` finds only `gemini-4-argon` in runtime paths. The one exception is a price table in an old probe script.
- Before the rule (10:50 PDT), one capability probe touched Flash, Robotics-ER, and embeddings once each. Those calls are excluded below.

## Totals

| Metric | Value |
|---|---|
| Argon calls made (live) | **226** |
| Calls served from the record/replay cache | 0 |
| Input tokens | 924,214 |
| Output tokens | 310,255 |
| Thinking tokens | 505,115 |
| Argon wall time | 174.7 min |
| List-price equivalent | $10.00 (covered by hackathon credits) |
| Ablation episodes run with Argon in the loop | 12 |

## By component

| Component | Live calls | Cached | Input tok | Output tok | Thinking tok | Seconds |
|---|---|---|---|---|---|---|
| Forecasting | 54 | 0 | 157,031 | 65,607 | 148,577 | 2625 |
| Real estate analysis | 47 | 0 | 284,199 | 154,700 | 235,265 | 4707 |
| Hunch / NEXTDAY analysis | 27 | 0 | 364,545 | 44,775 | 78,855 | 1348 |
| Recursive refinement | 27 | 0 | 27,870 | 10,426 | 3,099 | 221 |
| Perception (vision) | 16 | 0 | 21,152 | 1,794 | 0 | 90 |
| Planning (L2) | 14 | 0 | 6,006 | 2,927 | 1,179 | 104 |
| Capability probes | 11 | 0 | 6,574 | 532 | 520 | 123 |
| Narration | 11 | 0 | 3,589 | 1,148 | 13,011 | 244 |
| Memory consolidation | 7 | 0 | 1,698 | 240 | 0 | 37 |
| Judge panel (3 personas) | 3 | 0 | 0 | 0 | 0 | 281 |
| Category analysis | 2 | 0 | 19,467 | 7,087 | 8,163 | 195 |
| Child sub-goal recursion | 2 | 0 | 778 | 226 | 87 | 11 |
| Demo script draft | 1 | 0 | 6,841 | 4,432 | 7,888 | 134 |
| Daily-life analysis | 1 | 0 | 4,279 | 5,387 | 5,143 | 135 |
| World-model compile | 1 | 0 | 801 | 897 | 0 | 11 |
| Managed Agent (slow level) | 1 | 0 | 5,748 | 15 | 20 | 70 |
| Paper ingest (native PDF) | 1 | 0 | 13,636 | 10,062 | 3,308 | 150 |

## By thinking level (live calls)

| Level | Calls |
|---|---|
| low | 61 |
| medium | 14 |
| high | 150 |
| agent | 1 |

## By service tier (live calls)

| Tier | Calls |
|---|---|
| priority | 143 |
| standard | 83 |

## Where Argon sits in the product

| Role | What Argon does | Code |
|---|---|---|
| Reader | Ingests the RPWM paper natively as PDF and returns equations, claims, issues, and an executable spec | `tools/argon_ingest.py` |
| Eyes | Reads rendered frames and reports object positions | `rpwm/agent.py: perceive` |
| World model | Writes the likelihood tables P(outcome \| action, hypothesis) that the exact Bayesian math runs on | `rpwm/agent.py: compile_world_model` |
| Planner | Orders sub-goals (L2) and proposes child sub-goals when stuck (recursion) | `plan_order`, `child_subgoal` |
| Self-correction | Revises its world model under surprise, thinking low → medium → high, gated by the free-energy stopping rule | `refine` |
| Slow level | Managed Agent (Antigravity) on Argon: sandbox analysis plus a `recurse` tool that calls back into the fast loop | `rpwm/slow_agent.py` |
| Memory | Writes lessons into semantic memory after each episode | `run → consolidate` |
| Forecaster | 5-sample ensembles pooled in log-odds for next-day and next-week questions; pre-registered | `domino/live.py`, `domino/hunch_extended.py`, `domino/realestate.py` |
| Causal graph | Proposes the links between drivers, channels and outcomes; statistics test them | `domino/live.py`, `domino/realestate_dashboard.py` |
| Evidence resolver | Decides whether claims came true against held-out evidence | `domino/hunch_extended.py resolve` |
| Researcher | Google Search–grounded research with dated sources where no data feed exists | `domino/realestate_invest.py research` |
| Analyst | Reads social posts and headlines for froth, red flags and demand | `domino/realestate_invest.py social` |
| Investment committee | Ranks markets from the same evidence as a transparent model | `domino/realestate_invest_rank.py` |
| Auditor | Reviewed Hunch's benchmark code and data | `tools/argon_hunch_ingest.py` |
| Judge | Three-persona blind judge panel that ranked the demo options | `tools/argon_judges.py` |

## What is not Argon, and why

| Component | Why not Argon |
|---|---|
| numpy / scipy | Free energy, expected free energy, Bayes updates, CIs. The math must be exact, so Argon supplies distributions and numpy computes on them. |
| TimesFM 3.0 (Google) | Numeric next-step forecasts for weekly and monthly series; Argon reasons, TimesFM extrapolates |
| yfinance, Wikipedia, treg.to, Glasser, Zillow, Realtor.com, BLS, Freddie Mac | Data inputs, not models |
