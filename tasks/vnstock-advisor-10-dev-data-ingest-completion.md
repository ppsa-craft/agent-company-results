# Task: vnstock-advisor-10-dev-data-ingest-completion

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature — data-ingest service completion)
**Status:** ready (assign: DEV instance on `task/vnstock-advisor-10-dev-data-ingest-completion`)

---

## Goal

Complete the M1 data-ingest service by running and verifying the security gate (secret-scan, SAST, SCA), ensuring all tests pass, and validating the README works verbatim in a clean checkout. This unblocks QA-1 for the M1 ship gate.

The implementation (4-dev-data-ingest) is marked done with all acceptance criteria met. This task is the **final validation gate** before QA activation.

---

## Acceptance Criteria (traceable to UC-DI-1 through UC-DI-4; DoD Tier 2 security gate)

- [ ] **Secret-scan clean:** `gitleaks detect --source services/data-ingest/` passes with zero findings (baseline respected for `.env.example` only)
- [ ] **SAST clean:** `semgrep --config=auto services/data-ingest/` returns no high/critical findings
- [ ] **SCA clean:** `cd services/data-ingest && pip-audit` returns no exploitable vulnerabilities; Snyk scan clean
- [ ] **OWASP API Top 10 checks** for `/ingest/*` and `/health` endpoints verified (input validation via Pydantic, no stack traces in errors, rate limiting noted for API gateway)
- [ ] **All tests pass:** `pytest services/data-ingest/tests/ -v` — 100% pass rate on existing test suite
- [ ] **README verified:** exact run steps in `services/data-ingest/README.md` work in a clean checkout (docker-compose up, init-db, service start, test run)
- [ ] **Disclaimer integration confirmed:** every API response includes `meta.disclaimer` (VN/EN) per `docs/compliance/disclaimer.md`
- [ ] **Service starts and responds:** `uvicorn main:app --port 8001` serves `/health` and `/ingest/run` without errors

---

## Implementation Plan (for DEV)

**Architecture seam — file boundary:** this task operates ONLY within `services/data-ingest/` — running validation commands, fixing any gate failures, and documenting results. It does NOT modify implementation logic (that was 4-dev-data-ingest). If a gate fails, the fix is scoped to the failing surface only (e.g., a SAST finding in `ingest_service.py` → fix that pattern).

**Worktree:** use the existing `worktrees/dev-data-ingest/` worktree (already has the completed implementation) or stage from `workspace/apps/vnstock-advisor/` if needed.

Ordered subtasks (each a committed unit):
1. **Checkout & deps:** ensure `services/data-ingest/` is current in worktree; `uv sync --all-extras` from repo root; `pip install gitleaks semgrep pip-audit` (or use pre-installed)
2. **Run test suite:** `pytest services/data-ingest/tests/ -v` — confirm 100% pass; if any fail, fix minimally and re-run
3. **Secret-scan:** `gitleaks detect --source services/data-ingest/` — if findings, remediate (rotate secret, update baseline) and re-scan
4. **SAST:** `semgrep --config=auto services/data-ingest/` — if high/critical, fix pattern (e.g., parameterize query, validate input) and re-scan
5. **SCA:** `cd services/data-ingest && pip-audit` — if exploitable vulns, upgrade dependency (pin in `pyproject.toml`) and re-audit
6. **OWASP API spot-check:** manually verify `/health` and `/ingest/run` reject invalid input with Problem Details (RFC 7807), no stack traces; confirm Pydantic models on all endpoints
7. **README verification:** in a clean temp directory, clone/follow the README steps exactly — document any gaps, fix README or scripts
8. **Disclaimer audit:** curl `/health` and `/ingest/run` (mocked) → verify `meta.disclaimer` present with VN/EN exact text from `docs/compliance/disclaimer.md`
9. **Commit gate results:** add a `SECURITY_GATE_RESULTS.md` in `services/data-ingest/` with scan outputs (redacted) and pass confirmation

---

## Test Plan (for DEV and TESTER)

1. **Test suite execution:**
   - Steps: `cd services/data-ingest && pytest tests/ -v`
   - Expected: All 18 tests pass (health, root, ingest-run validation, trading-day logic, CAFEF/VNDIRECT fetch, fallback, both-fail, non-trading-day, network-error, malformed-response, status endpoint, edge cases)

2. **Secret-scan:**
   - Steps: `gitleaks detect --source services/data-ingest/ --config .gitleaks.toml` (or default)
   - Expected: Zero new findings; baseline `.env.example` entries allowed

3. **SAST:**
   - Steps: `semgrep --config=auto services/data-ingest/ --json=semgrep-results.json`
   - Expected: No findings with severity HIGH or CRITICAL; medium/low logged for backlog

4. **SCA:**
   - Steps: `cd services/data-ingest && pip-audit --format=json`
   - Expected: No vulnerabilities with `fixable` true and severity HIGH/CRITICAL

5. **README clean-run:**
   - Steps: In `/tmp/test-checkout/`, follow README steps 1-6 exactly
   - Expected: Service starts, `/health` returns 200 with `database: ok`, tests pass

6. **Disclaimer presence:**
   - Steps: Start service, `curl -X POST /ingest/run -H "Content-Type: application/json" -d '{"date":"2024-01-08"}'` (with DB mocked or test DB)
   - Expected: Response JSON contains `meta.disclaimer.vi-VN` and `meta.disclaimer.en-US` matching exact text from compliance doc

---

## Dependencies

- **4-dev-data-ingest** (implementation) — must be done (marked done)
- **1-repo-scaffold** (done)
- **2-ba-data-ingest** (done — schema, source choice, disclaimer ready)
- Feeds: **vnstock-advisor-8-qa-data-ingest** (QA-1 activates once this completes)