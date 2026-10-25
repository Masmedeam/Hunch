"""Build every demo profile for the Domino UI (same layout as the live Domino page, different worlds).

Profiles: hunch (built by domino/hunch_profile.py), hunch-world, hunch-social, hunch-markets, hunch-life, daily-life, categories.
Each writes domino/static/profiles/<id>/{profile,graph,forecast,backtest,replay,pizza,events}.json (contract: domino/CONTRACT.md),
plus profiles/index.json. Inputs are this project's result files; missing inputs degrade a panel, never crash.
Run: .venv/bin/python -I domino/profiles_build.py   (isolated mode: inputs include downloaded data)
"""
import hashlib
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import numpy as np

PROF = os.path.join(ROOT, "domino", "static", "profiles")
R = lambda *p: os.path.join(ROOT, *p)


def load(path, default=None):
    p = R(*path.split("/"))
    return json.load(open(p)) if os.path.exists(p) else default


def node(i, label, kind, lat, lon, level, prob=None, value=None, unit=None, narration=None):
    return {"id": i, "label": label, "kind": kind, "lat": lat, "lon": lon, "level": level, "prob": prob, "value": value, "unit": unit,
            "z": None, "state": None, "narration": narration}


def edge(s, t, mech, evidence="Argon prior", active=0.6, measured=None):
    return {"source": s, "target": t, "sign": 1, "lag_days": 1, "mechanism": mech, "prior": 0.5, "measured": measured,
            "evidence": evidence, "active": active}


def item(i, label, unit, median, p10=None, p90=None, base=None, kind="market", narration=None, model=None, p_big=None):
    return {"id": i, "label": label, "unit": unit, "median": median, "p10": p10, "p90": p90, "p_up": None, "p_big_move": p_big,
            "baseline": {"median": base, "p10": None, "p90": None}, "kind": kind, "model": model, "narration": narration}


def gauge(i, label, prob, source, narration=None, pair=None):
    return {"id": i, "label": label, "prob": None if prob is None else round(float(prob), 3), "source": source, "narration": narration, "pair": pair}


def write(pid, brand, subtitle, labels, panels, graph, forecast, backtest, replay=None, pizza=None, events=None, view=None):
    d = os.path.join(PROF, pid)
    os.makedirs(d, exist_ok=True)
    forecast = dict(forecast)
    forecast["hash"] = hashlib.sha256(json.dumps(forecast, sort_keys=True, default=float).encode()).hexdigest()
    fx = {"graph": graph, "forecast": forecast, "backtest": backtest, "replay": replay or {"frames": []},
          "pizza": pizza or {"asof": None, "index": None, "places": [], "note": ""}, "events": events or []}
    for k, v in fx.items():
        json.dump(v, open(os.path.join(d, f"{k}.json"), "w"), indent=2, default=float)
    prof = {"id": pid, "brand": brand, "subtitle": subtitle, "labels": labels, "panels": panels,
            "fixtures": {k: f"profiles/{pid}/{k}.json" for k in fx}}
    if view:
        prof["view"] = view
    json.dump(prof, open(os.path.join(d, "profile.json"), "w"), indent=2)
    return {"id": pid, "title": brand, "blurb": subtitle}


def stream(calls):
    t, ev = 0.0, []
    for c in calls:
        t += c.pop("dt", 0.7)
        ev.append({**c, "t": round(t, 1)})
    return ev


SHORT_M = {"gemini-4-argon": "Argon", "gemini-3.1-pro-preview": "3.1 Pro", "gemini-3.8-flash": "3.8 Flash", "gemini-3.1-flash-lite": "Flash-Lite"}


# ------------------------------------------------------------------------------------------ hunch-world (Q4)
def build_world(b, days):
    cs = load("runs/hunch_claim_scores.json", {}) or {}
    cl = (load("runs/hunch_claims.json", {}) or {}).get("claims", [])
    pilot = load("runs/hunch_pilot_domino.json", {}) or {}
    q4 = [c for c in cl if c["track"] == "q4"]
    by_type = cs.get("by_type", {})
    nodes = [node("exa", "Exa news bodies (6 global panels)", "news", 40.71, -74.0, 0),
             node("jp", "Japan / Japanese supplement", "news", 35.68, 139.69, 0), node("in", "India / English supplement", "news", 28.61, 77.21, 0),
             node("br", "Brazil / Portuguese supplement", "news", -23.55, -46.63, 0), node("me", "Middle East / Arabic supplement", "news", 25.2, 55.27, 0),
             node("continuation", "Running stories (continuations)", "latent", 46.2, 6.14, 1, prob=(by_type.get("continuation") or {}).get("yes_rate")),
             node("scheduled", "Scheduled events (calendars)", "latent", 50.85, 4.35, 1, prob=(by_type.get("scheduled") or {}).get("yes_rate")),
             node("new_event", "Genuinely new events", "latent", 51.5, -0.13, 1, prob=(by_type.get("new_event") or {}).get("yes_rate")),
             node("q4", "Q4 · next-day world developments", "market", 40.75, -73.97, 2),
             node("cyclone", "Bay of Bengal system (IMD)", "market", 15.0, 88.0, 2, prob=(pilot.get("domino", {}).get("fc-1") or {}).get("p")),
             node("ukpower", "UK Storm Boelo outages", "market", 53.48, -2.24, 2, prob=(pilot.get("domino", {}).get("fc-2") or {}).get("p")),
             node("embassy", "US embassies / strikes (Oct 26)", "market", 31.95, 35.93, 2, prob=(pilot.get("domino", {}).get("fc-4") or {}).get("p"))]
    edges = [edge(s, "continuation", "today's story continues tomorrow") for s in ("exa", "jp", "in", "br", "me")]
    edges += [edge("continuation", "q4", "most next-day claims are continuations",
                   evidence=f"granger YES-rate {((by_type.get('continuation') or {}).get('yes_rate') or 0):.0%} on resolved claims"),
              edge("scheduled", "q4", "calendars make the news"), edge("new_event", "q4", "the hard part"),
              edge("me", "embassy", "regional escalation"), edge("in", "cyclone", "IMD bulletins"), edge("exa", "ukpower", "utility updates")]
    hunch = pilot.get("hunch_argon_pilot", {})
    dom = pilot.get("domino", {})
    gauges = []
    for k, lab in (("fc-1", "IMD upgrades Bay of Bengal system to Cyclonic Storm"), ("fc-2", "UK homes without power < 25,000 by Oct 27"),
                   ("fc-4", "No US embassy departure order and no US strike inside Iran")):
        gauges.append(gauge(f"{k}-h", lab, hunch.get(k), "hunch", "Hunch's Argon pilot", pair=k))
        gauges.append(gauge(f"{k}-d", lab, (dom.get(k) or {}).get("p"), "domino", "Domino: live treg news + 5-sample Argon ensemble", pair=k))
    items = []
    if dom.get("fc-2", {}).get("buckets"):
        bk = dom["fc-2"]["buckets"]
        items.append(item("fc2b", "UK outages Oct 27: P(<25k / 25–82k / >82k)", "probability", round(bk[0], 3), kind="market",
                          narration=f"Domino buckets {bk[0]:.2f} / {bk[1]:.2f} / {bk[2]:.2f} vs Hunch 0.72 / 0.23 / 0.05"))
    for t, lab in (("continuation", "Continuations that came true"), ("scheduled", "Scheduled events that came true"), ("cadence", "Cadence claims that came true")):
        v = by_type.get(t) or {}
        if v.get("claims"):
            items.append(item(f"type_{t}", lab, "probability", v.get("yes_rate"), kind="attention",
                              narration=f"{v['claims']} claims, {v['resolved']} resolved; mean stated probability {v.get('mean_prob') or 0:.2f}"))
    items.append(item("type_new_event", "Claims calling a genuinely new event", "count", (by_type.get("new_event") or {}).get("claims", 0), kind="attention",
                      narration=f"of {sum(v.get('claims', 0) for v in by_type.values())} claims"))
    jv = cs.get("judge_vs_outcome", {})
    if jv:
        items.append(item("judge_brier", "Judge ~ outcome Brier (ρ)", "ratio", round(jv["spearman_judge_vs_brier"], 2), kind="attention",
                          narration=f"p = {jv['p']:.2f}: Hunch's judge does not reward being right"))
        items.append(item("judge_spec", "Judge ~ claim specificity (ρ)", "ratio", round(jv["spearman_judge_vs_specificity"], 2), kind="attention",
                          narration=f"p = {jv['p_specificity']:.4f}: it rewards sounding specific"))
    rows = []
    for m, v in (cs.get("by_model") or {}).items():
        a, q = v.get("all", {}), v.get("q4", {})
        rows.append({"model": m, "claims": q.get("claims"), "resolved_pct": round(100 * (q.get("resolution_rate") or 0)),
                     "yes_rate": q.get("yes_rate"), "mean_prob": q.get("mean_prob"), "brier_resolved": q.get("brier"),
                     "specificity": a.get("mean_specificity")})
    rows.sort(key=lambda r: r["brier_resolved"] if r["brier_resolved"] is not None else 9)
    probs = [(c["probability"], 1.0 if c["verdict"] == "YES" else 0.0) for c in q4 if c["verdict"] in ("YES", "NO") and c.get("probability") is not None]
    rel = []
    for lo, hi in ((0, 0.5), (0.5, 0.7), (0.7, 0.85), (0.85, 1.01)):
        sub = [(p, y) for p, y in probs if lo <= p < hi]
        if sub:
            rel.append({"bin": f"{lo:.2f}-{min(hi, 1):.2f}", "pred": float(np.mean([p for p, _ in sub])), "obs": float(np.mean([y for _, y in sub])), "n": len(sub)})
    jvo = cs.get("judge_vs_outcome", {})
    best = rows[0] if rows else {}
    backtest = {"window": f"{days[0]['targetDate']}..{days[-1]['targetDate']}", "n_days": len(days), "target": "Q4 world claims, resolved by Argon against held-out evidence",
                "metrics": {"crps": {"domino": {"mean": best.get("brier_resolved")}, "ewma": {"mean": (rows[-1] if rows else {}).get("brier_resolved")}}},
                "dm_test": {},
                "reliability": rel, "series": [], "leaderboard": rows}
    frames = []
    for x in days:
        dc = [c for c in q4 if c["claim_id"].startswith(x["caseId"])]
        frames.append({"date": x["cutoffDate"], "graph": {"nodes": nodes, "edges": edges},
                       "forecast": {"target_date": x["targetDate"], "items": [], "events": [gauge(c["claim_id"], f"{c['model'].split('-')[1]}: {c['title']}"[:90], c["probability"], "argon", c["verdict"]) for c in dc[:4]]},
                       "actual": {"yes": sum(c["verdict"] == "YES" for c in dc), "no": sum(c["verdict"] == "NO" for c in dc)},
                       "surprise": float(np.mean([-math.log(max(1e-3, c["probability"] if c["verdict"] == "YES" else 1 - c["probability"])) for c in dc if c["verdict"] in ("YES", "NO") and c.get("probability") is not None] or [0.0])),
                       "narration": (x.get("judgeSummary") or "")[:280]})
    ev = stream([{"type": "data_call", "target": "glasser · exa news (held-out reference)", "usd": 0.007, "seconds": 0, "cached": True}] +
                [{"type": "argon_call", "purpose": f"Argon resolver · {x['caseId']}", "thinking_level": "high", "seconds": 60, "input_tokens": 12000,
                  "output_tokens": 1500, "thought_tokens": 3000, "cached": True} for x in days] +
                [{"type": "log", "level": "info", "text": "Unmentioned ≠ false: unresolved claims are excluded from Brier (Hunch's own rule)"}])
    return write("hunch-world", "HUNCH × DOMINO · WORLD", "Q4 next-day world developments: every model's claims resolved on outcomes, not impressions",
                 {"forecast_panel": "MON 26 OCT · WORLD HEAD-TO-HEAD", "attention_panel": "CLAIM TYPES · YES-RATE", "backtest_panel": "Q4 CLAIM SCORES (resolved)",
                  "crps_label": "Q4 CLAIM BRIER · best vs worst model", "replay_button": "Replay Oct 14–23",
                  "domino_name": SHORT_M.get(best.get("model"), "best"), "baseline_name": SHORT_M.get((rows[-1] if rows else {}).get("model"), "worst"),
                  "leaderboard_cols": {"claims": "claims", "resolved_pct": "resolved %", "yes_rate": "YES rate", "mean_prob": "mean p", "brier_resolved": "Brier", "specificity": "specificity"}},
                 {"pizza": False, "attention": True, "week_ahead": False, "leaderboard": True, "replay": True, "gauges": True},
                 {"asof": b["generated_at"], "nodes": nodes, "edges": edges},
                 {"asof": b["generated_at"], "target_date": "2026-10-26", "items": items, "events": gauges,
                  "headline_summary": "Outcome-resolved world claims; Domino and Hunch pre-registered head-to-head for Oct 26."},
                 backtest, {"frames": frames}, None, ev)


# ------------------------------------------------------------------------------------------ hunch-social (Q3, Q5, YouTube)
def build_social(b, days):
    ha = load("runs/hunch_analysis.json", {}) or {}
    cs = load("runs/hunch_claim_scores.json", {}) or {}
    pilot = load("runs/hunch_pilot_domino.json", {}) or {}
    vert = load("runs/hunch_verticals_argon.json", {}) or {}
    qr = b["prospective"]["quality_report"]
    yt = pilot.get("youtube", {})
    nodes = [node("nasa", "NASA (X / YouTube)", "attention", 38.88, -77.02, 0), node("who", "WHO (X)", "attention", 46.23, 6.13, 0),
             node("bbc", "BBCWorld / BBCNews", "attention", 51.52, -0.14, 0), node("dw", "DW News (TikTok)", "attention", 50.71, 7.12, 0),
             node("kda", "K/DA 'FIRESTARTER' (YouTube)", "attention", 34.03, -118.45, 0, value=yt.get("views_now"), unit="views"),
             node("cadence", "Weekday posting cadence", "latent", 39.0, -77.5, 1, prob=0.7), node("velocity", "View velocity (decaying)", "observed", 37.4, -122.08, 1,
                  value=round(yt["velocity_per_hour"]) if yt.get("velocity_per_hour") else None, unit="views/h"),
             node("q3", "Q3 · NASA X posts tomorrow", "market", 38.88, -77.02, 2), node("q5", "Q5 · cohort publication claims", "market", 51.5, -0.13, 2),
             node("fc5", "Views ≥ 26.85M by Oct 27", "market", 34.03, -118.45, 2, prob=(pilot.get("domino", {}).get("fc-5") or {}).get("p"))]
    edges = [edge("nasa", "cadence", "same weekday rhythm"), edge("who", "cadence", "campaign rhythm"), edge("bbc", "q5", "daily posting"),
             edge("cadence", "q3", "Poisson by day type",
                  evidence=f"granger MAE {((ha.get('scores') and next((s['mae_q3'] for s in ha['scores'] if s['model'] == 'domino-stats'), None)) or 0):.2f} vs Argon 1.30"),
             edge("kda", "velocity", "observed views per hour"), edge("velocity", "fc5", "extrapolate with decay")]
    lam = float(np.mean([p["value"] for p in b["benchmark"]["cases"][-1]["publication_counts"] if p.get("value") is not None]))
    items = [item("q3_mon", "NASA X posts Mon 26 Oct", "posts", round(lam, 1), 0, 3, 1.6, kind="attention", narration="Poisson, weekday rate from the prior week")]
    dom5 = pilot.get("domino", {}).get("fc-5") or {}
    if dom5.get("median"):
        items.append(item("kda_views", "K/DA FIRESTARTER views by Oct 27 (UTC midnight)", "views", dom5["median"], dom5.get("p10"), dom5.get("p90"), 27_050_000,
                          kind="attention", model="Domino velocity model",
                          narration=f"Their snapshot {yt.get('views_then'):,} → ours {yt.get('views_now'):,} ({yt.get('velocity_per_hour', 0):,.0f}/h). Hunch estimate 27.05M [26.78M, 27.6M]."
                          if yt.get("views_then") and yt.get("views_now") else "View counter unavailable"))
    for k, lab in (("trend_points_older_than_7_days", "TikTok trend points older than 7 days"), ("growth_intervals", "Measured engagement growth intervals"),
                   ("observations", "Normalized social observations")):
        if qr.get(k) is not None:
            items.append(item(k, lab, "count", qr[k], kind="attention", narration="Hunch quality report"))
    gauges = [gauge("fc5-h", "K/DA video reaches 26.85M views by Oct 27", 0.78, "hunch", "Hunch's Argon pilot", pair="fc-5"),
              gauge("fc5-d", "K/DA video reaches 26.85M views by Oct 27", dom5.get("p"), "domino", "Domino view-velocity model", pair="fc-5")]
    q5 = {m: (v.get("q5") or {}) for m, v in (cs.get("by_model") or {}).items()}
    rows = []
    for s in ha.get("scores", []):
        m = s["model"]
        rows.append({"model": m, "mae_q3": s.get("mae_q3"), "q5_claims": (q5.get(m) or {}).get("claims"), "q5_resolved": (q5.get(m) or {}).get("resolved"),
                     "q5_brier": (q5.get(m) or {}).get("brier")})
    rows.sort(key=lambda r: r["mae_q3"] if r["mae_q3"] is not None else 9)
    hb = load("domino/static/profiles/hunch/backtest.json", {}) or {}
    backtest = {"window": f"{days[0]['targetDate']}..{days[-1]['targetDate']}", "n_days": len(days), "target": "NASA X posts per day (Q3) + Q5 social claims",
                "metrics": {"crps": {"domino": {"mean": next((r["mae_q3"] for r in rows if r["model"] == "domino-stats"), None)},
                                     "ewma": {"mean": next((r["mae_q3"] for r in rows if r["model"] == "baseline"), None)}}},
                "dm_test": {"vs": "baseline", "stat": None, "p": None}, "reliability": [], "series": hb.get("series", []), "leaderboard": rows}
    audit = vert.get("social_audit") or []
    ev = stream([{"type": "data_call", "target": f"glasser · {k}", "usd": 0.0011, "seconds": 0, "cached": True} for k in list(qr.get("source_counts", {}))[:8]] +
                [{"type": "data_call", "target": "treg · youtube.video.detail (K/DA)", "usd": 0.0, "seconds": 1.2, "cached": True},
                 {"type": "argon_call", "purpose": "Argon social audit + Q5 resolution", "thinking_level": "high", "seconds": 70, "input_tokens": 20000,
                  "output_tokens": 2000, "thought_tokens": 4000, "cached": True}] +
                [{"type": "log", "level": "warn", "text": a.get("finding", "")[:140]} for a in audit[:4]])
    return write("hunch-social", "HUNCH × DOMINO · SOCIAL", "Social media next-day: posting cadence, view velocity, and what stale counters cannot tell you",
                 {"forecast_panel": "MON 26 OCT · SOCIAL", "attention_panel": "TOMORROW'S SOCIAL SIGNALS", "backtest_panel": "Q3 + Q5 SCORES",
                  "crps_label": "MAE, NASA posts · lower is better", "series_label": "NASA X posts per day: actual vs Domino Poisson band",
                  "replay_button": "Replay Oct 14–23", "domino_name": "Domino stats", "baseline_name": "Hunch baseline",
                  "leaderboard_cols": {"mae_q3": "Q3 MAE", "q5_claims": "Q5 claims", "q5_resolved": "Q5 resolved", "q5_brier": "Q5 Brier"}},
                 {"pizza": False, "attention": True, "week_ahead": False, "leaderboard": True, "replay": True, "gauges": True},
                 {"asof": b["generated_at"], "nodes": nodes, "edges": edges},
                 {"asof": b["generated_at"], "target_date": "2026-10-26", "items": items, "events": gauges,
                  "headline_summary": "Cadence beats prose for posting counts; view velocity beats guesswork for YouTube."},
                 backtest, load("domino/static/profiles/hunch/replay.json", {"frames": []}), None, ev)


# ------------------------------------------------------------------------------------------ hunch-markets (Q1, Q2, META)
HQ = {"AAPL": (37.33, -122.01), "MSFT": (47.64, -122.13), "NVDA": (37.37, -121.96), "AMZN": (47.62, -122.34), "GOOGL": (37.42, -122.08),
      "META": (37.48, -122.15), "JPM": (40.76, -73.98), "XOM": (30.07, -95.42), "WMT": (36.37, -94.21), "NFLX": (37.26, -121.96)}


def build_markets(b, days):
    ha = load("runs/hunch_analysis.json", {}) or {}
    pilot = load("runs/hunch_pilot_domino.json", {}) or {}
    hp = load("domino/static/profiles/hunch/forecast.json", {}) or {}
    from domino.hunch_analysis import q2_prob, sec_8k_dates
    import pandas as pd
    p8k, det = q2_prob(pd.Timestamp("2026-10-26"), sec_8k_dates())
    nodes = [node("calendar", "Earnings calendar (last year's week)", "observed", 40.76, -73.99, 0), node("sec", "SEC EDGAR filings", "observed", 38.9, -77.04, 0)]
    nodes += [node(tk.lower(), f"{tk} · P(8-K Mon) {det.get(tk, 0):.0%}", "observed", la, lo, 1, prob=det.get(tk)) for tk, (la, lo) in HQ.items()]
    nodes += [node("q2", "Q2 · any cohort 8-K Mon 26 Oct", "market", 38.9, -77.04, 2, prob=p8k), node("q1", "Q1 · ticker direction", "market", 40.71, -74.01, 2),
              node("meta_ret", "META Monday return", "market", 37.48, -122.15, 2)]
    edges = [edge("calendar", tk.lower(), "same week last year") for tk in HQ] + [edge(tk.lower(), "q2", "8-K hazard") for tk in HQ]
    edges += [edge("sec", "q2", "acceptance log", evidence="granger Q2 Brier 0.153 vs Argon 0.177"), edge("meta_ret", "q1", "random walk, nearly")]
    dom3 = (pilot.get("domino", {}).get("fc-3") or {}).get("buckets")
    gauges = []
    for i, lab in enumerate(("META down > 1.5%", "META within ±1.5%", "META up > 1.5%")):
        gauges.append(gauge(f"meta{i}-h", lab, [0.35, 0.45, 0.20][i], "hunch", "Hunch's Argon pilot", pair=f"meta{i}"))
        gauges.append(gauge(f"meta{i}-d", lab, dom3[i] if dom3 else None, "domino", "Domino: Student-t on EWMA volatility", pair=f"meta{i}"))
    gauges.append(gauge("q2-d", "Any cohort 8-K accepted Mon 26 Oct", p8k, "domino", "SEC histories × last-year earnings week", pair="q2"))
    gauges.append(gauge("q2-h", "Any cohort 8-K accepted Mon 26 Oct", 0.30, "hunch", "Hunch fixed baseline", pair="q2"))
    items = [i for i in (hp.get("items") or []) if i["id"] == "q2_mon"]
    rows = [{"model": s["model"], "brier_q1": s.get("brier_q1"), "brier_q2": s.get("brier_q2"), "brier_all": s.get("brier_all")} for s in ha.get("scores", [])]
    rows.sort(key=lambda r: r["brier_all"] if r["brier_all"] is not None else 9)
    series = []
    for x in days:
        a = (ha.get("argon_entry") or {}).get(x["caseId"], {})
        series.append({"date": x["targetDate"], "actual": 1.0 if x["q2Actual"] else 0.0, "median": a.get("q2Prob"), "p10": 0.0, "p90": 1.0,
                       "surprise": None, "tension": a.get("q2Prob")})
    pizza = {"asof": "2026-10-26", "index": round(p8k, 3), "note": "Per-company P(8-K Mon 26 Oct) vs its own daily base rate (bars = lift from earnings timing)",
             "places": [{"name": tk, "lat": la, "lon": lo, "live": round(100 * det.get(tk, 0), 1), "usual": None, "ratio": None,
                         "status": "earnings week" if det.get(tk, 0) > 0.1 else "quiet"} for tk, (la, lo) in HQ.items()]}
    ev = stream([{"type": "data_call", "target": f"sec.gov · submissions {tk}", "usd": 0.0, "seconds": 0.3, "cached": True} for tk in HQ] +
                [{"type": "log", "level": "info", "text": f"P(any cohort 8-K Mon 26 Oct) = {p8k:.2f}; Hunch baseline says 0.30"}])
    return write("hunch-markets", "HUNCH × DOMINO · MARKETS", "Corporate events and equities: the earnings calendar is the first domino for 8-K filings",
                 {"forecast_panel": "MON 26 OCT · MARKETS HEAD-TO-HEAD", "pizza_panel": "COHORT 8-K ODDS MONDAY (SEC × CALENDAR)", "pizza_unit": "% chance",
                  "backtest_panel": "Q1 + Q2 SCORES (10 cases)", "crps_label": "BRIER Q1+Q2 · lower is better", "series_label": "Q2 outcome (0/1) vs Domino-Argon probability",
                  "domino_name": "Domino-Argon", "baseline_name": "Hunch baseline", "replay_button": "Replay Oct 14–23",
                  "leaderboard_cols": {"brier_all": "Brier all", "brier_q1": "Brier Q1", "brier_q2": "Brier Q2"}},
                 {"pizza": True, "attention": False, "week_ahead": False, "leaderboard": True, "replay": True, "gauges": True},
                 {"asof": b["generated_at"], "nodes": nodes, "edges": edges},
                 {"asof": b["generated_at"], "target_date": "2026-10-26", "items": items, "events": gauges,
                  "headline_summary": "Earnings week: Domino puts Monday's cohort 8-K odds at {:.0%}; Hunch's fixed baseline says 30%.".format(p8k)},
                 {"window": f"{days[0]['targetDate']}..{days[-1]['targetDate']}", "n_days": len(days), "target": "Q1 ticker direction + Q2 cohort 8-K",
                  "metrics": {"crps": {"domino": {"mean": next((r["brier_all"] for r in rows if r["model"] == "domino-argon"), None)},
                                       "ewma": {"mean": next((r["brier_all"] for r in rows if r["model"] == "baseline"), None)}}},
                  "dm_test": {"vs": "baseline (sign-flip permutation)", "stat": None, "p": 0.178}, "reliability": [], "series": series, "leaderboard": rows},
                 load("domino/static/profiles/hunch/replay.json", {"frames": []}), pizza, ev)


# ------------------------------------------------------------------------------------------ hunch-life (verticals)
def build_life(b):
    vc = b["prospective"]["vertical_cache"]
    vert = load("runs/hunch_verticals_argon.json", {}) or {}
    tfm = (load("runs/timesfm_week_ahead.json", {}) or {}).get("targets", {})
    hp_pizza = load("domino/static/profiles/hunch/pizza.json")
    reg, dsl = vc["aaa_gas_national"]["prices"]["Regular"], vc["aaa_gas_national"]["prices"]["Diesel"]
    ev_cost = [float(x["ev_costperkwh"]) for x in vc.get("aaa_ev_charging", []) if x.get("ev_costperkwh")]
    z30 = next((r for r in vc["zillow_mortgage"]["rates"] if r["name"].startswith("30-Year Fixed")), {})
    rc = vc.get("rentcast_market", {}).get("saleSummary", {})
    cars = [c["listPrice"] for c in vc.get("carfax_used", []) if c.get("listPrice")]
    ins = vc.get("insider_ratios", {})
    sell_buy = [s / b_ for s, b_ in zip(ins.get("recent_sell_counts", []), ins.get("recent_buy_counts", [])) if b_]
    nodes = [node("aaa", f"AAA regular ${reg['current']:.3f}", "observed", 28.4, -81.3, 0, value=reg["current"], unit="$/gal"),
             node("ev", "EV charging", "observed", 39.0, -105.5, 0, value=round(float(np.mean(ev_cost)), 3) if ev_cost else None, unit="$/kWh"),
             node("zillow", "Zillow 30-yr quote", "observed", 47.61, -122.33, 0, value=z30.get("interestRate"), unit="%"),
             node("rentcast", "Austin 78701 median sale", "observed", 30.27, -97.74, 0, value=rc.get("medianPrice"), unit="$"),
             node("carfax", "Carfax used Camry", "observed", 38.84, -77.43, 0, value=float(np.median(cars)) if cars else None, unit="$"), node("keepa", "Keepa Amazon prices", "observed", 47.62, -122.34, 0),
             node("insider", "Insider sell/buy", "observed", 38.9, -77.04, 0, value=round(sell_buy[-1], 2) if sell_buy else None, unit="×"),
             node("jobs", "Wellfound startup jobs", "observed", 37.77, -122.42, 0),
             node("driving", "Cost of driving", "latent", 39.8, -98.6, 1, prob=0.6), node("housing", "Cost of housing", "latent", 41.9, -87.6, 1, prob=0.6),
             node("goods", "Prices of goods", "latent", 36.2, -115.1, 1, prob=0.4), node("labor", "Labor market", "latent", 40.7, -74.0, 1, prob=0.5),
             node("pump", "Gas next week (TimesFM)", "daily_life", 39.83, -98.58, 3, value=(tfm.get("gas") or {}).get("median")),
             node("mortgage", "Mortgage next week (TimesFM)", "daily_life", 38.9, -77.03, 3, value=(tfm.get("mortgage") or {}).get("median"))]
    edges = [edge("aaa", "driving", "pump prices"), edge("ev", "driving", "kWh prices"), edge("zillow", "housing", "rates"), edge("rentcast", "housing", "prices"),
             edge("carfax", "goods", "used-car prices"), edge("keepa", "goods", "shelf prices"), edge("insider", "labor", "corporate confidence"),
             edge("jobs", "labor", "hiring"), edge("driving", "pump", "pass-through", evidence="granger p=2e-15; MAE -35%"),
             edge("housing", "mortgage", "10-year Treasury", evidence="granger p=3e-34; MAE -26%")]
    items = []
    for key, label, unit in (("gas", "Gas next week", "$/gal"), ("mortgage", "Mortgage next week", "%")):
        t = tfm.get(key)
        if t:
            items.append(item(f"life_{key}", label, unit, round(t["median"], 3), round(t["quantiles"][0], 3), round(t["quantiles"][-1], 3), round(t["last"], 3),
                              kind="daily_life", model="TimesFM 3.0 (Google)"))
    items.append(item("life_diesel", "Diesel today", "$/gal", round(dsl["current"], 3), base=round(dsl["week_ago"], 3), kind="daily_life", model="AAA via Glasser",
                      narration=f"+{100 * (dsl['current'] / dsl['year_ago'] - 1):.0f}% vs a year ago"))
    if ev_cost:
        items.append(item("life_ev", "EV charging", "$/kWh", round(float(np.mean(ev_cost)), 3), round(float(np.quantile(ev_cost, 0.1)), 3),
                          round(float(np.quantile(ev_cost, 0.9)), 3), kind="daily_life", model="AAA via Glasser"))
    if cars:
        items.append(item("life_car", "Used Camry", "$", float(np.median(cars)), float(np.quantile(cars, 0.1)), float(np.quantile(cars, 0.9)),
                          kind="daily_life", model="Carfax via Glasser"))
    if sell_buy:
        items.append(item("insider_ratio", "Insider sell/buy ratio (latest)", "ratio", round(sell_buy[-1], 2), round(min(sell_buy), 2), round(max(sell_buy), 2),
                          base=round(float(np.mean(sell_buy)), 2), kind="attention", narration="SEC Form 4 counts, last 10 periods"))
    gauges = []
    for key, lab in (("gas", "Gas lower next week than today"), ("mortgage", "Mortgage rate lower next week")):
        t = tfm.get(key)
        if t:
            q = np.array(t["quantiles"])
            p_down = float(np.interp(t["last"], np.sort(q), np.linspace(0.1, 0.9, 9))) if q.min() < t["last"] < q.max() else (0.95 if t["last"] >= q.max() else 0.05)
            gauges.append(gauge(f"{key}-down", lab, p_down, "domino", "TimesFM 3.0 quantiles"))
    vrows = [{"model": v["vertical"][:34], "today": v["what_it_says_today"][:60], "first_domino": v["first_domino"][:50]} for v in (vert.get("verticals") or [])[:8]]
    dl = (load("runs/daily_life_results.json", {}) or {}).get("targets", {})
    sota = (load("runs/sota_timesfm.json", {}) or {}).get("results", {})
    rows = []
    for k in ("gas", "mortgage", "flu"):
        if k in dl:
            rows.append({"model": f"{k}: Domino regression", "error_vs_no_change_pct": round(dl[k]["vs_no_change"]["pct"], 1), "direction_hit": round(dl[k]["direction_hit"], 2)})
        if k in sota:
            rows.append({"model": f"{k}: TimesFM 3.0", "error_vs_no_change_pct": round(sota[k]["timesfm_vs_no_change"]["pct"], 1), "direction_hit": round(sota[k]["timesfm_direction_hit"], 2)})
    ev = stream([{"type": "data_call", "target": f"glasser · {k}", "usd": 0.002, "seconds": 0, "cached": True} for k in vc] +
                [{"type": "argon_call", "purpose": "Argon cross-vertical brief", "thinking_level": "high", "seconds": 80, "input_tokens": 25000,
                  "output_tokens": 3000, "thought_tokens": 5000, "cached": True}] +
                [{"type": "log", "level": "info", "text": (vert.get("cross_vertical_story") or "")[:160]}])
    return write("hunch-life", "HUNCH × DOMINO · DAILY LIFE", "What Hunch's verticals mean for your week: pump, power, rent, mortgage, cars and jobs",
                 {"forecast_panel": "YOUR WEEK · ODDS", "pizza_panel": "GAS AT THE PUMP BY STATE (AAA via Glasser)", "pizza_unit": "state ÷ national",
                  "week_ahead": "YOUR WEEK AHEAD", "attention_panel": "CORPORATE CONFIDENCE", "backtest_panel": "BACKTESTED SKILL (weekly, vs no-change)",
                  "crps_label": "GAS MAE $/gal, week ahead · lower is better", "domino_name": "TimesFM 3.0", "baseline_name": "No change",
                  "leaderboard_cols": {"error_vs_no_change_pct": "error vs no-change %", "direction_hit": "direction right"}},
                 {"pizza": True, "attention": True, "week_ahead": True, "leaderboard": True, "replay": False, "gauges": True},
                 {"asof": b["generated_at"], "nodes": nodes, "edges": edges},
                 {"asof": b["generated_at"], "target_date": "2026-11-02", "items": items, "events": gauges,
                  "headline_summary": vert.get("cross_vertical_story", "")[:300], "vertical_notes": vrows},
                 {"window": "2016..2026 weekly", "n_days": None, "target": "Week-ahead skill on the series behind Hunch's verticals",
                  "metrics": {"crps": {"domino": {"mean": (sota.get("gas") or {}).get("mae_timesfm")}, "ewma": {"mean": (sota.get("gas") or {}).get("mae_no_change")}}},
                  "dm_test": {"vs": "no-change", "stat": None, "p": ((sota.get("gas") or {}).get("timesfm_vs_no_change") or {}).get("dm", {}).get("p")},
                  "reliability": [], "series": [], "leaderboard": rows}, None, hp_pizza, ev)


# ------------------------------------------------------------------------------------------ our analyses: daily-life and categories
def build_daily_life():
    dl = (load("runs/daily_life_results.json", {}) or {}).get("targets", {})
    sota = (load("runs/sota_timesfm.json", {}) or {}).get("results", {})
    tfm = (load("runs/timesfm_week_ahead.json", {}) or {}).get("targets", {})
    g = load("runs/graph_latest.json", {}) or {}
    keep = {"hormuz", "brent", "gasoline", "pump", "treasury", "mortgage", "flu", "escalation", "news", "attention"}
    nodes = [n for n in g.get("nodes", []) if n["id"] in keep]
    edges = [e for e in g.get("edges", []) if e["source"] in keep and e["target"] in keep]
    items = []
    for key, label, unit in (("gas", "Your gas price next week", "$/gal"), ("mortgage", "30-year mortgage next week", "%"), ("flu", "Flu activity next week", "% ILI")):
        t = tfm.get(key)
        if t:
            items.append(item(f"life_{key}", label, unit, round(t["median"], 3), round(t["quantiles"][0], 3), round(t["quantiles"][-1], 3), round(t["last"], 3),
                              kind="daily_life", model="TimesFM 3.0 (Google)",
                              narration=f"Backtest error {((sota.get(key) or {}).get('timesfm_vs_no_change') or {}).get('pct', 0):+.0f}% vs no-change"))
    rows = []
    for k, r in dl.items():
        rows.append({"model": r["label"][:40], "n": r["n"], "domino_vs_no_change_pct": round(r["vs_no_change"]["pct"], 1),
                     "timesfm_vs_no_change_pct": round(((sota.get(k) or {}).get("timesfm_vs_no_change") or {}).get("pct"), 1) if k in sota else None,
                     "dm_p": r["vs_no_change"]["dm"]["p"], "direction_hit": round(r["direction_hit"], 2)})
    gs = dl.get("gas", {}).get("series", {})
    series = []
    if gs:
        for d_, lp, ac, pm in list(zip(gs["dates"], gs["level_prev"], gs["actual_change"], gs["pred_model"]))[-52:]:
            mae = dl["gas"]["mae_model"]
            series.append({"date": d_, "actual": lp + ac, "median": lp + pm, "p10": lp + pm - 1.28 * mae * 1.25, "p90": lp + pm + 1.28 * mae * 1.25,
                           "surprise": abs(ac - pm) / max(mae, 1e-6), "tension": None})
    gauges = []
    for key, lab in (("gas", "Gas lower next week"), ("mortgage", "Mortgage lower next week"), ("flu", "Flu higher next week")):
        t = tfm.get(key)
        if t:
            q = np.sort(np.array(t["quantiles"]))
            cdf = float(np.interp(t["last"], q, np.linspace(0.1, 0.9, 9))) if q[0] < t["last"] < q[-1] else (0.95 if t["last"] >= q[-1] else 0.05)
            gauges.append(gauge(f"{key}-dir", lab, 1 - cdf if key == "flu" else cdf, "domino", "TimesFM 3.0 quantiles"))
    return write("daily-life", "DOMINO · YOUR WEEK", "From Hormuz to your pump: measured week-ahead forecasts for gas, mortgages and flu",
                 {"forecast_panel": "YOUR WEEK · ODDS", "week_ahead": "YOUR WEEK AHEAD", "backtest_panel": "WEEK-AHEAD SKILL (rolling, out of sample)",
                  "crps_label": "GAS MAE $/gal · lower is better", "series_label": "Gas at the pump: actual vs Domino band (last 52 weeks)",
                  "domino_name": "TimesFM 3.0", "baseline_name": "No change",
                  "leaderboard_cols": {"n": "weeks", "domino_vs_no_change_pct": "Domino %", "timesfm_vs_no_change_pct": "TimesFM %", "dm_p": "DM p", "direction_hit": "direction"}},
                 {"pizza": False, "attention": False, "week_ahead": True, "leaderboard": True, "replay": False, "gauges": True},
                 {"asof": g.get("asof"), "nodes": nodes, "edges": edges},
                 {"asof": g.get("asof"), "target_date": "2026-11-02", "items": items, "events": gauges,
                  "headline_summary": "Futures lead the pump by a week; Treasuries lead mortgages by two."},
                 {"window": "2016..2026 weekly", "n_days": None, "target": "Next-week level forecasts vs no-change",
                  "metrics": {"crps": {"domino": {"mean": (sota.get("gas") or {}).get("mae_timesfm")}, "ewma": {"mean": (sota.get("gas") or {}).get("mae_no_change")}}},
                  "dm_test": {"vs": "no-change", "stat": None, "p": dl.get("gas", {}).get("vs_no_change", {}).get("dm", {}).get("p")},
                  "reliability": [], "series": series, "leaderboard": rows})


CAT_LL = {"geopolitics_energy": (26.57, 56.25), "macro_stress": (40.71, -74.01), "crypto": (37.77, -122.42), "ai_tech": (37.39, -122.08),
          "russia_ukraine": (50.45, 30.52), "china_taiwan_trade": (25.03, 121.57), "health": (46.23, 6.13), "weather_disasters": (25.76, -80.19)}


def build_categories():
    cr = (load("runs/category_results.json", {}) or {}).get("categories", {})
    fd = load("runs/first_domino_results.json", []) or []
    interp = load("analysis/argon_category_interpretation.json", {}) or {}
    nodes, edges, rows = [], [], []
    for k, c in cr.items():
        la, lo = CAT_LL.get(k, (0, 0))
        f = c.get("first_domino") or {}
        af = c["attention_forecast"]
        nodes.append(node(f"att_{k}", f"{c['label']} · attention", "attention", la, lo, 0, prob=max(0.0, min(1.0, -af["diff"]["mean"] * 20))))
        if f:
            nodes.append(node(f"fd_{k}", f"First domino: {f['signal'].replace('_', ' ')}", "latent", la + 3, lo + 3, 1, prob=0.8))
            edges.append(edge(f"att_{k}", f"fd_{k}", "leading article", evidence=f"granger leads {f['leads']} (best p={f['best_p']:.1g})"))
        rows.append({"model": c["label"][:38], "attention_mae_diff": round(af["diff"]["mean"], 3), "attention_p": af["dm"]["p"],
                     "first_domino": (f.get("signal") or "none").replace("_", " ")[:28], "attn_leads_mkts": c.get("attention_leads_markets"),
                     "mkts_lead_attn": c.get("markets_lead_attention")})
    for r in fd:
        tid = f"tgt_{r['target']}"
        if not any(n["id"] == tid for n in nodes):
            la, lo = CAT_LL.get(r["category"], (0, 0))
            nodes.append(node(tid, f"{r['target'].upper()} volatility", "market", la - 3, lo - 3, 2))
        lsd = r["logscore_diff"]
        sig = lsd["lo"] is not None and lsd["lo"] > 0
        edges.append(edge(f"fd_{r['category']}", tid, "attention scales volatility",
                          evidence=(f"granger logS {lsd['mean']:+.3f} [{lsd['lo']:+.3f},{lsd['hi']:+.3f}]" if sig else f"logS {lsd['mean']:+.3f} (n.s.)")))
    rows.sort(key=lambda r: r["attention_mae_diff"])
    gauges = [gauge(f"rank{int(r['rank'])}", f"#{int(r['rank'])} {r['category'].split('(')[0].strip()}", r["score_0_10"] / 10, "argon", r["first_domino"][:120])
              for r in interp.get("ranking", [])[:4]]
    return write("categories", "DOMINO · 8 WORLDS", "Where next-day prediction works: attention is predictable, returns are not, and one first domino is real",
                 {"forecast_panel": "ARGON'S RANKING (score / 10)", "backtest_panel": "NEXT-DAY ATTENTION vs PERSISTENCE (8 categories)",
                  "crps_label": "ATTENTION MAE, log views · mean of 8", "domino_name": "Domino AR", "baseline_name": "Persistence",
                  "leaderboard_cols": {"attention_mae_diff": "MAE diff", "attention_p": "DM p", "first_domino": "first domino", "attn_leads_mkts": "attn→mkt", "mkts_lead_attn": "mkt→attn"}},
                 {"pizza": False, "attention": False, "week_ahead": False, "leaderboard": True, "replay": False, "gauges": True},
                 {"asof": None, "nodes": nodes, "edges": edges},
                 {"asof": None, "target_date": None, "items": [], "events": gauges,
                  "headline_summary": "Recession attention → next-day S&P volatility is the one confirmed first domino (log score +0.018 [+0.004, +0.036])."},
                 {"window": "2024..2026 daily", "n_days": None, "target": "Next-day attention (social-engagement proxy) and first-domino volatility models",
                  "metrics": {"crps": {"domino": {"mean": float(np.mean([c["attention_forecast"]["mae_ar"]["mean"] for c in cr.values()]))},
                                       "ewma": {"mean": float(np.mean([c["attention_forecast"]["mae_persistence"]["mean"] for c in cr.values()]))}}},
                  "dm_test": {}, "reliability": [], "series": [], "leaderboard": rows})


# ------------------------------------------------------------------------------------------ real estate (domino/realestate.py)
def build_real_estate():
    rr = load("runs/realestate_results.json")
    if not rr:
        raise RuntimeError("run domino/realestate.py stats first")
    ra = load("runs/realestate_argon.json", {}) or {}
    tf = load("runs/realestate_timesfm.json", {}) or {}
    vc = ((load("external/hunch_live/bundle.json", {}) or {}).get("prospective") or {}).get("vertical_cache", {})
    rc = (vc.get("rentcast_market") or {}).get("saleSummary", {}) or {}
    rt, pr, rn, cu = rr["rates"], rr["prices"], rr["rents"], rr["cuts"]
    ens, st, brief = ra.get("argon_ensemble") or {}, ra.get("stats") or {}, ra.get("brief") or {}
    wm, fn, h6 = rt["weekly_model"], rt["forecast_next"], pr["h6"]
    gp = min((v["p"] for v in (wm.get("granger") or {}).values() if v), default=None)
    notes = {m["metro"]: m for m in brief.get("metros", [])}
    by_fc = sorted(pr["metros"], key=lambda x: x["forecast_next_mom_pct"])
    pick = []
    for x in by_fc[:5] + by_fc[-3:] + [m for m in pr["metros"] if m["metro"] in ("Austin, TX", "New York, NY", "Los Angeles, CA", "Miami, FL")]:
        if x not in pick:
            pick.append(x)
    slug = lambda m: "m_" + re.sub(r"[^a-z]+", "_", m.lower()).strip("_")
    sd_med = float(np.median([x["resid_sd"] for x in pr["metros"]]))
    cuts_med = float(np.median([x["realtor"]["price_reduced_share"] for x in pr["metros"] if x.get("realtor")]))
    dom_med = float(np.median([x["realtor"]["days_on_market"] for x in pr["metros"] if x.get("realtor")]))
    tnx = rt["tnx_last"]
    nodes = [node("tnx", "10-year Treasury", "observed", 40.71, -74.01, 0, value=round(tnx["yield"], 2), unit="%",
                  narration=f"{tnx['week_change_bp']:+.0f} bp on the week to {tnx['date']}"),
             node("zori", "Market rents (Zillow ZORI)", "observed", 47.61, -122.33, 0, value=round(rn["now"]["zori_yoy"], 2), unit="% y/y"),
             node("cuts", "Price cuts (Realtor.com)", "observed", 37.0, -95.0, 0, value=round(100 * cuts_med, 1), unit="% of listings"),
             node("pmms", "Freddie Mac 30-year (PMMS)", "observed", 38.93, -77.18, 1, value=rt["pmms_last"]["rate"], unit="%",
                  narration=f"{rt['pmms_last']['date']}; year ago {rt['pmms_year_ago']:.2f}%"),
             node("spread", "Mortgage spread over Treasury", "observed", 41.5, -72.5, 1, value=round(rt["spread"]["now"], 2), unit="pp"),
             node("momentum", "US price momentum", "observed", 39.1, -94.6, 2, value=round(pr["us"]["mom_pct"], 2), unit="% m/m"),
             node("cpi_rent", "CPI rent (BLS)", "daily_life", 38.90, -77.01, 2, value=round(rn["now"]["cpi_rent_yoy"], 2), unit="% y/y"),
             node("rent_2027", f"Your rent inflation, {rn['forecast_12m']['target']}", "daily_life", 34.0, -84.0, 3,
                  value=round(rn["forecast_12m"]["cpi_rent_yoy"], 2), unit="% y/y")]
    if rc:
        nodes.append(node("austin", "Austin 78701 (RentCast)", "observed", 30.27, -97.74, 2, value=rc.get("averageDaysOnMarket"), unit="days on market",
                          narration=brief.get("austin_78701", "")[:220]))
    for x in pick:
        city = x["metro"].split(",")[0]
        rl = x.get("realtor") or {}
        nodes.append(node(slug(x["metro"]), f"{city} · Oct", "market", x["lat"], x["lon"], 3, prob=x["p_decline_next"], value=round(x["forecast_next_mom_pct"], 2),
                          unit="% m/m", narration=(notes.get(x["metro"], {}).get("outlook") or
                                                   f"ZHVI ${x['zhvi']:,.0f} ({x['yoy_pct']:+.1f}% y/y); {100 * rl.get('price_reduced_share', 0):.0f}% of listings cut, "
                                                   f"{rl.get('days_on_market', 0):.0f} days on market")[:240]))
    tf_pct = wm.get("timesfm_vs_no_change_pct")
    edges = [edge("tnx", "pmms", "lenders price off the 10-year", evidence=f"granger p={gp:.0e} weekly; TimesFM {tf_pct:+.0f}% error vs no-change" if gp else "Argon prior", active=0.95),
             edge("spread", "pmms", "the spread mean-reverts", evidence=f"Argon prior; spread z {rt['spread']['z']:+.2f} vs 2024+", active=0.4),
             edge("pmms", "momentum", "payments rise with rates; demand shows up in prices only slowly",
                  evidence=f"prior: no out-of-sample skill (next month {pr['rates_vs_ar']['pct']:+.0f}% error, 6 months {h6['pct']:+.1f}%)", active=0.25),
             edge("cuts", "momentum", "price cuts precede price changes?", evidence=f"prior: no skill ({cu.get('pct', 0):+.1f}% error, p={cu.get('dm', {}).get('p', 1):.2f})", active=0.2),
             edge("zori", "cpi_rent", "new leases reach the CPI sample with a lag",
                  evidence=f"corr {rn['corr_at_best']:.2f} at a {rn['best_lead_months']}-month lead; granger p={rn['granger']['p']:.3f}", active=0.95),
             edge("cpi_rent", "rent_2027", "rent inflation a year out", evidence=f"corr-lead model {rn['oos_12m']['vs_persistence']['pct']:+.0f}% error vs persistence", active=0.8),
             edge("cpi_rent", "tnx", "shelter is a third of CPI; inflation expectations move long yields", evidence="Argon prior", active=0.5)]
    if rc:
        edges.append(edge("austin", "momentum", "a buyer's market downtown", evidence="anecdotal: one ZIP snapshot (RentCast via Glasser)", active=0.3))
    edges += [edge("momentum", slug(x["metro"]), "this month's trend continues",
                   evidence=f"corr: AR momentum {100 * (pr['mae']['ar_only'] / pr['mae']['momentum'] - 1):+.0f}% error vs naive momentum", active=0.7) for x in pick]
    pm_p = (fn.get("p_lower_than_last"), ens.get("p_pmms_below_last"))
    zh_p = (pr["us"]["p_decline_next"], ens.get("p_zhvi_decline"))
    cp_p = (rn["next_print"]["p_below_0_30"], ens.get("p_cpi_rent_below_0_30"))
    gauges = []
    for key, lab, (ps, pa), how in (("pmms", f"Freddie 30-yr below {rt['pmms_last']['rate']:.2f}% on Thu 29 Oct", pm_p, "TimesFM 3.0 quantiles"),
                                    ("zhvi", f"US home values fall in {pr['next_month']}", zh_p, "pooled AR momentum"),
                                    ("cpi", f"CPI rent {rn['next_print']['month']} m/m below 0.30%", cp_p, "AR + market rents a year earlier")):
        gauges.append(gauge(f"{key}-d", lab, ps, "domino", f"Domino stats: {how}", pair=key))
        gauges.append(gauge(f"{key}-a", lab, pa, "argon", "5-sample Argon ensemble with live news", pair=key))
    us = pr["us"]
    zt = tf.get("zori_us", {}).get("next", {})
    np_ = rn["next_print"]
    items = [item("pmms_oct29", "Freddie 30-yr, Thu 29 Oct", "%", round(fn["median"], 2), round(fn["p10"], 2), round(fn["p90"], 2), rt["pmms_last"]["rate"], kind="market",
                  model=fn["model"], narration=(f"Argon ensemble: {ens['pmms_median']:.2f}% [{ens['pmms_p10']:.2f}, {ens['pmms_p90']:.2f}]" if ens.get("pmms_median") else None)),
             item("cpi_rent_next", f"CPI rent m/m, {np_['month']}", "%", round(np_["mom_pct"], 3), round(np_["p10"], 3), round(np_["p90"], 3), round(np_["last_mom_pct"], 3),
                  kind="market", model="AR + market rents a year earlier"),
             ]
    items += [item("wk_mortgage", "Mortgage next week", "%", round(fn["median"], 2), round(fn["p10"], 2), round(fn["p90"], 2), rt["pmms_last"]["rate"], kind="daily_life",
                   model="TimesFM 3.0 (Google)", narration=f"Backtest error {tf_pct:+.0f}% vs no-change" if tf_pct else None),
              item("wk_rent", f"Rent inflation, {rn['forecast_12m']['target']}", "%", round(rn["forecast_12m"]["cpi_rent_yoy"], 2), round(rn["forecast_12m"]["p10"], 2),
                   round(rn["forecast_12m"]["p90"], 2), round(rn["now"]["cpi_rent_yoy"], 2), kind="daily_life", model="market-rent lead",
                   narration=f"Backtest error {rn['oos_12m']['vs_persistence']['pct']:+.0f}% vs persistence"),
              item("wk_home", f"US home value, {pr['next_month']}", "$", round(us["zhvi"] * (1 + us["forecast_next_mom_pct"] / 100)), base=round(us["zhvi"]), kind="daily_life",
                   model="AR momentum (Zillow ZHVI)", narration=f"{us['yoy_pct']:+.1f}% over the last year")]
    items += [item("dom_med", "Median days on market (36 metros)", "days", round(dom_med), kind="attention", narration="Realtor.com, Sep 2026"),
              item("cuts_med", "Listings with a price cut (median metro)", "%", round(100 * cuts_med, 1), kind="attention", narration="Realtor.com, Sep 2026")]
    if rc:
        items += [item("austin_dom", "Austin 78701 days on market", "days", rc.get("averageDaysOnMarket"), kind="attention", narration="RentCast via Glasser, 25 Oct"),
                  item("austin_listings", "Austin 78701 sale listings", "count", rc.get("totalListings"), kind="attention", narration="RentCast via Glasser, 25 Oct")]
    top_cuts = sorted([x for x in pr["metros"] if x.get("realtor")], key=lambda x: -x["realtor"]["price_reduced_share"])[:10]
    pizza = {"asof": "2026-09", "index": round(100 * cuts_med, 1),
             "note": "Share of active listings with a price cut, Sep 2026 (Realtor.com). Momentum, not cuts, predicts next month's prices (measured).",
             "places": [{"name": x["metro"].split(",")[0], "lat": x["lat"], "lon": x["lon"], "live": round(100 * x["realtor"]["price_reduced_share"], 1), "usual": None,
                         "ratio": None, "status": f"{x['realtor']['days_on_market']:.0f} days on market"} for x in top_cuts]}
    o12 = rn["oos_12m"]
    err = np.array([r["y"] - r["zori_model"] for r in o12["rows"]])
    q10, q90 = (float(np.quantile(err, 0.1)), float(np.quantile(err, 0.9))) if len(err) else (0.0, 0.0)
    series = [{"date": f"{r['target']}-15", "actual": r["y"], "median": r["zori_model"], "p10": r["zori_model"] + q10, "p90": r["zori_model"] + q90,
               "surprise": abs(r["y"] - r["zori_model"]) / max(o12["mae_zori_model"], 1e-6), "tension": None} for r in o12["rows"]]
    t = lambda k: tf.get(k, {})
    rows = [{"model": "Mortgage weekly · TimesFM 3.0", "vs_naive_pct": round(tf_pct, 1) if tf_pct else None, "compared_with": "no change", "dm_p": None, "verdict": "works"},
            {"model": "Mortgage weekly · Treasury regression", "vs_naive_pct": round(wm["domino_vs_no_change_pct"], 1), "compared_with": "no change", "dm_p": wm["dm_p"], "verdict": "works"},
            {"model": "CPI rent 12 mo ahead · market-rent lead", "vs_naive_pct": round(o12["vs_persistence"]["pct"], 1), "compared_with": "persistence",
             "dm_p": o12["vs_persistence"]["dm"]["p"], "verdict": "works (n.s.)"},
            {"model": "CPI rent next print · AR + rents", "vs_naive_pct": round(100 * (np_["mae_model"] / np_["mae_no_change"] - 1), 1), "compared_with": "no change", "dm_p": None, "verdict": "works"}]
    if t("cpi_rent"):
        rows.append({"model": "CPI rent next print · TimesFM 3.0", "vs_naive_pct": round(t("cpi_rent")["timesfm_vs_momentum_pct"], 1), "compared_with": "momentum",
                     "dm_p": t("cpi_rent")["dm_vs_momentum"]["p"], "verdict": "works (n.s.)"})
    if t("zori_us"):
        rows.append({"model": "Market rent next month · TimesFM 3.0", "vs_naive_pct": round(t("zori_us")["timesfm_vs_momentum_pct"], 1), "compared_with": "momentum",
                     "dm_p": t("zori_us")["dm_vs_momentum"]["p"], "verdict": "works"})
    rows += [{"model": "Home values next month · AR momentum", "vs_naive_pct": round(100 * (pr["mae"]["ar_only"] / pr["mae"]["momentum"] - 1), 1), "compared_with": "naive momentum",
              "dm_p": None, "verdict": "works"},
             {"model": "Home values next month · + mortgage rates", "vs_naive_pct": round(pr["rates_vs_ar"]["pct"], 1), "compared_with": "AR momentum",
              "dm_p": pr["rates_vs_ar"]["dm"]["p"], "verdict": "no skill"},
             {"model": "Home values 6 months · + mortgage rates", "vs_naive_pct": round(h6["pct"], 1), "compared_with": "momentum model", "dm_p": h6["dm"]["p"], "verdict": "no skill"},
             {"model": "Home values next month · + price cuts", "vs_naive_pct": round(cu.get("pct", 0), 1), "compared_with": "AR momentum", "dm_p": cu.get("dm", {}).get("p"), "verdict": "no skill"}]
    if t("zhvi_us"):
        rows.append({"model": "Home values next month · TimesFM 3.0", "vs_naive_pct": round(t("zhvi_us")["timesfm_vs_momentum_pct"], 1), "compared_with": "momentum",
                     "dm_p": t("zhvi_us")["dm_vs_momentum"]["p"], "verdict": "worse"})
    backtest = {"window": o12["window"], "n_days": None, "target": "What predicts housing, out of sample (weekly rates, monthly prices and rents)",
                "metrics": {"crps": {"domino": {"mean": o12["mae_zori_model"]}, "ewma": {"mean": o12["mae_persistence"]}}},
                "dm_test": {"vs": "persistence", "stat": o12["vs_persistence"]["dm"].get("stat"), "p": o12["vs_persistence"]["dm"]["p"]},
                "reliability": [], "series": series, "leaderboard": rows}
    srcs = [("zillow.com · ZHVI metro CSV", 0), ("zillow.com · ZORI metro CSV", 0), ("realtor.com · inventory history", 0), ("bls.gov · CPI rent (API v1)", 0),
            ("freddiemac.com · PMMS history", 0), ("yfinance · ^TNX", 0)]
    ev = stream([{"type": "data_call", "target": n, "usd": c, "seconds": 0.8, "cached": True} for n, c in srcs] +
                [{"type": "data_call", "target": f"treg · news '{k}'", "usd": 0.0, "seconds": 1.5, "cached": True} for k in (ra.get("news") or {})] +
                [{"type": "argon_call", "purpose": f"Argon housing ensemble {i + 1}/5", "thinking_level": "high", "seconds": 60, "input_tokens": 6000, "output_tokens": 900,
                  "thought_tokens": 2500, "cached": True} for i in range(int(ens.get("n") or 0))] +
                ([{"type": "argon_call", "purpose": "Argon metro brief", "thinking_level": "high", "seconds": 80, "input_tokens": 14000, "output_tokens": 2500,
                   "thought_tokens": 4000, "cached": True}] if brief else []) +
                [{"type": "log", "level": "info", "text": f"Market rents lead CPI rent by {rn['best_lead_months']} months (corr {rn['corr_at_best']:.2f})"},
                 {"type": "log", "level": "warn", "text": f"Mortgage rates add no next-month skill for home values ({pr['rates_vs_ar']['pct']:+.0f}% error); momentum rules"},
                 {"type": "log", "level": "warn", "text": f"Price cuts add no next-month skill ({cu.get('pct', 0):+.1f}%, p={cu.get('dm', {}).get('p', 1):.2f})"}])
    return write("real-estate", "DOMINO · REAL ESTATE", "From the 10-year Treasury to your rent: what moves housing next, and what does not",
                 {"forecast_panel": "THIS WEEK · HOUSING", "attention_panel": "LISTINGS RIGHT NOW", "week_ahead": "YOUR HOUSING AHEAD",
                  "pizza_panel": "PRICE CUTS BY METRO (REALTOR.COM, SEP)", "pizza_unit": "% of listings", "backtest_panel": "WHAT PREDICTS HOUSING (out of sample)",
                  "crps_label": "CPI RENT Y/Y, 12 MONTHS AHEAD · MAE (pp)", "domino_name": "Market-rent lead", "baseline_name": "Persistence",
                  "series_label": "CPI rent y/y: actual vs forecast made 12 months earlier from market rents", "market_prob": "P(fall)",
                  "gauges_caption": "Odds · Domino stats vs 5-sample Argon ensemble", "chain_title": "MEASURED CHAINS",
                  "chain_hint": "Level cards: measured links only, read left to right",
                  "short": {"pmms_oct29": "Mortgage · Thu", "cpi_rent_next": "CPI rent · Oct", "zhvi_next": "Home values · Oct"},
                  "legend_note": "Rings: high P(fall). Near-solid arcs = measured lead (Granger / out of sample), dashed = mechanism without measured skill, "
                                 "fine dashes = anecdotal. Ivory arcs end at your rent.",
                  "leaderboard_cols": {"vs_naive_pct": "error vs comparison %", "compared_with": "compared with", "dm_p": "DM p", "verdict": "verdict"}},
                 {"pizza": True, "attention": True, "week_ahead": True, "leaderboard": True, "replay": False, "gauges": True},
                 {"asof": rr["created"], "nodes": nodes, "edges": edges},
                 {"asof": rr["created"], "target_date": "2026-10-29", "items": items, "events": gauges,
                  "headline_summary": (brief.get("chain_story") or "Treasuries move mortgages within days; market rents move CPI rent a year later; "
                                       "home values mostly follow their own momentum.")[:320]},
                 backtest, None, pizza, ev,
                 view={"page": "realestate", "level": True,
                       "chains": [{"title": "Rates · measured weekly", "ids": ["tnx", "pmms"]}, {"title": "Rents · 13-month lead", "ids": ["zori", "cpi_rent", "rent_2027"]}]})


def main():
    b = json.load(open(R("external", "hunch_live", "bundle.json")))
    days = b["benchmark"]["evaluations"]["days"]
    index = [{"id": "domino", "title": "DOMINO (live)", "blurb": "Live next-day world model: Hormuz → oil → your pump"}]
    hp = load("domino/static/profiles/hunch/profile.json")
    if hp:
        index.append({"id": "hunch", "title": hp["brand"], "blurb": hp["subtitle"]})
    for fn in (lambda: build_world(b, days), lambda: build_social(b, days), lambda: build_markets(b, days), lambda: build_life(b), build_daily_life, build_categories, build_real_estate):
        try:
            index.append(fn())
        except Exception as exc:  # one profile failing never blocks the others
            print("profile failed:", type(exc).__name__, str(exc)[:200])
    json.dump(index, open(os.path.join(PROF, "index.json"), "w"), indent=2)
    print("profiles:", [p["id"] for p in index])
    try:
        from domino.realestate_dashboard import build as build_re_dashboard
        build_re_dashboard()
    except Exception as exc:  # the simple real estate page is optional
        print("real estate dashboard failed:", type(exc).__name__, str(exc)[:200])


if __name__ == "__main__":
    main()
