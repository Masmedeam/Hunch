"""Glasser REST client (https://api.glasser.ai, docs: glasser.ai/docs/openapi.json).

The Node CLI fails with a local transport error on this network, so this client uses curl (macOS trust store).
The Key is read from GLASSER_API_KEY or .env (GLASSER), handed to curl through a 0600 header file, and never printed.
Idempotency keys are derived from the request, so a retry replays the original Run without a second charge.
Every response is appended to runs/glasser_cassette.jsonl; mode="replay" serves from it (offline stage fallback).
Caps: refuse an endpoint priced above MAX_RUN_USD; stop live calls after MAX_SESSION_USD in one process.
"""
import hashlib
import json
import os
import subprocess
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.glasser.ai"
CASSETTE = os.path.join(ROOT, "runs", "glasser_cassette.jsonl")
CHARGES = os.path.join(ROOT, "runs", "glasser_charges.jsonl")
MAX_RUN_USD = 0.15
MAX_SESSION_USD = 0.90  # Glasser balance was $1.00 on 2026-10-25
_spent = {"usd": 0.0}


def _key():
    k = os.environ.get("GLASSER_API_KEY") or os.environ.get("GLASSER")
    if not k and os.path.exists(os.path.join(ROOT, ".env")):
        for line in open(os.path.join(ROOT, ".env")):
            name, sep, val = line.strip().removeprefix("export ").partition("=")
            if sep and name.strip() in ("GLASSER_API_KEY", "GLASSER"):
                k = val.strip().strip('"').strip("'")
                break
    return k


def _curl(method, path, body=None, idem=None, timeout=180):
    with tempfile.NamedTemporaryFile("w", delete=False, prefix="glh_") as hf:
        os.chmod(hf.name, 0o600)
        hf.write(f"Authorization: Bearer {_key()}\n")
        if idem:
            hf.write(f"Idempotency-Key: {idem}\n")
        if body is not None:
            hf.write("Content-Type: application/json\n")
    try:
        cmd = ["curl", "-sS", "--max-time", str(timeout), "-X", method, "-H", f"@{hf.name}", "-w", "\n%{http_code}", API + path]
        if body is not None:
            cmd[1:1] = ["--data-binary", "@-"]
        p = subprocess.run(cmd, input=json.dumps(body) if body is not None else None, capture_output=True, text=True, timeout=timeout + 10)
    finally:
        os.unlink(hf.name)
    text, _, code = p.stdout.rpartition("\n")
    try:
        return int(code), json.loads(text) if text.strip() else {}
    except ValueError:
        return int(code) if code.isdigit() else 0, {"raw": text[:500], "stderr": p.stderr[:300]}


def _log(path, rec):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def _replay(kind, req):
    if not os.path.exists(CASSETTE):
        return None
    k = hashlib.sha256(json.dumps([kind, req], sort_keys=True).encode()).hexdigest()
    hit = None
    for line in open(CASSETTE, encoding="utf-8"):
        r = json.loads(line)
        if r.get("k") == k and r.get("ok"):
            hit = r
    return hit


def balance():
    return _curl("GET", "/v1/balance")


def search(query, use_case, limit=10):
    return _curl("POST", "/v1/endpoints/search", {"query": query, "use_case": use_case, "limit": limit})


def inspect(provider, endpoint):
    return _curl("POST", "/v1/endpoints/inspect", {"provider": provider, "endpoint": endpoint})


def _finish(code, out, timeout):
    """Poll a queued/running Run or Solution result until it settles."""
    t0 = time.time()
    while code == 202 or (isinstance(out, dict) and out.get("status") in ("QUEUED", "RUNNING")) or (isinstance(out, dict) and out.get("result_status") == "pending"):
        if time.time() - t0 > timeout:
            break
        time.sleep(3)
        if out.get("id") and "status" in out:  # a Run: run_url points at the web app, so poll the API by id
            path = f"/v1/runs/{out['id']}"
        else:
            url = out.get("result_url") or ""
            path = url.replace(API, "") if url.startswith((API, "/")) else None
        if not path:
            break
        code, out = _curl("GET", path)
    return code, out


def _charge(out):
    try:
        return float((out or {}).get("charge_usd") or 0)
    except (TypeError, ValueError):
        return 0.0


def run(provider, endpoint, inp, label="", mode="live", timeout=300, price_usd=None):
    """Run a marketplace Endpoint. Returns (output, meta)."""
    req = {"provider": provider, "endpoint": endpoint, "input": inp}
    return _do("run", req, "/v1/runs", label, mode, timeout, price_usd)


def market_data(action, label="", mode="live", timeout=300, **kw):
    """Glasser market_data Solution (RentCast / SerpApi / Google Finance): property_value, property_rent, property_search,
    listings_sale, listings_rental, market_stats (zip), stock_quote (symbol)."""
    req = {"action": action, **kw}
    return _do("market_data", req, "/v1/solutions/gtm/market_data", label, mode, timeout, None)


def _do(kind, req, path, label, mode, timeout, price_usd):
    k = hashlib.sha256(json.dumps([kind, req], sort_keys=True).encode()).hexdigest()
    if mode in ("replay", "cassette_only"):
        hit = _replay(kind, req)
        if hit:
            return hit["output"], {"cached": True, "usd": 0.0, "label": label, "status": hit.get("status")}
        if mode == "cassette_only":
            return None, {"error": "cassette miss", "label": label}
    if price_usd is not None and price_usd > MAX_RUN_USD:
        return None, {"error": f"price {price_usd} above cap {MAX_RUN_USD}", "label": label}
    if _spent["usd"] >= MAX_SESSION_USD:
        return None, {"error": "session spend cap reached", "label": label}
    t0 = time.time()
    code, out = _curl("POST", path, req, idem=k[:32])
    code, out = _finish(code, out, timeout)
    usd = _charge(out)
    _spent["usd"] += usd
    ok = code in (200, 201) and isinstance(out, dict) and (out.get("status") in (None, "COMPLETED") and out.get("result_status") in (None, "success"))
    rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "k": k, "kind": kind, "req": req, "label": label, "http": code, "ok": ok,
           "status": (out or {}).get("status") or (out or {}).get("result_status"), "charge_usd": usd, "seconds": round(time.time() - t0, 2),
           "output": (out or {}).get("output", out)}
    _log(CASSETTE, rec)
    _log(CHARGES, {k2: rec[k2] for k2 in ("ts", "kind", "label", "http", "ok", "status", "charge_usd", "seconds")} | {"target": req.get("endpoint") or req.get("action")})
    meta = {"cached": False, "usd": usd, "label": label, "http": code, "ok": ok, "status": rec["status"], "seconds": rec["seconds"],
            "failure": (out or {}).get("failure") or (out or {}).get("error")}
    return (out or {}).get("output", out), meta


if __name__ == "__main__":
    c, b = balance()
    print("balance", c, {k: v for k, v in (b or {}).items() if k not in ("client",)})
