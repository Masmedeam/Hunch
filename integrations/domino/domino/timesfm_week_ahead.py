"""TimesFM 3.0 week-ahead forecasts for the live payload (gas, mortgage, flu, plus next-day markets).

Run with the TimesFM venv:  <venv>/bin/python -m domino.timesfm_week_ahead --weights <timesfm-3.0 dir>
Writes runs/timesfm_week_ahead.json, which domino/live.py prefers over the OLS forecasts when present.
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd

from .daily_life import asof_before, fluview, fred, long_prices
from .sota_timesfm import load_fc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = [round(x, 1) for x in np.linspace(0.1, 0.9, 9)]


def forecast_next(fc, series, cov=None, ctx=512):
    y = np.asarray(series[-ctx:], np.float32)
    kw = {"horizon": 1, "return_quantiles": True}
    if cov is not None:
        kw["past_future_covariates"] = [np.asarray(cov[-(ctx + 1):], np.float32)[None, :]]
    o = list(fc.predict_batch([y], **kw))[0]
    return float(o.forecast[0]), [float(v) for v in o.quantiles[0]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()
    fc = load_fc(a.weights, a.device)
    px = long_prices([])
    out = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "model": "google/timesfm-3.0-pytorch", "targets": {}}

    g = fred("GASREGW")
    nxt = g.index[-1] + pd.Timedelta(days=7)
    dates = list(g.index) + [nxt]
    rb = np.log(asof_before(px["RB=F"], pd.DatetimeIndex(dates), 0))
    med, q = forecast_next(fc, g.values, rb)
    out["targets"]["gas"] = {"last_date": str(g.index[-1].date()), "target_date": str(nxt.date()), "last": float(g.iloc[-1]),
                             "median": med, "quantiles": q, "unit": "$/gal", "covariate": "RBOB futures (log), known through the target date"}

    m = fred("MORTGAGE30US")
    nxt = m.index[-1] + pd.Timedelta(days=7)
    dates = list(m.index) + [nxt]
    tnx = asof_before(px["^TNX"], pd.DatetimeIndex(dates), 0)
    med, q = forecast_next(fc, m.values, tnx)
    out["targets"]["mortgage"] = {"last_date": str(m.index[-1].date()), "target_date": str(nxt.date()), "last": float(m.iloc[-1]),
                                  "median": med, "quantiles": q, "unit": "%", "covariate": "10-year Treasury yield"}

    f = fluview()
    med, q = forecast_next(fc, np.log(f.values))
    out["targets"]["flu"] = {"last_date": str(f.index[-1].date()), "target_date": str((f.index[-1] + pd.Timedelta(days=7)).date()),
                             "last": float(f.iloc[-1]), "median": float(np.exp(med)), "quantiles": [float(np.exp(v)) for v in q], "unit": "% ILI"}

    mk = pd.read_csv(os.path.join(ROOT, "data", "markets.csv"), index_col=0, parse_dates=True)
    for col in ("brent", "wti", "natgas", "gasoline", "sp500", "gold"):
        s = mk[col].dropna()
        lp = np.log(s.values)
        med, q = forecast_next(fc, lp)
        out["targets"][col] = {"last_date": str(s.index[-1].date()), "last": float(s.iloc[-1]), "unit": "% return",
                               "median": 100 * (med - lp[-1]), "quantiles": [100 * (v - lp[-1]) for v in q]}
    json.dump(out, open(os.path.join(ROOT, "runs", "timesfm_week_ahead.json"), "w"), indent=2)
    for k, v in out["targets"].items():
        print(f"{k:<9} median {v['median']:.4f}  P10 {v['quantiles'][0]:.4f}  P90 {v['quantiles'][-1]:.4f}  (last {v['last']:.3f})")


if __name__ == "__main__":
    main()
