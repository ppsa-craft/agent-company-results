# Task: vnstock-advisor-4-dev-data-ingest

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: data-ingest service)
**Status:** done (DEV-1)

---

## Goal

Implement the `data-ingest` service per BA docs: scheduled/manual ingest from CAFEF (primary) with VNDIRECT fallback, idempotent upsert to Postgres, health endpoint, canonical `market_data` schema.

---

## Acceptance Criteria (traceable to use cases)

- [x] UC-DI-1: Scheduled ingest job runs daily for configured symbols (trading days only) — `is_trading_day()` implemented in ingest_service.py, APScheduler cron at 06:00 ICT
- [x] UC-DI-2: Manual trigger via `POST /ingest/run` returns ingestion results — endpoint wired to real `run_ingestion_job`
- [x] UC-DI-3: `GET /health` returns service status + DB connectivity + source status — implemented with real DB and source checks
- [x] UC-DI-4: Idempotent upsert — re-runs don't duplicate (unique constraint handling) — implemented in `ingest_data_for_date` with duplicate detection
- [x] Canonical `market_data` table created per `docs/schema/market-data.md` DDL — done via init-db.sql
- [x] Primary source CAFEF with VNDIRECT fallback implemented per `docs/research/data-sources.md` — fetch logic implemented in ingest_service.py with retry
- [x] Disclaimer framework integrated per `docs/compliance/disclaimer.md` — every ingest response includes disclaimer in summary.meta
- [x] Tests pass (unit + integration), README works verbatim — pytest passes, README verified
- [x] Security gate (DoD Tier 2): gitleaks secret-scan clean, semgrep SAST clean (high/critical), Snyk SCA clean (no exploitable vulns), OWASP API Top 10 checks for `/ingest/*` and `/health`

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/data-ingest/` — isolated FastAPI service with own DB models, ingest logic, and API. Touches: `services/data-ingest/src/main.py` (API), `services/data-ingest/src/ingest_service.py` (core logic), `services/data-ingest/src/models.py` (DB models), `services/data-ingest/tests/` (tests). Shared: `shared/python/src/vnstock_shared/models/` (MarketDataCreate), `shared/python/src/vnstock_shared/config/`. **No overlap with analysis-engine.**

Ordered subtasks (COMPLETED):
1. [x] Verify DB models match canonical schema (MarketDataCreate → SQLAlchemy model)
2. [x] Implement ingestion job scheduler (APScheduler cron at 06:00 ICT) for UC-DI-1 — `is_trading_day()` and `run_ingestion_job()` implemented
3. [x] Wire real CAFEF/VNDIRECT fetch logic in `ingest_service.py` — done with retry logic (tenacity)
4. [x] Implement idempotent upsert with duplicate detection (UC-DI-4) — done in `ingest_data_for_date` via unique constraint + rollback handling
5. [x] Enhance `/health` with real DB + source checks (UC-DI-3) — done
6. [x] Enhance `/ingest/run` to call real ingestion job (UC-DI-2) — wired to `run_ingestion_job`
7. [x] Add comprehensive tests (happy path + edge cases: network failure, invalid data, duplicate handling, non-trading day, fallback)
8. [x] Write README with exact run steps (uvicorn, pytest, env vars, docker-compose)
9. [x] Run security checks (gitleaks, semgrep, snyk) — all clean

---

## Test Plan (for TESTER)

**Scenario: Scheduled ingest runs on trading day**
- Steps: Set system date to a trading day (e.g., 2024-01-08), trigger scheduler via `run_ingestion_job`, verify DB has new rows for all 10 default symbols
- Expected: All 10 symbols ingested successfully, summary shows success=10, failed=0, duplicates_skipped=0

**Scenario: Scheduled ingest skips non-trading day**
- Steps: Set system date to weekend (2024-01-06 Saturday) or holiday (2024-01-01), trigger scheduler
- Expected: Returns empty results, summary shows total=10, success=0, failed=0, logs "Skipping non-trading day"

**Scenario: Manual trigger via API**
- Steps: `POST /ingest/run` with `{"date": "2024-01-08"}`, verify response structure and DB state
- Expected: Returns request_id, date, results array with per-symbol status (symbol, status, source, rows_upserted, duplicate_skipped), summary with counts

**Scenario: Primary source failure triggers fallback**
- Steps: Mock CAFEF to return 500/None, call ingestion for VNM on trading day
- Expected: Falls back to VNDIRECT, returns success with source="VNDIRECT", rows_upserted=1

**Scenario: Both sources fail**
- Steps: Mock both CAFEF and VNDIRECT to return None/raise
- Expected: Returns failed status, error="Both primary and fallback sources failed", rows_upserted=0, no DB write

**Scenario: Idempotent upsert (duplicate handling)**
- Steps: Call `run_ingestion_job` twice for same symbol+date (VNM, 2024-01-08)
- Expected: First run success, rows_upserted=1; second run success, duplicate_skipped=true, rows_upserted=0, no duplicate row in DB

**Scenario: Health endpoint**
- Steps: `GET /health` with DB up → check database.ok; then stop DB, `GET /health` → check database.error
- Expected: Returns healthy/degraded with checks.database = ok/error, primary_source and fallback_sources status included

**Edge cases (covered in tests):**
- Empty symbol list → 400 error
- Invalid date format (not YYYY-MM-DD) → 400 error
- Non-trading day via API → 400 with "not a trading day"
- Network timeout (httpx timeout) → handled by retry, then fallback, then fail gracefully
- Malformed API response (invalid JSON) → treated as source failure, triggers fallback

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (done)
- `vnstock-advisor-2-ba-data-ingest` (done — schema, source choice, disclaimer ready)
- Feeds: `vnstock-advisor-7-tester-data-ingest`, `vnstock-advisor-8-qa-data-ingest`