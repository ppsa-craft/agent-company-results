# Use Cases: Suggestion API Service

**Product:** vnstock-advisor  
**Component:** suggestion-api  
**Version:** 1.0  
**Status:** Draft — pending PM sign-off  
**PM Sign-off:** _awaiting_

---

## Overview

The `suggestion-api` service exposes a read-only, authenticated HTTP API that lets a client submit a portfolio (a set of symbols with optional weights) and receive it mapped into ranked suggestions with human-readable reasoning and mandatory disclaimer framing. It relies on the analysis-engine `/rank` contract (frozen, `specs/screening-ranking.md` + `use-cases/analysis-engine.md` UC-AE-3) for the underlying ranking computation, and on the compliance `disclaimer` framework (`compliance/disclaimer.md`) for the mandatory "informational only — not financial advice" wrapper.

The service is the M3 north-facing seam: it owns authentication (`/auth/*`), the suggestion endpoint (`GET /suggestions`), and health reporting (`GET /health`). Every suggestion response carries the disclaimer both in the `X-Disclaimer` response header and in the `meta.disclaimer` body object, in both `vi-VN` and `en-US` per `compliance/disclaimer.md`.

---

## Actors

| Actor | Description |
|-------|-------------|
| **Authenticated User** | Signed-in consumer (web-ui, mobile, API client) holding a valid RS256 JWT access token with the `suggestions:read` scope |
| **Web UI** | The M3 browser front-end that logs in via `/auth/login`, stores tokens, and calls `GET /suggestions` on behalf of the end user |
| **Analysis Engine** | Internal `analysis-engine` service whose frozen `/rank` contract supplies the ranked list + reasoning (dependency) |
| **Monitoring System** | Probes `GET /health` for liveness/readiness |
| **Anonymous Client** | Unauthenticated requester; must complete `/auth/login` first |

---

## UC-SA-1: Authenticated User Requests Ranked Suggestions via GET /suggestions

### Actor

Authenticated User (via Web UI or API client) holding a valid access token.

### Description

The authenticated user calls `GET /suggestions` with an `Authorization: Bearer <access_token>` header and receives the ranked suggestion list with reasoning, plus the mandatory disclaimer in the `X-Disclaimer` header and `meta.disclaimer` body.

### Preconditions

- Client holds a valid, unexpired RS256 JWT access token with `suggestions:read` scope (obtained via UC-SA-2)
- Token signature verifies against the JWKS keys at `GET /auth/jwks`
- At least one invitation to rank is available (symbols are defaulted to the analysis universe if not supplied)

### Main Flow

1. Client calls `GET /suggestions` with `Authorization: Bearer <access_token>`.
2. API authenticates the token (UC-SA-2 validation rules).
3. API authorizes: token scope must include `suggestions:read`.
4. API resolves the portfolio input (from query params, or defaults to the analysis universe).
5. API calls analysis-engine `POST /rank` with the resolved symbols, optional weights (UC-SA-3).
6. API maps the ranked result into the suggestion response shape (adds per-symbol display metadata, e.g., latest price if available upstream).
7. API attaches the disclaimer: response header `X-Disclaimer` + `meta.disclaimer` (both locales).
8. API returns `200 OK` with the ranked list, `meta.generated_at`, `meta.source`, and `meta.disclaimer`.

### Postconditions

- Response `200 OK` containing `ranked[]` (each with `rank`, `symbol`, `composite_score`, `components`, `reasoning`, `sub_components`) and `excluded[]` (when applicable).
- `X-Disclaimer` header present and matching `compliance/disclaimer.md` text for the negotiated locale.
- `meta.disclaimer` object present with both `vi-VN` and `en-US` full text.
- `meta.generated_at` and `meta.source` populated for freshness/traceability.

### Success / Error Flows

- **200 OK** — successful response (happy path).
- **401 Unauthorized** — missing/invalid/expired token → `ProblemDetails` (`auth.token_missing` / `auth.token_invalid` / `auth.token_expired`).
- **403 Forbidden** — token valid but lacks `suggestions:read` scope → `auth.scope_denied`.
- **422 Unprocessable** — malformed/empty symbol list, invalid weights → `validation.portfolio_invalid`.
- **429 Too Many Requests** — rate limit exceeded → `rate_limit.exceeded`.

### Acceptance Criteria

- AC-SA-1.1: `GET /suggestions` returns `200 OK` with a ranked list when the access token is valid and carries `suggestions:read`.
- AC-SA-1.2: Every successful response includes `X-Disclaimer` header, `meta.disclaimer`, `meta.generated_at`, `meta.source`.
- AC-SA-1.3: Request with no token returns `401`; request with a token missing the scope returns `403`.
- AC-SA-1.4: No orphan — the endpoint maps 1:1 to UC-SA-3 (portfolio→ranked) and UC-SA-2 (auth).

---

## UC-SA-2: JWT RS256 Authentication — Token Validation, Expiry, Refresh Flow

### Actor

Authenticated User / Web UI initiating login or refresh.

### Description

The user authenticates via `POST /auth/login`, receives a short-lived RS256 access token (15 minutes) plus a rotating refresh token; thereafter the Web UI refreshes automatically via `POST /auth/refresh`, and the server validates every protected call against the JWKS public keys at `GET /auth/jwks`.

### Preconditions

- User has credentials (or Web UI acts on behalf of the user via the configured identity provider path).
- Server holds the RS256 private key (`kid` published in JWKS).
- The service has a JWKS endpoint reachable by token verifiers.

### The Flow

1. Client calls `POST /auth/login` with credentials → server validates and issues:
   - `access_token` (JWT RS256, `exp` = 15 min)
   - `refresh_token` (opaque, server-persisted, single-use)
2. Client presents `access_token` as `Bearer` on `GET /suggestions`.
3. Server verifies the token: RS256 `alg` is enforced (no `none`, no symmetric downgrade), signature checked against `GET /auth/jwks` keys, `exp` and `iat` nbf validated, required claims present.
4. On expiry / near-expiry, client calls `POST /auth/refresh` with the current `refresh_token`.
5. Server **rotates**: the presented refresh token is revoked (single-use) and a new `(access_token, refresh_token)` pair is issued.
6. On reuse of a revoked refresh token, the whole session is terminated (token-family detection).

### Postconditions

- Valid token grants access; invalid/expired/scope-insufficient token is rejected with the appropriate Problem Details error.
- Refresh returns a new token pair; the used refresh token is no longer valid.
- Reuse of an old (rotated) refresh token triggers session revocation.

### Error Flows

- `401 auth.token_expired` — access token `exp` passed.
- `401 auth.token_invalid` — bad `alg`, bad signature, malformed JWT.
- `401 auth.refresh_invalid` — unknown/revoked/already-rotated refresh token.
- `409 auth.refresh_reuse` — reuse of a rotated refresh token (token family breach).

### Acceptance Criteria

- AC-SA-2-01: Only RS256 is accepted; a token with any other `alg` is rejected.
- AC-SA-2-02: Access token `exp` is 15 minutes from issue.
- AC-SA-2-03: Refresh rotates — the old refresh token becomes invalid after use.
- AC-SA-2-04: Reusing a rotated refresh token revokes the family (fails closed).
- AC-SA-2-05: `/auth/jwks` returns the public JWK(s) used to verify RS256 tokens.

---

## UC-SA-3: Portfolio Input (Symbols + Optional Weights) → Ranked Suggestions with Reasoning

**Description**

The client supplies the portfolio: a list of symbols and optionally custom weights. The API passes these to analysis-engine `POST /rank` (UC-AE-3 / `screening-ranking.md`), and returns the ranked list with per-symbol `reasoning`.

### Preconditions

- Valid authenticated request (UC-SA-1).
- Analysis-engine `/rank` contract frozen and reachable.
- When custom weights supplied: sum to 1.0 (tolerance ±0.001), each in `[0.0, 1.0]`.

### The Flow

1. Client supplies portfolio: `symbols[]` (required or default universe) and optional `weights {momentum, trend, volume, volatility}`.
2. API validates portfolio (non-empty, known symbol format, weights valid).
3. API calls `POST /rank` with `/rank` contract payload: `{symbols, date?, algorithm_version?, weights?}`.
4. `/rank` returns `ranked[]` (rank/composite/components/sub_components/reasoning) and `excluded[]`.
5. API wraps the ranked list in the suggestion response envelope; reason array is passed through untouched from `/rank`.

### Postconditions

- Response includes ranked suggestions with full reasoning arrays.
- Custom weights honored / default weights used when absent.
- Excluded symbols surfaced in `excluded[]` (not silently dropped).

### Error Flows

- **400 validation.symbols_empty** — empty symbol list.
- **422 validation.weights_invalid** — weights do not sum to 1, or out of range.
- **502 upstream.rank_failed** — analysis-engine `/rank` is down or errors.

### Acceptance Criteria

- AC-SA-3-1: Portfolio input (symbols + optional weights) yields a ranked suggestion list with reasoning.
- AC-SA-3-2: Each ranked entry includes `rank`, `symbol`, `composite_score`, `components`, `reasoning`.
- AC-SA-3-3: Excluded symbols returned (not dropped).
- AC-SA-3-4: Invalid portfolio (empty symbols / bad weights) is rejected with a validation error.

---

## UC-SA-4: Mandatory Disclaimer on Every Response

**Description**

Every suggestion response must carry the compliance disclaimer — both in the `X-Disclaimer` response header and in the `meta.disclaimer` body object — in `/vi-VN` and `en-US`. This is a hard, non-optional requirement per `compliance/disclaimer.md`.

### The Flow

1. After building any suggestion response, the API appends:
   - `X-Disclaimer` header (short/full VN+EN per negotiation)
   - `meta.disclaimer = { "vi-VN": <full VN>, "en-US": <full EN> }`
2. The text is sourced from the single source of truth in `compliance/disclaimer.md` (no hardcoded duplicates).

### Error Flows / Guardrails

- A suggestion response missing `meta.disclaimer` **fails the contract test** (no silent pass).
- No dismissible/hide mechanism on any UI; disclaimer is non-removable.

### Acceptance Criteria

- AC-SA-4-1: Every `/suggestions` response present contains `X-Disclaimer` header.
- AC-SA-4-2: Every `meta.disclaimer` object contains both locales (`vi-VN`, `en-US`).
- AC-SA-4-3: Disclaimer text matches `compliance/disclaimer.md` exactly (single source of truth).
- AC-SA-4-4: Test fails if `meta.disclaimer` missing from any suggestion response.

---

## UC-SA-5: Rate Limiting and Error Responses per Problem Details (RFC 7807)

**Description:** The API enforces per-user rate limits and returns all errors as `application/problem+json` following RFC 7807.

### RateLimiting

- Per-user (identified by `sub`), per-endpoint bucket.
- Default: `SUGGESTIONS_RATE_LIMIT` (e.g., 100 req / 15 min) per user for `/suggestions`.
- `GET /health` is exempt from rate limiting.
- `Retry-After` header returned on 429.

### Problem Details (RFC 7807) Shape

```json
{
  "type": "https://api.vnstock-advisor.dev/problems/rate_limit_exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "Too many requests. Retry after <Retry-After>.",
  "instance": "/suggestions",
  "code": "rate_limit.exceeded"
}
```

### Error Flows

- `429 rate_limit.exceeded` with `Retry-After`.
- `4xx/5xx` all as Problem Details (`application/problem+json`, RFC 7807). See `specs/errors.md` catalog.

### Acceptance Criteria

- AC-SA-5-1: Exceeding the rate limit returns `429` with a `Retry-After` header and a Problem Details body.
- AC-SA-5-2: All errors use `application/problem+json` (RFC 7807) with `type`, `title`, `status`, `detail`, `instance`.
- AC-SA-5-3: Rate limit keyed per user, not per client.

---

## Traceability Matrix

| Use Case | AC IDs | Feeds Task |
|----------|--------|------------|
| UC-SA-1 | AC-SA-1-01 .. 1-04 | `vnstock-advisor-13-dev-suggestion-api` (GET /suggestions) |
| UC-SA-2 | AC-SA-2-01 .. 2-05 | `vnstock-advisor-13-dev-suggestion-api` (auth endpoints, JWKS) |
| UC-SA-3 | AC-SA-3-01 .. 3-04 | `vnstock-advisor-13-dev-suggestion-api` (portfolio→rank mapping) |
| UC-SA-4 | AC-SA-4-01 .. 4-04 | `vnstock-advisor-13-dev-suggestion-api` (disclaimer middleware) |
| UC-SA-5 | AC-SA-5-01 .. 5-03 | `vnstock-advisor-13-dev-suggestion-api` (rate limit + errors) |

**Dependencies:** `vnstock-advisor-3-ba-analysis-engine` (`/rank` contract), `vnstock-advisor-2-ba-data-ingest` (disclaimer framework), `specs/auth.md`, `specs/errors.md`, `api/suggestion-api.openapi.yaml`.

**Orphans / gaps flagged:** None internal. External gap — the portfolio `weights` override maps on to analysis-engine `POST /rank` (UC-AE-3). Confirm the exact `/rank` request schema (field names, weights sum-to-1 rule, `weights` override contract) is frozen before DEV starts `vnstock-advisor-13-dev-suggestion-api`.

---

*Document status: Draft — awaiting PM review. PM to add sign-off line above when approved.*