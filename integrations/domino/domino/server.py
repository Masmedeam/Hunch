"""Domino demo server (contract: domino/CONTRACT.md).

Run:  .venv/bin/python -m uvicorn domino.server:app --port 8100
Env:  DOMINO_DATA_MODE = live (default) | replay (treg cassette first) | cassette_only (offline stage fallback)
"""
import asyncio
import glob
import json
import os
import threading
import time
from collections import deque

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(ROOT, "domino", "static")
RUNS = os.path.join(ROOT, "runs")
os.environ.setdefault("RPWM_APP", "domino-server")
app = FastAPI(title="Domino")
subscribers, loop_ref = set(), {}
state = {"recent": deque(maxlen=300), "running": False}


def _load(name, default=None):
    path = os.path.join(RUNS, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def emit(ev):
    ev.setdefault("t", 0)
    state["recent"].append(ev)
    loop = loop_ref.get("loop")
    if loop:
        for q in list(subscribers):
            loop.call_soon_threadsafe(q.put_nowait, ev)


@app.on_event("startup")
async def _startup():
    loop_ref["loop"] = asyncio.get_running_loop()


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC, "index.html"))


@app.get("/realestate")
def realestate():
    return FileResponse(os.path.join(STATIC, "realestate.html"))


@app.get("/realestate/mock")
def realestate_mock():
    return FileResponse(os.path.join(STATIC, "realestate_mock.html"))


@app.get("/vendor/{name}")
def vendor(name: str):
    return FileResponse(os.path.join(STATIC, "vendor", os.path.basename(name)))


@app.get("/profiles/{name}")
def profile_index(name: str):
    path = os.path.join(STATIC, "profiles", os.path.basename(name))
    return FileResponse(path) if os.path.isfile(path) else JSONResponse({"error": "not found"}, status_code=404)


@app.get("/profiles/{profile}/{name}")
def profile_file(profile: str, name: str):
    path = os.path.join(STATIC, "profiles", os.path.basename(profile), os.path.basename(name))
    return FileResponse(path) if os.path.exists(path) else JSONResponse({"error": "not found"}, status_code=404)


@app.get("/fixtures/{name}")
def fixtures(name: str):
    return FileResponse(os.path.join(STATIC, "fixtures", os.path.basename(name)))


@app.get("/api/graph")
def graph():
    return _load("graph_latest.json") or JSONResponse({"error": "no live run yet; POST /api/run_live"}, status_code=404)


@app.get("/api/forecast")
def forecast():
    return _load("forecast_latest.json") or JSONResponse({"error": "no live run yet; POST /api/run_live"}, status_code=404)


@app.get("/api/backtest")
def backtest():
    return _load("backtest_latest.json") or JSONResponse({"error": "run python -m domino.build_static"}, status_code=404)


@app.get("/api/replay")
def replay(start: str = "2025-06-09", end: str = "2025-06-24"):
    rp = _load("replay_2025-06.json") or {"frames": []}
    return {"frames": [f for f in rp["frames"] if start <= f["date"] <= end]}


@app.get("/api/pizza")
def pizza():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "pizza_popular_times_*.json")))
    if not files:
        return {"asof": None, "index": None, "places": []}
    rows = json.load(open(files[-1]))
    places = []
    for e in rows:
        p, v = e["place"], e.get("popular_times") or {}
        pt = v.get("popular_times") if isinstance(v, dict) else None
        live = usual = None
        if isinstance(pt, dict):
            live, usual = pt.get("live"), pt.get("usual")
        places.append({"name": p["name"], "lat": p["latitude"], "lon": p["longitude"], "live": live, "usual": usual,
                       "ratio": (live / usual) if live and usual else None,
                       "status": "no live data from Google today" if pt is None else "ok"})
    ratios = [p["ratio"] for p in places if p["ratio"]]
    return {"asof": rows[0].get("fetched"), "index": (sum(ratios) / len(ratios)) if ratios else None, "places": places,
            "note": "Google exposed no busyness for these shops when fetched (litescrape + SerpApi via treg); shown as anecdotal hook."}


@app.get("/api/categories")
def categories():
    res = _load("category_results.json") or {}
    fd = _load("first_domino_results.json") or []
    interp_path = os.path.join(ROOT, "analysis", "argon_category_interpretation.json")
    interp = json.load(open(interp_path)) if os.path.exists(interp_path) else {}
    return {"categories": {k: {"label": c["label"], "attention_forecast": c["attention_forecast"], "first_domino": c.get("first_domino"),
                               "attention_leads_markets": c.get("attention_leads_markets"), "markets_lead_attention": c.get("markets_lead_attention")}
                           for k, c in res.get("categories", {}).items()},
            "first_domino_models": fd, "argon_ranking": interp.get("ranking", [])}


@app.get("/events")
async def events(request: Request):
    q = asyncio.Queue()
    subscribers.add(q)

    async def gen():
        try:
            yield "retry: 2000\n\n"
            while not await request.is_disconnected():
                try:
                    ev = await asyncio.wait_for(q.get(), timeout=15)
                    yield f"data: {json.dumps(ev, default=str)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            subscribers.discard(q)

    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/api/run_live")
async def run_live():
    if state["running"]:
        return JSONResponse({"ok": False, "error": "a live run is already in progress"}, status_code=409)

    def work():
        from .live import LivePipeline
        state["running"] = True
        try:
            LivePipeline(emit, data_mode=os.environ.get("DOMINO_DATA_MODE", "live")).run(ensemble_n=int(os.environ.get("DOMINO_ENSEMBLE", "5")))
        except Exception as exc:
            emit({"type": "log", "level": "warn", "text": f"live run failed: {type(exc).__name__}: {str(exc)[:200]}"})
        finally:
            state["running"] = False

    threading.Thread(target=work, daemon=True).start()
    return {"ok": True}


@app.get("/api/status")
def status():
    return {"running": state["running"], "recent": list(state["recent"])[-50:],
            "has": {n: os.path.exists(os.path.join(RUNS, n)) for n in ("graph_latest.json", "forecast_latest.json", "backtest_latest.json", "replay_2025-06.json")}}
