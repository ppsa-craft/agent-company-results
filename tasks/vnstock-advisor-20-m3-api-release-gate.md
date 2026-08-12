# Task vnstock-advisor-20 — M3 API Release Gate

- **Role:** qa — **Product:** vnstock-advisor — **Assignee:** _ready_ — **DoD tier:** gate task (validates 15/16/17 DoD tiers + §7.2)

## Goal
Run QA's ship gate on the M3 API release: validate DoD tier assignments (15/16 Tier 2, 17 Tier 1 — flag any mislabeled), the full Tier-1 artifact table for 17, and the §7.2 security gate. No-go blocks the merge; CEO ratifies but never overrides security no-gos.

## Gate checklist
- **Quality:** use cases trace to ACs; README works verbatim in clean checkout (TESTER 18 pass confirms); tests green; artifact table complete for Tier 1.
- **Security:** secret-scan clean (gitleaks), SCA clean of known-exploitable vulns + SBOM (snyk), SAST clean of high/critical (semgrep), OWASP-appropriate checks on the API/auth surface (JWT negative matrix, rate limiting, input validation, RFC 7807 no-stack-traces). Unresolved high/critical = security no-go.
- **Seam compliance:** weights-override frozen schema honored; auth middleware interface pin held; rate-limit owned by M3-A; disclaimer from single source; openapi matches frozen contract (no `screening` field).
- **Business-impact:** if TECHLEAD flags `BUSINESS-IMPACT`, hand the wanted/unwanted judgment to PM for approval before GO.

## Output
Gate verdict: GO / NO-GO with findings, each mapped to the blocking task id. Log lower-severity findings as prioritized backlog items for PM.

## Report to PM at end: verdict, findings, task status, blockers.
