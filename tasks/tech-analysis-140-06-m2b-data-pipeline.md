# Task: tech-analysis-140-06-m2b-data-pipeline

**Task ID**: T-140-06
**Title**: M2B Data Pipeline — VN source adapters, normalization (DEV-2)
**Role**: DEV
**Status**: READY
**Assigned Agent**: dev-2
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M2B Data Pipeline Service)
- `workspace/apps/tech-analysis/src/services/data-pipeline/` (entire service directory)
- `workspace/apps/tech-analysis/src/adapters/vn-sources/` (VN source adapters)
- `workspace/apps/tech-analysis/src/core/normalization/` (normalization pipeline)

## Goal
Implement M2B Data Pipeline Service: VN stock data source adapters (VNDIRECT, VNINDEX, CAFE, VCI), normalization pipeline (schema validation, deduplication, gap filling, timestamp alignment), and storage interface (TimescaleDB/PostgreSQL). Service exposes gRPC/HTTP for downstream consumers (M2A, M3A).

## Acceptance Criteria (trace to M2B-UC specs from T-140-08)
| AC | Trace |
|----|-------|
| VNDIRECT adapter fetches OHLCV + metadata | UC-M2B-01 |
| VNINDEX adapter fetches index data | UC-M2B-02 |
| CAFE adapter fetches derivatives data | UC-M2B-03 |
| VCI adapter fetches fund flow data | UC-M2B-04 |
| Normalization: schema validation (Zod) | UC-M2B-05 |
| Normalization: deduplication (same symbol+timestamp) | UC-M2B-06 |
| Normalization: gap filling (forward fill config) | UC-M2B-07 |
| Normalization: timestamp alignment (exchange timezone) | UC-M2B-08 |
| Storage: write to TimescaleDB with partitioning | UC-M2B-09 |
| gRPC: GetBars(symbol, timeframe, range) | UC-M2B-10 |
| HTTP: GET /bars/:symbol/:timeframe | UC-M2B-11 |
| Health: /health, /ready endpoints | UC-M2B-12 |
| Metrics: ingestion latency, rows written, errors | UC-M2B-13 |

## Implementation Plan (for DEV-2)
**Architecture Seam**: M2B Data Pipeline Service (owns: adapters, normalization, storage interface)

### Files/Modules to Create/Touch
1. `src/services/data-pipeline/service.ts` — main service, DI container, lifecycle
2. `src/services/data-pipeline/config.ts` — env config (Zod), source priorities
3. `src/adapters/vn-sources/base.ts` — abstract adapter interface
4. `src/adapters/vn-sources/vndirect.ts` — VNDIRECT REST API adapter
5. `src/adapters/vn-sources/vnindex.ts` — VNINDEX adapter
6. `src/adapters/vn-sources/cafe.ts` — CAFE adapter
7. `src/adapters/vn-sources/vci.ts` — VCI adapter
8. `src/core/normalization/pipeline.ts` — normalization pipeline orchestrator
9. `src/core/normalization/schema.ts` — Zod schemas for raw/normalized
10. `src/core/normalization/dedupe.ts` — deduplication logic
11. `src/core/normalization/gapfill.ts` — gap filling (forward/linear)
12. `src/core/normalization/timezone.ts` — VN timezone (UTC+7) alignment
13. `src/core/storage/timescaledb.ts` — TimescaleDB writer with hypertables
14. `src/core/storage/interface.ts` — storage interface (for testing/mocks)
15. `src/grpc/data-pipeline.proto` — gRPC service definition
16. `src/http/routes/bars.ts` — HTTP GET /bars/:symbol/:timeframe
17. `src/http/health.ts` — health/readiness endpoints
18. `src/metrics/ingestion.ts` — Prometheus metrics
19. `tests/unit/adapters/*.test.ts` — adapter unit tests
20. `tests/unit/normalization/*.test.ts` — normalization unit tests
21. `tests/integration/data-pipeline.test.ts` — integration test (T-140-07)

### Ordered Subtask Checklist
- [ ] Scaffold service directory structure and config
- [ ] Implement base adapter interface and VNDIRECT adapter
- [ ] Implement VNINDEX, CAFE, VCI adapters
- [ ] Implement normalization pipeline (schema → dedupe → gapfill → timezone)
- [ ] Implement TimescaleDB storage writer with hypertables
- [ ] Implement gRPC service (GetBars, SubscribeBars)
- [ ] Implement HTTP gateway routes
- [ ] Add health/readiness endpoints and metrics
- [ ] Write unit tests for adapters and normalization
- [ ] Ensure all tests pass locally
- [ ] Push branch and notify TESTER (T-140-07)

## Test Plan (for TESTER - T-140-07)
See T-140-07 for detailed test scenarios.

## DoD Tier 2 Checklist
- [ ] All ACs implemented and tested
- [ ] Unit tests pass (≥80% coverage on adapters/normalization)
- [ ] Integration test passes (T-140-07)
- [ ] BA specs (T-140-08) reviewed and traced
- [ ] Contract review (T-140-09) passed
- [ ] Security gate (T-140-10) passed
- [ ] README with run instructions