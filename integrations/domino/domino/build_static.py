"""Build the precomputed payloads the Domino UI needs: backtest (Brent) and the June 2025 replay (with Argon narration).

Run: .venv/bin/python -m domino.build_static   -> runs/backtest_latest.json, runs/replay_2025-06.json
"""
import concurrent.futures as cf
import json
import os
import time

import numpy as np

from rpwm.argon import Argon
from . import history as H
from . import model as M
from .live import EDGES, NODES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARR_SCHEMA = {"type": "object", "properties": {"narration": {"type": "string"}, "escalation_prob": {"type": "number"},
                                                "hormuz_prob": {"type": "number"}}, "required": ["narration", "escalation_prob", "hormuz_prob"]}


def backtest_payload():
    mk, pv = H.markets(), H.attention()
    z, A = H.attention_index(pv)
    bt, fit = M.backtest(mk, A.shift(1), target="brent")
    met, dm = M.summarize(bt)
    rel = M.reliability(bt["p_big"], bt["big"])
    series = bt.tail(260)[["date", "actual", "median", "p10", "p90", "surprise", "tension"]].round(4).to_dict("records")
    return {"window": f'{bt["date"].iloc[0]}..{bt["date"].iloc[-1]}', "n_days": int(len(bt)), "target": "Brent next-day log return (%)",
            "spec": "strict lag; 2-state HMM tension on Wikipedia crisis attention + Student-t(5) regime mixture vs EWMA Student-t(5)",
            "metrics": {"crps": {"domino": met["crps"]["domino"], "ewma": met["crps"]["ewma_t"], "diff": met["crps"]["diff"]},
                        "log_score": {"domino": met["log_score"]["domino"], "ewma": met["log_score"]["ewma_t"], "diff": met["log_score"]["diff"]},
                        "coverage80": {"domino": met["coverage80"]["domino"], "ewma": met["coverage80"]["ewma_t"]},
                        "brier_big_move": {"domino": met["brier_big_move"]["domino"], "ewma": met["brier_big_move"]["ewma_t"],
                                           "diff": met["brier_big_move"]["diff"], "base_rate": met["brier_big_move"]["base_rate"]}},
            "dm_test": {"vs": "ewma", **dm["crps"]}, "dm_brier": dm["brier"], "reliability": rel, "series": series,
            "fit": {"mixture": fit["mixture"]}}, bt, z, A, mk


def replay_payload(bt, z, A, mk, start="2025-06-09", end="2025-06-24"):
    argon = Argon(mode="replay")
    days = bt[(bt["date"] >= start) & (bt["date"] <= end)]
    arts = ["Strait_of_Hormuz", "Iran", "Israel", "Iran–Israel_war"]

    def narrate(row):
        d = row["date"]
        att = {a: round(float(z[a].get(d, np.nan)), 2) for a in arts if a in z.columns}
        prompt = (f"Replay of {d}. You are narrating Domino's world-model state for that trading day, for a 3-minute demo. "
                  f"Facts available that day: Brent next-day forecast median {row['median']:+.2f}%, 80% band [{row['p10']:+.2f}, {row['p90']:+.2f}], "
                  f"latent tension {row['tension']:.2f}; realized Brent move {row['actual']:+.2f}%; surprise {row['surprise']:.2f} nats; "
                  f"Wikipedia attention z-scores {att}. In <= 30 words narrate the domino chain that day (what moved first, what followed). "
                  f"Also give your probability, as of that morning, of a US/Israel-Iran escalation and of a Hormuz shipping disruption.")
        v, _ = argon.call(f"replay narration {d}", prompt, level="high", schema=NARR_SCHEMA, timeout=180)
        return d, v or {}

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        narr = dict(ex.map(narrate, [r for _, r in days.iterrows()]))
    frames = []
    for _, r in days.iterrows():
        d = r["date"]
        nv = narr.get(d, {})
        probs = {"attention": float(min(1, max(0, (A.get(d, 0) or 0) / 6))), "news": float(min(1, max(0, (A.get(d, 0) or 0) / 8))),
                 "escalation": float(nv.get("escalation_prob", r["tension"])), "hormuz": float(nv.get("hormuz_prob", r["tension"] * 0.6)),
                 "pentagon": float(nv.get("escalation_prob", 0.1)) * 0.8, "pizza": None, "brent": float(r["tension"])}
        nodes = [{"id": nid, "label": lab, "kind": kind, "lat": lat, "lon": lon, "level": lvl, "prob": probs.get(nid, float(r["tension"])),
                  "value": None, "unit": None, "z": float(A.get(d, np.nan)) if nid == "attention" else None, "state": None}
                 for nid, lab, kind, lat, lon, lvl in NODES]
        edges = [{"source": s, "target": t, "sign": sg, "lag_days": lg, "mechanism": None, "prior": 0.5, "measured": None,
                  "evidence": "anecdotal" if s == "pizza" else "Argon prior", "active": round(min(1.0, (probs.get(s) or 0) * 1.2), 3)}
                 for s, t, sg, lg in EDGES]
        forecast = {"asof": d, "target_date": d, "items": [{"id": "brent", "label": "Brent crude", "unit": "% return", "median": r["median"],
                                                            "p10": r["p10"], "p90": r["p90"], "p_up": None, "p_big_move": r["p_big"],
                                                            "baseline": {"median": 0.0, "p10": r["b_p10"], "p90": r["b_p90"]}}],
                    "events": [{"id": "escalation24h", "label": "US/Israel–Iran escalation (Argon, hindsight-aware)", "prob": probs["escalation"], "source": "argon"}]}
        frames.append({"date": d, "graph": {"asof": d, "nodes": nodes, "edges": edges}, "forecast": forecast,
                       "actual": {"brent": r["actual"]}, "surprise": r["surprise"],
                       "narration": nv.get("narration", ""), "narration_note": "Argon narration written with hindsight; numbers are strict-lag model outputs."})
    return {"frames": frames}


if __name__ == "__main__":
    os.environ.setdefault("RPWM_APP", "domino-build")
    t0 = time.time()
    payload, bt, z, A, mk = backtest_payload()
    json.dump(payload, open(os.path.join(ROOT, "runs", "backtest_latest.json"), "w"), indent=2, default=float)
    print(f"backtest {payload['n_days']} days; CRPS diff {payload['metrics']['crps']['diff']['mean']:+.4f}; coverage "
          f"{payload['metrics']['coverage80']['domino']['mean']:.3f} vs {payload['metrics']['coverage80']['ewma']['mean']:.3f} ({time.time() - t0:.0f}s)")
    rp = replay_payload(bt, z, A, mk)
    json.dump(rp, open(os.path.join(ROOT, "runs", "replay_2025-06.json"), "w"), indent=2, default=float)
    print(f"replay {len(rp['frames'])} frames ({time.time() - t0:.0f}s)")
    for f in rp["frames"]:
        print(" ", f["date"], f"actual {f['actual']['brent']:+.2f}", "|", f["narration"][:120])
