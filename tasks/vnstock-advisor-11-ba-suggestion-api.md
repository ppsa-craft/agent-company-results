# Task: vnstock-advisor-11-ba-suggestion-api

**Role:** BA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: suggestion-api use cases + API contract)
**Status:** ready

---

## Goal

Produce BA documentation for `suggestion-api` service: use cases, API contract (OpenAPI), authentication/authorization rules, disclaimer integration, and error handling patterns.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Use case document: `workspace/apps/vnstock-advisor/docs/use-cases/suggestion-api.md` covering:
  - UC-SA-1: Authenticated user requests ranked suggestions via `GET /suggestions`
  - UC-SA-2: JWT RS256 authentication — token validation, expiry, refresh flow
  - UC-SA-3: Portfolio input (symbols + optional weights) → ranked suggestions with reasoning
  - UC-SA-4: Mandatory disclaimer on every response ("informational only — not financial advice")
  - UC-SA-5: Rate limiting and error responses per Problem Details (RFC 7807)
- [ ] API contract: `workspace/apps/vnstock-advisor/docs/api/suggestion-api.openapi.yaml` — complete OpenAPI 3.1 spec for `/suggestions`, `/auth/*`, `/health`
- [ ] Auth/z rules: `workspace/apps/vnstock-advisor/docs/specs/auth.md` — JWT claims, scopes, RS256 only, short expiry + refresh rotation, JWKS endpoint
- [ ] Disclaimer integration: exact text, placement (response header + body), localization (VN/EN) per `docs/compliance/disclaimer.md`
- [ ] Error catalog: `workspace/apps/vnstock-advisor/docs/specs/errors.md` — all error codes, HTTP status, Problem Details shape
- [ ] All docs reviewed and approved by PM

---

## Implementation Plan (for BA)

1. Define use cases with actors, preconditions, postconditions, and error flows
2. Design OpenAPI contract for `/suggestions` endpoint (request: portfolio input; response: ranked list + reasoning + disclaimer)
3. Define JWT auth flow: login/refresh, token structure, RS256 verification, JWKS
4. Specify disclaimer integration per existing framework
5. Define error catalog with Problem Details format
6. Get PM sign-off

---

## Test Plan (for TESTER)

**Scenario: API contract completeness**
- Steps: Verify OpenAPI spec covers all endpoints, request/response schemas, auth, error responses
- Expected: No missing endpoints; all schemas reference shared types; auth documented as Bearer JWT

**Scenario: Disclaimer mandate**
- Steps: Verify spec requires disclaimer in response header `X-Disclaimer` and body field `disclaimer`
- Expected: Both present, exact text matches `docs/compliance/disclaimer.md`

**Scenario: Auth contract**
- Steps: Verify `/auth/login`, `/auth/refresh`, `/auth/jwks` endpoints defined with correct schemas
- Expected: RS256 only; `alg` claim enforced; short access token (15m) + refresh rotation documented

---

## Dependencies

- `vnstock-advisor-3-ba-analysis-engine` (needs analysis-engine `/rank` contract frozen)
- `vnstock-advisor-2-ba-data-ingest` (needs disclaimer framework)
- Output feeds: `vnstock-advisor-13-dev-suggestion-api`, `vnstock-advisor-15-tester-suggestion-api`