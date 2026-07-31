# Task: vnstock-advisor-7-tester-data-ingest

**Role:** TESTER
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: data-ingest test execution)
**Status:** ready

---

## Goal

Execute test plan for `data-ingest` service, report defects, verify DoD tier 2 quality gate.

---

## Acceptance Criteria

- [ ] All test scenarios from `vnstock-advisor-4-dev-data-ingest` executed
- [ ] Defects reported in `workspace/apps/vnstock-advisor/docs/testing/defects-data-ingest.md` (if any)
- [ ] Security gate verified: Semgrep, Snyk, Gitleaks clean (no high/critical)
- [ ] Test evidence recorded (logs, screenshots, output)
- [ ] Verdict: PASS / FAIL with reasoning
- [ ] Report to PM in-session (task output)

---

## Test Scenarios (from DEV task)

1. **Scheduled ingest runs** — trigger `/ingest/run`, verify `market_data` rows
2. **Idempotent upsert** — run twice, verify no duplicates
3. **Fallback source** — mock primary failure, verify fallback data
4. **Health endpoint** — call `GET /ingest/health`, verify response shape
5. **Security gate** — run Semgrep, Snyk, Gitleaks on service

---

## Execution Approach

1. Ensure `data-ingest` service is running (docker compose)
2. Run unit tests: `pytest services/data-ingest/tests/ -v`
3. Run integration tests against test DB
4. Manually test endpoints via curl/Postman
5. Run security tools: `semgrep --config=auto services/data-ingest/`, `snyk test`, `gitleaks detect`
6. Record results per scenario
7. Report defects (if any) with reproduction steps

---

## Dependencies

- `vnstock-advisor-4-dev-data-ingest` (service must be implemented)
- `vnstock-advisor-1-repo-scaffold` (docker-compose, CI)
- Can run in parallel with `vnstock-advisor-8-tester-analysis-engine`