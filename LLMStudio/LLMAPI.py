import os

import requests

DEFAULT_BASE_URL = "http://localhost:1234/v1/"
DEFAULT_TIMEOUT = 60


class LMStudioError(Exception):
    """Raised when the LM Studio server cannot be reached or returns an error."""


class LMStudioAPIWrapper:
    def __init__(self, base_url=None, timeout=DEFAULT_TIMEOUT):
        base_url = base_url or os.environ.get("LMSTUDIO_BASE_URL", DEFAULT_BASE_URL)
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise LMStudioError(
                f"Could not connect to LM Studio at {self.base_url}. "
                "Start the local server in LM Studio (Developer tab) and load a model, "
                "or set LMSTUDIO_BASE_URL."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise LMStudioError(
                f"LM Studio at {self.base_url} did not answer within {self.timeout}s."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            raise LMStudioError(f"LM Studio returned an error for {url}: {exc}") from exc
        return response.json()

    def get_models(self):
        return self._request("GET", "models")

    def post_chat_completions(self, data):
        return self._request("POST", "chat/completions", json=data)

    def post_completions(self, data):
        return self._request("POST", "completions", json=data)
