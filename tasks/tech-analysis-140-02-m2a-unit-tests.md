# Task: tech-analysis-140-02-m2a-unit-tests

**Task ID**: T-140-02
**Title**: M2A Unit Tests
**Role**: TESTER
**Status**: READY
**Assigned Agent**: tester-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature (use cases + tests + docs/README update + analytics update)

## File Ownership (Architecture Seam: M2A Core Indicators Service)
- `workspace/apps/tech-analysis/tests/unit/m2a-core-indicators/**`
- `workspace/apps/tech-analysis/tests/integration/m2a-core-indicators/**`

## Goal
Execute comprehensive unit and integration tests for M2A Core Indicators Service (T-140-01) per the Test Plan defined in T-140-01.

## Acceptance Criteria
- All unit test scenarios from T-140-01 Test Plan pass
- All integration test scenarios from T-140-01 Test Plan pass
- Coverage ≥90% per indicator file achieved
- Test report generated at `workspace/apps/tech-analysis/test-reports/m2a-core-indicators/`

## Test Plan (verbatim execution from T-140-01)
**Test Scenarios per Acceptance Criterion**:
- UC-M2A-01 SMA: Happy/Edge cases per T-140-01
- UC-M2A-02 EMA: Happy/Edge cases per T-140-01
- UC-M2A-03 RSI: Happy/Edge cases per T-140-01
- UC-M2A-04 MACD: Happy/Edge cases per T-140-01
- UC-M2A-05 Bollinger: Happy/Edge cases per T-140-01
- UC-M2A-06 NaN propagation: All indicators
- UC-M2A-07 gRPC/HTTP: Happy + Edge cases
- UC-M2A-08 Coverage: `npm run test:coverage` ≥90% per file

**Execution Steps**:
1. Checkout dev-1's branch for T-140-01 in isolated worktree
2. Install dependencies: `cd workspace/apps/tech-analysis/services/m2a-core-indicators && npm ci`
3. Run unit tests: `npm run test:unit` — verify all pass
4. Run integration tests: `npm run test:integration` — verify all pass
5. Run coverage: `npm run test:coverage` — verify ≥90% per indicator file
6. Generate HTML report: `npm run test:report`
7. Verify README.md run instructions work in clean checkout
8. Report results to PM with pass/fail per scenario

## Exploratory Pass (TESTER discretion)
- Fuzz input validation with random/malformed data
- Test concurrent gRPC requests
- Test large dataset performance (100k+ points)
- Test memory leaks with repeated calls

## Deliverables
- Test report: `workspace/apps/tech-analysis/test-reports/m2a-core-indicators/index.html`
- JUnit XML: `workspace/apps/tech-analysis/test-reports/m2a-core-indicators/results.xml`
- Coverage report: `workspace/apps/tech-analysis/coverage/m2a-core-indicators/`
- Test execution log with pass/fail per scenario

## DoD Tier 2 Checklist
- [ ] All test scenarios from T-140-01 Test Plan executed and passed
- [ ] Coverage ≥90% per indicator file verified
- [ ] Test report generated
- [ ] README.md run instructions verified in clean checkout
- [ ] Results reported to PM