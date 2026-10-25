"""Direct Gemini API transport. Exact model selection; no paid POST retries."""
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from dotenv import load_dotenv

from .client import APIError, NoRedirect

DEFAULT_MODEL = "gemini-4-argon"


class Gemini:
    def __init__(self, env_file=".env", model=DEFAULT_MODEL):
        load_dotenv(env_file, override=False)
        self.key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.key:
            raise APIError("Set GEMINI_API_KEY (or GOOGLE_API_KEY) locally.")
        self.model = model.removeprefix("models/")
        if not re.fullmatch(r"[a-zA-Z0-9._-]+", self.model):
            raise ValueError("Invalid Gemini model ID.")
        self.opener = build_opener(NoRedirect())

    def request(self, method, path, body=None, timeout=900):
        headers = {"x-goog-api-key": self.key, "Accept": "application/json"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body, ensure_ascii=False).encode()
        request = Request("https://generativelanguage.googleapis.com/v1beta/" + path, data=data, headers=headers, method=method)
        try:
            with self.opener.open(request, timeout=timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            try:
                status = json.loads(exc.read()).get("error", {}).get("status", "request_failed")
            except (ValueError, AttributeError):
                status = "request_failed"
            raise APIError(f"Gemini HTTP {exc.code}: {status}. No model fallback or generation retry performed.") from None
        except (URLError, TimeoutError, ConnectionError):
            raise APIError("Gemini transport failure. Generation may have been charged; automatic retry is disabled.") from None

    def info(self):
        return self.request("GET", "models/" + self.model, timeout=60)

    def list_models(self):
        models, token = [], None
        while True:
            params = {"pageSize": 1000}
            if token:
                params["pageToken"] = token
            page = self.request("GET", "models?" + urlencode(params), timeout=60)
            models.extend(page.get("models", []))
            token = page.get("nextPageToken")
            if not token:
                return {"models": models}

    def count_tokens(self, payload):
        request = dict(payload, model="models/" + self.model)
        return self.request("POST", "models/" + self.model + ":countTokens", {"generateContentRequest": request}, timeout=120)

    def generate(self, payload):
        return self.request("POST", "models/" + self.model + ":generateContent", payload)


def response_text(response):
    candidates = response.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini returned no candidate (possibly blocked); raw response retained.")
    candidate = candidates[0]
    if candidate.get("finishReason") != "STOP":
        raise ValueError(f"Incomplete Gemini response: {candidate.get('finishReason', 'unknown')}; raw response retained.")
    return "".join(part.get("text", "") for part in candidate.get("content", {}).get("parts", []) if not part.get("thought"))
