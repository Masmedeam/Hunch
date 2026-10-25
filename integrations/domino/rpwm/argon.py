"""Gemini 4 Argon client for RPWM: every model call goes through here.

- One model only: gemini-4-argon. Compute is varied with thinking_level (low / medium / high).
- Record/replay cache (runs/argon_cache.jsonl) keyed by a hash of the request: rehearsal runs make the stage
  demo work offline, and identical requests are never paid twice.
- Timeouts, retry with backoff, and an `argon_call` event for every call (purpose, level, seconds, tokens).
"""
import base64
import concurrent.futures as cf
import hashlib
import json
import os
import re
import threading
import time

MODEL = "gemini-4-argon"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(ROOT, "runs", "argon_cache.jsonl")
LEDGER_PATH = os.path.join(ROOT, "runs", "argon_ledger.jsonl")
# Team rule (2026-10-25): never economize on Argon. Every call runs at the most performant settings available:
# thinking_level high and the Priority inference tier. Override only for experiments: RPWM_MIN_LEVEL / RPWM_SERVICE_TIER.
LEVELS = ("low", "medium", "high")
MIN_LEVEL = os.environ.get("RPWM_MIN_LEVEL", "high")
SERVICE_TIER = os.environ.get("RPWM_SERVICE_TIER", "priority")


def max_level(level):
    if level not in LEVELS:
        return level
    return LEVELS[max(LEVELS.index(level), LEVELS.index(MIN_LEVEL) if MIN_LEVEL in LEVELS else 0)]
_pool = cf.ThreadPoolExecutor(max_workers=16)
_lock = threading.Lock()


def _load_env():
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            m = re.match(r'\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$', line)
            if m and m.group(1) not in os.environ:
                os.environ[m.group(1)] = m.group(2).strip().strip('"').strip("'")


class Argon:
    def __init__(self, mode="live", emit=None):
        """mode: 'live' (call API, record), 'replay' (cache first, API on miss), 'cache_only'."""
        _load_env()
        from google import genai
        self.client = genai.Client()
        self.mode = mode
        self.emit = emit or (lambda ev: None)
        self.cache = {}
        self.totals = {"calls": 0, "cached": 0, "seconds": 0.0, "input_tokens": 0, "output_tokens": 0, "thought_tokens": 0}
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        if os.path.exists(CACHE_PATH):
            for line in open(CACHE_PATH, encoding="utf-8"):
                try:
                    rec = json.loads(line)
                    self.cache[rec["key"]] = rec
                except (json.JSONDecodeError, KeyError):
                    continue

    @staticmethod
    def _key(level, parts, schema):
        h = hashlib.sha256()
        h.update(f"{MODEL}|{level}|".encode())
        for p in parts:
            h.update((p if isinstance(p, str) else json.dumps(p, sort_keys=True)).encode())
        h.update(json.dumps(schema, sort_keys=True).encode() if schema else b"-")
        return h.hexdigest()

    def call(self, purpose, prompt, level="low", schema=None, image_png=None, timeout=45.0, t=None, retries=2,
             use_cache=True, tools=None):
        """Returns (parsed_json_or_text, meta). parsed is None on failure (caller falls back)."""
        parts = [prompt] + ([hashlib.sha256(image_png).hexdigest()] if image_png else [])
        key = self._key(max_level(level) + "|" + (SERVICE_TIER or "standard") + ("|tools=" + json.dumps(tools, sort_keys=True) if tools else ""), parts, schema)
        if use_cache and self.mode in ("replay", "cache_only") and key in self.cache:
            rec = self.cache[key]
            meta = {**rec["meta"], "cached": True, "seconds": 0.0}
            self._account(purpose, level, meta, t)
            return rec["value"], meta
        if self.mode == "cache_only":
            return None, {"error": "cache miss", "cached": False}

        level = max_level(level)  # team rule: most performant option (thinking high) unless RPWM_MIN_LEVEL lowers it
        inp = prompt
        if image_png is not None:
            inp = [{"type": "text", "text": prompt},
                   {"type": "image", "data": base64.b64encode(image_png).decode("utf-8"), "mime_type": "image/png"}]
        kwargs = {"model": MODEL, "input": inp, "generation_config": {"thinking_level": level}}
        if SERVICE_TIER:
            kwargs["service_tier"] = SERVICE_TIER  # Priority inference: fastest, non-sheddable; overflow downgrades to standard
        if schema is not None:
            kwargs["response_format"] = {"type": "text", "mime_type": "application/json", "schema": schema}
        if tools:
            kwargs["tools"] = tools  # e.g. [{"type": "google_search"}] for grounded research

        last_err = None
        for attempt in range(retries + 1):
            t0 = time.time()
            fut = _pool.submit(self.client.interactions.create, **kwargs)
            try:
                it = fut.result(timeout=timeout)
                text = it.output_text or ""
                value = json.loads(text) if schema is not None else text
                u = it.usage
                meta = {"seconds": round(time.time() - t0, 2), "input_tokens": u.total_input_tokens or 0,
                        "output_tokens": u.total_output_tokens or 0, "thought_tokens": u.total_thought_tokens or 0,
                        "cached": False}
                with _lock:
                    self.cache[key] = {"key": key, "purpose": purpose, "level": level, "value": value, "meta": meta}
                    with open(CACHE_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps(self.cache[key]) + "\n")
                self._account(purpose, level, meta, t)
                return value, meta
            except cf.TimeoutError:
                last_err = f"timeout after {timeout}s"
            except json.JSONDecodeError as exc:
                last_err = f"bad JSON: {exc}"
            except Exception as exc:  # API errors: retry with backoff on rate limits and server errors
                last_err = f"{type(exc).__name__}: {str(exc)[:160]}"
                if "429" in last_err or "503" in last_err or "500" in last_err:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                break
        meta = {"error": last_err, "cached": False, "seconds": timeout}
        self.emit({"type": "log", "t": t, "level": "warn", "text": f"Argon {purpose} failed: {last_err}"})
        return None, meta

    def _account(self, purpose, level, meta, t):
        with _lock:
            self.totals["calls"] += 1
            self.totals["cached"] += int(bool(meta.get("cached")))
            for k in ("seconds", "input_tokens", "output_tokens", "thought_tokens"):
                self.totals[k] += meta.get(k, 0) or 0
            with open(LEDGER_PATH, "a", encoding="utf-8") as f:  # every call, live or cached: docs/ARGON_USAGE.md
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "model": MODEL, "purpose": purpose,
                                    "thinking_level": max_level(level), "service_tier": SERVICE_TIER or "standard",
                                    "cached": bool(meta.get("cached")),
                                    **{k: meta.get(k, 0) or 0 for k in ("seconds", "input_tokens", "output_tokens", "thought_tokens")},
                                    "app": os.environ.get("RPWM_APP", "rpwm")}) + "\n")
        self.emit({"type": "argon_call", "t": t, "purpose": purpose, "thinking_level": level,
                   "seconds": meta.get("seconds", 0), "input_tokens": meta.get("input_tokens", 0),
                   "output_tokens": meta.get("output_tokens", 0), "thought_tokens": meta.get("thought_tokens", 0),
                   "cached": bool(meta.get("cached"))})
