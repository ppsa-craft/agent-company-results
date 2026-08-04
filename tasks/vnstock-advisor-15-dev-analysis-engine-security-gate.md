# Task: vnstock-advisor-15-dev-analysis-engine-security-gate

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: security gate completion for analysis-engine service)
**Status:** ready (DEV-1)

---

## Goal

Complete the security gate for the `analysis-engine` service per DoD Tier 2 requirements: gitleaks secret-scan clean, semgrep SAST clean (high/critical), Snyk SCA clean (no exploitable vulns), OWASP API Top 10 checks for `/indicators/compute`, `/screen`, `/rank`, `/health`.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Gitleaks scan passes with zero findings (no hardcoded secrets in code/history)
- [ ] Semgrep SAST scan passes with zero high/critical findings
- [ ] Snyk SCA scan passes with zero exploitable vulnerabilities in dependencies
- [ ] OWASP API Top 10 checks for `/indicators/compute`, `/screen`, `/rank`, `/health` endpoints verified (broken auth, excessive data exposure, rate limiting, etc.)
- [ ] Security gate documented in service README with run commands and results
- [ ] CI pipeline includes all four security checks as mandatory gates

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/analysis-engine/` — security tooling configuration and CI integration only. Touches: `services/analysis-engine/.gitleaks.toml`, `services/analysis-engine/.semgrep.yml`, `services/analysis-engine/.snyk` config, `.github/workflows/analysis-engine-security.yml`. **No functional code changes** — this is security tooling setup and verification only. **Independent of analysis-engine implementation** — can run in parallel with DEV-2's implementation work.

Ordered subtasks:
1. [ ] Configure gitleaks with custom rules for VN stock domain (API keys, DB passwords) — run `gitleaks detect --source . --config .gitleaks.toml`
2. [ ] Configure semgrep with custom rules for FastAPI/Python security patterns — run `semgrep scan --config .semgrep.yml`
3. [ ] Configure Snyk for Python dependencies — run `snyk test --file=pyproject.toml` and `snyk monitor`
4. [ ] Implement OWASP API Top 10 test suite for `/indicators/compute`, `/screen`, `/rank`, `/health` endpoints (auth, rate limit, input validation, error handling, logging)
5. [ ] Add GitHub Actions workflow `analysis-engine-security.yml` running all four checks as required status checks
6. [ ] Fix any findings (must be zero high/critical for ship)
7. [ ] Document security gate run steps in `services/analysis-engine/README.md` (update existing)

---

## Test Plan (for TESTER)

**Scenario: Gitleaks secret scan**
- Steps: Run `gitleaks detect --source . --config .gitleaks.toml` in `services/analysis-engine/`
- Expected: Exit code 0, no findings reported

**Scenario: Semgrep SAST scan**
- Steps: Run `semgrep scan --config .semgrep.yml` in `services/analysis-engine/`
- Expected: Exit code 0, no high/critical severity findings

**Scenario: Snyk SCA scan**
- Steps: Run `snyk test --file=pyproject.toml` in `services/analysis-engine/`
- Expected: Exit code 0, no exploitable vulnerabilities (CVSS >= 7.0)

**Scenario: OWASP API Top 10 endpoint tests**
- Steps: Run pytest with OWASP test markers against `/indicators/compute`, `/screen`, `/rank`, `/health`
- Expected: All tests pass — auth enforced on compute/screen/rank, rate limiting present, input validation on symbols/date ranges, no stack traces in errors, security headers present

**Scenario: CI pipeline integration**
- Steps: Push to feature branch, verify GitHub Actions runs all four checks
- Expected: All four checks run and pass; merge blocked if any fails

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (done — docker-compose, CI structure exists)
- **Independent of `vnstock-advisor-5-dev-analysis-engine` implementation** — can run in parallel
- Feeds: QA verification of security gate completion