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
uvicorn main:app --host 0.0.0.0 --port 8002
```

(equivalently `python -m uvicorn main:app --host 0.0.0.0 --port 8002`).
The app module lives in `src/`; uvicorn picks it up from the console-script
entry when running inside the activated venv. Health check:

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

## Project layout

```
src/
  main.py          FastAPI app + /analyze endpoint
  indicators.py    indicator computation (compute_all_indicators)
tests/
  test_main.py     endpoint + payload tests
  test_indicators.py
  fixtures/        JSON OHLCV fixtures (normal/insufficient/low-volume/...)
```
