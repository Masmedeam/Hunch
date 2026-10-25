"""Glasser HTTP transport. Never log credentials or entire request headers."""
import json
import os
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from dotenv import load_dotenv


class APIError(RuntimeError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise APIError("API redirect refused to prevent credential forwarding.")


class Glasser:
    def __init__(self, env_file=".env"):
        load_dotenv(env_file, override=False)
        self.key = os.getenv("GLASSER_API_KEY")
        if not self.key:
            raise APIError("Set GLASSER_API_KEY in .env or the environment.")
        self.base = os.getenv("GLASSER_API_BASE_URL", "https://api.glasser.ai").rstrip("/")
        if urlparse(self.base).scheme != "https":
            raise APIError("API base URL must use HTTPS.")
        self.opener = build_opener(NoRedirect())

    def request(self, method, path, body=None, key=None, timeout=180):
        if not path.startswith(("/v1/", "/public/")):
            raise APIError("Refusing an unexpected API path.")
        headers = {"Accept": "application/json", "User-Agent": "nextday-data/0.1"}
        if not path.startswith("/public/"):
            headers["Authorization"] = f"Bearer {self.key}"
        if key:
            headers["Idempotency-Key"] = key
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode()
        # One transport/rate-limit retry. Paid POSTs must carry a persisted key.
        for attempt in range(2):
            try:
                with self.opener.open(Request(self.base + path, data=data, headers=headers, method=method), timeout=timeout) as response:
                    return json.load(response)
            except HTTPError as exc:
                try:
                    error = json.loads(exc.read()).get("error", {})
                except (ValueError, AttributeError):
                    error = {}
                if exc.code == 429 and attempt == 0:
                    delay = float(error.get("retry_after_ms") or 1000) / 1000
                    if delay > 120:
                        raise APIError("Rate limited with a long backoff; resume this batch later.") from None
                    time.sleep(max(0, delay))
                    continue
                # Don't echo arbitrary server bodies which may contain sensitive input.
                raise APIError(f"Glasser HTTP {exc.code}: {error.get('code', 'request_failed')}") from None
            except (URLError, TimeoutError, ConnectionError) as exc:
                if attempt == 0 and (method == "GET" or key):
                    continue
                raise APIError("Transport failure; retry the same batch to reuse its persisted idempotency key.") from None

    def catalog(self):
        return self.request("GET", "/public/catalog")

    def inspect(self, provider, endpoint):
        return self.request("POST", "/v1/endpoints/inspect", {"provider": provider, "endpoint": endpoint, "task_id": "nextday-ingestion"})


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temp.replace(path)
