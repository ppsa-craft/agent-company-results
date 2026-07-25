# Task: pm-s2-test-001 — S2 Technical Indicator Tests

## Metadata
- **ID**: pm-s2-test-001
- **Role**: TESTER
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1-S2
- **Assignee**: tester-1
- **Depends on**: pm-s2-002 (Core Indicators), pm-s2-001 (S2 Scaffold)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
S2 Signal Engine: Indicator Correctness + Property Tests + Integration with S1 Data

## Description
Test the S2 indicator library and signal generation pipeline. Verify mathematical correctness, property-based invariants, and integration with S1 Redis stream data.

## Acceptance Criteria
- [ ] Unit tests: each indicator against known reference values (TA-Lib compatibility)
- [ ] Property tests (Hypothesis): RSI bounds, MACD convergence, Bollinger band containment
- [ ] Edge cases: zero volume, flat prices, missing data, single-bar inputs
- [ ] Integration test: consume S1 Redis stream → compute indicators → publish signals
- [ ] Contract test: signal output matches S2→S3 contract schema
- [ ] Performance: indicator computation on 1000 symbols within SLA
- [ ] Regression test: indicator outputs stable across versions

## Verification
- All tests pass in CI with hypothesis examples reported
- Property test shrinking finds minimal failing cases
- Integration test uses testcontainers for Redis
- Benchmark results tracked in CI artifacts

## Security Notes
- No external dependencies in test execution
- Deterministic seeds for property tests