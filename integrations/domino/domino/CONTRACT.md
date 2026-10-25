# Domino demo: server ↔ UI contract

Backend: FastAPI, `domino/server.py`, at `http://127.0.0.1:8100`. UI: `domino/static/index.html`, served at `/`. Vendored JS libraries live in `domino/static/vendor/` and are served at `/vendor/<file>`.

All endpoints return JSON. Fixtures with the same shapes live in `domino/static/fixtures/<name>.json`. The UI must support `?mock=1`, which loads the fixtures instead of the API and replays `fixtures/events.json` as if streamed.

## GET /api/graph

The causal chain (the dominoes).

```json
{"asof": "2026-10-25T11:45:00-07:00",
 "nodes": [{"id": "pizza", "label": "Pentagon pizza traffic", "kind": "observed|latent|market|attention|news",
            "lat": 38.86, "lon": -77.056, "value": 1.42, "unit": "× usual", "z": 2.1,
            "prob": 0.31, "state": "elevated", "level": 0}],
 "edges": [{"source": "pizza", "target": "escalation", "sign": 1, "lag_days": 0, "mechanism": "late-night staff surge…",
            "prior": 0.3, "measured": null, "evidence": "anecdotal", "active": 0.25}]}
```

- `level`: 0 = observations; 1 = latent events; 2 = regimes and markets.
- `prob`: current probability of the node's alarming state (latent and event nodes).
- `active`: 0–1, how strongly the edge is firing now. Drive particle speed and count from it.
- `evidence`: `"anecdotal"`, `"granger p=0.003"`, or `"corr 0.41 (lag 1)"`.
- `lat` / `lon` may be null for nodes that are not geographic. The UI then places them in the graph only, not on the globe.

## GET /api/forecast

Next-day predictions.

```json
{"asof": "...", "target_date": "2026-10-26", "hash": "sha256 hex of the forecast payload",
 "items": [{"id": "brent", "label": "Brent crude", "unit": "% return", "median": 0.4, "p10": -2.1, "p90": 3.0,
            "p_up": 0.56, "p_big_move": 0.22, "baseline": {"median": 0.0, "p10": -1.6, "p90": 1.6},
            "narration": "one sentence by Argon"}],
 "events": [{"id": "escalation24h", "label": "Major Middle East escalation within 24 h", "prob": 0.18,
             "source": "argon|stats|market", "narration": "..."}]}
```

## GET /api/backtest

Out-of-sample evidence.

```json
{"window": "2024-11-01..2026-10-23", "n_days": 480, "target": "Brent next-day log return",
 "metrics": {"crps": {"domino": {"mean": 1.05, "lo": 0.98, "hi": 1.12}, "ewma": {"mean": 1.09, "lo": 1.02, "hi": 1.16}},
             "log_score": {...}, "coverage80": {...}, "brier_big_move": {...}},
 "dm_test": {"vs": "ewma", "stat": -2.1, "p": 0.03},
 "reliability": [{"bin": 0.1, "pred": 0.08, "obs": 0.07, "n": 120}],
 "series": [{"date": "2026-01-02", "actual": 0.8, "median": 0.1, "p10": -1.7, "p90": 1.9, "surprise": 1.2, "tension": 0.1}]}
```

## GET /api/replay?start=YYYY-MM-DD&end=YYYY-MM-DD

Day-by-day frames for the history replay (for example June 9–20, 2025).

```json
{"frames": [{"date": "2025-06-12", "graph": <graph payload>, "forecast": <forecast payload>,
             "actual": {"brent": 7.0}, "surprise": 3.2, "narration": "..."}]}
```

## GET /api/pizza

```json
{"asof": "...", "index": 1.42, "places": [{"name": "Extreme Pizza", "lat": 38.86, "lon": -77.056,
  "live": 64, "usual": 35, "ratio": 1.83, "status": "busier than usual"}]}
```

## GET /events (Server-Sent Events)

Messages are `data: <json>\n\n`; every message has a `type`.

| type | fields |
|---|---|
| `data_call` | `target, usd, seconds, cached` (a treg or Glasser call, with its price) |
| `argon_call` | `purpose, thinking_level, seconds, input_tokens, output_tokens, thought_tokens, cached` |
| `surprise` | `node, observed, expected, surprise_nats` |
| `recursion` | `depth, thinking_level, question, F_before, F_after, dF_rel, stop, note` |
| `graph_update` | `graph` (a full `/api/graph` payload) |
| `forecast_update` | `forecast` (a full `/api/forecast` payload) |
| `log` | `level, text` |

## POST /api/run_live

Body `{}`. Starts the live pipeline: pull signals, run Argon interpretation and recursion, update graph and forecast, streaming events as it goes. Returns `{"ok": true}`.
