# Task: pm-s1-test-002 — S1 End-to-End Data Flow Tests

## Metadata
- **ID**: pm-s1-test-002
- **Role**: TESTER
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1-S1
- **Assignee**: tester-2
- **Depends on**: pm-s1-003, pm-s1-004 (S1 normalization + REST API)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
S1 End-to-End Data Flow Verification: Adapters → Normalization → Redis → Postgres → REST API

## Description
Comprehensive integration test suite verifying the complete S1 data pipeline from external API ingestion through to REST API consumption. Uses testcontainers for Postgres/Redis.

## Acceptance Criteria
- [ ] Test: Full adapter → normalization → Redis stream → Postgres → REST API roundtrip
- [ ] Test: All 4 adapters produce valid normalized output for sample VN market data
- [ ] Test: Redis stream messages match S2 contract schema exactly
- [ ] Test: Postgres persistence is idempotent (re-ingestion doesn't duplicate)
- [ ] Test: REST API returns correct data with pagination, filtering, time ranges
- [ ] Test: Error handling — adapter failures don't crash pipeline, dead letter queue works
- [ ] Test: Backpressure — consumer lag detection alerts when S2 falls behind
- [ ] Test: Data quality metrics emitted (latency, throughput, error rate, schema violations)
- [ ] Performance: End-to-end latency < 2s p99 from adapter fetch to API availability

## Verification
- All tests pass in CI pipeline with testcontainers
- Test report shows coverage of all 4 adapter paths
- Contract test results published to Pact broker
- Benchmark results recorded in CI artifacts

## Security Notes
- Test data only — no real API keys in tests
- Mock external APIs with recorded responses
- Verify no secrets in test logs