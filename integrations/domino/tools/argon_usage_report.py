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

    L = ["# Gemini 4 Argon usage: RPWM hackathon project", "",
         f"Generated {time.strftime('%Y-%m-%d %H:%M %Z')} by `tools/argon_usage_report.py` from the project's own logs. Re-run it any time to refresh.", "",
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
          "| Next-day predictor | Causal graph, event extraction, calibrated forecasts, recursive investigation, narration (in progress) | `domino/` |",
          "| Judge | Three-persona blind judge panel that ranked the demo options | `tools/argon_judges.py` |", "",
          "## What is not Argon, and why", "",
          "| Component | Why not Argon |", "|---|---|",
          "| numpy / scipy | Free energy, expected free energy, Bayes updates, CIs. The math must be exact, so Argon supplies distributions and numpy computes on them. |",
          "| yfinance, Wikipedia, treg.to, Glasser | Data inputs, not models |", ""]
    os.makedirs(P("docs"), exist_ok=True)
    with open(P("docs", "ARGON_USAGE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"live Argon calls {len(live)}, cached {len(rows) - len(live)}, tokens in/out/thought {tot['in']}/{tot['out']}/{tot['thought']}, "
          f"{tot['sec'] / 60:.1f} min, list ${cost:.2f}; components {len(by_comp)}; wrote docs/ARGON_USAGE.md")


if __name__ == "__main__":
    main()
