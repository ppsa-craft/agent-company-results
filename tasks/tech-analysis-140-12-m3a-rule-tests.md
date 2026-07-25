# Task: tech-analysis-140-12-m3a-rule-tests

**Task ID**: T-140-12
**Title**: M3A Rule Tests (TESTER)
**Role**: TESTER
**Status**: READY
**Assigned Agent**: tester-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M3A Alert Rules Service)
- `workspace/apps/tech-analysis/tests/unit/m3a-alert-rules/**`
- `workspace/apps/tech-analysis/tests/integration/m3a-alert-rules/**`

## Goal
Execute comprehensive unit and integration tests for M3A Alert Rule Engine (T-140-11) per the Test Plan defined in T-140-11.

## Acceptance Criteria
- All unit test scenarios from T-140-11 Test Plan pass
- All integration test scenarios from T-140-11 Test Plan pass
- Coverage ≥90% per evaluator file achieved
- Test report generated at `workspace/apps/tech-analysis/test-reports/m3a-alert-rules/`

## Test Plan (verbatim execution from T-140-11)
**Test Scenarios per Acceptance Criterion**:
- UC-M3A-01 Threshold: Happy/Edge cases per T-140-11
- UC-M3A-02 Crossover: Happy/Edge cases per T-140-11
- UC-M3A-03 Multi-Condition: Happy/Edge cases per T-140-11
- UC-M3A-04 CRUD: Happy/Edge cases per T-140-11
- UC-M3A-05 Evaluation: Happy/Edge cases per T-140-11
- UC-M3A-06 Emission: Happy/Edge cases per T-140-11
- UC-M3A-07 State: Happy/Edge cases per T-140-11
- UC-M3A-08 Cooldown: Happy/Edge cases per T-140-11
- UC-M3A-09 API: Happy/Edge cases per T-140-11
- UC-M3A-10 Coverage: `npm run test:coverage` ≥90% per evaluator file

**Execution Steps**:
1. Checkout dev-1's branch for T-140-11 in isolated worktree
2. Install dependencies: `cd workspace/apps/tech-analysis/services/m3a-alert-rules && npm ci`
3. Start NATS test container: `docker run -d -p 4222:4222 nats:latest`
4. Start PostgreSQL test container for rule storage
5. Start Redis test container for state/throttle
6. Run unit tests: `npm run test:unit` — verify all pass
7. Run integration tests: `npm run test:integration` — verify all pass
8. Run coverage: `npm run test:coverage` — verify ≥90% per evaluator file
9. Generate HTML report: `npm run test:report`
10. Verify README.md run instructions work in clean checkout
11. Report results to PM with pass/fail per scenario

## Exploratory Pass (TESTER discretion)
- Stress test: 10,000 rules evaluating simultaneously
- NATS reconnection behavior during evaluation
- Rule hot-reload without service restart
- Clock skew handling (bar timestamp vs evaluation time)
- Memory leak detection with long-running evaluation

## Deliverables
- Test report: `workspace/apps/tech-analysis/test-reports/m3a-alert-rules/index.html`
- JUnit XML: `workspace/apps/tech-analysis/test-reports/m3a-alert-rules/results.xml`
- Coverage report: `workspace/apps/tech-analysis/coverage/m3a-alert-rules/`
- Test execution log with pass/fail per scenario

## DoD Tier 2 Checklist
- [ ] All test scenarios from T-140-11 Test Plan executed and passed
- [ ] Coverage ≥90% per evaluator file verified
- [ ] Test report generated
- [ ] README.md run instructions verified in clean checkout
- [ ] Results reported to PM