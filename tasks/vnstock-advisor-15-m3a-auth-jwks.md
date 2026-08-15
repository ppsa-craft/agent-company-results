# Task vnstock-advisor-15 — M3-A: Auth + Hardening (JWT RS256 + JWKS)

- **Role:** dev — **Product:** vnstock-advisor — **Assignee:** _ready (idle-first)_
- **DoD tier:** Tier 2 (use cases + tests + docs + analytics)
- **Seam:** M3-A slice per `tasks/stack-vnstock-advisor.md` §3.3 — `suggestion_api/auth/*`, `middleware/rate_limit.py`, `tests/test_auth_*.py`, auth half of `tests/test_owasp_security.py`. NEVER touches `suggestion_api/suggestions/`, `main.py`, root `requirements.txt`/`pyproject.toml`.

## Goal
Ship app-wide authn/z: JWT RS256 issued/verified via JWKS, refresh rotation with token-family revocation, and protection of **ALL existing endpoints** (M1 ingest, M2 rank) — not just the new surface (UC-SA-2 scope amendment, debate decision).

## Acceptance criteria (from UC-SA-2, amended scope)
- AC-SA-2-01..02: RS256 only (no `none`/symmetric downgrade); access token `exp` = 15 min.
- AC-SA-2-03..04: refresh rotates (old token invalid after use); reuse revokes the family (fails closed, `409 auth.refresh_reuse`).
- AC-SA-2-05: `GET /auth/jwks` publishes verifying public JWK(s).
- App-wide: M1 ingest + M2 rank endpoints now require valid authn/z too (401/403 Problem Details per error catalog).
- Rate-limit middleware is M3-A-owned (`middleware/rate_limit.py`), consumed by M3-B — keyed per `sub`, `Retry-After` on 429, `/health` exempt.

## Seam-risk requirements (debate decision)
- **Auth middleware interface pin:** expose `require_scope("suggestions:read")` with the signature frozen in `stack-vnstock-advisor.md` — M3-B builds against it without touching auth files.
- **Weights-override schema freeze:** do NOT touch `/rank` contract (read-only) or the weights rules (exactly 4 keys, each [0,1], sum 1.0 ±0.001) — validated by M3-B.
- **Disclaimer single-source:** not M3-A's concern; `compliance/disclaimer.md` text is consumed by M3-B.

## Implementation plan (DEV)
Touch only M3-A files above. JWT: RS256 key pair generated at startup, `kid` published; verify `alg`/sig/`exp`/`iat`/required claims against JWKS. Login issues access+refresh; refresh single-use via server store; family-id on reuse → revoke. Wire auth middleware onto ingest/rank routers via the pinned `require_scope` dependency. OWASP-negative matrix tests (alg:none, HS256 downgrade, expired, bad kid).

## Test plan (TESTER)
Run after branch APPROVED, alongside M3-B's. Verbatim scenarios: (1) login → valid token → 200 on a protected endpoint; (2) no token → 401; (3) token without scope → 403; (4) expired access → 401 `auth.token_expired`; (5) refresh → old token reuse → 409 + family revoked (subsequent calls 401); (6) `alg:none` token → 401; (7) `/health` exempt from rate limit, protected endpoint 429s with `Retry-After` after limit; (8) M1 ingest / M2 rank endpoints now reject unauthenticated calls.

## Report to PM at end: what shipped, task status, blockers.
