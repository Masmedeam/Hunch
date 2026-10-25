"""treg.to client for Domino: CLI-backed, record/replay cassette, per-call spend log, hard caps.

Every call goes through `tools/treg.sh call ...` (token injected server-side; we never hold the provider keys).
Responses are cached in runs/treg_cassette.jsonl keyed by (target, method, params, body) so the stage demo can
replay without network, and nothing is paid for twice. Charges are logged to runs/treg_charges.jsonl.
"""
import hashlib
import json
import os
import subprocess
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASSETTE = os.path.join(ROOT, "runs", "treg_cassette.jsonl")
CHARGES = os.path.join(ROOT, "runs", "treg_charges.jsonl")
TREG = os.path.join(ROOT, "tools", "treg.sh")
_lock = threading.Lock()
_cache = {}
MAX_CALL_USD = 0.03      # refuse any endpoint priced above this per call
MAX_SESSION_USD = 0.40   # stop live calls after this much spend in one process
_spent = {"usd": 0.0, "calls": 0}


def _key(target, method, params, body):
    return hashlib.sha256(json.dumps([target, method, params or {}, body or {}], sort_keys=True).encode()).hexdigest()


def _load():
    if _cache or not os.path.exists(CASSETTE):
        return
    for line in open(CASSETTE, encoding="utf-8"):
        try:
            r = json.loads(line)
            _cache[r["key"]] = r
        except (json.JSONDecodeError, KeyError):
            pass


def call(target, params=None, body=None, method=None, price_usd=0.0, mode="replay", timeout=60, emit=None):
    """mode: replay (cassette first, live on miss) | live (always call, record) | cassette_only.
    Returns (json_or_none, meta)."""
    _load()
    method = method or ("POST" if body is not None else "GET")
    k = _key(target, method, params, body)
    if mode in ("replay", "cassette_only") and k in _cache:
        rec = _cache[k]
        meta = {"cached": True, "usd": 0.0, "seconds": 0.0, "target": target, "recorded": rec.get("ts")}
        if emit:
            emit({"type": "data_call", **meta})
        return rec["value"], meta
    if mode == "cassette_only":
        return None, {"cached": False, "error": "cassette miss", "target": target}
    if price_usd > MAX_CALL_USD:
        return None, {"error": f"price ${price_usd} above cap ${MAX_CALL_USD}", "target": target}
    if _spent["usd"] + price_usd > MAX_SESSION_USD:
        return None, {"error": "session spend cap reached", "target": target}
    cmd = [TREG, "call", target, "--method", method]
    for kk, vv in (params or {}).items():
        cmd += ["-p", f"{kk}={vv}"]
    if body is not None:
        cmd += ["--data", json.dumps(body), "--header", f"X-Treg-Route-Max-Cost: {max(price_usd * 3, 0.005):.4f}"]
    t0 = time.time()
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {"error": "timeout", "target": target}
    secs = round(time.time() - t0, 2)
    try:
        value = json.loads(out.stdout)
    except json.JSONDecodeError:
        return None, {"error": (out.stderr or out.stdout)[:300], "target": target, "seconds": secs}
    with _lock:
        _spent["usd"] += price_usd
        _spent["calls"] += 1
        rec = {"key": k, "target": target, "method": method, "params": params, "body": body, "value": value,
               "ts": time.strftime("%Y-%m-%d %H:%M:%S")}
        _cache[k] = rec
        with open(CASSETTE, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        with open(CHARGES, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": rec["ts"], "target": target, "usd_estimate": price_usd, "seconds": secs}) + "\n")
    meta = {"cached": False, "usd": price_usd, "seconds": secs, "target": target}
    if emit:
        emit({"type": "data_call", **meta})
    return value, meta


def spent():
    return dict(_spent)
