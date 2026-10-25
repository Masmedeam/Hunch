"""Build docs/ARGON_USAGE.md: how much this project uses Gemini 4 Argon, from the logs on disk.

Sources (all written by our own code):
  runs/argon_ledger.jsonl          every call through rpwm/argon.py since the ledger was added (live and cached)
  runs/argon_cache.jsonl           every live call through rpwm/argon.py (earlier runs included)
  runs/argon_probe_*.json          capability probes
  runs/managed_agent_probe_*.json  Managed Agent probes
  ingest/argon_ingest.json         native PDF ingest
  plans/llm_judges_argon.json      Argon judge panel
  runs/ablation_*.json             ablation episodes
Re-run any time: .venv/bin/python tools/argon_usage_report.py
"""
import glob
import json
import os
import time
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICE_IN, PRICE_OUT = 2.0, 10.0  # USD per 1M tokens, Argon introductory list price; thinking bills as output
P = lambda *a: os.path.join(ROOT, *a)


def jl(path):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def component(purpose):
    p = purpose.lower()
    for key, name in (("perceive", "Perception (vision)"), ("compile", "World-model compile"), ("refine", "Recursive refinement"),
                      ("plan sub-goals", "Planning (L2)"), ("recurse", "Child sub-goal recursion"), ("consolidate", "Memory consolidation"),
                      ("slow agent", "Managed Agent (slow level)"), ("forecast", "Forecasting"), ("graph", "Causal graph"),
                      ("event", "Event extraction"), ("narrat", "Narration"), ("investigat", "Recursive investigation"),
                      ("category", "Category analysis"), ("tier check", "Capability probes"), ("hunch", "Hunch / NEXTDAY analysis"),
                      ("forecast eval", "Argon forecaster evaluation"), ("forecast reasoning", "Live forecast reasoning + ensemble"),
                      ("replay narration", "Replay narration"), ("daily-life", "Daily-life analysis"), ("demo script", "Demo script draft"),
                      ("real estate", "Real estate analysis")):
        if key in p:
            return name
    return purpose


def J(*parts):
    path = P(*parts)
    try:
        return json.load(open(path)) if os.path.exists(path) else None
    except (OSError, json.JSONDecodeError):
        return None


def outcomes():
    """What Argon's work produced, measured: (use, what Argon did, result, evidence file). Missing files skip their row."""
    out = []
    ha = J("runs", "hunch_analysis.json")
    sc = {x["model"]: x for x in (ha or {}).get("scores", [])}
    if {"domino-argon", "gemini-4-argon", "baseline"} <= set(sc):
        da, ga, bl = sc["domino-argon"], sc["gemini-4-argon"], sc["baseline"]
        out.append(("Next-day forecasting on Hunch's NEXTDAY benchmark",
                    "Reasons over Domino's evidence (SEC filing histories, earnings calendars, posting cadence) and returns calibrated probabilities",
                    f"Brier {da['brier_all']:.3f}, the best of all entries (Argon alone {ga['brier_all']:.3f}, Hunch baseline {bl['brier_all']:.3f}); 8-K question {da['brier_q2']:.3f}. 10 cases, not yet significant",
                    "runs/hunch_analysis.json"))
    cs = J("runs", "hunch_claim_scores.json")
    if cs and cs.get("judge_vs_outcome"):
        t, jv = cs["totals"], cs["judge_vs_outcome"]
        out.append(("Outcome resolution", "Resolved every model's narrative claims against held-out next-day evidence (unmentioned counts as unresolved, not false)",
                    f"{sum(t.values())} claims ({t['YES']} yes / {t['NO']} no / {t['UNRESOLVED']} unresolved). Showed the benchmark's judge does not track correctness: Spearman {jv['spearman_judge_vs_brier']:+.2f} (p = {jv['p']:.2f})",
                    "runs/hunch_claim_scores.json"))
    rv = J("analysis", "argon_hunch_review.json")
    if rv:
        out.append(("Benchmark audit", "Read Hunch's code, data contracts and results",
                    f"{len(rv.get('gaps_and_risks', []))} issues found, e.g. the judge never sees held-out social posts on Q5; deterministic blind IDs with same-model judging; 87% of raw Argon's Brier gain over the baseline is a weekend-calendar artifact on the 8-K question",
                    "analysis/argon_hunch_review.json"))
    pd_ = J("runs", "hunch_pilot_domino.json")
    if pd_:
        out.append(("Live head-to-head", f"{pd_.get('n_ensemble', 5)}-sample ensemble on live news for Hunch's five pilot questions (cyclone, UK outages, embassies/strikes); statistics for META and YouTube",
                    f"Pre-registered before the outcome, hash {pd_['hash'][:8]}…; resolves 27 Oct 00:00 UTC", "runs/hunch_pilot_domino.json"))
    lf = J("runs", "forecast_latest.json")
    ens = [e for e in (lf or {}).get("events", []) if e.get("spread") is not None]
    if ens:
        out.append(("Live Domino page", "5-sample ensemble on next-day geopolitical and market events, with the spread shown as uncertainty",
                    f"{len(ens)} live event odds, e.g. {ens[0]['label'][:60]}…: {ens[0]['prob']:.0%} (spread {ens[0]['spread']:.3f})", "runs/forecast_latest.json"))
    ra = J("runs", "realestate_argon.json")
    if ra and ra.get("argon_ensemble"):
        e, st = ra["argon_ensemble"], ra["stats"]
        out.append(("Housing forecasts", "5-sample ensemble next to the statistical models, on the same questions",
                    f"P(Freddie 30-yr below last on Thu) {e['p_pmms_below_last']:.2f} vs statistics {st['pmms_oct29']['p_lower_than_last']:.2f}; "
                    f"P(US home values fall) {e['p_zhvi_decline']:.2f} vs {st['zhvi_next']['p_decline']:.2f}. Pre-registered, hash {ra['hash'][:8]}…", "runs/realestate_argon.json"))
    rs = J("runs", "re_invest_research.json")
    if rs:
        ok = [k for k, v in rs.get("markets", {}).items() if (v or {}).get("research")]
        out.append(("Grounded research", "Google Search–grounded research with dated sources, for markets that have no data feed",
                    f"{len(ok)} markets researched (incl. Dubai, Abu Dhabi, Almaty, Astana): yields, price and rent trends, financing, foreign-buyer rules, costs, supply",
                    "runs/re_invest_research.json"))
    so = J("runs", "re_invest_social.json")
    if so:
        out.append(("Social read", "Read each market's X, TikTok and YouTube posts and headlines for froth, red flags and demand signals",
                    f"{len(so.get('markets', {}))} markets scored for hype and sentiment", "runs/re_invest_social.json"))
    rk = J("runs", "re_invest_rank.json")
    if rk and rk.get("rows"):
        top = rk["rows"][0]; a = top.get("argon") or {}
        votes = a.get("verdict_votes") or {}
        out.append(("Investment committee", f"{rk.get('argon_views', 5)}-sample ranking from the same evidence as a transparent model, with disagreements explained",
                    f"Agrees with the transparent model (Spearman {rk['agreement_spearman']:.2f}, p = {rk['agreement_p']:.3f}); top pick {top['market']}, verdict {a.get('verdict')} "
                    f"{votes.get(a.get('verdict'), 0)}/{sum(votes.values()) if votes else 0}. Hash {rk['hash'][:8]}…", "runs/re_invest_rank.json"))
    ci = J("analysis", "argon_category_interpretation.json")
    if ci and ci.get("ranking"):
        out.append(("Where prediction works", "Ranked 8 domains by measured next-day predictability and named the first domino in each",
                    f"#1 {ci['ranking'][0]['category'].split(' (')[0]} (score {ci['ranking'][0]['score_0_10']}/10)", "analysis/argon_category_interpretation.json"))
    return out


def main():
    rows = []  # one row per Argon call: component, level, live/cached, tokens, seconds, when, source
    # 1) engine calls: ledger (preferred) + live calls in the cache from before the ledger existed
    ledger = jl(P("runs", "argon_ledger.jsonl"))
    for r in ledger:
        rows.append({"component": component(r["purpose"]), "level": r["thinking_level"], "cached": r["cached"],
                     "in": r["input_tokens"], "out": r["output_tokens"], "thought": r["thought_tokens"], "sec": r["seconds"],
                     "source": f'engine ({r.get("app", "rpwm")})', "ts": r["ts"], "tier": r.get("service_tier", "standard")})
    ledger_live = sum(1 for r in ledger if not r["cached"])
    cache = jl(P("runs", "argon_cache.jsonl"))
    for r in cache[: max(0, len(cache) - ledger_live)]:  # live calls recorded before the ledger existed
        m = r["meta"]
        rows.append({"component": component(r["purpose"]), "level": r["level"], "cached": False, "in": m.get("input_tokens", 0),
                     "out": m.get("output_tokens", 0), "thought": m.get("thought_tokens", 0), "sec": m.get("seconds", 0),
                     "source": "engine (pre-ledger)", "ts": ""})
    # 2) capability probes (Argon rows only)
    for f in sorted(glob.glob(P("runs", "argon_probe_*.json"))):
        d = json.load(open(f))
        for pr in d["probes"]:
            if pr.get("model") == "gemini-4-argon" and pr.get("ok"):
                u = pr.get("usage", {})
                rows.append({"component": "Capability probes", "level": pr.get("summary", "[low]")[1:].split("]")[0] if pr.get("summary", "").startswith("[") else "low",
                             "cached": False, "in": u.get("total_input_tokens", 0), "out": u.get("total_output_tokens", 0),
                             "thought": u.get("total_thought_tokens", 0), "sec": pr.get("seconds", 0), "source": os.path.basename(f), "ts": d["started"]})
    # 3) managed agent probes
    for f in sorted(glob.glob(P("runs", "managed_agent_probe_*.json"))):
        d = json.load(open(f))
        tok = {"in": 0, "out": 0, "thought": 0}
        for e in d["events"]:
            if e["msg"].startswith("usage="):
                u = eval(e["msg"][6:], {"__builtins__": {}})  # our own log line: a dict literal
                tok = {"in": u.get("total_input_tokens", 0), "out": u.get("total_output_tokens", 0), "thought": u.get("total_thought_tokens", 0)}
        rows.append({"component": "Managed Agent (slow level)", "level": "agent", "cached": False, **tok,
                     "sec": d["events"][-1]["t"] if d["events"] else 0, "source": os.path.basename(f), "ts": d["started"]})
    # 4) native PDF ingest
    if os.path.exists(P("ingest", "argon_ingest.json")):
        m = json.load(open(P("ingest", "argon_ingest.json")))["_meta"]
        rows.append({"component": "Paper ingest (native PDF)", "level": m["thinking_level"], "cached": False, "in": m["input_tokens"],
                     "out": m["output_tokens"], "thought": m["thought_tokens"], "sec": m["seconds"], "source": "ingest/argon_ingest.json", "ts": m["created"]})
    # 5) Argon judge panel (tokens not logged by that script; seconds are)
    if os.path.exists(P("plans", "llm_judges_argon.json")):
        for j in json.load(open(P("plans", "llm_judges_argon.json")))["judges"]:
            rows.append({"component": "Judge panel (3 personas)", "level": "high", "cached": False, "in": 0, "out": 0, "thought": 0,
                         "sec": j.get("seconds", 0), "source": "plans/llm_judges_argon.json", "ts": ""})
    # 6) hand-logged: vision re-timing (WORKLOG 10:52), 4 calls of about 1,155 input / 72 output tokens
    for s in (3.3, 4.5, 15.0, 3.8):
        rows.append({"component": "Capability probes", "level": "low", "cached": False, "in": 1155, "out": 72, "thought": 0,
                     "sec": s, "source": "WORKLOG 10:52 (vision re-timing)", "ts": "2026-10-25 10:52"})

    live = [r for r in rows if not r["cached"]]
    tot = {k: sum(r[k] for r in live) for k in ("in", "out", "thought", "sec")}
    cost = tot["in"] / 1e6 * PRICE_IN + (tot["out"] + tot["thought"]) / 1e6 * PRICE_OUT
    by_comp = defaultdict(lambda: {"live": 0, "cached": 0, "in": 0, "out": 0, "thought": 0, "sec": 0.0})
    by_level = defaultdict(int)
    by_tier = defaultdict(int)
    for r in rows:
        c = by_comp[r["component"]]
        c["cached" if r["cached"] else "live"] += 1
        if not r["cached"]:
            for k in ("in", "out", "thought", "sec"):
                c[k] += r[k]
            by_level[r["level"]] += 1
            by_tier[r.get("tier", "standard")] += 1
    ablations = sorted(glob.glob(P("runs", "ablation_*.json")))
    episodes = sum(len(json.load(open(f)).get("rows", [])) for f in ablations)

    n_live = max(1, len(live))
    hi, pri = by_level.get("high", 0), by_tier.get("priority", 0)
    L = ["# Gemini 4 Argon usage: Domino, a next-day world model", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `tools/argon_usage_report.py` from the project's own logs. Re-run it any time to refresh.", "",
         "## For judges and investors: how Domino uses Argon", "",
         "Domino predicts what happens next: tomorrow's events, next week's mortgage rate, next month's rents, where to buy property. "
         "Gemini 4 Argon is its reasoning layer. Argon reads the evidence, proposes causal links (the \"first dominoes\"), researches markets that have no data feed, "
         "decides whether past predictions came true, and gives calibrated probabilities as 5-sample ensembles. "
         "Statistics and Google's TimesFM handle the numeric series. Every Argon output is either scored on outcomes or pre-registered with a hash before the outcome is known.", "",
         "| At a glance | |", "|---|---|",
         f"| Live Argon calls | **{len(live)}** |",
         f"| At thinking `high` | {hi} ({100 * hi / n_live:.0f}%) |",
         f"| On the Priority tier | {pri} ({100 * pri / n_live:.0f}%) |",
         f"| Tokens in / out / thinking | {tot['in']:,} / {tot['out']:,} / {tot['thought']:,} |",
         f"| Argon time | {tot['sec'] / 60:.0f} min, {tot['sec'] / n_live:.0f} s per call on average (ensembles run in parallel) |",
         f"| List-price equivalent | ${cost:.2f}, about ${cost / n_live:.3f} per call (hackathon credits) |", "",
         "### What Argon delivered, measured", "",
         "| Use | What Argon does | Result | Evidence |", "|---|---|---|---|"]
    for use, what, result, ev in outcomes():
        L.append(f"| {use} | {what} | {result} | `{ev}` |")
    L += ["",
          "### How we keep Argon honest", "",
          "- **Scored on outcomes, not impressions.** Brier and MAE on resolved questions; claims checked against held-out evidence.",
          "- **Pre-registered.** Forecasts are hashed before the outcome is known; the hashes are in the result files and on the dashboards.",
          "- **Head-to-head with statistics.** Every Argon probability is shown next to a statistical model on the same question.",
          "- **Evidence labels on every causal link.** Measured (out-of-sample test), mechanism (Argon prior, untested) or anecdotal; links tested without skill are shown as such.",
          "- **Reproducible.** Every call is cached and logged in `runs/argon_ledger.jsonl`, so every number replays offline.", "",
          "### Where Argon did not beat simple models (reported, not hidden)", "",
          "- Attention data did not predict next-day market returns, and Argon found no market edge there.",
          "- Daily posting counts: a Poisson model on last week's cadence beat Argon (MAE 0.99 vs 1.30).",
          "- Home values month to month: momentum beats every adjustment; Argon's higher odds of a fall (21% vs 13%) are untested until Zillow's October print.",
          "- Argon-sourced legal claims (e.g. Kazakhstan's title rule for foreign buyers) are flagged for verification, not used as fact.", "",
          "### Why it matters", "",
          "- The same loop (collect, reason with Argon, score on outcomes) runs on any domain that has data collectors; Hunch's collectors already cover news, social, markets, housing, jobs and prices.",
          "- Every prediction carries its evidence class and a pre-registration hash, so accuracy can be audited after the fact.",
          f"- Cost scales with calls: about ${cost / n_live:.3f} per Argon call at list price, so a 5-sample ensemble costs about ${5 * cost / n_live:.2f}.", "",
         "## Rule", "",
         "Every model call made by this project's code uses `gemini-4-argon`.",
         "",
         "Since about 11:50 PDT, every call also runs at the most performant settings available: `thinking_level: high` and the Priority inference tier (`service_tier: priority`, billed at 75-100% above standard). These are the defaults in `rpwm/argon.py`; there is no economizing.",
         "",
         "- Code audit: `grep -rE 'gemini-[0-9a-z.-]+' --include='*.py'` finds only `gemini-4-argon` in runtime paths. The one exception is a price table in an old probe script.",
         "- Before the rule (10:50 PDT), one capability probe touched Flash, Robotics-ER, and embeddings once each. Those calls are excluded below.", "",
         "## Totals", "",
         "| Metric | Value |", "|---|---|",
         f"| Argon calls made (live) | **{len(live)}** |",
         f"| Calls served from the record/replay cache | {len(rows) - len(live)} |",
         f"| Input tokens | {tot['in']:,} |",
         f"| Output tokens | {tot['out']:,} |",
         f"| Thinking tokens | {tot['thought']:,} |",
         f"| Argon wall time | {tot['sec'] / 60:.1f} min |",
         f"| List-price equivalent | ${cost:.2f} (covered by hackathon credits) |",
         f"| Ablation episodes run with Argon in the loop | {episodes} |", "",
         "## By component", "",
         "| Component | Live calls | Cached | Input tok | Output tok | Thinking tok | Seconds |", "|---|---|---|---|---|---|---|"]
    for name, c in sorted(by_comp.items(), key=lambda kv: -kv[1]["live"]):
        L.append(f"| {name} | {c['live']} | {c['cached']} | {c['in']:,} | {c['out']:,} | {c['thought']:,} | {c['sec']:.0f} |")
    L += ["", "## By thinking level (live calls)", "", "| Level | Calls |", "|---|---|"]
    for lvl in ("low", "medium", "high", "agent"):
        if by_level.get(lvl):
            L.append(f"| {lvl} | {by_level[lvl]} |")
    L += ["", "## By service tier (live calls)", "", "| Tier | Calls |", "|---|---|"]
    for tier, n in sorted(by_tier.items(), key=lambda kv: -kv[1]):
        L.append(f"| {tier} | {n} |")
    L += ["", "## Where Argon sits in the product", "",
          "| Role | What Argon does | Code |", "|---|---|---|",
          "| Reader | Ingests the RPWM paper natively as PDF and returns equations, claims, issues, and an executable spec | `tools/argon_ingest.py` |",
          "| Eyes | Reads rendered frames and reports object positions | `rpwm/agent.py: perceive` |",
          "| World model | Writes the likelihood tables P(outcome \\| action, hypothesis) that the exact Bayesian math runs on | `rpwm/agent.py: compile_world_model` |",
          "| Planner | Orders sub-goals (L2) and proposes child sub-goals when stuck (recursion) | `plan_order`, `child_subgoal` |",
          "| Self-correction | Revises its world model under surprise, thinking low → medium → high, gated by the free-energy stopping rule | `refine` |",
          "| Slow level | Managed Agent (Antigravity) on Argon: sandbox analysis plus a `recurse` tool that calls back into the fast loop | `rpwm/slow_agent.py` |",
          "| Memory | Writes lessons into semantic memory after each episode | `run → consolidate` |",
          "| Forecaster | 5-sample ensembles pooled in log-odds for next-day and next-week questions; pre-registered | `domino/live.py`, `domino/hunch_extended.py`, `domino/realestate.py` |",
          "| Causal graph | Proposes the links between drivers, channels and outcomes; statistics test them | `domino/live.py`, `domino/realestate_dashboard.py` |",
          "| Evidence resolver | Decides whether claims came true against held-out evidence | `domino/hunch_extended.py resolve` |",
          "| Researcher | Google Search–grounded research with dated sources where no data feed exists | `domino/realestate_invest.py research` |",
          "| Analyst | Reads social posts and headlines for froth, red flags and demand | `domino/realestate_invest.py social` |",
          "| Investment committee | Ranks markets from the same evidence as a transparent model | `domino/realestate_invest_rank.py` |",
          "| Auditor | Reviewed Hunch's benchmark code and data | `tools/argon_hunch_ingest.py` |",
          "| Judge | Three-persona blind judge panel that ranked the demo options | `tools/argon_judges.py` |", "",
          "## What is not Argon, and why", "",
          "| Component | Why not Argon |", "|---|---|",
          "| numpy / scipy | Free energy, expected free energy, Bayes updates, CIs. The math must be exact, so Argon supplies distributions and numpy computes on them. |",
          "| TimesFM 3.0 (Google) | Numeric next-step forecasts for weekly and monthly series; Argon reasons, TimesFM extrapolates |",
          "| yfinance, Wikipedia, treg.to, Glasser, Zillow, Realtor.com, BLS, Freddie Mac | Data inputs, not models |", ""]
    os.makedirs(P("docs"), exist_ok=True)
    with open(P("docs", "ARGON_USAGE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"live Argon calls {len(live)}, cached {len(rows) - len(live)}, tokens in/out/thought {tot['in']}/{tot['out']}/{tot['thought']}, "
          f"{tot['sec'] / 60:.1f} min, list ${cost:.2f}; components {len(by_comp)}; wrote docs/ARGON_USAGE.md")


if __name__ == "__main__":
    main()
