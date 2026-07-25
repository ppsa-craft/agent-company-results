# Task: tech-analysis-140-05-m2a-security-gate

**Task ID**: T-140-05
**Title**: M2A Security Gate (QA)
**Role**: QA
**Status**: READY
**Assigned Agent**: qa-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature (security gate part of DoD)

## File Ownership (Architecture Seam: M2A Core Indicators Service)
- `workspace/apps/tech-analysis/security/m2a-gate-report.md`

## Goal
Execute security gate for M2A Core Indicators Service (T-140-01) per Tier 2 security requirements. Block ship on high/critical findings.

## Acceptance Criteria
- Security gate report `workspace/apps/tech-analysis/security/m2a-gate-report.md` completed with:
  - Secret scan: `gitleaks detect` — clean (no secrets in code/history)
  - Dependency scan: `snyk test` / `npm audit` — no critical/high CVEs in deps
  - SAST: `semgrep --config=auto` — no high/critical findings
  - Input validation review: all external inputs validated (Zod schemas present)
  - Output encoding review: no XSS vectors in HTTP responses
  - AuthN/Z review: gRPC/HTTP endpoints require auth, rate limits configured
  - Secrets management: no hardcoded secrets, env vars used
  - Crypto review: no custom crypto, TLS enforced for gRPC/HTTP
  - SBOM generated: `syft packages . -o spdx-json`
- Report verdict: PASS / FAIL (high/critical = FAIL, blocks ship)
- If FAIL: specific findings listed with file:line, CVE IDs, remediation guidance

## Security Checks (Tier 2 proportional)
| Check | Tool | Severity Gate |
|-------|------|---------------|
| Secret scanning | gitleaks | Any = FAIL |
| SCA (deps) | snyk/npm audit | Critical/High = FAIL |
| SAST | semgrep | High/Critical = FAIL |
| Input validation | Manual review | Missing = FAIL |
| AuthN/Z | Manual review | Missing = FAIL |
| TLS enforcement | Manual review | Missing = FAIL |
| SBOM | syft | Generated = required |

## Execution Steps
1. Checkout T-140-01 branch in isolated worktree
2. Run `gitleaks detect --source . --verbose`
3. Run `npm audit --audit-level=high` and `snyk test --severity-threshold=high`
4. Run `semgrep --config=auto --error --json=semgrep-results.json`
4. Manual review: input validation (Zod schemas on all endpoints), auth middleware, rate limiting, TLS config
5. Generate SBOM: `syft packages . -o spdx-json=m2a-sbom.spdx.json`
6. Compile report with findings table and verdict
7. Report verdict to PM (blocks T-140-01 ship if FAIL)

## Deliverables
- `workspace/apps/tech-analysis/security/m2a-gate-report.md` — complete report
- SBOM: `workspace/apps/tech-analysis/security/m2a-sbom.spdx.json`
- Semgrep SARIF: `workspace/apps/tech-analysis/security/m2a-semgrep.sarif`

## DoD Tier 2 Checklist
- [ ] All automated scans executed
- [ ] Manual review completed
- [ ] Report verdict recorded (PASS/FAIL)
- [ ] If FAIL: findings documented with remediation
- [ ] Report delivered to PM