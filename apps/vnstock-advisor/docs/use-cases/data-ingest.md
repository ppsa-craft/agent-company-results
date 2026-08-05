# Use Cases: Data Ingest Service

**Product:** vnstock-advisor  
**Component:** data-ingest  
**Version:** 1.0  
**Status:** Approved — PM signed off 2026-08-01  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Overview

The `data-ingest` service is responsible for fetching market data (OHLCV) from free Vietnamese stock market sources (CAFEF, VNDIRECT, Vietstock) and persisting it into the canonical `market_data` table. It supports scheduled runs, manual triggers, health monitoring, and idempotent upserts.

---

## Actors

| Actor | Description |
|-------|-------------|
| **Scheduler** | External cron/Orchestrator (e.g., GitHub Actions, Airflow, cron) that triggers scheduled ingest |
| **API Consumer** | Internal service or admin user calling the manual trigger endpoint |
| **Monitoring System** | Prometheus/Grafana or health-check endpoint consumer |
| **Data Analyst** | Downstream consumer of `market_data` table (read-only) |

---

## UC-DI-1: Scheduled Ingest from Free VN Source

### Description
Automated daily ingestion of end-of-day OHLCV data for all listed symbols from the primary free source (CAFEF), with fallback to VNDIRECT then Vietstock.

### Preconditions
- Scheduler has network access to the selected source API
- Database is reachable and `market_data` table exists
- Source is within rate limits

### Postconditions
- All active symbols have a row in `market_data` for the trading date
- `ingested_at` timestamp recorded
- `source` column reflects actual source used (primary or fallback)
- Metrics emitted: `ingest_duration_ms`, `symbols_processed`, `symbols_failed`, `fallback_used`

### Main Flow
1. Scheduler calls `POST /ingest/scheduled` (or CLI equivalent)
2. Service determines trading date (latest completed session)
3. For each symbol in the active symbol list:
   a. Fetch OHLCV from primary source (CAFEF)
   b. If primary fails (timeout, 4xx/5xx, schema mismatch), try VNDIRECT
   c. If VNDIRECT fails, try Vietstock
   d. On success: upsert into `market_data` (see UC-DI-4)
   e. On all sources failed: log error, increment `symbols_failed`, continue
4. Emit completion metrics
5. Return summary: `{ date, symbols_processed, symbols_failed, sources_used, duration_ms }`

### Alternate Flows
- **Partial outage:** If primary source is down for all symbols, service logs warning, switches to fallback for entire batch, sets `fallback_used=true` in metrics
- **Rate limit hit:** Service backs off with exponential backoff (max 3 retries), then fails symbol

### Acceptance Criteria
- AC-DI-1.1: Completes within 10 minutes for full symbol universe (~500 symbols)
- AC-DI-1.2: Zero duplicate rows for same `(symbol, timestamp)` after re-run
- AC-DI-1.3: Fallback chain executes automatically without manual intervention
- AC-DI-1.4: Metrics exposed at `/metrics` (Prometheus format)

---

## UC-DI-2: Manual Trigger via API

### Description
On-demand ingestion for a specific date or symbol range, invoked by API consumer (e.g., backfill, correction, ad-hoc analysis).

### Preconditions
- API consumer authenticated (internal service token or admin session)
- Request payload validates: `date` (optional, defaults to latest), `symbols` (optional, defaults to all), `source` (optional, defaults to primary)

### Postconditions
- Requested data ingested per same upsert logic as UC-DI-1
- Response includes per-symbol status

### Main Flow
1. Consumer calls `POST /ingest/manual` with JSON body:
   ```json
   { "date": "2026-07-30", "symbols": ["VNM", "VCB"], "source": "CAFEF" }
   ```
2. Service validates payload (date not future, symbols exist in reference list)
3. Executes ingest for requested symbols/date using specified or default source
4. Returns:
   ```json
   {
     "request_id": "uuid",
     "date": "2026-07-30",
     "results": [
       { "symbol": "VNM", "status": "success", "source": "CAFEF", "rows_upserted": 1 },
       { "symbol": "VCB", "status": "failed", "error": "source_timeout" }
     ],
     "summary": { "total": 2, "success": 1, "failed": 1 }
   }
   ```

### Alternate Flows
- **Invalid date:** Returns 400 with error `date_in_future` or `date_not_trading_day`
- **Unknown symbols:** Returns 400 with list of unknown symbols
- **Source override:** If `source` specified, bypasses fallback chain; fails fast if that source fails

### Acceptance Criteria
- AC-DI-2.1: Returns 202 Accepted with request_id for async processing (if >50 symbols)
- AC-DI-2.2: Returns 200 OK with inline results for ≤50 symbols
- AC-DI-2.3: Input validation rejects future dates and unknown symbols
- AC-DI-2.4: Authentication required (401 if missing/invalid)

---

## UC-DI-3: Health/Monitoring Endpoint

### Description
Exposes service health, last run status, and data freshness for monitoring systems.

### Preconditions
- Service is running

### Postconditions
- Response includes liveness, readiness, and data freshness indicators

### Main Flow
1. Monitor calls `GET /health`
2. Service returns:
   ```json
   {
     "status": "healthy",
     "checks": {
       "database": "ok",
       "primary_source": "ok",
       "fallback_sources": ["VNDIRECT: ok", "Vietstock: ok"]
     },
     "last_scheduled_run": {
       "date": "2026-07-30",
       "started_at": "2026-07-31T06:00:00Z",
       "completed_at": "2026-07-31T06:04:12Z",
       "symbols_processed": 498,
       "symbols_failed": 2,
       "fallback_used": false
     },
     "data_freshness": {
       "latest_date": "2026-07-30",
       "symbols_with_latest": 498,
       "stale_symbols": ["ABC", "XYZ"]
     }
   }
   ```

### Acceptance Criteria
- AC-DI-3.1: Returns 200 within 500ms (no external calls in health check)
- AC-DI-3.2: `database` check verifies connectivity only (no query)
- AC-DI-3.3: `data_freshness.stale_symbols` lists symbols missing latest trading date
- AC-DI-3.4: Kubernetes liveness/readiness probes can use this endpoint

---

## UC-DI-4: Idempotent Upsert (Re-runs Don't Duplicate)

### Description
Ensures that re-ingesting the same symbol/date combination updates the existing row rather than creating a duplicate.

### Preconditions
- `market_data` table has unique constraint on `(symbol, timestamp)`
- Ingest payload contains `symbol`, `timestamp`, `open`, `high`, `low`, `close`, `volume`, `source`

### Postconditions
- Exactly one row exists for each `(symbol, timestamp)` after any number of ingest runs
- `ingested_at` updated to latest run time
- `source` reflects the source of the latest successful ingest

### Main Flow
1. Service prepares batch of records for upsert
2. Executes single PostgreSQL `INSERT ... ON CONFLICT (symbol, timestamp) DO UPDATE SET ...`
3. Updates `open`, `high`, `low`, `close`, `volume`, `source`, `ingested_at = NOW()`
4. Returns count of rows inserted vs updated

### Acceptance Criteria
- AC-DI-4.1: Unique constraint exists on `(symbol, timestamp)`
- AC-DI-4.2: Re-running same ingest twice produces 1 row, not 2
- AC-DI-4.3: `ingested_at` reflects most recent run
- AC-DI-4.4: `source` reflects most recent successful source
- AC-DI-4.5: Batch upsert completes in <2s for 500 symbols

---

## Traceability Matrix

| Use Case | AC IDs | Feeds Task |
|----------|--------|------------|
| UC-DI-1 | AC-DI-1.1–1.4 | `vnstock-advisor-3-dev-data-ingest` (scheduler, fallback logic) |
| UC-DI-2 | AC-DI-2.1–2.4 | `vnstock-advisor-3-dev-data-ingest` (API endpoint) |
| UC-DI-3 | AC-DI-3.1–3.4 | `vnstock-advisor-3-dev-data-ingest` (health endpoint) |
| UC-DI-4 | AC-DI-4.1–4.5 | `vnstock-advisor-3-dev-data-ingest` (DDL + upsert logic) |

---

## Open Questions

1. **Trading calendar:** Should the service maintain its own trading day calendar, or rely on source data presence? (Affects UC-DI-1 date determination)
2. **Symbol universe:** Where does the active symbol list come from? (Reference data service? Static file? CAFEF listing?)
3. **Rate limits:** What are the exact rate limits for each free source? (Affects batch sizing in UC-DI-1)

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*