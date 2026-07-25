# Task: tech-analysis-140-07-m2b-integration-tests

**Task ID**: T-140-07
**Title**: M2B Integration Tests (TESTER)
**Role**: TESTER
**Status**: READY
**Assigned Agent**: tester-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M2B Data Pipeline Service)
- `workspace/apps/tech-analysis/tests/integration/data-pipeline.test.ts`

## Goal
Execute integration test scenarios for M2B Data Pipeline Service (T-140-06) per acceptance criteria traceability.

## Test Plan — Step-by-Step Scenarios

### Scenario 1: VNDIRECT Adapter Happy Path
**Given**: VNDIRECT API returns valid OHLCV for VNM, 1D timeframe, 2024-01-01 to 2024-01-31
**When**: Call adapter `fetch(symbol="VNM", timeframe="1D", from, to)`
**Then**: Returns normalized bars array with correct schema (symbol, timestamp, open, high, low, close, volume)
**Expected**: 22 bars (trading days), all fields non-null, timestamps UTC+7 aligned

### Scenario 2: VNINDEX Adapter — Index Data
**Given**: VNINDEX API returns VNINDEX daily values
**When**: Call adapter `fetch(symbol="VNINDEX", timeframe="1D", ...)`
**Then**: Returns bars with symbol="VNINDEX", volume=0 (index), correct close values

### Scenario 3: CAFE Adapter — Derivatives
**Given**: CAFE API returns VN30F1M futures data
**When**: Call adapter `fetch(symbol="VN30F1M", timeframe="1H", ...)`
**Then**: Returns hourly bars with open_interest field populated

### Scenario 4: VCI Adapter — Fund Flow
**Given**: VCI API returns foreign/proprietary net buy/sell
**When**: Call adapter `fetch(symbol="VNM", timeframe="1D", ...)`
**Then**: Returns bars with `foreign_net_buy`, `proprietary_net_buy` fields

### Scenario 5: Normalization — Schema Validation Rejects Invalid
**Given**: Raw bar with negative volume, or missing close
**When**: Pass through normalization pipeline
**Then**: Bar rejected, validation error logged, valid bars pass through

### Scenario 6: Normalization — Deduplication
**Given**: Two raw bars same symbol+timestamp (different sources)
**When**: Deduplication step runs
**Then**: Single bar kept (priority: VNDIRECT > VNINDEX > CAFE > VCI), warning logged

### Scenario 7: Normalization — Gap Fill Forward
**Given**: Missing bars for 2024-01-03 (holiday), config `gapFill: "forward"`
**When**: Gap fill runs
**Then**: 2024-01-03 bar = copy of 2024-01-02 bar, `gap_filled: true` flag set

### Scenario 8: Normalization — Timestamp Alignment (UTC+7)
**Given**: Source returns timestamp "2024-01-01 14:30:00" (VN time, no TZ)
**When**: Timezone alignment runs
**Then**: Output timestamp = "2024-01-01T07:30:00Z" (UTC)

### Scenario 9: Storage — TimescaleDB Write
**Given**: Normalized bars for VNM 1D, 30 days
**When**: Storage writer `write(bars)` called
**Then**: Rows inserted into `bars_1d` hypertable, partitioned by time, no duplicates

### Scenario 10: gRPC GetBars — Happy Path
**Given**: Data exists in DB for VNM 1D 2024-01-01..2024-01-31
**When**: gRPC `GetBars(symbol="VNM", timeframe="1D", from, to)`
**Then**: Returns 22 bars, correct order, gRPC status OK

### Scenario 11: HTTP GET /bars/VNM/1D — Happy Path
**Given**: Same data as Scenario 10
**When**: HTTP GET `/bars/VNM/1D?from=2024-01-01&to=2024-01-31`
**Then**: 200 OK, JSON array of bars, correct Content-Type

### Scenario 12: HTTP — Invalid Symbol
**Given**: Symbol "INVALID" not in DB
**When**: GET `/bars/INVALID/1D`
**Then**: 404 Not Found, error body `{code: "NOT_FOUND", message: "..."}`

### Scenario 13: HTTP — Invalid Timeframe
**Given**: Timeframe "5M" not supported
**When**: GET `/bars/VNM/5M`
**Then**: 400 Bad Request, error `{code: "INVALID_TIMEFRAME"}`

### Scenario 14: Health Endpoints
**When**: GET `/health`, GET `/ready`
**Then**: `/health` = 200 `{status: "ok"}`, `/ready` = 200 `{ready: true}` when DB connected

### Scenario 14: Metrics Emitted
**When**: Ingestion runs, gRPC/HTTP requests served
**Then**: Prometheus metrics `ingestion_latency_ms`, `bars_written_total`, `grpc_requests_total`, `http_requests_total` increment

## Edge Cases
- Empty date range → empty array, not error
- Future date range → empty array
- Source API timeout → retry with exponential backoff, then circuit breaker
- Source API rate limit → respect Retry-After, queue request
- DB connection loss → readiness=false, health=degraded, auto-reconnect

## Execution
- Run against T-140-06 branch in isolated worktree
- Use testcontainers for TimescaleDB
- Mock external APIs with MSW/nock
- Report: pass/fail per scenario, screenshots/logs for failures

## DoD Tier 2 Checklist
- [ ] All 14 scenarios executed
- [ ] Edge cases explored (minimum 5)
- [ ] Test report with pass/fail matrix
- [ ] Failures reported to DEV-2 with reproduction steps