# Task: vnstock-advisor-14-dev-data-ingest-security-gate

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: security gate completion for data-ingest service)
**Status:** ready (DEV-1)

---

## Goal

Complete the security gate for the `data-ingest` service per DoD Tier 2 requirements: gitleaks secret-scan clean, semgrep SAST clean (high/critical), Snyk SCA clean (no exploitable vulns), OWASP API Top 10 checks for `/ingest/*` and `/health`.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Gitleaks scan passes with zero findings (no hardcoded secrets in code/history)
- [ ] Semgrep SAST scan passes with zero high/critical findings
- [ ] Snyk SCA scan passes with zero exploitable vulnerabilities in dependencies
- [ ] OWASP API Top 10 checks for `/ingest/run`, `/health` endpoints verified (broken auth, excessive data exposure, rate limiting, etc.)
- [ ] Security gate documented in service README with run commands and results
- [ ] CI pipeline includes all four security checks as mandatory gates

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/data-ingest/` — security tooling configuration and CI integration only. Touches: `services/data-ingest/.gitleaks.toml`, `services/data-ingest/.semgrep.yml`, `services/data-ingest/.snyk` config, `.github/workflows/data-ingest-security.yml`. **No functional code changes** — this is security tooling setup and verification only. Independent of analysis-engine tasks.

Ordered subtasks:
1. [ ] Configure gitleaks with custom rules for VN stock domain (API keys, DB passwords) — run `gitleaks detect --source . --config .gitleaks.toml`
2. [ ] Configure semgrep with custom rules for FastAPI/Python security patterns — run `semgrep scan --config .semgrep.yml`
3. [ ] Configure Snyk for Python dependencies — run `snyk test --file=pyproject.toml` and `snyk monitor`
4. [ ] Implement OWASP API Top 10 test suite for `/ingest/run` and `/health` endpoints (auth, rate limit, input validation, error handling, logging)
5. [ ] Add GitHub Actions workflow `data-ingest-security.yml` running all four checks as required status checks
6. [ ] Fix any findings (must be zero high/critical for ship)
7. [ ] Document security gate run steps in `services/data-ingest/README.md` (update existing)

---

## Test Plan (for TESTER)

**Scenario: Gitleaks secret scan**
- Steps: Run `gitleaks detect --source . --config .gitleaks.toml` in `services/data-ingest/`
- Expected: Exit code 0, no findings reported

**Scenario: Semgrep SAST scan**
- Steps: Run `semgrep scan --config .semgrep.yml` in `services/data-ingest/`
- Expected: Exit code 0, no high/critical severity findings

**Scenario: Snyk SCA scan**
- Steps: Run `snyk test --file=pyproject.toml` in `services/data-ingest/`
- Expected: Exit code 0, no exploitable vulnerabilities (CVSS >= 7.0)

**Scenario: OWASP API Top 10 endpoint tests**
- Steps: Run pytest with OWASP test markers against `/ingest/run` and `/health`
- Expected: All tests pass — auth enforced on `/ingest/run`, rate limiting present, input validation on date/symbols, no stack traces in errors, security headers present

**Scenario: CI pipeline integration**
- Steps: Push to feature branch, verify GitHub Actions runs all four checks
- Expected: All four checks run and pass; merge blocked if any fails

---

## Dependencies

- `vnstock-advisor-4-dev-data-ingest` (done — service implementation complete)
- Independent of M2 analysis-engine tasks — can run in parallel
- Feeds: QA verification of security gate completion