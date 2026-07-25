# Task: tech-analysis-140-15-m3a-security-gate

**Task ID**: T-140-15
**Title**: M3A Security Gate (QA)
**Role**: QA
**Status**: READY
**Assigned Agent**: qa-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership
- `workspace/apps/tech-analysis/security/m3a-gate-report.md`

## Goal
Execute security gate for M3A Alert Rule Engine (T-140-11).

## Acceptance Criteria
- Security gate report completed with:
  - Secret scan (gitleaks): clean
  - SCA (snyk/npm audit): no critical/high CVEs
  - SAST (semgrep): no high/critical findings
  - Input validation: Rule AST validated on create/update (Zod schema rejects malicious ASTs)
  - AuthN/Z: gRPC/HTTP require JWT, role-based (admin: write, user: read)
  - Rate limiting: rule CRUD 100/min, evaluation internal
  - NATS: auth enabled, TLS enforced
  - No custom crypto, TLS for all external connections
  - SBOM generated (syft)
- Verdict: PASS / FAIL (high/critical = FAIL, blocks ship)
- If FAIL: findings with file:line, remediation

## Security Checks (Tier 2)
| Check | Tool | Gate |
|-------|------|------|
| Secrets | gitleaks | Any = FAIL |
| Dependencies | snyk/npm audit | Critical/High = FAIL |
| SAST | semgrep --config=auto | High/Critical = FAIL |
| Input Validation | Manual review | Missing = FAIL |
| AuthN/Z | Manual review | Missing = FAIL |
| NATS Security | Manual review | Missing = FAIL |
| TLS | Manual review | Missing = FAIL |
| SBOM | syft | Generated = required |

## Execution
1. Checkout T-140-11 branch in isolated worktree
2. Run automated scans
3. Manual review: rule AST validation, auth middleware, rate limit config, NATS config, TLS config
4. Generate SBOM: `syft packages . -o spdx-json=m3a-sbom.spdx.json`
5. Compile report with verdict
6. Report to PM

## Deliverables
- `workspace/apps/tech-analysis/security/m3a-gate-report.md`
- SBOM: `workspace/apps/tech-analysis/security/m3a-sbom.spdx.json`
- Semgrep SARIF: `workspace/apps/tech-analysis/security/m3a-semgrep.sarif`

## DoD Tier 2 Checklist
- [ ] All scans executed
- [ ] Manual review completed
- [ ] Report verdict recorded
- [ ] If FAIL: findings documented
- [ ] Report delivered to PM