"""Daily-life predictions: what can the Domino world model forecast that matters to people's lives?

Targets (all free data, forecast one step ahead, rolling origin, expanding-window OLS, no look-ahead):
  gas       US regular gasoline, $/gal, weekly (FRED GASREGW, Mondays)      drivers: RBOB futures (RB=F), Brent (BZ=F)
  mortgage  30-year fixed mortgage rate, %, weekly (FRED MORTGAGE30US)      drivers: 10-year Treasury yield (^TNX)
  flu       CDC weighted influenza-like illness, %, weekly (Delphi FluView) drivers: Wikipedia 'Influenza' attention
  claims    US initial jobless claims, weekly (FRED ICSA)                    drivers: Wikipedia 'Unemployment', 'Layoff' attention
  eggs      US average egg price, $/dozen, monthly (FRED APU0000708111)      drivers: Wikipedia 'Avian_influenza' attention
Each: model vs no-change baseline (and vs autoregression-only, to isolate the first domino's added value); MAE with
block-bootstrap 95% CI, Diebold-Mariano p, direction hit rate; Granger tests driver -> target change.
Run: .venv/bin/python -m domino.daily_life   -> runs/daily_life_results.json
"""
import json
import os
import time
import warnings

import numpy as np
import pandas as pd

from . import model as M
from .categories import granger_min_p, wiki

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def fred(series):
    df = pd.read_csv(os.path.join(DATA, f"fred_{series}.csv"))
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    s = pd.to_numeric(df["value"], errors="coerce")
    return pd.Series(s.values, index=df["date"], name=series).dropna()


def fluview():
    d = json.load(open(os.path.join(DATA, "delphi_fluview.json")))["epidata"]

    def mmwr_week_end(epiweek):  # MMWR week 1 ends on the first Saturday on or after January 4 (Sun-Sat weeks)
        year, week = int(str(epiweek)[:4]), int(str(epiweek)[4:])
        jan4 = pd.Timestamp(year=year, month=1, day=4)
        first_sat = jan4 + pd.Timedelta(days=(5 - jan4.weekday()) % 7)
        return first_sat + pd.Timedelta(weeks=week - 1)

    idx = [mmwr_week_end(r["epiweek"]) for r in d]
    return pd.Series([r["wili"] for r in d], index=idx, name="wili").sort_index()


def long_prices(tickers, start="2012-01-01"):
    path = os.path.join(DATA, "markets_long.csv")
    have = pd.read_csv(path, index_col=0, parse_dates=True) if os.path.exists(path) else pd.DataFrame()
    need = [t for t in tickers if t not in have.columns]
    if need:
        import yfinance as yf
        for tk in need:
            for _ in range(3):
                try:
                    s = yf.download(tk, start=start, progress=False, auto_adjust=True)["Close"]
                    s = s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s
                    if len(s):
                        s.index = pd.to_datetime(s.index).tz_localize(None)
                        have = have.join(s.rename(tk), how="outer") if len(have) else s.rename(tk).to_frame()
                        break
                except Exception:
                    time.sleep(1.5)
        have.sort_index().to_csv(path)
    return have


def asof_before(series, dates, days=0):
    """Value of a daily series strictly before each date (minus `days`)."""
    s = series.dropna().sort_index()
    out = []
    for d in dates:
        sub = s[s.index < d - pd.Timedelta(days=days)]
        out.append(sub.iloc[-1] if len(sub) else np.nan)
    return np.array(out, float)


def weekly_attention(article, dates, window_days=7):
    s = wiki(article)
    if s is None:
        return None
    s = np.log1p(s.astype(float))
    vals = []
    for d in dates:
        sub = s[(s.index < d) & (s.index >= d - pd.Timedelta(days=window_days))]
        vals.append(sub.mean() if len(sub) else np.nan)
    return np.array(vals)


def rolling_ols(y, X, start):
    """One-step-ahead predictions for y[t] using rows < t (expanding window). X rows aligned with y."""
    preds = np.full(len(y), np.nan)
    for t in range(start, len(y)):
        Xt, yt = X[:t], y[:t]
        ok = np.isfinite(yt) & np.all(np.isfinite(Xt), axis=1)
        if ok.sum() < 30 or not np.all(np.isfinite(X[t])):
            continue
        beta = np.linalg.lstsq(Xt[ok], yt[ok], rcond=None)[0]
        preds[t] = X[t] @ beta
    return preds


def evaluate(name, label, unit, dates, level, X_full, X_ar, start, granger_drivers):
    """Target = next-period change of `level`. Models: full (drivers + AR), AR-only, and no-change."""
    dlev = np.diff(level, prepend=np.nan)  # change into period t
    y = dlev
    p_full = rolling_ols(y, X_full, start)
    p_ar = rolling_ols(y, X_ar, start)
    ok = np.isfinite(p_full) & np.isfinite(p_ar) & np.isfinite(y)
    e_full, e_ar, e_rw = np.abs(y[ok] - p_full[ok]), np.abs(y[ok] - p_ar[ok]), np.abs(y[ok])
    res = {"label": label, "unit": unit, "n": int(ok.sum()), "window": f"{dates[ok][0].date()}..{dates[ok][-1].date()}",
           "mae_model": float(e_full.mean()), "mae_ar": float(e_ar.mean()), "mae_no_change": float(e_rw.mean()),
           "vs_no_change": {"diff": M.block_bootstrap_mean(e_full - e_rw, block=4), "dm": M.dm_test(e_full, e_rw, lag=4),
                            "pct": float(100 * (e_full.mean() / e_rw.mean() - 1))},
           "vs_ar": {"diff": M.block_bootstrap_mean(e_full - e_ar, block=4), "dm": M.dm_test(e_full, e_ar, lag=4),
                     "pct": float(100 * (e_full.mean() / e_ar.mean() - 1))},
           "direction_hit": float(np.mean(np.sign(p_full[ok]) == np.sign(y[ok]))), "granger": {},
           "series": {"dates": [str(x.date()) for x in dates[ok]], "level_prev": [float(v) for v in level[np.where(ok)[0] - 1]],
                      "actual_change": [float(v) for v in y[ok]], "pred_model": [float(v) for v in p_full[ok]],
                      "pred_ar": [float(v) for v in p_ar[ok]], "test_index": [int(i) for i in np.where(ok)[0]]}}
    for dname, dvals in granger_drivers.items():
        g = granger_min_p(pd.Series(dvals), pd.Series(y))
        res["granger"][dname] = g
    beta = np.linalg.lstsq(X_full[np.isfinite(y) & np.all(np.isfinite(X_full), axis=1)],
                           y[np.isfinite(y) & np.all(np.isfinite(X_full), axis=1)], rcond=None)[0]
    last = X_full[-1]
    nxt = float(last @ beta) if np.all(np.isfinite(last)) else None
    res["latest"] = {"date": str(dates[-1].date()), "level": float(level[-1]), "next_change_forecast": nxt,
                     "next_level_forecast": (float(level[-1] + nxt) if nxt is not None else None)}
    return res


def run():
    out = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "targets": {}}
    px = long_prices(["RB=F", "BZ=F", "^TNX"])
    ones = lambda n: np.ones(n)

    # 1. Gasoline at the pump: futures lead the pump by about 1-2 weeks ("rockets and feathers")
    g = fred("GASREGW")
    g = g[g.index >= "2013-01-01"]
    d = g.index
    rb = np.log(asof_before(px["RB=F"], d, 0))
    rb1, rb2 = rb - np.log(asof_before(px["RB=F"], d, 7)), np.log(asof_before(px["RB=F"], d, 7)) - np.log(asof_before(px["RB=F"], d, 14))
    gap = np.log(g.values) - rb  # pump vs futures spread (error-correction term)
    lev = g.values
    dl = np.diff(lev, prepend=np.nan)
    X_ar = np.column_stack([ones(len(d)), np.roll(dl, 1)])
    X_full = np.column_stack([X_ar, np.roll(rb1, 0), np.roll(rb2, 0), np.roll(gap, 1)])
    X_ar[0], X_full[0] = np.nan, np.nan
    # rb1 is the futures change over the week before date t (known before the Monday survey); gap uses t-1
    out["targets"]["gas"] = evaluate("gas", "US regular gasoline at the pump", "$/gal", d, lev, X_full, X_ar, 156,
                                     {"RBOB futures weekly change": rb1})

    # 2. Mortgage rates follow the 10-year Treasury
    m = fred("MORTGAGE30US")
    m = m[m.index >= "2013-01-01"]
    d = m.index
    tnx = asof_before(px["^TNX"], d, 0)
    t1 = tnx - asof_before(px["^TNX"], d, 7)
    lev = m.values
    dl = np.diff(lev, prepend=np.nan)
    spread = lev - tnx
    X_ar = np.column_stack([ones(len(d)), np.roll(dl, 1)])
    X_full = np.column_stack([X_ar, t1, np.roll(spread, 1)])
    X_ar[0], X_full[0] = np.nan, np.nan
    out["targets"]["mortgage"] = evaluate("mortgage", "30-year fixed mortgage rate", "%", d, lev, X_full, X_ar, 156,
                                          {"10-year Treasury weekly change": t1})

    # 3. Flu activity: public attention vs the CDC's own lagging report
    f = fluview()
    f = f[f.index >= "2023-01-01"]
    d = f.index
    lev = np.log(f.values)
    att = weekly_attention("Influenza", d)
    datt = att - weekly_attention("Influenza", d - pd.Timedelta(days=7))
    dl = np.diff(lev, prepend=np.nan)
    X_ar = np.column_stack([ones(len(d)), np.roll(dl, 1), np.roll(dl, 2)])
    X_full = np.column_stack([X_ar, datt])
    X_ar[:2], X_full[:2] = np.nan, np.nan
    out["targets"]["flu"] = evaluate("flu", "Flu activity (CDC weighted ILI, log)", "log %", d, lev, X_full, X_ar, 52,
                                     {"Wikipedia 'Influenza' weekly attention change": datt})

    # 4. Initial jobless claims
    c = fred("ICSA")
    c = c[c.index >= "2016-01-01"]
    d = c.index
    lev = np.log(c.values)
    a1 = weekly_attention("Unemployment", d)
    a2 = weekly_attention("Layoff", d)
    da1 = a1 - weekly_attention("Unemployment", d - pd.Timedelta(days=7))
    da2 = a2 - weekly_attention("Layoff", d - pd.Timedelta(days=7)) if a2 is not None else np.zeros(len(d))
    dl = np.diff(lev, prepend=np.nan)
    X_ar = np.column_stack([ones(len(d)), np.roll(dl, 1), np.roll(dl, 2)])
    X_full = np.column_stack([X_ar, da1, da2])
    X_ar[:2], X_full[:2] = np.nan, np.nan
    keep = d >= "2021-01-01"  # exclude the 2020 pandemic shock from evaluation (fit still sees history)
    res = evaluate("claims", "US initial jobless claims (log)", "log", d, lev, X_full, X_ar, int(np.argmax(keep)) or 260,
                   {"Wikipedia 'Unemployment' attention change": da1, "Wikipedia 'Layoff' attention change": da2})
    out["targets"]["claims"] = res

    # 5. Eggs: avian-flu attention vs the monthly egg price
    e = fred("APU0000708111")
    e = e[e.index >= "2016-01-01"]
    d = e.index
    lev = np.log(e.values)
    s = wiki("Avian_influenza")
    s = np.log1p(s.astype(float))
    att = np.array([s[(s.index < dd) & (s.index >= dd - pd.Timedelta(days=31))].mean() for dd in d])
    datt = att - np.array([s[(s.index < dd - pd.Timedelta(days=31)) & (s.index >= dd - pd.Timedelta(days=62))].mean() for dd in d])
    dl = np.diff(lev, prepend=np.nan)
    X_ar = np.column_stack([ones(len(d)), np.roll(dl, 1)])
    X_full = np.column_stack([X_ar, datt, np.roll(datt, 1)])
    X_ar[:2], X_full[:2] = np.nan, np.nan
    out["targets"]["eggs"] = evaluate("eggs", "US egg price (log, monthly)", "log", d, lev, X_full, X_ar, 48,
                                      {"Wikipedia 'Avian influenza' monthly attention change": datt})
    path = os.path.join(ROOT, "runs", "daily_life_results.json")
    json.dump(out, open(path, "w"), indent=2, default=float)
    for k, r in out["targets"].items():
        v, a = r["vs_no_change"], r["vs_ar"]
        g = "; ".join(f"{n}: p={x['p']:.2g} lag {x['lag']}" for n, x in r["granger"].items() if x)
        print(f"{k:<9} n={r['n']} MAE model {r['mae_model']:.4f} vs no-change {r['mae_no_change']:.4f} ({v['pct']:+.1f}%, "
              f"CI [{v['diff']['lo']:+.4f},{v['diff']['hi']:+.4f}], DM p={v['dm']['p']:.2g}) | vs AR {a['pct']:+.1f}% (DM p={a['dm']['p']:.2g}) | "
              f"dir {r['direction_hit']:.2f} | Granger {g} | next {r['latest']['next_level_forecast']}")
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    run()
