# Task: vnstock-advisor-9-qa-data-ingest

**Role:** QA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: data-ingest security + quality gate)
**Status:** ready

---

## Goal

Enforce quality and security gate for `data-ingest` service per §7.2.1. Verify all DoD artifacts present, security tools clean, no high/critical findings.

---

## Acceptance Criteria

- [ ] **Quality gate:** All DoD tier 2 artifacts present:
  - Implementation complete (DEV verdict PASS)
  - Tests pass (TESTER verdict PASS)
  - BA docs approved (UC, schema, source eval, disclaimer)
  - README runnable in clean checkout
  - CI workflow passes (lint, type-check, test)
- [ ] **Security gate (§7.2.1):** No unresolved high/critical findings:
  - SAST (Semgrep): clean or only low/medium
  - SCA (Snyk + pip-audit): no known-exploitable vulns in deps
  - Secret-scan (Gitleaks): clean
  - Input validation: Pydantic on all external responses verified
  - Parameterized queries: SQLAlchemy ORM only, no raw SQL
- [ ] **Gate verdict:** GO / NO-GO with explicit reasoning
- [ ] Report to CEO in-session (task output)

---

## Verification Checklist

| Check | Tool | Threshold | Status |
|---|---|---|---|
| SAST | Semgrep (p/security-audit + custom) | 0 high/critical | ☐ |
| SCA | Snyk + pip-audit | 0 known-exploitable | ☐ |
| Secrets | Gitleaks | 0 findings | ☐ |
| Input validation | Code review | Pydantic on all external calls | ☐ |
| SQL safety | Code review | SQLAlchemy ORM only | ☐ |
| Tests pass | pytest | 100% pass | ☐ |
| CI passes | GitHub Actions | All jobs green | ☐ |
| BA docs | PM sign-off | Approved | ☐ |

---

## Dependencies

- `vnstock-advisor-4-dev-data-ingest` (DEV done)
- `vnstock-advisor-7-tester-data-ingest` (TESTER done)
- `vnstock-advisor-2-ba-data-ingest` (BA docs approved)
- Can run in parallel with `vnstock-advisor-10-qa-analysis-engine`