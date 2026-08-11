# vnstock-analysis-engine

Technical analysis engine for **vnstock-advisor**: computes indicators (SMA/EMA/RSI/MACD/VWAP/ATR/OBV/ROC) from OHLCV market data and exposes them over a small FastAPI surface.

> **Disclaimer:** informational only — not financial advice. See
> `docs/compliance/disclaimer.md`.

## Requirements

- Python 3.11+
- pip (with git + build support)

## Setup

From this service directory (`services/analysis-engine/`):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
```

The `vnstock-shared-python` dependency is installed as a local path package
(`file:../../shared/python`) — no network registry entry needed.

## Run the service

```bash
uvicorn analysis_engine.main:app --host 0.0.0.0 --port 8002
```

(equivalently `python -m uvicorn analysis_engine.main:app --host 0.0.0.0 --port 8002`).
The app module lives in `src/analysis_engine/`; uvicorn picks it up from the
console-script entry when running inside the activated venv. Health check:

```bash
curl http://localhost:8002/health
```

## Run the tests

From the **app root** (`apps/vnstock-advisor/`) — this is what CI runs
(`pytest -q` at app root, collecting `services/analysis-engine/tests`):

```bash
pytest services/analysis-engine/tests -q
```

Or from this directory:

```bash
pytest tests -q
```

A root-level `conftest.py` at `apps/vnstock-advisor/` supplies
dev/test-only JWT placeholder keys so the suite collects and runs in a clean
checkout with no `.env` (production deployments must inject real keys via
environment variables).

## API surface

| Method | Path | Description |
|---|---|---|
| GET | `/health` | liveness + service info |
| GET | `/` | service banner |
| POST | `/analyze` | compute indicators for a `MarketDataCreate` payload |
| POST | `/indicators/compute` | compute indicators for an OHLCV payload |
| POST | `/rank` | rank symbols from computed indicator series |

## Security gate

This service clears the DoD Tier 2 security gate — gitleaks secret-scan clean,
semgrep SAST clean (no high/critical), Snyk SCA clean (no exploitable
vulnerabilities), OWASP API Top 10 checks for the exposed endpoints.

Run the security checks locally (from the **app root** `apps/vnstock-advisor/`):

```bash
# Secret scan — fail on ANY secret-like finding (empty allowlist)
gitleaks detect --source . --config .gitleaks.toml

# SAST — fail on high-severity (ERROR) findings
semgrep scan --config .semgrep.yml services/analysis-engine/src

# SCA — fail on CVSS >= 7.0 known-exploitable vulnerabilities
snyk test --file=requirements.txt --severity-threshold=high

# OWASP API Top 10 endpoint tests (also runs in the main suite)
pytest services/analysis-engine/tests/test_owasp_security.py -q
```

Gate configuration lives at the app root: `.gitleaks.toml`, `.semgrep.yml`,
`.snyk`. The four checks are wired as mandatory gates in the orchestrator-owned
CI workflow; scan evidence is recorded in `SECURITY_GATE_RESULTS.md`.

## Project layout

```
src/analysis_engine/
  main.py          FastAPI app + /analyze + /rank endpoints
  indicators.py    indicator computation (compute_all_indicators)
  schemas.py       frozen-contract Pydantic request/response models
tests/
  test_main.py     endpoint + payload tests
  test_indicators.py
  fixtures/        JSON OHLCV fixtures (normal/insufficient/low-volume/...)
```
