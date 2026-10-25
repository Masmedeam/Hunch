"""Domino vs Google TimesFM 3.0 (zero-shot time-series foundation model) on the same test weeks / days.

TimesFM gets the same information as Domino's model: the target's own history (up to 512 points) and, for gas and
mortgage, the leading driver as a covariate known at forecast time (RBOB futures, 10-year Treasury). One-step-ahead.
Run with the venv that has timesfm 3.0.2 + torch (MPS):
  <research venv>/bin/python -m domino.sota_timesfm --weights <dir of google/timesfm-3.0-pytorch>
Writes runs/sota_timesfm.json. Note: TimesFM 3.0 weights are licensed non-commercial (fine for a hackathon demo).
"""
import argparse
import json
import os
import time

import numpy as np
import pandas as pd

from . import model as M
from .daily_life import asof_before, fluview, fred, long_prices

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_fc(weights, device):
    from timesfm3 import TimesFM3Forecaster
    return TimesFM3Forecaster.from_pretrained(weights, device=device, per_core_batch_size=64)


def tfm_one_step(fc, contexts, covs=None):
    kw = {"horizon": 1, "return_quantiles": True}
    if covs is not None:
        kw["past_future_covariates"] = covs
    outs = list(fc.predict_batch(contexts, **kw))
    return np.array([o.forecast[0] for o in outs]), np.array([o.quantiles[0] for o in outs])


def compare(name, level, test_idx, cov=None, fc=None, log_target=False, ctx=512, dl=None):
    contexts, covs = [], []
    for t in test_idx:
        lo = max(0, t - ctx)
        contexts.append(np.asarray(level[lo:t], np.float32))
        if cov is not None:
            covs.append(np.asarray(cov[lo:t + 1], np.float32)[None, :])  # driver known through the forecast date
    t0 = time.time()
    point, q = tfm_one_step(fc, contexts, covs if cov is not None else None)
    secs = time.time() - t0
    actual = np.array([level[t] for t in test_idx])
    prev = np.array([level[t - 1] for t in test_idx])
    s = dl["series"]
    model_lvl = np.array(s["level_prev"]) + np.array(s["pred_model"])
    e_tfm, e_dom, e_rw = np.abs(point - actual), np.abs(model_lvl - actual), np.abs(prev - actual)
    return {"target": name, "n": int(len(test_idx)), "seconds": round(secs, 2),
            "mae_timesfm": float(e_tfm.mean()), "mae_domino": float(e_dom.mean()), "mae_no_change": float(e_rw.mean()),
            "domino_vs_timesfm": {"diff": M.block_bootstrap_mean(e_dom - e_tfm, block=4), "dm": M.dm_test(e_dom, e_tfm, lag=4),
                                  "pct": float(100 * (e_dom.mean() / e_tfm.mean() - 1))},
            "timesfm_vs_no_change": {"pct": float(100 * (e_tfm.mean() / e_rw.mean() - 1)), "dm": M.dm_test(e_tfm, e_rw, lag=4)},
            "timesfm_direction_hit": float(np.mean(np.sign(point - prev) == np.sign(actual - prev))),
            "timesfm_cov80": float(np.mean((actual >= q[:, 0]) & (actual <= q[:, -1]))) if q.shape[1] >= 9 else None}


def brent_daily(fc, n_days=592, ctx=512):
    mk = pd.read_csv(os.path.join(ROOT, "data", "markets.csv"), index_col=0, parse_dates=True)
    lp = np.log(mk["brent"].dropna()).values
    idx = list(range(len(lp) - n_days, len(lp)))
    contexts = [np.asarray(lp[max(0, t - ctx):t], np.float32) for t in idx]
    point, q = tfm_one_step(fc, contexts)
    r_true = 100 * (lp[idx] - lp[np.array(idx) - 1])
    r_med = 100 * (point - lp[np.array(idx) - 1])
    qr = 100 * (q - lp[np.array(idx) - 1][:, None])  # 9 deciles 0.1..0.9
    levels = np.linspace(0.1, 0.9, 9)
    pin = np.mean([np.mean(np.maximum(a * (r_true - qr[:, i]), (a - 1) * (r_true - qr[:, i]))) for i, a in enumerate(levels)])
    cov80 = float(np.mean((r_true >= qr[:, 0]) & (r_true <= qr[:, -1])))
    return {"target": "Brent next-day return (%)", "n": len(idx), "timesfm_pinball_9q": float(pin), "timesfm_cov80": cov80,
            "timesfm_mae_median": float(np.mean(np.abs(r_med - r_true))), "dates": [str(d.date()) for d in mk["brent"].dropna().index[idx]],
            "timesfm_p10": qr[:, 0].tolist(), "timesfm_p50": r_med.tolist(), "timesfm_p90": qr[:, -1].tolist()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()
    fc = load_fc(a.weights, a.device)
    dlr = json.load(open(os.path.join(ROOT, "runs", "daily_life_results.json")))["targets"]
    px = long_prices([])
    out = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "model": "google/timesfm-3.0-pytorch (zero-shot)", "results": {}}

    g = fred("GASREGW")
    g = g[g.index >= "2013-01-01"]
    rb = np.log(asof_before(px["RB=F"], g.index, 0))
    out["results"]["gas"] = compare("gas", g.values, dlr["gas"]["series"]["test_index"], cov=rb, fc=fc, dl=dlr["gas"])

    m = fred("MORTGAGE30US")
    m = m[m.index >= "2013-01-01"]
    tnx = asof_before(px["^TNX"], m.index, 0)
    out["results"]["mortgage"] = compare("mortgage", m.values, dlr["mortgage"]["series"]["test_index"], cov=tnx, fc=fc, dl=dlr["mortgage"])

    f = fluview()
    f = f[f.index >= "2023-01-01"]
    out["results"]["flu"] = compare("flu", np.log(f.values), dlr["flu"]["series"]["test_index"], fc=fc, dl=dlr["flu"])

    out["results"]["brent"] = brent_daily(fc)
    json.dump(out, open(os.path.join(ROOT, "runs", "sota_timesfm.json"), "w"), indent=2, default=float)
    for k, r in out["results"].items():
        if k == "brent":
            print(f"brent     n={r['n']} TimesFM pinball(9q) {r['timesfm_pinball_9q']:.3f} cov80 {r['timesfm_cov80']:.3f} MAE(median) {r['timesfm_mae_median']:.3f}")
            continue
        d = r["domino_vs_timesfm"]
        print(f"{k:<9} n={r['n']} MAE TimesFM {r['mae_timesfm']:.4f} | Domino {r['mae_domino']:.4f} | no-change {r['mae_no_change']:.4f} | "
              f"Domino vs TimesFM {d['pct']:+.1f}% CI [{d['diff']['lo']:+.4f},{d['diff']['hi']:+.4f}] DM p={d['dm']['p']:.2g} | "
              f"TimesFM vs no-change {r['timesfm_vs_no_change']['pct']:+.1f}% | TFM dir {r['timesfm_direction_hit']:.2f} cov80 {r['timesfm_cov80']} ({r['seconds']}s)")


if __name__ == "__main__":
    main()
