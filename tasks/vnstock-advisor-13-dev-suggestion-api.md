# Task: vnstock-advisor-13-dev-suggestion-api

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: suggestion-api service)
**Status:** ready

---

## Goal

Implement the `suggestion-api` service per BA docs: REST API (Fastify/Node.js) that authenticates users via JWT RS256, calls `analysis-engine` `/rank` endpoint, returns ranked suggestions with reasoning and mandatory disclaimer.

---

## Acceptance Criteria (traceable to use cases)

- [ ] UC-SA-1: `GET /suggestions` returns ranked suggestions for authenticated user's portfolio
- [ ] UC-SA-2: JWT RS256 authentication — token validation, expiry (15min), refresh flow, JWKS endpoint
- [ ] UC-SA-3: Portfolio input (symbols + optional weights) → ranked suggestions with reasoning from analysis-engine
- [ ] UC-SA-4: Mandatory disclaimer on every response ("informational only — not financial advice") in header `X-Disclaimer` and body field `disclaimer`
- [ ] UC-SA-5: Rate limiting and error responses per Problem Details (RFC 7807)
- [ ] API contract matches `workspace/apps/vnstock-advisor/docs/api/suggestion-api.openapi.yaml` exactly
- [ ] Auth/z rules match `workspace/apps/vnstock-advisor/docs/specs/auth.md`
- [ ] Disclaimer text matches `workspace/apps/vnstock-advisor/docs/compliance/disclaimer.md`
- [ ] Error catalog matches `workspace/apps/vnstock-advisor/docs/specs/errors.md`
- [ ] Tests pass (unit + integration + contract), README works verbatim
- [ ] Security gate: secret-scan clean, SAST clean, SCA clean, OWASP API checks pass

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/suggestion-api/` — isolated Fastify/TypeScript service. Touches: `services/suggestion-api/src/main.ts` (app entry), `services/suggestion-api/src/routes/suggestions.ts`, `services/suggestion-api/src/routes/auth.ts`, `services/suggestion-api/src/routes/health.ts`, `services/suggestion-api/src/middleware/auth.ts`, `services/suggestion-api/src/middleware/rate-limit.ts`, `services/suggestion-api/src/clients/analysis-engine.ts`, `services/suggestion-api/src/utils/disclaimer.ts`, `services/suggestion-api/src/utils/errors.ts`, `services/suggestion-api/tests/`. **Shared:** calls `analysis-engine` `/rank` via typed client; reads JWT config from env; uses shared TypeScript types from `shared/typescript/src/`. **No overlap with analysis-engine or web-ui.**

Ordered subtasks:
1. [ ] Scaffold Fastify project with TypeScript, ESLint, Prettier, Vitest
2. [ ] Implement JWT RS256 auth middleware (verify access token, JWKS endpoint, refresh flow)
3. [ ] Implement typed client for `analysis-engine` `/rank` endpoint (with timeout, retry, circuit breaker)
4. [ ] Implement `GET /suggestions` route: validate portfolio input → call analysis-engine → attach disclaimer → return ranked list
5. [ ] Implement `POST /auth/login`, `POST /auth/refresh`, `GET /auth/jwks` routes
6. [ ] Implement `GET /health` route
6. [ ] Add rate limiting middleware (per-tenant, configurable)
7. [ ] Add Problem Details error handling (RFC 7807) for all error responses
8. [ ] Add disclaimer utility: inject `X-Disclaimer` header + `disclaimer` body field on all suggestion responses
9. [ ] Add comprehensive tests (unit: auth, client, disclaimer; integration: full flow; contract: OpenAPI compliance)
10. [ ] Write README with exact run steps (Docker Compose local dev)
11. [ ] Run security checks (npm audit, Snyk, Gitleaks, Semgrep)

---

## Test Plan (for TESTER)

**Scenario: Authenticated suggestions flow**
- Steps: Login via `/auth/login` → get access token → call `GET /suggestions` with portfolio → verify response
- Expected: 200 OK, ranked list with reasoning, `X-Disclaimer` header present, `disclaimer` field in body

**Scenario: JWT RS256 validation**
- Steps: Call `/suggestions` with invalid/expired/malformed token
- Expected: 401 with Problem Details error; RS256 only (reject `none`/`HS256`)

**Scenario: Token refresh flow**
- Steps: Use refresh token via `/auth/refresh` → get new access token → call `/suggestions`
- Expected: New access token works; old access token rejected after expiry

**Scenario: Disclaimer mandate**
- Steps: Inspect every suggestion response (success, error, empty)
- Expected: `X-Disclaimer` header + `disclaimer` body field on ALL responses, exact text matches compliance doc

**Scenario: Rate limiting**
- Steps: Exceed rate limit on `/suggestions`
- Expected: 429 with Problem Details, `Retry-After` header

**Scenario: Analysis-engine failure handling**
- Steps: Mock analysis-engine returning 5xx/timeout
- Expected: 503/504 with Problem Details, no stack trace leakage

**Scenario: Input validation**
- Steps: Call `/suggestions` with invalid portfolio (empty symbols, invalid weights)
- Expected: 400 with Problem Details, Zod validation errors

**Edge cases:** Empty portfolio, all symbols filtered out, analysis-engine returns empty ranking, concurrent requests, token rotation mid-request

---

## Dependencies

- `vnstock-advisor-11-ba-suggestion-api` (BA docs + OpenAPI contract ready)
- `vnstock-advisor-3-ba-analysis-engine` (analysis-engine `/rank` contract frozen)
- `vnstock-advisor-5-dev-analysis-engine` (analysis-engine running for integration tests)
- Feeds: `vnstock-advisor-15-tester-suggestion-api`, `vnstock-advisor-17-qa-suggestion-api`