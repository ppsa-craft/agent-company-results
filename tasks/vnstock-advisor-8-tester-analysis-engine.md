# Task: vnstock-advisor-8-tester-analysis-engine

**Role:** TESTER
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine test execution)
**Status:** ready

---

## Goal

Execute test plan for `analysis-engine` service, report defects, verify DoD tier 2 quality gate.

---

## Acceptance Criteria

- [ ] All test scenarios from `vnstock-advisor-5-dev-analysis-engine` executed
- [ ] Defects reported in `workspace/apps/vnstock-advisor/docs/testing/defects-analysis-engine.md` (if any)
- [ ] Security gate verified: Semgrep, Snyk, Gitleaks clean (no high/critical)
- [ ] Test evidence recorded
- [ ] Verdict: PASS / FAIL with reasoning
- [ ] Report to PM in-session

---

## Test Scenarios (from DEV task)

1. **Indicator accuracy** — fixture data → compare outputs to expected
2. **Screening correctness** — known pass/fail symbols → only passing returned
3. **Ranking determinism** — same input twice → identical output
3. **Insufficient data** — < 20 data points → partial with warning, no crash
4. **Timeout guard** — 1000 symbols → completes in 30s or partial with notice
5. **Security gate** — Semgrep, Snyk, Gitleaks clean

---

## Execution Approach

1. Ensure `analysis-engine` service running (docker compose)
2. Run unit tests: `pytest services/analysis-engine/tests/ -v`
3. Run integration tests against test DB with BA fixture data
4. Manually test `/rank` endpoint with various query params
5. Run security tools on service
6. Record results per scenario
7. Report defects with reproduction steps

---

## Dependencies

- `vnstock-advisor-5-dev-analysis-engine` (service implemented)
- `vnstock-advisor-1-repo-scaffold` (docker-compose, CI)
- Can run in parallel with `vnstock-advisor-7-tester-data-ingest`