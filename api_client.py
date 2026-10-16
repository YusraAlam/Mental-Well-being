"""Thin client for the FastAPI backend. No Streamlit imports, so it is easy to test."""
from __future__ import annotations

import math

import requests

from config import REQUEST_TIMEOUT


class ApiError(Exception):
    """A failure the UI can explain to the user."""

    def __init__(self, kind: str, title: str, message: str, details: list[str] | None = None):
        super().__init__(message)
        self.kind = kind
        self.title = title
        self.message = message
        self.details = details or []


def _base(url: str) -> str:
    return (url or "").strip().rstrip("/")


def check_health(base_url: str, timeout: float = 2.0) -> bool:
    """True if the API answers. Tries /health first, then / (works with the original main.py)."""
    base = _base(base_url)
    for path in ("/health", "/"):
        try:
            response = requests.get(base + path, timeout=timeout)
        except requests.exceptions.RequestException:
            return False
        if response.ok:
            return True
    return False


def _validation_details(response: requests.Response) -> list[str]:
    try:
        detail = response.json().get("detail", [])
    except Exception:
        return []
    out = []
    if isinstance(detail, list):
        for item in detail:
            if isinstance(item, dict):
                loc = [str(p) for p in item.get("loc", []) if p != "body"]
                out.append(f"{'.'.join(loc) or 'request'}: {item.get('msg', 'invalid value')}")
    elif isinstance(detail, str):
        out.append(detail)
    return out


def predict(base_url: str, payload: dict, timeout: float = REQUEST_TIMEOUT) -> float:
    """POST /predict and return predicted_mental_health_score. Raises ApiError."""
    base = _base(base_url)
    try:
        response = requests.post(f"{base}/predict", json=payload, timeout=timeout)
    except (requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL):
        raise ApiError(
            "config", "The API address is not valid",
            "Enter a full address such as http://127.0.0.1:8000 under API settings.",
        )
    except requests.exceptions.Timeout:
        raise ApiError(
            "timeout", "The API took too long to answer",
            f"No response within {timeout:g} seconds. Check that the server is running and try again.",
        )
    except requests.exceptions.ConnectionError:
        raise ApiError(
            "connection", "Can't reach the API",
            f"Nothing is answering at {base}. Start the backend with: uvicorn main:app --reload",
        )
    except requests.exceptions.RequestException as exc:
        raise ApiError("network", "The request failed", str(exc))

    if response.status_code == 422:
        raise ApiError(
            "validation", "The API rejected these inputs",
            "Fix the values below and run the analysis again.",
            _validation_details(response),
        )
    if response.status_code >= 500:
        raise ApiError(
            "server", "The API hit an error",
            "The server failed while predicting. Check the uvicorn terminal for the traceback.",
            [response.text[:300]] if response.text else [],
        )
    if not response.ok:
        raise ApiError(
            "http", f"Unexpected response ({response.status_code})",
            "The API answered, but not with a prediction.",
            [response.text[:300]] if response.text else [],
        )

    try:
        score = response.json()["predicted_mental_health_score"]
        score = float(score)
    except (ValueError, KeyError, TypeError):
        raise ApiError(
            "bad_response", "The response was not in the expected format",
            "Expected JSON with a numeric predicted_mental_health_score field.",
            [response.text[:300]] if response.text else [],
        )
    if not math.isfinite(score):
        raise ApiError("bad_response", "The model returned an invalid number",
                       "The predicted score was not a finite value.")
    return score
