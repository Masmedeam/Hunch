"""Historical daily data for Domino (free sources), cached under data/.

Markets: yfinance daily closes. Attention: Wikipedia pageviews per article (Wikimedia REST, free, since 2015).
"""
import json
import os
import time
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TICKERS = {"brent": "BZ=F", "wti": "CL=F", "natgas": "NG=F", "gasoline": "RB=F", "vix": "^VIX", "sp500": "^GSPC",
           "energy": "XLE", "defense": "ITA", "airlines": "JETS", "gold": "GC=F"}
ARTICLES = ["Strait_of_Hormuz", "Iran", "Israel", "Iran–Israel_war", "Houthis", "Hezbollah",
            "Islamic_Revolutionary_Guard_Corps", "Brent_Crude", "Price_of_oil", "OPEC", "World_War_III",
            "The_Pentagon", "Nuclear_program_of_Iran"]
UA = {"User-Agent": "Domino-hackathon/0.1 (Gemini 4 Argon hackathon research demo)"}


def markets(start="2023-06-01", end=None, refresh=False):
    path = os.path.join(DATA, "markets.csv")
    if os.path.exists(path) and not refresh:
        return pd.read_csv(path, index_col=0, parse_dates=True)
    import yfinance as yf
    frames = {}
    for name, tk in TICKERS.items():  # one ticker at a time: avoids yfinance's sqlite cache lock under batch download
        for attempt in range(3):
            try:
                s = yf.download(tk, start=start, end=end, progress=False, auto_adjust=True)["Close"]
                s = s.iloc[:, 0] if isinstance(s, pd.DataFrame) else s
                if len(s):
                    frames[name] = s
                    break
            except Exception:
                time.sleep(1.5)
    df = pd.DataFrame(frames).sort_index()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    os.makedirs(DATA, exist_ok=True)
    df.to_csv(path)
    return df


def pageviews(article, start="20230601", end=None):
    end = end or time.strftime("%Y%m%d")
    url = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"
           f"{urllib.parse.quote(article, safe='')}/daily/{start}/{end}")
    req = urllib.request.Request(url, headers=UA)
    try:
        items = json.load(urllib.request.urlopen(req, timeout=30))["items"]
    except Exception:
        return None
    s = pd.Series({pd.Timestamp(i["timestamp"][:8]): i["views"] for i in items}, name=article)
    return s.sort_index()


def attention(refresh=False):
    path = os.path.join(DATA, "wiki_pageviews.csv")
    if os.path.exists(path) and not refresh:
        return pd.read_csv(path, index_col=0, parse_dates=True)
    cols = {}
    for a in ARTICLES:
        s = pageviews(a)
        if s is not None and len(s) > 100:
            cols[a] = s
    df = pd.DataFrame(cols).sort_index()
    df.to_csv(path)
    return df


def attention_index(pv, window=60):
    """Mean robust z-score of log pageviews against each article's trailing window (no look-ahead)."""
    lg = np.log1p(pv)
    mu = lg.rolling(window, min_periods=20).mean().shift(1)
    sd = lg.rolling(window, min_periods=20).std().shift(1)
    z = (lg - mu) / sd.replace(0, np.nan)
    return z.clip(-5, 15), z.mean(axis=1).rename("attention")


if __name__ == "__main__":
    m = markets(refresh=True)
    a = attention(refresh=True)
    print("markets", m.shape, m.index[0].date(), "->", m.index[-1].date(), "cols", list(m.columns))
    print("pageviews", a.shape, a.index[0].date(), "->", a.index[-1].date(), "cols", list(a.columns))
