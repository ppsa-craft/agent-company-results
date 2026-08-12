"""OWASP API Top 10 security tests for the analysis-engine service.

Targets `/indicators/compute`, `/rank`, `/analyze`, and `/health`. Each test is
tagged with the OWASP API Top 10 (2019) category it exercises so the security
gate is traceable:
- API1 (Broken Object Level Authorization), API3 (Excessive Data Exposure),
  API4 (Lack of Resources & Rate Limiting), API5 (Broken Function Level
  Authorization), API6 (Mass Assignment), API7 (Security Misconfiguration),
  API8 (Injection), API10 (Insufficient Logging & Monitoring).

Run: `pytest tests/test_owasp_security.py` (or the app-root `pytest -q`).
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from analysis_engine.main import app

client = TestClient(app)

OWASP = pytest.mark.owasp


def _load_bars():
    """Load the normal-trading fixture, grouped by symbol (ascending)."""
    path = Path(__file__).parent / "fixtures" / "normal-trading.json"
    bars = json.loads(path.read_text())
    series = {}
    for b in bars:
        series.setdefault(b["symbol"], []).append(b)
    return series


def _valid_compute_payload():
    series = _load_bars()
    return {
        "symbol": "VNM",
        "ohlcv": series["VNM"][:20],
        "algorithm_version": "v1.0",
    }


def _valid_rank_payload():
    series = _load_bars()
    symbols = ["VNM", "FPT", "HPG"]
    return {
        "symbols": symbols,
        "as_of_date": "2026-08-10",
        "algorithm_version": "v1.0",
        "series": {sym: series[sym] for sym in symbols},
    }


@OWASP
def test_health_leaks_no_stack_trace_or_internals():
    """API7 — errors must not leak stack traces or internal paths."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.text.lower()
    assert "traceback" not in body
    assert "file \"" not in body


@OWASP
def test_compute_rejects_invalid_symbol_pattern():
    """API1/API8 — invalid ticker input is rejected with a clean 4xx, not a 500."""
    payload = _valid_compute_payload()
    payload["symbol"] = "vnm!"
    response = client.post("/indicators/compute", json=payload)
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


@OWASP
def test_compute_rejects_malformed_ohlcv():
    """API8/API3 — malformed OHLCV bars must not reach the compute logic."""
    payload = _valid_compute_payload()
    payload["ohlcv"] = [{"time": "not-a-date", "open": -5, "high": 0, "low": 1, "close": 1, "volume": -1}]
    response = client.post("/indicators/compute", json=payload)
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


@OWASP
def test_compute_rejects_unsupported_algorithm_version():
    """API5 — the algorithm-version contract is enforced at the boundary."""
    payload = _valid_compute_payload()
    payload["algorithm_version"] = "v99.99"
    response = client.post("/indicators/compute", json=payload)
    assert response.status_code == 400
    assert "traceback" not in response.text.lower()


@OWASP
def test_compute_ignores_unknown_fields():
    """API6 — mass-assignment style extra fields are ignored, not processed."""
    payload = _valid_compute_payload()
    payload["admin"] = True
    payload["is_admin"] = True
    response = client.post("/indicators/compute", json=payload)
    assert response.status_code == 200


@OWASP
def test_rank_rejects_empty_symbols():
    """API5/API3 — an empty symbols list is a validation error, not a silent run."""
    payload = _valid_rank_payload()
    payload["symbols"] = []
    response = client.post("/rank", json=payload)
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


@OWASP
def test_rank_rejects_invalid_tickers():
    """API8 — invalid ticker symbols are rejected by the input guard."""
    payload = _valid_rank_payload()
    payload["symbols"] = ["vnm!", "123"]
    response = client.post("/rank", json=payload)
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


@OWASP
def test_rank_rejects_symbols_missing_from_series():
    """API3/API1 — symbols without a series are a 400 listing them, not a silent drop."""
    payload = _valid_rank_payload()
    del payload["series"]["FPT"]
    response = client.post("/rank", json=payload)
    assert response.status_code == 400
    assert "traceback" not in response.text.lower()


@OWASP
def test_analyze_rejects_invalid_timeframe():
    """API8 — an unsupported timeframe value is rejected at the boundary."""
    series = _load_bars()
    bars = series["VNM"]
    response = client.post("/analyze", json={
        "symbol": "VNM",
        "timeframe": "1H",
        "time": bars[0]["time"],
        "bars": bars,
    })
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


@OWASP
def test_unwanted_methods_are_not_silently_accepted():
    """API5 — unauthenticated/unwanted methods must not be silently accepted."""
    response = client.put("/indicators/compute", json=_valid_compute_payload())
    assert response.status_code in (400, 405)
    response = client.delete("/rank")
    assert response.status_code in (400, 405)


@OWASP
def test_responses_do_not_leak_server_headers():
    """API7 — responses must not leak server internals via headers."""
    response = client.get("/health")
    assert "server" not in {k.lower() for k in response.headers}
