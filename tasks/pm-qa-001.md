# Task: pm-qa-001 — Quality + Security Gate Checklists per Service

## Metadata
- **ID**: pm-qa-001
- **Role**: QA
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1
- **Assignee**: qa
- **Depends on**: techlead-001 (Threat Models + Contracts), cto-001 (Stack Decision)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
Create Quality Gate and Security Gate Checklists for S1, S2, S3, S4

## Description
Produce the QA checklists that each service must pass before being considered "done" and shippable. Includes code quality, testing, security, and operational readiness criteria.

## Acceptance Criteria
- [ ] **S1 Quality Gate**: 
  - [ ] Unit test coverage ≥ 80% (normalization, adapters, persistence)
  - [ ] Integration tests: adapter→normalization→Redis→Postgres→API
  - [ ] Contract tests: S1→S2 schema verified via Pact
  - [ ] Security: Secret scan clean, SAST clean, dependency scan clean, input validation on all adapters
  - [ ] Observability: Health, metrics (Prometheus), structured logs, tracing headers
  - [ ] Docs: README with run instructions, API spec published, ADR for key decisions
- [ ] **S2 Quality Gate**:
  - [ ] Unit test coverage ≥ 85% (indicators, signal generation)
  - [ ] Property tests pass (Hypothesis)
  - [ ] Contract tests: S2→S3 signal schema verified
  - [ ] Security: No unsafe deserialization, input validation on Redis consumption
  - [ ] Observability: Computation latency histograms, error counters
  - [ ] Docs: Indicator library API docs, signal schema reference
- [ ] **S3 Quality Gate**:
  - [ ] Load test: 1000 req/s, p99 < 100ms, error rate < 0.1%
  - [ ] Circuit breaker integration test passes
  - [ ] Contract tests: S3→S4 API schema verified
  - [ ] Security: Rate limit bypass tests, JWT validation tests, CORS config verified
  - [ ] Observability: Request latency, upstream health, cache hit rate, breaker state
  - [ ] Docs: Gateway routing config, auth integration guide
- [ ] **S4 Quality Gate**:
  - [ ] E2E tests: Critical user flows (login, dashboard, live signals)
  - [ ] Accessibility: axe-core WCAG 2.1 AA
  - [ ] Visual regression: Baseline approved
  - [ ] Security: CSP headers, no XSS vectors, token handling verified
  - [ ] Performance: Lighthouse CI budgets met
  - [ ] Docs: Component storybook, deployment guide
- [ ] **Cross-Cutting**: All services have Dockerfile, CI/CD green, SBOM generated

## Verification
- Checklists executed by QA before any service ships
- Results recorded in `workspace/reports/qa-gate-<service>.md`
- No-go items block deployment (CEO ratifies but never overrides)

## Security Notes
- Security gate is a HARD gate — unresolved high/critical = no ship
- SAST: Semgrep custom rules + defaults
- SCA: Snyk + SBOM (CycloneDX)
- Secret scan: Gitleaks