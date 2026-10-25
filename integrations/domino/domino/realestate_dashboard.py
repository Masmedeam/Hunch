"""Build domino/static/profiles/real-estate/dashboard.json for the simple real estate page (domino/static/realestate.html).

Inputs (all produced by this project): runs/realestate_results.json, realestate_argon.json, realestate_timesfm.json,
re_invest_rank.json, re_invest_collect.json, re_invest_zips.json, re_invest_research.json, treg/glasser charge logs.
Run: .venv/bin/python -I domino/realestate_dashboard.py   (also called by domino/profiles_build.py)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

R = lambda *p: os.path.join(ROOT, *p)
OFFSETS = {"dallas": [16, -6], "austin": [-16, -4], "houston": [16, 10], "san_antonio": [16, 30], "miami": [-16, 6],
           "dubai": [16, -8], "abu_dhabi": [16, 22], "almaty": [-18, 7], "astana": [-18, 7]}
TREG_PRICE = {"harvestapi.linkedin.search.jobs": 0.001, "anyapi.x.search.posts": 0.00075, "anyapi.tiktok.search.videos": 0.0012,
              "crawl4ai.youtube.search.videos": 0.0009, "treg.youtube.video.detail": 0.001}  # catalog prices; the log records 0 estimates
GLASSER_START_USD = 1.00  # balance at 14:45 PDT, before the real estate collectors ran
SHORT = {"Dallas–Fort Worth": "Dallas", "San Antonio": "San Antonio", "Abu Dhabi": "Abu Dhabi"}


def load(name, default=None):
    p = R("runs", name)
    return json.load(open(p)) if os.path.exists(p) else default


def spend(log, prefix_ts):
    tot = 0.0
    if os.path.exists(log):
        seen = set()
        for line in open(log, encoding="utf-8"):
            r = json.loads(line)
            if str(r.get("ts", "")) < prefix_ts:
                continue
            key = (r.get("label") or r.get("target"), json.dumps(r.get("params") or r.get("body") or r.get("req") or "", sort_keys=True))
            if r.get("cached") or key in seen and log.endswith("glasser_charges.jsonl"):
                continue
            seen.add(key)
            tot += float(r.get("charge_usd") or r.get("usd") or r.get("usd_estimate") or TREG_PRICE.get(r.get("target"), 0) or 0)
    return tot


def investment_graph(rows, rr, col, rs):
    """Drivers -> channels -> markets, with the evidence class of every link (measured / prior / anecdotal / noskill)."""
    import re
    rt, rn, pr = rr["rates"], rr["rents"], rr["prices"]
    res = {k: (v.get("research") or {}) for k, v in (rs.get("markets") or {}).items()}
    cm = col.get("markets") or {}
    kzt = ((col.get("global") or {}).get("markets") or {}).get("KZT=X", {}).get("ret_1y_pct")
    tx = ("dallas", "austin", "houston", "san_antonio")
    jobs_tx = sum(((cm.get(k) or {}).get("linkedin_jobs") or {}).get("week") or 0 for k in tx)
    hold_tx = [res.get(k, {}).get("annual_holding_costs_pct") for k in tx if res.get(k, {}).get("annual_holding_costs_pct")]
    zones = re.search(r"(\d+)\s+designated Investment Zones", res.get("abu_dhabi", {}).get("foreign_buyer_access") or "")
    hype = {k: ((v.get("hype")) if isinstance(v, dict) else None) for k, v in {x["key"]: x for x in rows}.items()}
    nodes = [
        {"id": "us10y", "label": "10-year Treasury", "group": "driver", "level": 0, "lat": 40.71, "lon": -74.01, "value": f"{rt['tnx_last']['yield']:.2f}%"},
        {"id": "zori", "label": "US market rents (Zillow)", "group": "driver", "level": 0, "lat": 47.61, "lon": -122.33, "value": f"{rn['now']['zori_yoy']:+.1f}% y/y"},
        {"id": "jobs_tx", "label": "Texas jobs (LinkedIn)", "group": "driver", "level": 0, "lat": 33.6, "lon": -101.8, "value": f"{jobs_tx:,} this week"},
        {"id": "tx_tax", "label": "Texas tax + insurance", "group": "driver", "level": 0, "lat": 27.3, "lon": -102.5,
         "value": f"≈{sum(hold_tx) / len(hold_tx):.1f}% a year" if hold_tx else "≈4.5% a year"},
        {"id": "uae_credit", "label": "UAE loans + AED peg", "group": "driver", "level": 0, "lat": 22.6, "lon": 51.6,
         "value": f"{res.get('dubai', {}).get('typical_mortgage_rate_pct') or 5.25:.2f}% loans"},
        {"id": "dxb_supply", "label": "Dubai handover pipeline", "group": "driver", "level": 0, "lat": 27.9, "lon": 57.5, "value": "supply risk",
         "tip": (res.get("dubai", {}).get("supply_pipeline") or "")[:220]},
        {"id": "ad_zones", "label": "Abu Dhabi investment zones", "group": "driver", "level": 0, "lat": 21.6, "lon": 55.9,
         "value": f"{zones.group(1)} zones" if zones else "freehold zones"},
        {"id": "kzt", "label": "Tenge vs USD", "group": "driver", "level": 0, "lat": 46.6, "lon": 80.8, "value": f"{abs(kzt or 0):.0f}% swing in a year"},
        {"id": "kz_credit", "label": "KZ loans + title rule", "group": "driver", "level": 0, "lat": 48.0, "lon": 66.0,
         "value": f"{res.get('almaty', {}).get('typical_mortgage_rate_pct') or 19.5:.1f}% · VNZh"},
        {"id": "froth", "label": "Social froth (Argon)", "group": "driver", "level": 0, "lat": None, "lon": None,
         "value": f"Dubai {hype.get('dubai') or 0:.2f} · Abu Dhabi {hype.get('abu_dhabi') or 0:.2f}"},
        {"id": "us_mortgage", "label": "US 30-year mortgage", "group": "channel", "level": 1, "lat": 38.93, "lon": -77.18,
         "value": f"{rt['pmms_last']['rate']:.2f}% → {rt['forecast_next']['median']:.2f}%"},
        {"id": "cpi_rent", "label": "CPI rent (BLS)", "group": "channel", "level": 1, "lat": 36.2, "lon": -86.9,
         "value": f"{rn['now']['cpi_rent_yoy']:.1f}% → {rn['forecast_12m']['cpi_rent_yoy']:.1f}%"},
        {"id": "momentum", "label": "US price momentum", "group": "channel", "level": 1, "lat": 37.7, "lon": -92.0, "value": f"{pr['us']['forecast_next_mom_pct']:+.2f}% Oct"},
        {"id": "rent_2027", "label": "Your rent · Sep 2027", "group": "outcome", "level": 2, "lat": 34.0, "lon": -81.0, "value": f"{rn['forecast_12m']['cpi_rent_yoy']:.1f}%"}]
    for x in rows:
        a = x.get("argon") or {}
        nodes.append({"id": x["key"], "label": SHORT.get(x["market"], x["market"]), "group": "market", "level": 2, "lat": x["lat"], "lon": x["lon"],
                      "verdict": a.get("verdict"), "model": x.get("expected_12m_pct"), "argon": a.get("expected_12m_usd_return_pct"),
                      "value": f"{(x.get('expected_12m_pct') or 0):+.1f}% · {a.get('verdict') or '—'}", "tip": a.get("why")})
    E = lambda s, t, cls, ev: {"source": s, "target": t, "cls": cls, "evidence": ev}
    us = ("dallas", "austin", "houston", "san_antonio", "miami")
    edges = [E("us10y", "us_mortgage", "measured", "Granger p = 3e-34 at a 2-week lag; TimesFM −26% error vs no-change"),
             E("zori", "cpi_rent", "measured", f"r {rn['corr_at_best']:.2f} at a {rn['best_lead_months']}-month lead"),
             E("cpi_rent", "rent_2027", "measured", f"12-month-ahead {rn['oos_12m']['vs_ar']['pct']:+.0f}% error vs CPI's own history")]
    edges += [E("momentum", k, "measured", f"AR momentum {100 * (pr['mae']['ar_only'] / pr['mae']['momentum'] - 1):+.0f}% error vs naive") for k in us]
    edges += [E("us_mortgage", k, "noskill", f"tested: rates add {pr['rates_vs_ar']['pct']:+.0f}% error next month, {pr['h6']['pct']:+.1f}% at 6 months") for k in us]
    edges += [E("jobs_tx", k, "prior", "demand: new jobs bring renters") for k in tx]
    edges += [E("tx_tax", k, "prior", "holding costs eat about 4–5 points of gross yield") for k in tx]
    edges += [E("uae_credit", k, "prior", "dollar-pegged financing; no FX risk for a USD buyer") for k in ("dubai", "abu_dhabi")]
    edges += [E("dxb_supply", "dubai", "prior", "large 2026–27 handovers weigh on prices and rents"),
              E("ad_zones", "abu_dhabi", "prior", "more freehold zones widen foreign demand"),
              E("froth", "dubai", "anecdotal", "broker promotion vs macro skepticism (X, TikTok, YouTube)"),
              E("froth", "abu_dhabi", "anecdotal", "bullish chatter, sentiment +0.78")]
    edges += [E("kzt", k, "prior", "the tenge's swing is the USD investor's risk") for k in ("almaty", "astana")]
    edges += [E("kz_credit", k, "prior", "19.5% mortgages; sources say non-residents need a VNZh to register title") for k in ("almaty", "astana")]
    return {"nodes": nodes, "edges": edges}


def build():
    rr, ra, tf = load("realestate_results.json", {}), load("realestate_argon.json", {}), load("realestate_timesfm.json", {})
    rk, col, zp, rs = load("re_invest_rank.json", {}), load("re_invest_collect.json", {}), load("re_invest_zips.json", {}), load("re_invest_research.json", {})
    rt, rn, pr = rr["rates"], rr["rents"], rr["prices"]
    mon = lambda p: __import__("datetime").datetime.strptime(p, "%Y-%m").strftime("%b %Y")
    ens = ra.get("argon_ensemble") or {}
    rows = rk.get("rows") or []
    top = rows[0] if rows else {}
    ta = top.get("argon") or {}
    kpis = [{"label": "30-year mortgage · Thu 29 Oct", "value": f"{rt['forecast_next']['median']:.2f}%",
             "sub_html": f"from {rt['pmms_last']['rate']:.2f}% · P(lower) <b>{rt['forecast_next']['p_lower_than_last']:.0%}</b> stats · <b>{(ens.get('p_pmms_below_last') or 0):.0%}</b> Argon"},
            {"label": f"Rent inflation · {mon(rn['forecast_12m']['target'])}", "value": f"{rn['forecast_12m']['cpi_rent_yoy']:.1f}%",
             "sub_html": f"from {rn['now']['cpi_rent_yoy']:.1f}% · market rents lead CPI rent by <b>{rn['best_lead_months']} months</b> (r {rn['corr_at_best']:.2f})"},
            {"label": f"US home values · {mon(pr['next_month'])}", "value": f"{pr['us']['forecast_next_mom_pct']:+.2f}%",
             "sub_html": f"P(fall) <b>{pr['us']['p_decline_next']:.0%}</b> stats · <b>{(ens.get('p_zhvi_decline') or 0):.0%}</b> Argon · momentum drives it, rates don't"},
            {"label": "Best risk-adjusted market", "value": top.get("market", "—"),
             "sub_html": (f"model <b>{top.get('expected_12m_pct', 0):+.1f}%</b> a year in USD · Argon <b>{ta.get('verdict', '—')}</b> "
                          f"({(ta.get('expected_12m_usd_return_pct') or 0):+.1f}%)") if top else ""}]
    markets = []
    for x in rows:
        a = x.get("argon") or {}
        votes = a.get("verdict_votes") or {}
        markets.append({"key": x["key"], "market": x["market"], "short": SHORT.get(x["market"], x["market"]), "lat": x["lat"], "lon": x["lon"],
                        "note": ("measured · Zillow" if x["country"] == "US" else "reported · Argon-sourced") + (f" · {x['mortgage_rate_pct']:.1f}% loans" if x.get("mortgage_rate_pct") else ""),
                        "gross": x.get("gross_yield_pct"), "net": x.get("net_yield_pct"), "price_12m": x.get("price_12m_pct"), "model_12m": x.get("expected_12m_pct"),
                        "risk": x.get("risk"), "label_offset": OFFSETS.get(x["key"]), "source": x.get("gross_yield_source"),
                        "argon": {"exp": a.get("expected_12m_usd_return_pct"), "p10": a.get("p10_pct"), "p90": a.get("p90_pct"), "verdict": a.get("verdict"),
                                  "votes": f"{votes.get(a.get('verdict'), 0)}/{sum(votes.values())}" if votes else "", "best_for": a.get("best_for"), "why": a.get("why"),
                                  "first_domino": a.get("first_domino"), "change": a.get("what_would_change_my_mind")}})
    zips = {}
    for k, lab in (("dallas", "Dallas–Fort Worth"), ("austin", "Austin")):
        zips[lab] = [{"zip": z["zip"], "city": z["city"], "gross": z["gross_yield_pct"], "price_yoy": z["price_yoy_pct"]} for z in ((zp.get("metros") or {}).get(k) or {}).get("top", [])[:4]]
    chains = [{"title": "Rates · measured weekly",
               "cards": [{"label": "10-year Treasury", "value": f"{rt['tnx_last']['yield']:.2f}%", "sub": f"{rt['tnx_last']['week_change_bp']:+.0f} bp on the week"},
                         {"label": "Freddie 30-year", "value": f"{rt['pmms_last']['rate']:.2f}%", "sub": "Thu 22 Oct"},
                         {"label": "Freddie · Thu 29 Oct", "value": f"{rt['forecast_next']['median']:.2f}%", "sub": "forecast", "life": True}],
               "evidence_html": f"<b>measured</b> · Granger p = 3e-34 at a 2-week lag · TimesFM {rt['weekly_model']['timesfm_vs_no_change_pct']:+.0f}% error vs no-change"},
              {"title": "Rents · 13-month lead",
               "cards": [{"label": "Market rents (Zillow)", "value": f"{rn['now']['zori_yoy']:+.1f}%", "sub": "y/y, Sep"},
                         {"label": "CPI rent (BLS)", "value": f"{rn['now']['cpi_rent_yoy']:.1f}%", "sub": "y/y, Sep"},
                         {"label": f"Your rent · {mon(rn['forecast_12m']['target'])}", "value": f"{rn['forecast_12m']['cpi_rent_yoy']:.1f}%", "sub": "forecast", "life": True}],
               "evidence_html": f"<b>measured</b> · r {rn['corr_at_best']:.2f} at {rn['best_lead_months']} months · 12-month-ahead {rn['oos_12m']['vs_ar']['pct']:+.0f}% error vs CPI's own history (p {rn['oos_12m']['vs_ar']['dm']['p']:.2f})"}]
    h6, cu = pr["h6"], rr["cuts"]
    t_zhvi = (tf.get("zhvi_us") or {}).get("timesfm_vs_momentum_pct")
    scoreboard = [{"ok": True, "claim": "10-year Treasury → mortgage rate", "detail": f"weekly, {rt['weekly_model']['n']} weeks", "effect": f"{rt['weekly_model']['timesfm_vs_no_change_pct']:+.0f}% error"},
                  {"ok": True, "claim": "Market rents → CPI rent", "detail": f"12 months ahead, {rn['oos_12m']['n']} origins", "effect": f"{rn['oos_12m']['vs_ar']['pct']:+.0f}% error"},
                  {"ok": True, "claim": "Momentum → next month's home values", "detail": f"{pr['n_metros']} metros, {pr['n_months']} months", "effect": f"{100 * (pr['mae']['ar_only'] / pr['mae']['momentum'] - 1):+.0f}% error"},
                  {"ok": False, "claim": "Mortgage rates → next month's home values", "detail": f"6-month horizon too: {h6['pct']:+.1f}% (p {h6['dm']['p']:.2f})", "effect": f"{pr['rates_vs_ar']['pct']:+.0f}% error"},
                  {"ok": False, "claim": "Price cuts → next month's home values", "detail": "Realtor.com, 12 test months", "effect": f"{cu.get('pct', 0):+.1f}% error"},
                  {"ok": False, "claim": "TimesFM 3.0 on home values", "detail": "smoothed Zillow series: momentum wins", "effect": f"{t_zhvi:+.0f}% error" if t_zhvi is not None else "—"}]
    m = col.get("markets") or {}
    g_ = col.get("global") or {}
    n_air = sum((v.get("airbnb") or {}).get("n", 0) for v in m.values())
    n_soc = sum((v.get("social") or {}).get("n", 0) for v in m.values())
    n_news = sum(len(v.get("news") or []) for v in m.values())
    devs = {k: v for k, v in (g_.get("linkedin_companies") or {}).items() if v.get("match")}
    px = g_.get("markets") or {}
    li_d, li_a = (m.get("dallas") or {}).get("linkedin_jobs", {}).get("week"), (m.get("dubai") or {}).get("linkedin_jobs", {}).get("week")
    air = lambda k: (m.get(k) or {}).get("airbnb", {}).get("median_nightly_usd")
    collectors = [
        {"name": "LinkedIn jobs", "detail": f"9 markets · jobs posted this week: Dallas {li_d:,} · Dubai {li_a:,}" if li_d and li_a else "9 markets", "via": "treg · harvestapi (the actor Hunch runs)"},
        {"name": "Airbnb", "detail": f"{n_air} listings · median night: Dallas ${air('dallas'):.0f} · Dubai ${air('dubai'):.0f} · Almaty ${air('almaty'):.0f}" if air('dallas') else f"{n_air} listings",
         "via": "Glasser · apify tri_angle, Hunch's stay settings"},
        {"name": "Zillow", "detail": "lender quotes, agents, ZIP and metro values and rents", "via": "Glasser + research CSVs"},
        {"name": "RentCast", "detail": "ZIP market stats: " + ", ".join(sorted((zp.get("rentcast") or {}).keys())), "via": "Glasser market_data (Hunch's RentCast vertical)"},
        {"name": "LinkedIn companies", "detail": " · ".join(f"{v['name']} {v['followers']:,} followers" for v in devs.values()) if devs else "—", "via": "Glasser · tikhub"},
        {"name": "X · TikTok · YouTube · news", "detail": f"{n_soc} posts and videos + {n_news} headlines, read by Argon for froth", "via": "treg"},
        {"name": "Markets", "detail": " · ".join(f"{t} {v['ret_1y_pct']:+.0f}% 1y" for t, v in px.items() if v.get("ret_1y_pct") is not None and t in ("EMAAR.AE", "INVH", "DHI", "KZT=X")),
         "via": "yfinance (KZT=X up = tenge weaker)"},
        {"name": "Gemini 4 Argon", "detail": "9 grounded research calls (Google Search), 9 social readings, 5-sample ranking", "via": "high · priority"},
        {"name": "Official data", "detail": "Realtor.com, BLS CPI, Freddie Mac", "via": "free downloads"}]
    t_usd = spend(R("runs", "treg_charges.jsonl"), "2026-10-25 14:4")
    bal = (rk.get("glasser_balance") or {}).get("available_usd")
    g_usd = GLASSER_START_USD - float(bal) if bal is not None else spend(R("runs", "glasser_charges.jsonl"), "2026-10-25 14:4")
    out = {"asof": "25 Oct 2026", "subtitle": "What moves housing next, and where the numbers say to invest · Dallas, Austin, Houston, San Antonio, Miami, Dubai, Abu Dhabi, Almaty, Astana",
           "kpis": kpis, "markets": markets, "zips": zips, "chains": chains, "scoreboard": scoreboard, "collectors": collectors,
           "rank_hint": "hover a row for Argon's reasoning · model = net yield + half of momentum − entry/exit costs over 5 years · FX swing counts as risk",
           "spend_text": f"spend today: Glasser ${g_usd:.2f}" + (f" (balance ${bal})" if bal else "") + f" · treg ${t_usd:.2f}",
           "hash": rk.get("hash"),
           "footer": ("Research, not investment advice. US numbers are measured (Zillow, Realtor.com, BLS, Freddie Mac) and backtested; Dubai, Abu Dhabi, Almaty and Astana "
                      "use Argon-grounded published figures with sources (runs/re_invest_research.json). Risk = chance prices fall, price cuts, social froth, FX swing, supply "
                      "flags. Pre-registered hash covers the model and Argon numbers.")}
    out["graph"] = investment_graph(rows, rr, col, rs)
    out["pick"] = rk.get("argon_overall_pick")
    os.makedirs(R("domino", "static", "profiles", "real-estate"), exist_ok=True)
    json.dump(out, open(R("domino", "static", "profiles", "real-estate", "dashboard.json"), "w"), indent=1, default=float)
    print("dashboard.json:", len(markets), "markets ·", len(kpis), "kpis · top", top.get("market"))


if __name__ == "__main__":
    build()
