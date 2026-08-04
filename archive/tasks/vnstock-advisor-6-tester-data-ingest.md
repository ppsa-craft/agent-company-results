# Task: vnstock-advisor-6-tester-data-ingest

**Role:** TESTER
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: data-ingest service testing)
**Status:** claimed:TESTER-1 (waiting for DEV code-complete)

---

## Goal

Execute end-to-end testing of `data-ingest` service per Test Plan in `vnstock-advisor-4-dev-data-ingest.md`. Verify README works verbatim, all acceptance criteria met, edge cases covered.

---

## Acceptance Criteria (traceable to use cases)

- [ ] README verbatim run succeeds in clean checkout
- [ ] All Test Plan scenarios pass (scheduled ingest, manual trigger, health, idempotent upsert, fallback, edge cases)
- [ ] Automated test suite runs via one command (`pytest`) and passes
- [ ] Coverage includes BOTH happy path AND failure/edge paths
- [ ] No critical defects blocking ship
- [ ] Findings reported with exact reproduction steps, expected vs actual, severity

---

## Test Plan (for TESTER) — from DEV task

**Scenario: Scheduled ingest runs on trading day**
- Steps: Set system date to a trading day, trigger scheduler, verify DB has new rows for all symbols
- Expected: 4+ symbols ingested successfully, summary shows success count

**Scenario: Scheduled ingest skips non-trading day**
- Steps: Set system date to weekend/holiday, trigger scheduler
- Expected: No DB writes, log shows "Skipping non-trading day"

**Scenario: Manual trigger via API**
- Steps: `POST /ingest/run`, verify response structure and DB state
- Expected: Returns request_id, date, results array with per-symbol status, summary

**Scenario: Primary source failure triggers fallback**
- Steps: Mock CAFEF to return 500, call ingestion for one symbol
- Expected: Falls back to VNDIRECT, returns success with source="VNDIRECT"

**Scenario: Both sources fail**
- Steps: Mock both CAFEF and VNDIRECT to fail
- Expected: Returns failed status, error message, no DB write

**Scenario: Idempotent upsert (duplicate handling)**
- Steps: Ingest same symbol+date twice
- Expected: Second run returns success with duplicate_skipped=true, no duplicate row

**Scenario: Health endpoint**
- Steps: `GET /health` with DB up, then with DB down
- Expected: Returns healthy/degraded with checks.database = ok/error

**Exploratory edge cases (beyond Test Plan):**
- Empty symbol list
- Invalid date format
- Network timeout during fetch
- Malformed API response from source
- Database connection failure mid-ingestion
- Concurrent ingestion runs for same symbol/date

---

## Dependencies

- `vnstock-advisor-4-dev-data-ingest` (must be at least code-complete with README)
- Runs in parallel with: `vnstock-advisor-7-tester-analysis-engine`