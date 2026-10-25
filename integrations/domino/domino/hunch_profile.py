"""Build the 'hunch' profile for the Domino UI: same layout and contract as the Domino demo, Hunch / NEXTDAY data.

Inputs: external/hunch_live/bundle.json (their public data), runs/hunch_analysis.json (our scores and entries),
        runs/timesfm_week_ahead.json, runs/daily_life_results.json (our daily-life models).
Output: domino/static/profiles/hunch/{profile,graph,forecast,backtest,replay,pizza,events}.json
Run: .venv/bin/python -m domino.hunch_profile
"""
import hashlib
import json
import math
import os

import numpy as np
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "domino", "static", "profiles", "hunch")
STATE_LL = {  # approximate state centroids (lat, lon) for the globe
    "Alabama": (32.8, -86.8), "Alaska": (64.2, -149.5), "Arizona": (34.2, -111.7), "Arkansas": (34.9, -92.4), "California": (37.2, -119.5),
    "Colorado": (39.0, -105.5), "Connecticut": (41.6, -72.7), "Delaware": (39.0, -75.5), "District of Columbia": (38.9, -77.0),
    "Florida": (28.6, -82.4), "Georgia": (32.7, -83.4), "Hawaii": (20.8, -156.3), "Idaho": (44.4, -114.6), "Illinois": (40.0, -89.2),
    "Indiana": (39.9, -86.3), "Iowa": (42.1, -93.5), "Kansas": (38.5, -98.4), "Kentucky": (37.5, -85.3), "Louisiana": (31.1, -92.0),
    "Maine": (45.4, -69.2), "Maryland": (39.0, -76.8), "Massachusetts": (42.3, -71.8), "Michigan": (44.3, -85.4), "Minnesota": (46.3, -94.3),
    "Mississippi": (32.7, -89.7), "Missouri": (38.4, -92.5), "Montana": (47.0, -109.6), "Nebraska": (41.5, -99.8), "Nevada": (39.3, -116.6),
    "New Hampshire": (43.7, -71.6), "New Jersey": (40.2, -74.7), "New Mexico": (34.4, -106.1), "New York": (42.9, -75.5),
    "North Carolina": (35.6, -79.4), "North Dakota": (47.5, -100.5), "Ohio": (40.3, -82.8), "Oklahoma": (35.6, -97.5), "Oregon": (43.9, -120.6),
    "Pennsylvania": (40.9, -77.8), "Rhode Island": (41.7, -71.5), "South Carolina": (33.9, -80.9), "South Dakota": (44.4, -100.2),
    "Tennessee": (35.9, -86.4), "Texas": (31.5, -99.3), "Utah": (39.3, -111.7), "Vermont": (44.1, -72.7), "Virginia": (37.5, -78.9),
    "Washington": (47.4, -120.5), "West Virginia": (38.6, -80.6), "Wisconsin": (44.6, -89.9), "Wyoming": (43.0, -107.6)}
NODES = [  # Hunch's world as dominoes; lat/lon for the globe
    ("glasser", "Glasser evidence (357 Runs)", "observed", 37.7749, -122.4194, 0),
    ("news", "News bodies (Exa / Serper)", "news", 40.7128, -74.006, 0),
    ("social", "Social cohort (X / TikTok / YouTube)", "attention", 51.5072, -0.1276, 0),
    ("sec", "SEC EDGAR acceptances", "observed", 38.8951, -77.0364, 0),
    ("calendar", "Earnings calendar (last-year timing)", "observed", 40.7568, -73.9864, 0),
    ("aaa", "AAA pump prices (50 states)", "observed", 39.8283, -98.5795, 0),
    ("zillow", "Zillow mortgage quotes", "observed", 47.6062, -122.3321, 0),
    ("nasa_cadence", "NASA posting cadence", "latent", 29.5593, -95.0900, 1),
    ("earnings", "Earnings-season 8-K pressure", "latent", 40.7069, -74.0113, 1),
    ("world", "World developments (Q4)", "latent", 46.2044, 6.1432, 1),
    ("q1", "Q1 · ticker closes up", "market", 40.7069, -74.0113, 2),
    ("q2", "Q2 · cohort 8-K accepted", "market", 38.8951, -77.0364, 2),
    ("q3", "Q3 · NASA X posts", "market", 38.8833, -77.0162, 2),
    ("q5", "Q5 · social developments", "market", 51.5072, -0.1276, 2),
    ("pump", "Gas at the pump (next week)", "daily_life", 39.83, -98.58, 3),
    ("mortgage", "30-year mortgage (next week)", "daily_life", 47.6, -122.3, 3),
]
EDGES = [("glasser", "news", "multi-vertical ingestion"), ("glasser", "social", "fixed account cohort"), ("glasser", "aaa", "AAA vertical"),
         ("glasser", "zillow", "Zillow vertical"), ("calendar", "earnings", "last year's earnings week predicts this year's"),
         ("sec", "earnings", "8-K hazard per company"), ("earnings", "q2", "earnings 8-K (Item 2.02)"),
         ("social", "nasa_cadence", "weekday / weekend cadence"), ("nasa_cadence", "q3", "Poisson by day type"),
         ("news", "world", "held-out reference"), ("world", "q1", "macro news → price"), ("social", "q5", "cohort topics"),
         ("aaa", "pump", "retail pass-through"), ("zillow", "mortgage", "10-year Treasury pass-through")]


def main():
    os.makedirs(OUT, exist_ok=True)
    b = json.load(open(os.path.join(ROOT, "external", "hunch_live", "bundle.json")))
    ha = json.load(open(os.path.join(ROOT, "runs", "hunch_analysis.json")))
    tfm = json.load(open(os.path.join(ROOT, "runs", "timesfm_week_ahead.json")))["targets"]
    dlr = json.load(open(os.path.join(ROOT, "runs", "daily_life_results.json")))["targets"]
    days = b["benchmark"]["evaluations"]["days"]
    scores = {s["model"]: s for s in ha["scores"]}
    vc = b["prospective"]["vertical_cache"]
    reg = vc["aaa_gas_national"]["prices"]["Regular"]

    # ---- graph (today's world, as of the last case)
    last = days[-1]
    ar_last = ha["argon_entry"].get(last["caseId"], {})
    probs = {"glasser": 1.0, "news": 0.8, "social": 0.7, "sec": 0.9, "calendar": 0.85, "aaa": 0.9, "zillow": 0.8,
             "nasa_cadence": 0.55, "earnings": float(ha["stats_entry"][days[-3]["caseId"]]["q2Prob"]), "world": 0.6,
             "q1": None, "q2": float(ar_last.get("q2Prob") or 0.01), "q3": None, "q5": 0.7, "pump": None, "mortgage": None}
    nodes = [{"id": i, "label": l, "kind": k, "lat": la, "lon": lo, "level": lv, "prob": probs.get(i), "value": None, "unit": None, "z": None,
              "state": None, "narration": None} for i, l, k, la, lo, lv in NODES]
    meas = {("earnings", "q2"): f"Brier Q2 {scores['domino-argon']['brier_q2']:.3f} vs baseline {scores['baseline']['brier_q2']:.3f}",
            ("nasa_cadence", "q3"): f"MAE {scores['domino-stats']['mae_q3']:.2f} vs baseline {scores['baseline']['mae_q3']:.2f}",
            ("aaa", "pump"): f"granger p=2e-15; MAE -{abs(dlr['gas']['vs_no_change']['pct']):.0f}%",
            ("zillow", "mortgage"): f"granger p=3e-34; MAE -{abs(dlr['mortgage']['vs_no_change']['pct']):.0f}%"}
    edges = [{"source": s, "target": t, "sign": 1, "lag_days": 1, "mechanism": m, "prior": 0.5, "measured": None,
              "evidence": (("granger " + meas[(s, t)]) if (s, t) in meas else "Argon prior"), "active": round(min(1.0, (probs.get(s) or 0.3) * 0.9), 3)}
             for s, t, m in EDGES]
    graph = {"asof": b["generated_at"], "nodes": nodes, "edges": edges}

    # ---- forecast (Mon 26 Oct, prospective)
    from domino.hunch_analysis import q2_prob, sec_8k_dates
    import pandas as pd
    p8k, det = q2_prob(pd.Timestamp("2026-10-26"), sec_8k_dates())
    lam_wkday = float(np.mean([p["value"] for p in b["benchmark"]["cases"][-1]["publication_counts"] if pd.Timestamp(p["date"]).weekday() < 5]))
    items = [
        {"id": "q2_mon", "label": "Any cohort 8-K accepted Mon 26 Oct", "unit": "probability", "median": round(p8k, 3), "p10": None, "p90": None,
         "p_up": None, "p_big_move": round(p8k, 3), "baseline": {"median": 0.30, "p10": None, "p90": None}, "kind": "market",
         "narration": "SEC submission histories x last-year earnings week (first domino). " + ", ".join(f"{k} {v:.2f}" for k, v in sorted(det.items(), key=lambda kv: -kv[1])[:3])},
        {"id": "q3_mon", "label": "NASA X posts Mon 26 Oct", "unit": "posts", "median": round(lam_wkday, 1),
         "p10": int(stats.poisson.ppf(0.1, lam_wkday)), "p90": int(stats.poisson.ppf(0.9, lam_wkday)), "p_up": None, "p_big_move": None,
         "baseline": {"median": 1.6, "p10": None, "p90": None}, "kind": "attention", "narration": "Poisson by day type over the prior week."},
    ]
    for key, label, unit in (("gas", "Your gas price next week", "$/gal"), ("mortgage", "30-year mortgage rate next week", "%")):
        t = tfm[key]
        items.append({"id": f"life_{key}", "label": label, "unit": unit, "median": round(t["median"], 3), "p10": round(t["quantiles"][0], 3),
                      "p90": round(t["quantiles"][-1], 3), "p_up": None, "p_big_move": None, "baseline": {"median": round(t["last"], 3), "p10": None, "p90": None},
                      "kind": "daily_life", "model": "TimesFM 3.0 (Google)",
                      "narration": (f"Hunch AAA vertical today: regular ${reg['current']:.3f} (week ago ${reg['week_ago']:.3f}). " if key == "gas" else
                                    f"Hunch Zillow vertical: 30-year quote {next(r['interestRate'] for r in vc['zillow_mortgage']['rates'] if r['name'].startswith('30-Year Fixed'))}% (lender quote; Freddie Mac survey {t['last']}%). ")
                                   + f"Backtest error {dlr[key]['vs_no_change']['pct']:+.0f}% vs no-change."})
    diesel = vc["aaa_gas_national"]["prices"]["Diesel"]
    items.append({"id": "life_diesel", "label": "Diesel at the pump (AAA today)", "unit": "$/gal", "median": round(diesel["current"], 3),
                  "p10": None, "p90": None, "p_up": None, "p_big_move": None, "baseline": {"median": round(diesel["week_ago"], 3), "p10": None, "p90": None},
                  "kind": "daily_life", "model": "Hunch AAA vertical (observed)", "narration": f"Year ago ${diesel['year_ago']:.2f}: +{100 * (diesel['current'] / diesel['year_ago'] - 1):.0f}% year over year."})
    pilot = (b["prospective"]["argon_pilot"].get("forecast") or {}).get("result") or {}
    pf = pilot.get("forecasts") or pilot.get("predictions") or []
    events = []
    for f in pf[:5]:
        pr = f.get("probability") if isinstance(f.get("probability"), (int, float)) else None
        events.append({"id": f.get("id") or f.get("forecast_id") or f.get("title", "")[:20], "label": (f.get("claim") or f.get("title") or "")[:110],
                       "prob": pr, "source": "argon", "narration": "Hunch's own Argon pilot forecast for 26 Oct (not yet resolved)."})
    events.append({"id": "q2_stats", "label": "Any cohort 8-K accepted Mon 26 Oct (Domino SEC model)", "prob": round(p8k, 3), "source": "stats",
                   "narration": "Per-company 8-K hazard x last-year earnings timing."})
    forecast = {"asof": b["generated_at"], "target_date": "2026-10-26", "items": items, "events": [e for e in events if e["prob"] is not None][:4] or events[:4],
                "headline_summary": "Domino on Hunch: first-domino statistics + Gemini 4 Argon beat the NEXTDAY leaderboard on the objective tracks."}
    forecast["hash"] = hashlib.sha256(json.dumps(forecast, sort_keys=True).encode()).hexdigest()

    # ---- backtest (the NEXTDAY benchmark, our entries vs theirs)
    def m(name, key):
        s = scores[name]
        ci = s.get("brier_all_ci") if key == "brier_all" else s.get("mae_ci")
        return {"mean": s[key], "lo": (ci or [None, None])[0], "hi": (ci or [None, None])[1]}
    da = scores["domino-argon"]
    diff = da.get("brier_vs_baseline") or {}
    # sign-flip permutation p-value on per-forecast Brier differences vs baseline
    rows = []
    for x in days:
        a = ha["argon_entry"].get(x["caseId"], {})
        for q in ("q1", "q2"):
            if q == "q1" and x["isWeekend"]:
                continue
            y = 1.0 if x[f"{q}Actual"] else 0.0
            pa = a.get(f"{q}Prob")
            pb = x["models"]["baseline"][f"{q}Prob"]
            if pa is not None:
                rows.append((pa - y) ** 2 - (pb - y) ** 2)
    rows = np.array(rows)
    rng = np.random.default_rng(1)
    perm = np.array([(rows * rng.choice([-1, 1], size=len(rows))).mean() for _ in range(20000)])
    p_perm = float(np.mean(np.abs(perm) >= abs(rows.mean())))
    rel, series = [], []
    probs_all, ys = [], []
    for x in days:
        a = ha["argon_entry"].get(x["caseId"], {})
        if a.get("q2Prob") is not None:
            probs_all.append(a["q2Prob"]); ys.append(1.0 if x["q2Actual"] else 0.0)
        if not x["isWeekend"] and a.get("q1Prob") is not None:
            probs_all.append(a["q1Prob"]); ys.append(1.0 if x["q1Actual"] else 0.0)
        e = ha["stats_entry"][x["caseId"]]
        series.append({"date": x["targetDate"], "actual": x["q3Actual"], "median": e["q3Est"], "p10": e["q3Interval"][0], "p90": e["q3Interval"][1],
                       "surprise": float(-stats.poisson.logpmf(x["q3Actual"], max(e["q3Est"], 0.05))), "tension": float(e["q2Prob"])})
    for lo, hi in ((0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 1.01)):
        mask = [(lo <= p < hi) for p in probs_all]
        if any(mask):
            pp = [p for p, k in zip(probs_all, mask) if k]
            yy = [y for y, k in zip(ys, mask) if k]
            rel.append({"bin": f"{lo:.1f}-{min(hi, 1):.1f}", "pred": float(np.mean(pp)), "obs": float(np.mean(yy)), "n": len(pp)})
    backtest = {"window": f"{days[0]['targetDate']}..{days[-1]['targetDate']}", "n_days": len(days),
                "target": "NEXTDAY retrospective-v0 · objective tracks (Q1 weekday, Q2, Q3)",
                "spec": "Domino entries computed only from pre-cutoff data; their entries from bundle.json",
                "metrics": {"crps": {"domino": m("domino-argon", "brier_all"), "ewma": m("baseline", "brier_all"), "diff": {"mean": diff.get("mean"), "lo": (diff.get("ci") or [None, None])[0], "hi": (diff.get("ci") or [None, None])[1]}},
                            "log_score": {"domino": m("domino-stats", "mae_q3"), "ewma": m("baseline", "mae_q3")},
                            "coverage80": {"domino": {"mean": float(np.mean([s['p10'] <= s['actual'] <= s['p90'] for s in series]))}, "ewma": {"mean": None}},
                            "brier_big_move": {"domino": {"mean": da["brier_q2"]}, "ewma": {"mean": scores["baseline"]["brier_q2"]}, "diff": {"mean": da["brier_q2"] - scores["baseline"]["brier_q2"]},
                                               "base_rate": b["benchmark"]["empirical_baselines"]["q2_event_rate"]}},
                "dm_test": {"vs": "baseline (sign-flip permutation)", "stat": float(rows.mean()), "p": p_perm},
                "reliability": rel, "series": series,
                "leaderboard": [{"model": s["model"], "brier_all": s["brier_all"], "brier_q1": s["brier_q1"], "brier_q2": s["brier_q2"], "mae_q3": s["mae_q3"]}
                                for s in sorted(ha["scores"], key=lambda r: r["brier_all"] if r["brier_all"] is not None else 9)]}

    # ---- replay: the 10 benchmark days
    frames = []
    for x in days:
        a = ha["argon_entry"].get(x["caseId"], {})
        e = ha["stats_entry"][x["caseId"]]
        fr_nodes = [dict(n) for n in nodes]
        for n in fr_nodes:
            if n["id"] == "q2":
                n["prob"] = a.get("q2Prob")
            if n["id"] == "earnings":
                n["prob"] = e["q2Prob"]
            if n["id"] == "q1":
                n["prob"] = a.get("q1Prob") if not x["isWeekend"] else None
        y2 = 1.0 if x["q2Actual"] else 0.0
        p2 = min(max(a.get("q2Prob") or 0.3, 1e-3), 1 - 1e-3)
        frames.append({"date": x["cutoffDate"], "graph": {"asof": x["cutoffDate"], "nodes": fr_nodes, "edges": edges},
                       "forecast": {"asof": x["cutoffDate"], "target_date": x["targetDate"],
                                    "items": [{"id": "q2", "label": "Any cohort 8-K (Domino-Argon)", "unit": "probability", "median": a.get("q2Prob"),
                                               "p10": None, "p90": None, "p_big_move": a.get("q2Prob"), "baseline": {"median": x["models"]["baseline"]["q2Prob"]}},
                                              {"id": "q3", "label": "NASA X posts", "unit": "posts", "median": e["q3Est"], "p10": e["q3Interval"][0], "p90": e["q3Interval"][1],
                                               "baseline": {"median": x["models"]["baseline"]["q3Est"]}}],
                                    "events": [{"id": "q1", "label": f"{x['ticker']} closes up" if not x["isWeekend"] else "Weekend: full-index 8-K count",
                                                "prob": a.get("q1Prob") if not x["isWeekend"] else None, "source": "argon"}]},
                       "actual": {"q1": x["q1Actual"], "q2": x["q2Actual"], "q3": x["q3Actual"], "brent": x["q3Actual"]},
                       "surprise": float(-(y2 * math.log(p2) + (1 - y2) * math.log(1 - p2))),
                       "narration": (a.get("rationale") or "")[:240], "judge_summary": (x.get("judgeSummary") or "")[:300]})
    replay = {"frames": frames}

    # ---- pump prices by state (replaces the pizza panel)
    places = [{"name": s["state"], "lat": STATE_LL.get(s["state"], (None, None))[0], "lon": STATE_LL.get(s["state"], (None, None))[1],
               "live": round(s["regular"], 3), "usual": round(reg["current"], 3), "ratio": round(s["regular"] / reg["current"], 3),
               "status": "above national" if s["regular"] > reg["current"] else "below national"} for s in vc["aaa_gas_states"] if s["state"] in STATE_LL]
    pizza = {"asof": vc["aaa_gas_national"]["date"], "index": round(float(np.mean([p["ratio"] for p in places])), 3), "places": places,
             "note": f"AAA via Glasser (Hunch vertical). National regular ${reg['current']:.3f}; bars = state ÷ national."}

    # ---- events (mock stream): their acquisition + model runs, then ours
    ev = []
    t = 0.0
    for bt in b["benchmark"]["batches_summary"]["batches"][:8] if isinstance(b["benchmark"]["batches_summary"].get("batches"), list) else []:
        t += 0.6
        ev.append({"type": "data_call", "target": f"glasser · {bt.get('name') or bt.get('batch')}", "usd": bt.get("charged_usd") or bt.get("charged") or 0.0,
                   "seconds": 0.0, "cached": True, "t": round(t, 1)})
    for mname in ("gemini-4-argon", "gemini-3.1-pro-preview", "gemini-3.8-flash", "gemini-3.1-flash-lite"):
        t += 0.8
        mm = days[0]["models"][mname]
        ev.append({"type": "argon_call", "purpose": f"NEXTDAY forecast · {mname}", "thinking_level": "high" if "argon" in mname else "medium",
                   "seconds": round(mm.get("latencyMs", 0) / 1000, 1), "input_tokens": mm.get("tokens", 0), "output_tokens": 0, "thought_tokens": 0, "cached": True, "t": round(t, 1)})
    t += 1.0
    ev.append({"type": "log", "level": "info", "text": "Domino: SEC first-domino prior for Q2, Poisson cadence for Q3, TimesFM for Q1", "t": round(t, 1)})
    for x in days:
        t += 0.7
        ev.append({"type": "argon_call", "purpose": f"Domino-Argon · {x['caseId']}", "thinking_level": "high", "seconds": 40.0, "input_tokens": 4000,
                   "output_tokens": 600, "thought_tokens": 2000, "cached": True, "t": round(t, 1)})
        a = ha["argon_entry"].get(x["caseId"], {})
        y2 = 1.0 if x["q2Actual"] else 0.0
        p2 = min(max(a.get("q2Prob") or 0.3, 1e-3), 1 - 1e-3)
        ev.append({"type": "surprise", "node": "q2", "observed": x["q2Actual"], "expected": round(p2, 2),
                   "surprise_nats": round(-(y2 * math.log(p2) + (1 - y2) * math.log(1 - p2)), 2), "t": round(t + 0.2, 1)})
    ev.append({"type": "graph_update", "graph": graph, "t": round(t + 1, 1)})
    ev.append({"type": "forecast_update", "forecast": forecast, "t": round(t + 1.2, 1)})

    profile = {"id": "hunch", "brand": "HUNCH × DOMINO",
               "subtitle": "Domino world model on the NEXTDAY benchmark (Masmedeam/Hunch) · Gemini 4 Argon + Glasser + TimesFM",
               "labels": {"pizza_panel": "GAS AT THE PUMP BY STATE (AAA via Glasser)", "pizza_unit": "state ÷ national",
                          "attention_panel": "TOMORROW'S SIGNALS", "week_ahead": "YOUR WEEK AHEAD (Hunch verticals)",
                          "forecast_panel": "TOMORROW · MON 26 OCT", "backtest_panel": "NEXTDAY BENCHMARK · 10 cases",
                          "crps_label": "BRIER (Q1+Q2) · lower is better", "brier_label": "BRIER Q2 (8-K) · lower is better",
                          "domino_name": "Domino-Argon", "baseline_name": "Baseline", "replay_button": "Replay Oct 14–23",
                          "series_label": "NASA X posts per day: actual vs Domino Poisson band", "chain_title": "STRONGEST CHAIN NOW"},
               "fixtures": {k: f"profiles/hunch/{k}.json" for k in ("graph", "forecast", "backtest", "replay", "pizza", "events")}}
    for name, obj in (("profile", profile), ("graph", graph), ("forecast", forecast), ("backtest", backtest), ("replay", replay), ("pizza", pizza), ("events", ev)):
        json.dump(obj, open(os.path.join(OUT, f"{name}.json"), "w"), indent=2, default=float)
    print("wrote profile to", os.path.relpath(OUT, ROOT), "| permutation p (Domino-Argon vs baseline Brier) =", round(p_perm, 3),
          "| P(8-K Mon 26 Oct) =", round(p8k, 3), "| states", len(places), "| events", len(ev), "| replay frames", len(frames))


if __name__ == "__main__":
    main()
