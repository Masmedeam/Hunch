# Gemini 4 Argon usage: RPWM hackathon project

Generated 2026-10-25 15:16 PDT by `tools/argon_usage_report.py` from the project's own logs. Re-run it any time to refresh.

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
| Next-day predictor | Causal graph, event extraction, calibrated forecasts, recursive investigation, narration (in progress) | `domino/` |
| Judge | Three-persona blind judge panel that ranked the demo options | `tools/argon_judges.py` |

## What is not Argon, and why

| Component | Why not Argon |
|---|---|
| numpy / scipy | Free energy, expected free energy, Bayes updates, CIs. The math must be exact, so Argon supplies distributions and numpy computes on them. |
| yfinance, Wikipedia, treg.to, Glasser | Data inputs, not models |
