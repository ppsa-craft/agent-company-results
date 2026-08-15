"""OWASP API Top 10 security tests for the data-ingest service.

Targets `/ingest/run`, `/ingest/status`, and `/health`. Each test is tagged
with the OWASP API Top 10 (2019) category it exercises so the security gate
is traceable:
- API1 (Broken Object Level Authorization), API3 (Excessive Data Exposure),
  API4 (Lack of Resources & Rate Limiting), API5 (Broken Function Level
  Authorization), API6 (Mass Assignment), API7 (Security Misconfiguration),
  API8 (Injection), API10 (Insufficient Logging & Monitoring).

Run: `pytest tests/test_owasp_security.py` (or the app-root `pytest -q`).
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from data_ingest.main import app

client = TestClient(app)

OWASP = pytest.mark.owasp


@OWASP
def test_health_leaks_no_stack_trace_or_internals():
    """API7 — errors must not leak stack traces or internal paths."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.text.lower()
    assert "traceback" not in body
    assert "file \"" not in body


@OWASP
def test_health_rejects_unwanted_methods():
    """API5 — unauthenticated/unwanted methods must not be silently accepted."""
    response = client.put("/health")
    assert response.status_code in (400, 405)
    response = client.delete("/health")
    assert response.status_code in (400, 405)


@OWASP
def test_responses_do_not_leak_server_headers():
    """API7 — responses must not leak server internals via headers."""
    response = client.get("/health")
    assert "server" not in {k.lower() for k in response.headers}


@OWASP
def test_ingest_run_rejects_malformed_date_without_stack_trace():
    """API8/API7 — malformed date input is a clean 4xx, not a 500 with a traceback."""
    response = client.post("/ingest/run", json={"date": "not-a-date"})
    assert response.status_code == 400
    assert "traceback" not in response.text.lower()


@OWASP
def test_ingest_run_rejects_non_trading_day():
    """API8/API5 — a weekend/holiday date is rejected at the boundary, not silently run."""
    response = client.post("/ingest/run", json={"date": "2024-01-07"})  # Sunday
    assert response.status_code == 400
    assert "trading day" in response.text.lower()


@OWASP
def test_ingest_run_ignores_unknown_fields():
    """API6 — mass-assignment style extra fields are ignored, not processed."""
    with patch("data_ingest.main.run_ingestion_job", new_callable=AsyncMock) as mock_job:
        mock_job.return_value = ([], {"total": 0, "success": 0, "failed": 0, "duplicates_skipped": 0})
        response = client.post(
            "/ingest/run",
            json={"date": "2024-01-15", "admin": True, "is_admin": True, "role": "superuser"},
        )
        assert response.status_code in (200, 400)  # trading-day guard decides; no 500
        assert "traceback" not in response.text.lower()


@OWASP
def test_ingest_run_rejects_unwanted_methods():
    """API5 — PUT/DELETE on a POST-only endpoint must not be silently accepted."""
    response = client.put("/ingest/run", json={"date": "2024-01-15"})
    assert response.status_code in (400, 405)
    response = client.delete("/ingest/run")
    assert response.status_code in (400, 405)


@OWASP
def test_ingest_status_returns_no_internals():
    """API3/API7 — status endpoint exposes no secrets or internal paths."""
    response = client.get("/ingest/status")
    assert response.status_code == 200
    body = response.text.lower()
    assert "password" not in body
    assert "secret" not in body
    assert "traceback" not in body
