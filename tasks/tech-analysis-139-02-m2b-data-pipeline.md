# Task T-139-02: M2B Data Pipeline

## Goal
Build the M2B Data Pipeline service (m2-pipeline) that ingests raw market data (OHLCV), normalizes/validates it, computes indicators via M2A service, and stores enriched time-series for M3 Alerting consumption. Implements UC-M2B use cases from BA specs.

## Acceptance Criteria (Traceable to Use Cases)
- [ ] **UC-M2B-01**: Ingest raw OHLCV from Kafka topic `market.raw.ohlcv` (protobuf schema) — handles 10k msgs/sec peak
- [ ] **UC-M2B-02**: Validate OHLCV (OHLC relationships, volume ≥ 0, timestamp monotonic, no gaps > 5min) — invalid → DLQ topic
- [ ] **UC-M2B-03**: Normalize timestamps to UTC, align to 1-minute grid (forward-fill gaps ≤ 5min)
- [ ] **UC-M2B-04**: Call M2A `/indicators/calculate` batch API for each symbol window (500 bars) — retry with exponential backoff
- [ ] **UC-M2B-05**: Store enriched bars (OHLCV + 7 indicators) to TimescaleDB hypertable `market.enriched_1m` — partitioned by symbol, compressed
- [ ] **UC-M2B-06**: Publish enriched bars to Kafka `market.enriched.1m` for real-time M3 consumption
- [ ] **UC-M2B-07**: Backfill job: reprocess historical range (configurable start/end) with idempotent writes
- [ ] **UC-M2B-08**: Health endpoint `/health` reports: lag (ms), throughput (msg/s), error rate, DLQ size
- [ ] **UC-M2B-09**: End-to-end latency (ingest → enriched publish) < 500ms p99 at 1k msg/sec
- [ ] **UC-M2B-10**: Contract test against M2A OpenAPI spec — fails CI if contract broken

## Estimated Effort
- **Effort**: 3 cycles (Cycle 139-141)
- **DoD Tier**: Tier 2 (Feature: use cases + tests + docs + analytics update)

## Assigned Agent
- **Role**: DEV
- **Agent**: dev-2
- **Cycle**: 139
- **Status**: READY

## File Ownership (Disjoint Boundary: `services/m2-pipeline/`)
```
workspace/apps/tech-analysis/services/m2-pipeline/
├── src/
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── ingest.py           # Kafka consumer, protobuf deserialization
│   │   ├── validate.py         # OHLCV validation rules, DLQ producer
│   │   ├── normalize.py        # Timestamp alignment, gap filling
│   │   ├── enrich.py           # M2A client, batch indicator calculation
│   │   ├── store.py            # TimescaleDB writer, upsert logic
│   │   ├── publish.py          # Kafka producer for enriched topic
│   │   ├── backfill.py         # Historical reprocessing job
│   │   └── orchestrator.py     # Pipeline coordination, metrics
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── m2a_client.py       # Async HTTP client with retry/backoff
│   │   └── schemas.py          # Pydantic models for M2A request/response
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # Health, metrics, backfill trigger
│   │   └── schemas.py
│   ├── main.py
│   └── config.py
├── tests/
│   ├── unit/
│   │   ├── test_validate.py
│   │   ├── test_normalize.py
│   │   ├── test_enrich.py
│   │   └── test_store.py
│   ├── contract/
│   │   └── test_m2a_contract.py
│   ├── integration/
│   │   ├── test_pipeline_e2e.py
│   │   └── test_backfill.py
│   └── fixtures/
│       ├── sample_raw.protobuf
│       └── expected_enriched.json
├── contracts/
│   └── m2-pipeline.yaml        # Internal API contract
├── migrations/
│   └── 001_enriched_hypertable.sql
├── pyproject.toml
├── README.md
└── Dockerfile
```

## Implementation Plan (for DEV)

**Architecture Seam**: `services/m2-pipeline/` — disjoint from `m2-indicators` (T-139-01) and `m3-alerts` (T-139-06/07). Consumes M2A via HTTP contract. Produces to Kafka for M3.

**Tech Stack**:
- Python 3.11, FastAPI, aiokafka, asyncpg/TimescaleDB, pydantic
- Protobuf for Kafka schemas (shared `market-data-protos` package)
- Pytest, testcontainers for integration tests

**Ordered Subtask Checklist**:
1. [ ] Scaffold service structure (pyproject.toml, Dockerfile, config, main.py)
2. [ ] Define protobuf schemas for `market.raw.ohlcv` and `market.enriched.1m` (shared package)
3. [ ] Implement `ingest.py` — Kafka consumer group, protobuf deserialization, batching
4. [ ] Implement `validate.py` — OHLCV rules (high ≥ low, high ≥ open/close, low ≤ open/close, volume ≥ 0, ts monotonic)
5. [ ] Implement `normalize.py` — UTC conversion, 1-min grid alignment, forward-fill ≤ 5min gaps
6. [ ] Implement `m2a_client.py` — async client with circuit breaker, retry (3x, exp backoff 100ms/500ms/2s)
7. [ ] Implement `enrich.py` — batch symbols, call M2A `/indicators/calculate`, merge results
8. [ ] Implement `store.py` — TimescaleDB hypertable, upsert on (symbol, timestamp), compression policy
9. [ ] Implement `publish.py` — Kafka producer, enriched protobuf serialization, exactly-once semantics
10. [ ] Implement `orchestrator.py` — pipeline flow, metrics (Prometheus), DLQ handling
11. [ ] Implement `backfill.py` — idempotent range reprocessing, checkpoint tracking
12. [ ] API routes: `/health`, `/metrics`, `POST /backfill` (start, end, symbols[])
13. [ ] Write migrations for TimescaleDB hypertable + compression
14. [ ] Unit tests: validation rules, normalization edge cases, enrichment merging
15. [ ] Contract test: validate M2A request/response against `m2-indicators.yaml`
16. [ ] Integration test: testcontainers (Kafka, TimescaleDB, M2A mock) — full pipeline E2E
17. [ ] Performance test: 1k msg/sec sustained, p99 latency < 500ms
18. [ ] Backfill test: reprocess 30 days, verify idempotency (re-run = no duplicates)
19. [ ] Write README.md with docker-compose, run instructions, schema references
20. [ ] Update analytics plan (pipeline_lag_ms, throughput_msg_s, dlq_size, enrichment_errors)
21. [ ] Docker build, health check verification

**Dependencies**: Requires M2A OpenAPI contract (T-139-01 output). T-139-07 (M3B) depends on enriched Kafka topic from this task.

## Test Plan (for TESTER)

**Happy Path**:
1. **Single message flow**: Produce valid OHLCV to `market.raw.ohlcv` → verify enriched output on `market.enriched.1m` with all 7 indicators present
2. **Batch processing**: 1000 messages burst → all processed, stored, published within 500ms p99
3. **Backfill job**: POST `/backfill` with 7-day range → completes, TimescaleDB rows = expected count, re-run produces zero new rows

**Edge Cases**:
1. **Invalid OHLC**: high < low → message routed to DLQ `market.raw.dlq`, metric `dlq_size` increments
2. **Gap > 5min**: 10-min gap → forward-fill only first 5 min, remaining bars marked `gap_filled=false`
3. **M2A unavailable**: circuit breaker opens after 3 failures, returns cached/stale indicators? (config: fail fast vs stale)
4. **Duplicate timestamps**: same symbol+ts → upsert replaces, no duplicate rows
5. **Out-of-order arrival**: late message (ts < last processed) → processed correctly, upsert handles
6. **Empty batch**: consumer poll returns empty → no error, metrics idle

**Restart Behavior**:
1. Consumer group rebalance → no message loss (committed offsets)
2. DB connection pool exhaustion → backpressure, consumer pauses
3. Kafka broker failover → client reconnects, resumes from committed offset

**Expected Results**: All happy paths produce enriched bars with correct indicator values (cross-checked against M2A reference). DLQ captures invalid messages with error context. Metrics exposed at `/metrics` (Prometheus format). Backfill idempotent.

## DoD Tier 2 Checklist
- [ ] All 10 UCs implemented and tested
- [ ] Unit test coverage ≥ 85%
- [ ] Contract test against M2A OpenAPI passes in CI
- [ ] Integration test passes (testcontainers)
- [ ] Performance test: 1k msg/s, p99 < 500ms
- [ ] Backfill idempotency verified
- [ ] README.md with run instructions
- [ ] Analytics events defined
- [ ] Code review approved by TECHLEAD
- [ ] Security gate passed (QA)
- [ ] Changelog entry