"""Is Argon a good next-day forecaster? A leak-free mini-evaluation on trading days after Argon's release (2026-09-30).

For each trading day d: headlines dated the previous calendar day (treg news search with date filters; free), so every
headline predates the session that closes on d, plus Brent closes through d. (GDELT was the first choice but its
one-request-per-5-seconds limit made a 17-day pull take about an hour.) Argon (thinking high, priority tier) predicts the next
session: P(|return| > 2.5%), P(up), median and 80% interval. Scored against the statistical model (same days, from the
strict-lag backtest) and the base rate: Brier, log loss, interval coverage, pinball loss.
Run: .venv/bin/python -m domino.argon_forecast_eval
"""
import concurrent.futures as cf
import json
import math
import os
import time
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

from rpwm.argon import Argon
from . import history as H
from . import model as M

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data", "gdelt")
QUERY = "(Iran OR Israel OR Hormuz OR OPEC OR \"oil prices\")"
SCHEMA = {"type": "object", "properties": {"p_big_move": {"type": "number"}, "p_up": {"type": "number"}, "median": {"type": "number"},
                                           "p10": {"type": "number"}, "p90": {"type": "number"}, "reasoning": {"type": "string"}},
          "required": ["p_big_move", "p_up", "median", "p10", "p90", "reasoning"]}


def gdelt_headlines(day):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{day}.json")
    if os.path.exists(path):
        return json.load(open(path))
    d = day.replace("-", "")
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?query=" + urllib.parse.quote(QUERY) +
           f"&mode=artlist&maxrecords=60&format=json&sort=hybridrel&sourcelang=english&startdatetime={d}000000&enddatetime={d}180000")
    for attempt in range(4):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Domino-hackathon/0.1"}), timeout=40).read()
            data = json.loads(raw)
            arts = [{"title": a.get("title"), "domain": a.get("domain"), "seendate": a.get("seendate")} for a in data.get("articles", [])]
            json.dump(arts, open(path, "w"))
            return arts
        except Exception:
            time.sleep(6 * (attempt + 1))
    return []


def treg_headlines(day):
    from . import treg_client as tc
    os.makedirs(os.path.join(ROOT, "data", "tregnews"), exist_ok=True)
    path = os.path.join(ROOT, "data", "tregnews", f"{day}.json")
    if os.path.exists(path):
        return json.load(open(path))
    arts = []
    for page in (0, 1):
        v, m = tc.call("tinyfish.web.search.news", params={"domain_type": "news", "query": "oil prices Iran Israel Hormuz OPEC",
                                                           "after_date": day, "before_date": day, "language": "en", "page": page},
                       price_usd=0.0, mode="replay", timeout=90)
        o = (v or {}).get("output", v) or {}
        for r in (o.get("results") if isinstance(o, dict) else []) or []:
            arts.append({"title": r.get("title"), "domain": r.get("source") or r.get("url", "")[:40], "seendate": day})
    json.dump(arts, open(path, "w"))
    return arts


def main():
    os.environ.setdefault("RPWM_APP", "domino-argon-eval")
    mk, pv = H.markets(), H.attention()
    _, A = H.attention_index(pv)
    bt, _ = M.backtest(mk, A.shift(1), target="brent", n_samp=800)
    bt = bt.set_index("date")
    brent = mk["brent"].dropna()
    r = 100 * np.log(brent).diff()
    days = [d.strftime("%Y-%m-%d") for d in brent.index if pd.Timestamp("2026-09-30") <= d < brent.index[-1]]
    prev = {d: (pd.Timestamp(d) - pd.Timedelta(days=1)).strftime("%Y-%m-%d") for d in days}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        heads = dict(zip(days, ex.map(lambda d: treg_headlines(prev[d]), days)))
    argon = Argon(mode="live")

    def ask(d):
        i = brent.index.get_loc(pd.Timestamp(d))
        hist = ", ".join(f"{brent.index[j].strftime('%m-%d')} {brent.iloc[j]:.2f} ({r.iloc[j]:+.2f}%)" for j in range(max(1, i - 9), i + 1))
        h = "\n".join(f"- {a['title']} ({a['domain']})" for a in heads[d][:50]) or "- (no headlines retrieved)"
        prompt = (f"It is the evening of {d}, after the Brent close. You forecast the NEXT Brent crude session's close-to-close log "
                  f"return (%). Use only the information below; do not use any knowledge of later events.\nBrent closes (last 10 "
                  f"sessions): {hist}\nHeadlines dated {prev[d]} (the day before):\n{h}\n\nGive calibrated probabilities: P(|next return| > 2.5%), "
                  f"P(next return > 0), and the median, 10th and 90th percentiles of the next return in %.")
        v, meta = argon.call(f"forecast eval {d}", prompt, level="high", schema=SCHEMA, timeout=240)
        return d, v

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        preds = dict(ex.map(ask, days))
    rows = []
    for k, d in enumerate(days):
        nxt = brent.index[brent.index.get_loc(pd.Timestamp(d)) + 1].strftime("%Y-%m-%d")
        y = float(r.loc[nxt])
        p = preds.get(d) or {}
        s = bt.loc[nxt] if nxt in bt.index else None
        if not p or s is None:
            continue
        big = int(abs(y) > M.BIG)
        rows.append({"day": d, "target": nxt, "actual": y, "big": big, "n_headlines": len(heads[d]),
                     "argon_p_big": float(p["p_big_move"]), "stats_p_big": float(s["p_big"]),
                     "argon_p_up": float(p["p_up"]), "argon_p10": float(p["p10"]), "argon_p90": float(p["p90"]), "argon_median": float(p["median"]),
                     "stats_p10": float(s["p10"]), "stats_p90": float(s["p90"]), "stats_median": float(s["median"]),
                     "reasoning": p.get("reasoning", "")[:300]})
    df = pd.DataFrame(rows)
    br = lambda p: (df[p] - df["big"]) ** 2
    ll = lambda p: -(df["big"] * np.log(df[p].clip(1e-3, 1 - 1e-3)) + (1 - df["big"]) * np.log((1 - df[p]).clip(1e-3, 1 - 1e-3)))
    base = df["big"].mean()

    def pinball(lo, hi, med):
        q = {0.1: df[lo], 0.5: df[med], 0.9: df[hi]}
        return float(np.mean([np.mean(np.maximum(t * (df["actual"] - v), (t - 1) * (df["actual"] - v))) for t, v in q.items()]))

    res = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "n_days": int(len(df)), "window": f"{days[0]}..{days[-1]}",
           "big_move_rate": float(base),
           "brier": {"argon": M.block_bootstrap_mean(br("argon_p_big"), block=3), "stats": M.block_bootstrap_mean(br("stats_p_big"), block=3),
                     "climatology": float(np.mean((base - df["big"]) ** 2))},
           "log_loss": {"argon": float(ll("argon_p_big").mean()), "stats": float(ll("stats_p_big").mean())},
           "coverage80": {"argon": float(((df.actual >= df.argon_p10) & (df.actual <= df.argon_p90)).mean()),
                          "stats": float(((df.actual >= df.stats_p10) & (df.actual <= df.stats_p90)).mean())},
           "pinball": {"argon": pinball("argon_p10", "argon_p90", "argon_median"), "stats": pinball("stats_p10", "stats_p90", "stats_median")},
           "direction_hit_rate": float(((df.argon_p_up > 0.5) == (df.actual > 0)).mean()),
           "rows": rows}
    json.dump(res, open(os.path.join(ROOT, "runs", "argon_forecast_eval.json"), "w"), indent=2, default=float)
    print(f"days {res['n_days']} ({res['window']}), big-move rate {base:.2f}")
    print(f"Brier argon {res['brier']['argon']['mean']:.3f} [{res['brier']['argon']['lo']:.3f},{res['brier']['argon']['hi']:.3f}] | "
          f"stats {res['brier']['stats']['mean']:.3f} | climatology {res['brier']['climatology']:.3f}")
    print(f"log loss argon {res['log_loss']['argon']:.3f} stats {res['log_loss']['stats']:.3f} | coverage80 argon {res['coverage80']['argon']:.2f} "
          f"stats {res['coverage80']['stats']:.2f} | pinball argon {res['pinball']['argon']:.3f} stats {res['pinball']['stats']:.3f} | "
          f"direction hit {res['direction_hit_rate']:.2f}")


if __name__ == "__main__":
    main()
