"""First-domino volatility model: does the leading attention signal found by Granger tests improve next-day forecasts?

sigma_{t+1} = sigma_EWMA,t * exp(beta * z_{t-1}),  r_{t+1} ~ Student-t(5) with that scale.
z is the first-domino article's attention z-score, lagged one extra day (strict: complete before the interval starts).
beta is fitted by maximum likelihood on an expanding window, refit every 21 days. Compared with EWMA-t on CRPS and
log score with block-bootstrap CIs and a Diebold-Mariano test.
"""
import math

import numpy as np
import pandas as pd
from scipy import optimize, stats

from . import history as H
from . import model as M

PAIRS = [  # (category, first-domino article, target name, ticker) from runs/category_results.json lead-lag
    ("macro_stress", "Recession", "vix", "^VIX"),
    ("macro_stress", "Recession", "sp500", "^GSPC"),
    ("china_taiwan_trade", "China–United_States_trade_war", "china", "FXI"),
    ("russia_ukraine", "Russian_invasion_of_Ukraine", "defense", "ITA"),
    ("crypto", "Ethereum", "btc", "BTC-USD"),
]


def fit_beta(r, s, z):
    def nll(b):
        sc = s * np.exp(b[0] * z) * M.T_SCALE
        return -np.sum(stats.t.logpdf(r, M.NU, 0, sc))
    return float(optimize.minimize(nll, x0=[0.0], method="Nelder-Mead").x[0])


def evaluate(px, z_article, start=250, refit=21, n_samp=1000, seed=3):
    r = (100 * np.log(px.dropna()).diff()).dropna()
    z = z_article.reindex(r.index).ffill().shift(1).fillna(0.0).clip(-5, 10)
    s = pd.Series(M.ewma_sigma(r.values)[:-1], index=r.index)
    rng = np.random.default_rng(seed)
    rows, beta = [], 0.0
    for t in range(start, len(r)):
        if (t - start) % refit == 0:
            beta = fit_beta(r.values[20:t], s.values[20:t], z.values[20:t])
        y, sig, zz = r.values[t], s.values[t], z.values[t]
        sc = sig * math.exp(beta * zz)
        a = rng.standard_t(M.NU, n_samp) * M.T_SCALE * sc
        b = rng.standard_t(M.NU, n_samp) * M.T_SCALE * sig
        rows.append({"date": r.index[t], "crps": M.crps_samples(a, y), "crps_base": M.crps_samples(b, y),
                     "logs": stats.t.logpdf(y, M.NU, 0, sc * M.T_SCALE), "logs_base": stats.t.logpdf(y, M.NU, 0, sig * M.T_SCALE),
                     "beta": beta, "z": zz})
    df = pd.DataFrame(rows)
    return {"n": int(len(df)), "beta_last": float(beta),
            "crps_diff": M.block_bootstrap_mean(df["crps"] - df["crps_base"]),
            "crps_dm": M.dm_test(df["crps"], df["crps_base"]),
            "logscore_diff": M.block_bootstrap_mean(df["logs"] - df["logs_base"]),
            "crps_rel_pct": float(100 * (df["crps"].mean() / df["crps_base"].mean() - 1))}


def run():
    from .categories import prices, wiki
    px = prices([])
    out = []
    for cat, art, name, tk in PAIRS:
        pv = wiki(art)
        z, _ = H.attention_index(pv.to_frame())
        res = evaluate(px[tk], z[art])
        out.append({"category": cat, "first_domino": art, "target": name, "ticker": tk, **res})
    return out


if __name__ == "__main__":
    import json
    import os
    res = run()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json.dump(res, open(os.path.join(root, "runs", "first_domino_results.json"), "w"), indent=2, default=float)
    for r in res:
        c = r["crps_diff"]
        print(f'{r["category"]:<20} {r["first_domino"][:30]:<30} -> {r["target"]:<8} n={r["n"]} beta={r["beta_last"]:+.3f} '
              f'CRPS {r["crps_rel_pct"]:+.2f}% diff {c["mean"]:+.4f} [{c["lo"]:+.4f},{c["hi"]:+.4f}] DM p={r["crps_dm"]["p"]:.3g} '
              f'logS {r["logscore_diff"]["mean"]:+.4f} [{r["logscore_diff"]["lo"]:+.4f},{r["logscore_diff"]["hi"]:+.4f}]')
