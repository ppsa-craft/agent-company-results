# Task: tech-analysis-140-10-m2b-security-gate

**Task ID**: T-140-10
**Title**: M2B Security Gate (QA)
**Role**: QA
**Status**: READY
**Assigned Agent**: qa-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M2B Data Pipeline Service)
- `workspace/apps/tech-analysis/security/m2b-gate-report.md`

## Goal
Execute security gate for M2B Data Pipeline Service (T-140-06) per security mandate §7.2.

## Acceptance Criteria
- Security gate report completed with:
  - SAST: Semgrep scan clean (no high/critical)
  - SCA: Snyk scan clean (no high/critical vulns in deps)
  - Secret scan: Gitleaks clean (no secrets in code/history)
  - Input validation: All external inputs (source APIs, gRPC, HTTP) validated/sanitized
  - Output encoding: HTTP responses properly encoded (XSS prevention)
  - AuthN/AuthZ: gRPC/HTTP endpoints have auth (or documented exception)
  - Rate limiting: Source APIs and public endpoints rate limited
  - Secrets management: No hardcoded secrets, uses secret manager
  - TLS: gRPC/HTTP over TLS in production config
  - CORS: HTTP gateway CORS policy restrictive
  - Logging: No PII/sensitive data in logs
- Gate result: PASS / FAIL (blocks ship if FAIL with high/critical)

## Security Checks (per §7.2 Security Mandate)
1. **SAST** — Run Semgrep with custom rules + defaults on `services/m2b-data-pipeline/`
2. **SCA** — Run Snyk on `package.json` + lockfile
3. **Secrets** — Run Gitleaks on repo history + working tree
4. **Input Validation** — Review all external input boundaries:
   - Source API responses (VNDirect, CafeF, VietStock)
   - gRPC requests (GetBars, SubscribeBars)
   - HTTP query params (symbol, timeframe, from, to)
   - Config/env vars
5. **Output Encoding** — HTTP JSON responses, ensure charset, no injection
6. **Auth** — gRPC: mutual TLS or token; HTTP: JWT/API key
7. **Rate Limiting** — Token bucket per source IP + per API key
8. **Secrets** — DB creds, API keys in Vault/secret manager, not .env
9. **TLS** — Production config requires TLS certs
10. **CORS** — Restrict to known origins
11. **Logging** — Redact symbols? No, but redact API keys, tokens, passwords

## Deliverables
- `workspace/apps/tech-analysis/security/m2b-gate-report.md` with:
  - Executive summary: PASS/FAIL
  - Tool outputs (Semgrep, Snyk, Gitleaks) attached/summarized
  - Manual review findings per check above
  - Remediation items for any MEDIUM/LOW (tracked as backlog)
  - High/critical = FAIL, must fix before ship

## DoD Tier 2 Checklist
- [ ] All automated scans run and clean (high/critical)
- [ ] Manual review completed
- [ ] Report written and PASS/FAIL recorded
- [ ] If FAIL: blocking issues communicated to DEV-2 with reproduction