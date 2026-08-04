# Task: vnstock-advisor-9-qa-analysis-engine

**Role:** QA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine service quality gate)
**Status:** ready

---

## Goal

Run the quality and security gate for `analysis-engine` service. Validate DoD Tier 2 artifact completeness, test coverage (both flows), README verbatim, best practices, and security gate.

---

## Acceptance Criteria (traceable to use cases)

- [ ] DoD Tier 2 artifact set complete: use cases, BA docs, code, tests, README, analytics plan
- [ ] Automated test suite exists, runnable via one command (`pytest`), passes
- [ ] Test coverage includes BOTH happy path AND failure/edge paths (not happy-path-only)
- [ ] TESTER's README-verbatim run succeeded (confirmed)
- [ ] CTO stack best practices met (project structure, deps, error handling, security basics)
- [ ] Security gate clear:
  - Secret-scan clean (gitleaks)
  - Dependency/SCA + SBOM clean of known-exploitable CVEs (Snyk)
  - SAST clean of high/critical (semgrep)
  - No dependency confusion
  - OWASP API Top 10 checks for API surface
- [ ] No unresolved high/critical findings
- [ ] Verdict: GO or NO-GO with specific findings

---

## Dependencies

- `vnstock-advisor-5-dev-analysis-engine` (code complete)
- `vnstock-advisor-7-tester-analysis-engine` (TESTER pass confirmed)
- **BLOCKED** until `vnstock-advisor-3-ba-analysis-engine` completes (needs BA docs for traceability)
- Runs in parallel with: `vnstock-advisor-8-qa-data-ingest`