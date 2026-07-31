# Task: vnstock-advisor-10-qa-analysis-engine

**Role:** QA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine security + quality gate)
**Status:** ready

---

## Goal

Enforce quality and security gate for `analysis-engine` service per §7.2.1. Verify all DoD artifacts present, security tools clean, no high/critical findings.

---

## Acceptance Criteria

- [ ] **Quality gate:** All DoD tier 2 artifacts present:
  - Implementation complete (DEV verdict PASS)
  - Tests pass (TESTER verdict PASS)
  - BA docs approved (UC, indicators, screening, ranking, fixtures)
  - README runnable in clean checkout
  - CI workflow passes (lint, type-check, test)
- [ ] **Security gate (§7.2.1):** No unresolved high/critical findings:
  - SAST (Semgrep): clean or only low/medium
  - SCA (Snyk + pip-audit): no known-exploitable vulns in deps
  - Secret-scan (Gitleaks): clean
  - Input validation: Pydantic on all query params verified
  - Parameterized queries: SQLAlchemy ORM only
  - Rate-limit: per-tenant limit enforced
  - Timeout guard: computation bounded
- [ ] **Gate verdict:** GO / NO-GO with explicit reasoning
- [ ] Report to CEO in-session

---

## Verification Checklist

| Check | Tool | Threshold | Status |
|---|---|---|---|
| SAST | Semgrep (p/security-audit + custom) | 0 high/critical | ☐ |
| SCA | Snyk + pip-audit | 0 known-exploitable | ☐ |
| Secrets | Gitleaks | 0 findings | ☐ |
| Input validation | Code review | Pydantic on query params | ☐ |
| SQL safety | Code review | SQLAlchemy ORM only | ☐ |
| Rate-limit | Code review | Per-tenant enforced | ☐ |
| Timeout guard | Code review | asyncio.wait_for bounded | ☐ |
| Tests pass | pytest | 100% pass | ☐ |
| CI passes | GitHub Actions | All jobs green | ☐ |
| BA docs | PM sign-off | Approved | ☐ |

---

## Dependencies

- `vnstock-advisor-5-dev-analysis-engine` (DEV done)
- `vnstock-advisor-8-tester-analysis-engine` (TESTER done)
- `vnstock-advisor-3-ba-analysis-engine` (BA docs approved)
- Can run in parallel with `vnstock-advisor-9-qa-data-ingest`