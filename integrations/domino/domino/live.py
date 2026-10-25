"""Domino live pipeline: pull signals (treg + free sources), let Argon reason, forecast tomorrow, pre-register a hash.

Order of operations (each step emits events for the UI, see domino/CONTRACT.md):
  1. data pulls in parallel: treg news (free), treg Google Trends ($0.0012), Wikipedia attention (free),
     yfinance closes (free), treg pizza busyness (anecdotal; usually null today)
  2. statistical forecast per target: HMM tension + Student-t regime mixture (backtested, strict lag)
  3. Argon (thinking high, priority tier) reads headlines + signals + model output -> latent node probabilities,
     event probabilities, per-target adjustments, one-line narration per domino
  4. RPWM recursion on surprise: while belief entropy keeps falling by > delta (relative), Argon picks the next
     data purchase by expected information gain per dollar from a priced menu; we buy it and Argon updates
  5. forecast payload (stats and Argon-adjusted shown side by side) + SHA-256 pre-registration hash
"""
import concurrent.futures as cf
import glob
import hashlib
import json
import math
import os
import time

import numpy as np
import pandas as pd

from rpwm import core
from rpwm.argon import Argon
from . import history as H
from . import model as M
from . import treg_client as tc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = {"brent": ("Brent crude", "BZ=F"), "wti": ("WTI crude", "CL=F"), "natgas": ("Natural gas", "NG=F"),
           "gasoline": ("RBOB gasoline", "RB=F"), "airlines": ("Airlines (JETS)", "JETS"), "energy": ("Energy stocks (XLE)", "XLE"),
           "defense": ("Defense (ITA)", "ITA"), "sp500": ("S&P 500", "^GSPC"), "gold": ("Gold", "GC=F")}
NEWS_QUERIES = ["Iran Strait of Hormuz", "Israel Iran strike", "oil prices OPEC", "Houthis Red Sea shipping", "Pentagon Iran"]
TREND_SETS = [["Strait of Hormuz", "oil price", "Iran"], ["gas prices", "World War 3", "Iran war"]]
MENU = [  # priced data purchases Argon may choose during recursion (expected info gain per dollar decides)
    {"id": "news_tehran", "target": "treg.web.search.news", "body": {"q": "Tehran statement retaliation", "limit": 15}, "usd": 0.0},
    {"id": "news_tankers", "target": "treg.web.search.news", "body": {"q": "tanker attack Gulf shipping insurance", "limit": 15}, "usd": 0.0},
    {"id": "news_opec", "target": "treg.web.search.news", "body": {"q": "Saudi Arabia OPEC output response", "limit": 15}, "usd": 0.0},
    {"id": "trends_conflict", "target": "treg.google.keywords.trends", "body": {"keywords": ["Iran war", "draft", "oil shortage"], "country": "us"}, "usd": 0.0012},
    {"id": "reddit_worldnews", "target": "crawl4ai.reddit.search.posts", "body": {"q": "Iran Hormuz"}, "usd": 0.0009},
]
NODES = [  # the domino chain; lat/lon for the globe
    ("pizza", "Pentagon pizza traffic", "observed", 38.8602, -77.0560, 0),
    ("attention", "Public attention (Wikipedia)", "attention", None, None, 0),
    ("trends", "Search interest (Google Trends)", "attention", None, None, 0),
    ("news", "News flow", "news", None, None, 0),
    ("pentagon", "Pentagon late-night activity", "latent", 38.8719, -77.0563, 1),
    ("escalation", "US/Israel–Iran escalation", "latent", 35.6892, 51.3890, 1),
    ("hormuz", "Strait of Hormuz shipping risk", "latent", 26.5667, 56.2500, 1),
    ("brent", "Brent crude", "market", 51.5074, -0.0800, 2), ("wti", "WTI crude", "market", 40.7128, -74.0060, 2),
    ("natgas", "Natural gas", "market", 29.7604, -95.3698, 2), ("gasoline", "RBOB gasoline", "market", 40.71, -74.01, 2),
    ("airlines", "Airlines (JETS)", "market", 40.6413, -73.7781, 2), ("energy", "Energy stocks (XLE)", "market", 29.76, -95.37, 2),
    ("defense", "Defense (ITA)", "market", 38.9, -77.04, 2), ("sp500", "S&P 500", "market", 40.7069, -74.0113, 2),
    ("gold", "Gold", "market", 51.5133, -0.0886, 2),
]
EDGES = [("pizza", "pentagon", 1, 0), ("pentagon", "escalation", 1, 0), ("news", "escalation", 1, 0), ("attention", "escalation", 1, 0),
         ("trends", "escalation", 1, 0), ("escalation", "hormuz", 1, 0), ("hormuz", "brent", 1, 1), ("hormuz", "wti", 1, 1),
         ("brent", "gasoline", 1, 1), ("brent", "airlines", -1, 1), ("brent", "energy", 1, 1), ("escalation", "defense", 1, 1),
         ("escalation", "gold", 1, 1), ("brent", "sp500", -1, 1), ("hormuz", "natgas", 1, 1)]

ARGON_SCHEMA = {"type": "object", "properties": {
    "nodes": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "prob": {"type": "number"},
                                                                          "state": {"type": "string"}, "narration": {"type": "string"}},
                                         "required": ["id", "prob", "state", "narration"]}},
    "events": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "label": {"type": "string"},
                                                                           "prob": {"type": "number"}, "rationale": {"type": "string"}},
                                          "required": ["id", "label", "prob", "rationale"]}},
    "targets": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "p_tense_tomorrow": {"type": "number"},
                                                                            "direction": {"type": "string"}, "narration": {"type": "string"}},
                                           "required": ["id", "p_tense_tomorrow", "direction", "narration"]}},
    "next_purchase": {"type": "object", "properties": {"menu_id": {"type": "string"}, "expected_info_gain": {"type": "number"},
                                                       "why": {"type": "string"}}, "required": ["menu_id", "expected_info_gain", "why"]},
    "headline_summary": {"type": "string"}},
    "required": ["nodes", "events", "targets", "next_purchase", "headline_summary"]}


def _rows(v):
    o = (v or {}).get("output", v) or {}
    return o.get("results") or o.get("articles") or [] if isinstance(o, dict) else (o if isinstance(o, list) else [])


def _headlines(results):
    seen, out = set(), []
    for q, v in results:
        for r in _rows(v):
            t = (r.get("title") or "").strip()
            if t and t.lower() not in seen:
                seen.add(t.lower())
                out.append({"q": q, "title": t, "when": r.get("date") or r.get("published") or "", "source": r.get("source") if isinstance(r.get("source"), str) else ""})
    return out


def next_trading_day(d):
    d = pd.Timestamp(d) + pd.Timedelta(days=1)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    return d.strftime("%Y-%m-%d")


class LivePipeline:
    def __init__(self, emit, data_mode="live", argon_mode="live"):
        self.emit = emit
        self.data_mode = data_mode
        self.argon = Argon(mode=argon_mode, emit=lambda ev: emit({**ev, "t": round(time.time() - self.t0, 2)}))
        self.t0 = time.time()

    def log(self, text, level="info"):
        self.emit({"type": "log", "level": level, "text": text, "t": round(time.time() - self.t0, 2)})

    def buy(self, target, body=None, params=None, usd=0.0):
        v, m = tc.call(target, body=body, params=params, price_usd=usd, mode=self.data_mode)
        self.emit({"type": "data_call", "target": target, "usd": usd if not m.get("cached") else 0.0, "seconds": m.get("seconds", 0),
                   "cached": bool(m.get("cached")), "error": m.get("error"), "t": round(time.time() - self.t0, 2)})
        return v

    # ------------------------------------------------------------------------------------------ step 1
    def pull(self):
        self.log("Pulling live signals: treg news + Google Trends, Wikipedia attention, market closes.")
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            news_f = {q: ex.submit(self.buy, "treg.web.search.news", {"q": q, "limit": 15}) for q in NEWS_QUERIES}
            trend_f = [ex.submit(self.buy, "treg.google.keywords.trends", {"keywords": k, "country": "us"}, None, 0.0012) for k in TREND_SETS]
            mk_f = ex.submit(H.markets, refresh=True)
            pv_f = ex.submit(H.attention, refresh=True)
            news = [(q, f.result()) for q, f in news_f.items()]
            trends = [f.result() for f in trend_f]
            mk, pv = mk_f.result(), pv_f.result()
        self.signals = {"headlines": _headlines(news), "trends": trends, "markets": mk, "pageviews": pv}
        self.log(f"{len(self.signals['headlines'])} unique headlines; markets through {mk.index[-1].date()}; attention through {pv.index[-1].date()}.")

    # ------------------------------------------------------------------------------------------ step 2
    def stats_forecast(self):
        mk, pv = self.signals["markets"], self.signals["pageviews"]
        z, A = H.attention_index(pv)
        self.attention_z = float(A.dropna().iloc[-1])
        out = {}
        for tid in TARGETS:
            if tid not in mk.columns:
                continue
            df = M.assemble(mk, A.shift(1), tid)
            hmm, prm, w, sig = M.predictive(df, len(df))
            _, ahead = M.hmm_filter(df["attention"].values, hmm)
            w_next, s_next = float(ahead[-1]), float(M.ewma_sigma(df["r"].values)[-1])
            q = lambda p, ww=w_next: M.mix_quantile(p, ww, s_next, prm)
            out[tid] = {"w": w_next, "sigma": s_next, "prm": prm, "median": q(0.5), "p10": q(0.1), "p90": q(0.9),
                        "p_up": 1 - M.mix_cdf(0.0, w_next, s_next, prm),
                        "p_big": 1 - (M.mix_cdf(M.BIG, w_next, s_next, prm) - M.mix_cdf(-M.BIG, w_next, s_next, prm)),
                        "baseline": {"median": 0.0, "p10": float(-1.2816 * s_next), "p90": float(1.2816 * s_next)},
                        "last_close": float(mk[tid].dropna().iloc[-1]), "last_date": str(mk[tid].dropna().index[-1].date())}
        self.stats = out
        self.log(f"Statistical forecasts ready for {len(out)} targets (attention z {self.attention_z:+.2f}; HMM tension {out['brent']['w']:.2f}).")

    # ------------------------------------------------------------------------------------------ step 3 and 4
    def argon_reason(self, extra=None, depth=0):
        heads = self.signals["headlines"][:60]
        stats = {k: {kk: round(v[kk], 3) for kk in ("w", "median", "p10", "p90", "p_big")} for k, v in self.stats.items()}
        menu = [{"menu_id": m["id"], "what": m["target"], "query": m["body"], "usd": m["usd"]} for m in MENU if m["id"] not in self.bought]
        prompt = (
            "You are the reasoning core of Domino, a next-day predictive world model. Today is "
            f"{time.strftime('%A %Y-%m-%d %H:%M %Z')}. Markets last closed {self.stats['brent']['last_date']} "
            f"(Brent {self.stats['brent']['last_close']:.2f}). Tomorrow's session is {next_trading_day(self.stats['brent']['last_date'])}.\n\n"
            f"HEADLINES (live, via treg news):\n" + "\n".join(f"- [{h['when']}] {h['title']}" for h in heads) +
            f"\n\nATTENTION: Wikipedia crisis-attention index z = {self.attention_z:+.2f} (0 = normal).\n"
            f"GOOGLE TRENDS (weekly, latest points): {json.dumps([(t or {}).get('output', t) for t in self.signals['trends']])[:1500]}\n"
            f"PIZZA SIGNAL: Google exposes no live busyness for Pentagon-area pizza shops today (null); treat as missing.\n"
            f"STATISTICAL MODEL (backtested; w = P(tense regime tomorrow), returns in %):\n{json.dumps(stats)}\n"
            + (f"\nNEW DATA YOU REQUESTED:\n{json.dumps(extra)[:6000]}\n" if extra else "") +
            "\nTasks: (1) probability and state for each latent node (pentagon, escalation, hormuz) and observed node (news, "
            "attention, trends, pizza) with one-line narration; (2) calibrated probabilities for these events in the next "
            "24 h: escalation24h = 'US or Israeli strike on Iran, or Iranian strike on US/Israeli/Gulf assets', "
            "hormuz24h = 'confirmed new attack on commercial shipping in or near the Strait of Hormuz', "
            "brent_big = '|Brent next-session return| > 2.5%'; anchor on base rates and say why; (3) for each target id in "
            f"{list(self.stats)} your P(tense regime tomorrow) and direction (up/down/flat) with one-line narration; "
            f"(4) choose ONE next data purchase from this menu by expected information gain per dollar (0-1 gain): {json.dumps(menu)}.")
        v, meta = self.argon.call(f"forecast reasoning (depth {depth})", prompt, level="high", schema=ARGON_SCHEMA, timeout=240)
        return v

    def attention_items(self, articles=("Strait_of_Hormuz", "Iran", "Israel", "Brent_Crude", "Houthis")):
        """Next-day social attention (Wikipedia views): AR(1) on log views over the last year, empirical residual
        quantiles for the band, persistence as the baseline. Validated out of sample in analysis/category_analysis.md."""
        pv = self.signals["pageviews"]
        out = []
        for a in articles:
            if a not in pv.columns:
                continue
            s = np.log1p(pv[a].dropna().iloc[-365:])
            x, y = s.values[:-1], s.values[1:]
            X = np.vstack([np.ones_like(x), x]).T
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            resid = y - X @ beta
            pred = beta[0] + beta[1] * s.values[-1]
            q = {p: float(np.expm1(pred + np.quantile(resid, p))) for p in (0.1, 0.5, 0.9)}
            last = float(np.expm1(s.values[-1]))
            out.append({"id": f"attn_{a}", "label": f"Wikipedia views tomorrow: {a.replace('_', ' ')}", "unit": "views",
                        "median": round(q[0.5]), "p10": round(q[0.1]), "p90": round(q[0.9]), "p_up": float(np.mean(pred + resid > s.values[-1])),
                        "p_big_move": None, "baseline": {"median": round(last), "p10": None, "p90": None},
                        "argon_adjusted": None, "direction": "up" if q[0.5] > last else "down",
                        "narration": f"AR(1) on log views (beta {beta[1]:.2f}); last observed {last:,.0f} on {pv[a].dropna().index[-1].date()}.",
                        "last_close": last, "kind": "attention"})
        return out

    def pizza_live(self):
        files = sorted(glob.glob(os.path.join(ROOT, "data", "pizzint_*.json")))
        if not files:
            return False
        try:
            d = json.load(open(files[-1]))
            return any(x.get("percentage_of_usual") is not None for x in d.get("data", []))
        except Exception:
            return False

    def timesfm(self):
        path = os.path.join(ROOT, "runs", "timesfm_week_ahead.json")
        return json.load(open(path))["targets"] if os.path.exists(path) else None

    def sota_scores(self):
        path = os.path.join(ROOT, "runs", "sota_timesfm.json")
        return json.load(open(path))["results"] if os.path.exists(path) else None

    def daily_life(self):
        path = os.path.join(ROOT, "runs", "daily_life_results.json")
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return json.load(f)["targets"]

    def belief_entropy(self, v):
        ps = [min(max(e["prob"], 1e-4), 1 - 1e-4) for e in (v or {}).get("events", [])]
        return float(sum(-(p * math.log(p) + (1 - p) * math.log(1 - p)) for p in ps))

    def recurse(self, max_depth=3, delta=0.05):
        self.bought = set()
        v = self.argon_reason()
        F = self.belief_entropy(v)
        rule = core.StopRule(delta=delta, patience=1, r_max=max_depth)
        extra = []
        for depth in range(1, max_depth + 1):
            pick = (v or {}).get("next_purchase", {})
            item = next((m for m in MENU if m["id"] == pick.get("menu_id") and m["id"] not in self.bought), None)
            if item is None:
                break
            self.bought.add(item["id"])
            got = self.buy(item["target"], item["body"], None, item["usd"])
            extra.append({"menu_id": item["id"], "titles": [r.get("title") for r in _rows(got)][:15] or (got or {}).get("output")})
            self._extra = extra
            v2 = self.argon_reason(extra=extra, depth=depth)
            F2 = self.belief_entropy(v2)
            stop, why, d = rule.step(F, F2)
            self.emit({"type": "recursion", "depth": depth, "thinking_level": "high", "question": pick.get("why", "")[:200],
                       "F_before": round(F, 4), "F_after": round(F2, 4), "dF_rel": round(d, 4), "stop": stop,
                       "note": f"bought {item['id']} (${item['usd']}); {why}", "t": round(time.time() - self.t0, 2)})
            if v2:
                v, F = v2, F2
            if stop:
                break
        self.argon_view = v or {}

    # ------------------------------------------------------------------------------------------ step 5
    def assemble_payloads(self, category_results=None):
        av = self.argon_view
        node_view = {n["id"]: n for n in av.get("nodes", [])}
        tgt_view = {t["id"]: t for t in av.get("targets", [])}
        nodes = []
        for nid, label, kind, lat, lon, level in NODES:
            nv = node_view.get(nid, {})
            prob = nv.get("prob")
            if nid == "pizza" and not self.pizza_live():  # no busyness data today: never show a made-up probability
                prob, nv = None, {**nv, "state": "no live data", "narration": "Google exposes no busyness for Pentagon-area pizza shops today."}
            p_tense = None
            if nid in self.stats:  # UI contract: a market node's prob = P(big move next session)
                prob = self.stats[nid]["p_big"]
                p_tense = tgt_view.get(nid, {}).get("p_tense_tomorrow", self.stats[nid]["w"])
            nodes.append({"id": nid, "label": label, "kind": kind, "lat": lat, "lon": lon, "level": level,
                          "value": self.attention_z if nid == "attention" else (self.stats.get(nid, {}).get("last_close")),
                          "unit": "z" if nid == "attention" else ("price" if nid in self.stats else None),
                          "z": self.attention_z if nid == "attention" else None, "prob": prob, "p_tense": p_tense, "state": nv.get("state"),
                          "narration": nv.get("narration") or tgt_view.get(nid, {}).get("narration")})
        probs = {n["id"]: (n["prob"] or 0.0) for n in nodes}
        edges = []
        for s, t, sign, lag in EDGES:
            evidence = "anecdotal" if s == "pizza" else "Argon prior"
            edges.append({"source": s, "target": t, "sign": sign, "lag_days": lag, "mechanism": None, "prior": 0.5,
                          "measured": None, "evidence": evidence, "active": round(float(min(1.0, probs.get(s, 0) * 1.2)), 3)})
        dl = self.daily_life()
        if dl:
            for nid, label, lat, lon in (("pump", "Gas price at the pump (next week)", 39.83, -98.58),
                                         ("treasury", "10-year Treasury yield", 40.7069, -74.0113),
                                         ("mortgage", "30-year mortgage rate (next week)", 38.9, -77.03),
                                         ("flu", "Flu activity (next week)", 33.749, -84.388)):
                r = dl.get({"pump": "gas"}.get(nid, nid))
                nodes.append({"id": nid, "label": label, "kind": "daily_life", "lat": lat, "lon": lon, "level": 3,
                              "value": (r or {}).get("latest", {}).get("next_level_forecast"), "unit": (r or {}).get("unit"),
                              "z": None, "prob": None, "state": None, "narration": None})
            g, m = dl.get("gas", {}), dl.get("mortgage", {})
            gg = (g.get("granger") or {}).get("RBOB futures weekly change") or {}
            mg = (m.get("granger") or {}).get("10-year Treasury weekly change") or {}
            edges.append({"source": "gasoline", "target": "pump", "sign": 1, "lag_days": 7, "mechanism": "wholesale futures pass through to retail",
                          "prior": 0.8, "measured": round(-g.get("vs_no_change", {}).get("pct", 0) / 100, 3),
                          "evidence": f"granger p={gg.get('p', float('nan')):.1g} (lag {gg.get('lag')}w); MAE -{abs(g.get('vs_no_change', {}).get('pct', 0)):.0f}%",
                          "active": 0.9})
            edges.append({"source": "treasury", "target": "mortgage", "sign": 1, "lag_days": 14, "mechanism": "lenders price off the 10-year",
                          "prior": 0.8, "measured": round(-m.get("vs_no_change", {}).get("pct", 0) / 100, 3),
                          "evidence": f"granger p={mg.get('p', float('nan')):.1g} (lag {mg.get('lag')}w); MAE -{abs(m.get('vs_no_change', {}).get('pct', 0)):.0f}%",
                          "active": 0.7})
            edges.append({"source": "escalation", "target": "treasury", "sign": -1, "lag_days": 1, "mechanism": "flight to safety",
                          "prior": 0.4, "measured": None, "evidence": "Argon prior", "active": round(min(1.0, probs.get("escalation", 0) * 1.2), 3)})
        graph = {"asof": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "nodes": nodes, "edges": edges}
        target_date = next_trading_day(self.stats["brent"]["last_date"])
        items = []
        for tid, (label, _) in TARGETS.items():
            st = self.stats.get(tid)
            if not st:
                continue
            tv = tgt_view.get(tid, {})
            w_a = tv.get("p_tense_tomorrow")
            adj = None
            if w_a is not None:
                q = lambda p: M.mix_quantile(p, float(w_a), st["sigma"], st["prm"])
                adj = {"median": q(0.5), "p10": q(0.1), "p90": q(0.9), "w": float(w_a)}
            items.append({"id": tid, "label": label, "unit": "% return", "median": round(st["median"], 3), "p10": round(st["p10"], 3),
                          "p90": round(st["p90"], 3), "p_up": round(st["p_up"], 3), "p_big_move": round(st["p_big"], 3),
                          "baseline": {k: round(v, 3) for k, v in st["baseline"].items()},
                          "argon_adjusted": {k: round(v, 3) for k, v in adj.items()} if adj else None,
                          "direction": tv.get("direction"), "narration": tv.get("narration"), "last_close": st["last_close"]})
        items += self.attention_items()
        tfm = self.timesfm()
        sota = self.sota_scores()
        for key, label in (("gas", "Your gas price next week"), ("mortgage", "30-year mortgage rate next week"), ("flu", "Flu activity next week")):
            r = (dl or {}).get(key)
            t = (tfm or {}).get(key)
            if t:  # backtest-selected model: TimesFM 3.0 beats or ties our regression on these weekly series
                sc = (sota or {}).get(key, {})
                items.append({"id": f"life_{key}", "label": label, "unit": t["unit"], "median": round(t["median"], 3),
                              "p10": round(t["quantiles"][0], 3), "p90": round(t["quantiles"][-1], 3), "p_up": None, "p_big_move": None,
                              "baseline": {"median": round(t["last"], 3), "p10": None, "p90": None}, "argon_adjusted": None,
                              "direction": "up" if t["median"] > t["last"] else "down", "kind": "daily_life", "model": "TimesFM 3.0 (Google)",
                              "narration": (f"Google TimesFM 3.0, zero-shot{', with ' + t['covariate'] if t.get('covariate') else ''}. "
                                            f"Backtest over {sc.get('n', '?')} weeks: error {sc.get('timesfm_vs_no_change', {}).get('pct', float('nan')):+.0f}% "
                                            f"vs no-change; direction right {sc.get('timesfm_direction_hit', float('nan')):.0%}."),
                              "last_close": t["last"]})
                continue
            if not r or r["latest"]["next_level_forecast"] is None:
                continue
            lvl, nxt = r["latest"]["level"], r["latest"]["next_level_forecast"]
            if key == "flu":
                lvl, nxt = math.exp(lvl), math.exp(nxt)
            mae = r["mae_model"] * (math.exp(r["latest"]["level"]) if key == "flu" else 1.0)
            items.append({"id": f"life_{key}", "label": label, "unit": {"gas": "$/gal", "mortgage": "%", "flu": "% of visits (ILI)"}[key],
                          "median": round(nxt, 3), "p10": round(nxt - 1.28 * mae * 1.25, 3), "p90": round(nxt + 1.28 * mae * 1.25, 3),
                          "p_up": None, "p_big_move": None, "baseline": {"median": round(lvl, 3), "p10": None, "p90": None},
                          "argon_adjusted": None, "direction": "up" if nxt > lvl else "down", "kind": "daily_life",
                          "narration": f"Backtested over {r['n']} weeks: error {r['vs_no_change']['pct']:+.0f}% vs no-change "
                                       f"(DM p={r['vs_no_change']['dm']['p']:.1g}); direction right {r['direction_hit']:.0%}.",
                          "last_close": lvl})
        events = [{"id": e["id"], "label": e["label"], "prob": round(float(e["prob"]), 3), "source": "argon", "narration": e["rationale"],
                   "spread": round(float(e.get("spread", 0.0)), 3), "n_samples": e.get("n", 1)}
                  for e in av.get("events", [])]
        events.append({"id": "brent_big_stats", "label": "|Brent next-session return| > 2.5% (statistical model)",
                       "prob": round(self.stats["brent"]["p_big"], 3), "source": "stats", "narration": "HMM tension + Student-t mixture, backtested."})
        forecast = {"asof": graph["asof"], "target_date": target_date, "items": items, "events": events,
                    "headline_summary": av.get("headline_summary")}
        body = json.dumps(forecast, sort_keys=True, default=float)
        forecast["hash"] = hashlib.sha256(body.encode()).hexdigest()
        os.makedirs(os.path.join(ROOT, "runs"), exist_ok=True)
        with open(os.path.join(ROOT, "runs", f"forecast_{target_date}_{time.strftime('%H%M%S')}.json"), "w") as f:
            json.dump(forecast, f, indent=2, default=float)
        return graph, forecast

    def ensemble(self, n=5):
        """Self-consistency: n independent Argon forecasts (high, priority) on the final evidence. Event probabilities
        are pooled in log-odds space; the spread is reported as Argon's epistemic disagreement."""
        extra = getattr(self, "_extra", None)
        with cf.ThreadPoolExecutor(max_workers=n) as ex:
            views = [v for v in ex.map(lambda i: self.argon_reason(extra=extra, depth=f"ensemble {i + 1}/{n}"), range(n)) if v]
        if not views:
            return
        logit = lambda p: math.log(max(min(p, 1 - 1e-4), 1e-4) / (1 - max(min(p, 1 - 1e-4), 1e-4)))
        pooled = dict(self.argon_view)
        ev_ids = {e["id"] for v in views for e in v.get("events", [])}
        pooled_events = []
        for eid in ev_ids:
            ps = [e["prob"] for v in views for e in v.get("events", []) if e["id"] == eid]
            base = next(e for v in views for e in v.get("events", []) if e["id"] == eid)
            m = sum(logit(p) for p in ps) / len(ps)
            pooled_events.append({**base, "prob": 1 / (1 + math.exp(-m)), "spread": float(np.std(ps)), "n": len(ps)})
        pooled["events"] = pooled_events
        tg = {}
        for v in views:
            for t in v.get("targets", []):
                tg.setdefault(t["id"], []).append(t)
        pooled["targets"] = [{**ts[0], "p_tense_tomorrow": float(np.mean([t["p_tense_tomorrow"] for t in ts])),
                              "spread": float(np.std([t["p_tense_tomorrow"] for t in ts]))} for ts in tg.values()]
        self.argon_view = pooled
        self.log(f"Argon ensemble of {len(views)} pooled; event spreads " +
                 ", ".join(f"{e['id']} ±{e['spread']:.2f}" for e in pooled_events))

    def run(self, ensemble_n=5):
        self.t0 = time.time()
        self.pull()
        self.stats_forecast()
        self.recurse()
        if ensemble_n:
            self.ensemble(ensemble_n)
        graph, forecast = self.assemble_payloads()
        for name, obj in (("graph_latest.json", graph), ("forecast_latest.json", forecast)):
            with open(os.path.join(ROOT, "runs", name), "w") as f:
                json.dump(obj, f, indent=2, default=float)
        self.emit({"type": "graph_update", "graph": graph, "t": round(time.time() - self.t0, 2)})
        self.emit({"type": "forecast_update", "forecast": forecast, "t": round(time.time() - self.t0, 2)})
        self.log(f"Forecast for {forecast['target_date']} pre-registered: {forecast['hash'][:16]}…")
        return graph, forecast


if __name__ == "__main__":
    os.environ.setdefault("RPWM_APP", "domino-live")
    def pr(ev):
        t = ev["type"]
        if t in ("log", "recursion", "data_call", "argon_call"):
            print(t, json.dumps({k: v for k, v in ev.items() if k not in ("type",)}, default=str)[:220])
    g, f = LivePipeline(pr).run()
    for it in f["items"]:
        print(f'{it["label"]:<22} median {it["median"]:+.2f}  [{it["p10"]:+.2f}, {it["p90"]:+.2f}]  P(big) {it["p_big_move"]:.2f}  '
              f'argon w={(it["argon_adjusted"] or {}).get("w")}  {it["direction"]}: {(it["narration"] or "")[:80]}')
    for e in f["events"]:
        print(f'EVENT {e["label"][:70]:<70} p={e["prob"]:.2f} [{e["source"]}]')
    print("hash", f["hash"])
