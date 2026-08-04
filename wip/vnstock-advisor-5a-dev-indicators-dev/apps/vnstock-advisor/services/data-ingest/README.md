# vnstock-advisor Data Ingest Service

Market data ingestion service for Vietnamese equities. Fetches OHLCV data from free sources (CAFEF primary, VNDIRECT fallback), persists to PostgreSQL with idempotent upserts, exposes health and manual trigger endpoints.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (running locally or via Docker)
- `uv` (recommended) or `pip`

### Environment Variables

Create a `.env` file in the repo root (`apps/vnstock-advisor/`):

```bash
# Database (required)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/vnstock

# Ingestion symbols (comma-separated, required)
INGEST_SYMBOLS=VNM,VCB,FPT,HPG,MWG

# Service port (optional, default: 8001)
DATA_INGEST_PORT=8001

# Optional: CAFEF/VNDIRECT API timeouts
INGEST_TIMEOUT_SECONDS=30
```

### Install Dependencies

```bash
# From repo root (apps/vnstock-advisor/)
uv sync --all-extras
# or
pip install -e services/data-ingest/
```

### Initialize Database

```bash
# From repo root
psql $DATABASE_URL -f scripts/init-db.sql
```

### Run Service (Development)

```bash
# From repo root
uvicorn services.data_ingest.src.main:app --reload --port 8001
```

Service available at `http://localhost:8001`

### Run Tests

```bash
# From repo root
pytest services/data-ingest/tests/ -v
```

### Run with Docker Compose (Recommended)

```bash
# From repo root
docker-compose up -d data-ingest
```

This starts PostgreSQL, Redis, and the data-ingest service together.

## API Endpoints

### `GET /health`
Health check for monitoring/liveness probes.

**Response:**
```json
{
  "status": "healthy",
  "service": "data-ingest",
  "version": "0.1.0",
  "timestamp": "2026-08-01T08:00:00Z",
  "checks": {
    "database": "ok",
    "primary_source": "ok",
    "fallback_sources": ["VNDIRECT: ok", "Vietstock: ok"]
  }
}
```

### `POST /ingest/run`
Trigger manual ingestion for all configured symbols (today's trading day).

**Response:**
```json
{
  "request_id": "manual-ingest-a1b2c3d4",
  "date": "2026-08-01",
  "results": [
    {
      "symbol": "VNM",
      "status": "success",
      "source": "CAFEF",
      "rows_upserted": 1,
      "error": null,
      "duplicate_skipped": false
    }
  ],
  "summary": {
    "total": 5,
    "success": 4,
    "failed": 1,
    "duplicates_skipped": 0
  },
  "meta": {
    "generated_at": "2026-08-01T08:00:00Z",
    "source": "data-ingest-v0.1.0",
    "disclaimer": {
      "vi-VN": "⚠️ Thông tin chỉ mang tính chất tham khảo...",
      "en-US": "⚠️ Information for reference only..."
    }
  }
}
```

### `GET /`
Service info.

**Response:**
```json
{"message": "vnstock Data Ingest Service"}
```

## Architecture

```
services/data-ingest/
├── src/
│   ├── main.py              # FastAPI app, endpoints
│   ├── ingest_service.py    # Core ingestion logic
│   ├── models.py            # SQLAlchemy models, OHLCV DTOs
│   └── disclaimer.py        # Disclaimer framework (VN/EN)
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── pyproject.toml           # Dependencies
└── README.md                # This file
```

**Key Components:**
- **`ingest_service.py`**: `run_ingestion_job()` orchestrates fetch → upsert per symbol
- **CAFEF primary** → **VNDIRECT fallback** with retry logic (3 attempts, exponential backoff)
- **Idempotent upsert**: `INSERT ... ON CONFLICT (symbol, timestamp) DO UPDATE`
- **Trading day calendar**: Vietnam holidays + weekends excluded
- **Disclaimer**: Every response includes `meta.disclaimer` (VN/EN) per compliance spec

## Data Sources

| Source | Role | Endpoint | Rate Limit |
|--------|------|----------|------------|
| CAFEF | Primary | `https://www.cafef.vn/giaodich.jsp` | ~60 req/min |
| VNDIRECT | Fallback | `https://services.vndirect.com.vn/price-history` | ~100 req/min |

See `docs/research/data-sources.md` for details.

## Security

This service clears the DoD Tier 2 security gate:
- ✅ **Gitleaks**: Secret-scan clean (no hardcoded secrets)
- ✅ **Semgrep**: SAST clean (no high/critical findings)
- ✅ **Snyk/pip-audit**: SCA clean (no exploitable vulnerabilities)
- ✅ **OWASP API Top 10**: Input validation (Pydantic), rate limiting (via API gateway), no stack traces in errors

Run security checks locally:
```bash
# Secret scan
gitleaks detect --source services/data-ingest/

# SAST
semgrep --config=auto services/data-ingest/

# SCA
cd services/data-ingest && pip-audit
```

## Compliance

Every API response includes the mandatory disclaimer per `docs/compliance/disclaimer.md`:
- Vietnamese (authoritative) + English
- Full variant in API responses
- Non-dismissible, rendered in JSON (not client-side only)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: vnstock_shared` | Run `uv sync --all-extras` from repo root |
| DB connection failed | Check `DATABASE_URL`, ensure PostgreSQL running, run `init-db.sql` |
| CAFEF returns 403/500 | Service auto-falls back to VNDIRECT; check logs |
| Port 8001 in use | Set `DATA_INGEST_PORT` env var |
| Tests fail with DB errors | Tests mock DB; ensure no real DB needed for unit tests |

## License

Part of vnstock-advisor — see root `LICENSE`.