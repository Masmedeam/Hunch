"""Category sweep: apply the Domino world model to every topic we have data for, rank categories, find first dominoes.

For each category (a set of Wikipedia attention series + market targets):
  1. Market forecasts: strict-lag backtest (attention through UTC day t-2 for the close t-1 -> close t return),
     CRPS / log score / 80% coverage / Brier(big move) vs EWMA-t baseline, block-bootstrap CIs, Diebold-Mariano.
  2. Attention forecasts (social-engagement proxy): next-day log pageviews, AR(1)+tension vs persistence, MAE with CI.
  3. First domino: Granger tests attention -> |return| and |return| -> attention (lags 1-3), Holm-corrected; the
     first domino is the signal that leads the most targets without being led by them.
Run: .venv/bin/python -m domino.categories   (writes runs/category_results.json)
"""
import json
import os
import time
import warnings

import numpy as np
import pandas as pd

from . import history as H
from . import model as M

warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI_DIR = os.path.join(ROOT, "data", "wiki")

CATEGORIES = {
    "geopolitics_energy": {"label": "Middle East geopolitics → energy",
                           "articles": ["Strait_of_Hormuz", "Iran", "Israel", "Iran–Israel_war", "Houthis", "Hezbollah",
                                        "Islamic_Revolutionary_Guard_Corps", "OPEC", "Brent_Crude", "Price_of_oil"],
                           "targets": {"brent": "BZ=F", "wti": "CL=F", "gasoline": "RB=F", "energy": "XLE", "airlines": "JETS", "defense": "ITA"}},
    "macro_stress": {"label": "Macro stress → equities, rates, gold",
                     "articles": ["Recession", "Inflation", "Federal_Reserve", "Stock_market_crash", "Tariff", "Unemployment"],
                     "targets": {"sp500": "^GSPC", "vix": "^VIX", "gold": "GC=F", "bonds": "TLT", "banks": "KRE"}},
    "crypto": {"label": "Crypto attention → crypto prices",
               "articles": ["Bitcoin", "Ethereum", "Cryptocurrency", "Stablecoin", "Dogecoin"],
               "targets": {"btc": "BTC-USD", "eth": "ETH-USD", "coinbase": "COIN"}},
    "ai_tech": {"label": "AI hype → AI stocks",
                "articles": ["OpenAI", "ChatGPT", "Nvidia", "Google_Gemini", "Artificial_general_intelligence", "Anthropic"],
                "targets": {"nvda": "NVDA", "googl": "GOOGL", "semis": "SMH", "msft": "MSFT"}},
    "russia_ukraine": {"label": "Russia–Ukraine → gas, grain, defense",
                       "articles": ["Russia", "Ukraine", "Vladimir_Putin", "NATO", "Russian_invasion_of_Ukraine"],
                       "targets": {"natgas": "NG=F", "wheat": "ZW=F", "defense": "ITA", "eurusd": "EURUSD=X"}},
    "china_taiwan_trade": {"label": "China–Taiwan and trade → chips, China equities",
                           "articles": ["Taiwan", "Xi_Jinping", "China–United_States_trade_war", "Taiwan_Strait", "Rare-earth_element"],
                           "targets": {"tsmc": "TSM", "china": "FXI", "semis": "SMH"}},
    "health": {"label": "Outbreak attention → biotech",
               "articles": ["Measles", "Avian_influenza", "Mpox", "Pandemic", "Influenza"],
               "targets": {"biotech": "XBI", "moderna": "MRNA", "pfizer": "PFE"}},
    "weather_disasters": {"label": "Weather and disasters → gas, insurers, grains",
                          "articles": ["Hurricane", "Tropical_cyclone", "Heat_wave", "Wildfire", "Earthquake"],
                          "targets": {"natgas": "NG=F", "insurers": "KIE", "corn": "ZC=F"}},
}


def wiki(article):
    os.makedirs(WIKI_DIR, exist_ok=True)
    path = os.path.join(WIKI_DIR, article.replace("/", "_") + ".csv")
    if os.path.exists(path):
        s = pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]
        return s
    s = H.pageviews(article)
    if s is not None and len(s) > 100:
        s.to_frame().to_csv(path)
    return s


def prices(tickers):
    path = os.path.join(ROOT, "data", "markets_ext.csv")
    have = pd.read_csv(path, index_col=0, parse_dates=True) if os.path.exists(path) else pd.DataFrame()
    need = [t for t in tickers if t not in have.columns]
    if need:
        import yfinance as yf
        for tk in need:
            for _ in range(3):
                try:
                    s = yf.download(tk, start="2023-06-01", progress=False, auto_adjust=True)["Close"]
                    s = s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s
                    if len(s):
                        s.index = pd.to_datetime(s.index).tz_localize(None)
                        have = have.join(s.rename(tk), how="outer") if len(have) else s.rename(tk).to_frame()
                        break
                except Exception:
                    time.sleep(1.5)
        have.sort_index().to_csv(path)
    return have


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    m = len(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def granger_min_p(x, y, maxlag=3):
    """min p-value over lags 1..maxlag for 'x Granger-causes y' (ssr F test)."""
    from statsmodels.tsa.stattools import grangercausalitytests
    d = pd.concat([y, x], axis=1).dropna()
    if len(d) < 120:
        return None
    try:
        res = grangercausalitytests(d.values, maxlag=maxlag)  # statsmodels 0.15 removed verbose
    except Exception:
        return None
    best = min(((res[l][0]["ssr_ftest"][1], l) for l in res), key=lambda t: t[0])
    return {"p": float(best[0]), "lag": int(best[1])}


def attention_forecast(A):
    """Social-engagement proxy: forecast next-day category attention; AR(1) on index vs persistence (rolling, strict)."""
    a = A.dropna()
    errs_ar, errs_pers = [], []
    for t in range(250, len(a) - 1):
        hist = a.iloc[:t + 1].values
        x, y = hist[:-1], hist[1:]
        X = np.vstack([np.ones_like(x), x]).T
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        pred = beta[0] + beta[1] * hist[-1]
        truth = a.iloc[t + 1]
        errs_ar.append(abs(pred - truth))
        errs_pers.append(abs(hist[-1] - truth))
    e1, e0 = np.array(errs_ar), np.array(errs_pers)
    return {"mae_ar": M.block_bootstrap_mean(e1), "mae_persistence": M.block_bootstrap_mean(e0),
            "diff": M.block_bootstrap_mean(e1 - e0), "dm": M.dm_test(e1, e0), "n": int(len(e1))}


def run():
    t0 = time.time()
    all_tickers = sorted({tk for c in CATEGORIES.values() for tk in c["targets"].values()})
    px = prices(all_tickers)
    out = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "categories": {}}
    for key, cat in CATEGORIES.items():
        series = {a: wiki(a) for a in cat["articles"]}
        series = {a: s for a, s in series.items() if s is not None}
        if len(series) < 2:
            continue
        pv = pd.DataFrame(series).sort_index()
        z, A = H.attention_index(pv)
        A_strict = A.shift(1)
        res = {"label": cat["label"], "articles": list(series), "missing_articles": [a for a in cat["articles"] if a not in series],
               "targets": {}, "first_domino": None}
        mk = pd.DataFrame({name: px[tk] for name, tk in cat["targets"].items() if tk in px.columns})
        for name in mk.columns:
            try:
                bt, fit = M.backtest(mk, A_strict, target=name, n_samp=800)
                met, dm = M.summarize(bt)
                res["targets"][name] = {"n": int(len(bt)), "crps_diff": met["crps"]["diff"], "crps_dm_p": dm["crps"]["p"],
                                        "logscore_diff": met["log_score"]["diff"], "coverage80": met["coverage80"],
                                        "brier_diff": met["brier_big_move"]["diff"], "brier_dm_p": dm["brier"]["p"],
                                        "big_move_rate": met["brier_big_move"]["base_rate"], "mixture": fit["mixture"]}
            except Exception as exc:
                res["targets"][name] = {"error": f"{type(exc).__name__}: {str(exc)[:120]}"}
        res["attention_forecast"] = attention_forecast(A)
        # First domino: which attention series (or market) leads the others?
        lead = []
        absret = {name: (100 * np.log(mk[name].dropna()).diff()).abs() for name in mk.columns}
        for a, s in series.items():
            za = z[a]
            for name, ar in absret.items():
                fwd = granger_min_p(za.reindex(ar.index).ffill(), ar)
                rev = granger_min_p(ar, za.reindex(ar.index).ffill())
                if fwd and rev:
                    lead.append({"signal": a, "target": name, "p_fwd": fwd["p"], "lag_fwd": fwd["lag"], "p_rev": rev["p"]})
        if lead:
            adj_f = holm([l["p_fwd"] for l in lead])
            adj_r = holm([l["p_rev"] for l in lead])
            for l, f, r in zip(lead, adj_f, adj_r):
                l["p_fwd_holm"], l["p_rev_holm"] = float(f), float(r)
            score = {}
            for l in lead:
                s = score.setdefault(l["signal"], {"leads": 0, "led_by": 0, "best_p": 1.0, "targets": []})
                if l["p_fwd_holm"] < 0.05:
                    s["leads"] += 1
                    s["targets"].append(f'{l["target"]} (lag {l["lag_fwd"]}, p={l["p_fwd_holm"]:.3g})')
                if l["p_rev_holm"] < 0.05:
                    s["led_by"] += 1
                s["best_p"] = min(s["best_p"], l["p_fwd_holm"])
            ranked = sorted(score.items(), key=lambda kv: (-(kv[1]["leads"] - kv[1]["led_by"]), kv[1]["best_p"]))
            res["lead_lag"] = [{"signal": k, **v} for k, v in ranked]
            top = ranked[0]
            res["first_domino"] = {"signal": top[0], **top[1]} if top[1]["leads"] > 0 else None
            res["markets_lead_attention"] = sum(1 for l in lead if l["p_rev_holm"] < 0.05)
            res["attention_leads_markets"] = sum(1 for l in lead if l["p_fwd_holm"] < 0.05)
            res["n_pairs"] = len(lead)
        out["categories"][key] = res
        print(f"{key:<20} articles {len(series)} targets {len(res['targets'])} first domino "
              f"{(res['first_domino'] or {}).get('signal')} ({time.time() - t0:.0f}s)", flush=True)
    path = os.path.join(ROOT, "runs", "category_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=float)
    print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    run()
