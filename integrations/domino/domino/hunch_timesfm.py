"""TimesFM 3.0 entry for Hunch Q1 (weekday ticker direction): P(next close > last pre-cutoff close) from its quantiles.

Run with the TimesFM venv: <venv>/bin/python -m domino.hunch_timesfm --weights <timesfm-3.0 dir>  -> runs/hunch_timesfm.json
"""
import argparse
import json
import os

import numpy as np
import pandas as pd

from .sota_timesfm import load_fc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = np.linspace(0.1, 0.9, 9)


def p_up(q, last):
    """P(X > last) by linear interpolation of the 9-decile CDF, flat tails beyond P10/P90."""
    q = np.sort(np.asarray(q, float))
    if last <= q[0]:
        return float(1 - 0.1 * max(0.0, 1 - (q[0] - last) / max(q[0] - q[0] * 0.99, 1e-9)))
    if last >= q[-1]:
        return 0.05
    return float(1 - np.interp(last, q, LEVELS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--device", default="mps")
    a = ap.parse_args()
    fc = load_fc(a.weights, a.device)
    days = json.load(open(os.path.join(ROOT, "external", "hunch_live", "bundle.json")))["benchmark"]["evaluations"]["days"]
    px = pd.read_csv(os.path.join(ROOT, "data", "hunch_prices.csv"), index_col=0, parse_dates=True)
    out = {}
    for x in days:
        if x["isWeekend"]:
            continue
        s = px[x["ticker"]].dropna()
        s = s[s.index <= pd.Timestamp(x["cutoffDate"])]
        lp = np.log(s.values[-512:]).astype(np.float32)
        o = list(fc.predict_batch([lp], horizon=1, return_quantiles=True))[0]
        out[x["caseId"]] = p_up(o.quantiles[0], lp[-1])
    json.dump(out, open(os.path.join(ROOT, "runs", "hunch_timesfm.json"), "w"), indent=2)
    print({k: round(v, 3) for k, v in out.items()})


if __name__ == "__main__":
    main()
