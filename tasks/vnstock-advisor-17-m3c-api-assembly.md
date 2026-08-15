# Task vnstock-advisor-17 — M3-C: API Assembly (serial, last)

- **Role:** dev — **Product:** vnstock-advisor — **Assignee:** _ready (SERIAL — only after 15 AND 16 MERGE)_
- **DoD tier:** Tier 1 (product launch — full artifact table)
- **Seam:** `suggestion_api/main.py`, root `requirements.txt`/`pyproject.toml`, openapi finalize, README(s), e2e. Imports both M3-A and M3-B packages — **no branch may open until 15 + 16 are merged** (debate decision: serial-only).

## Goal
Assemble the M3 API into a runnable, README-runnable product: wire A+B routers into `main.py` with lifespan, register middleware (rate limit, security headers, error handlers), add `PyJWT`/`redis`/`slowapi` to root manifests, register pytest path + `suggestion_api` package, finalize `api/suggestion-api.openapi.yaml`, write the curl-runnable how-to-run README, run the e2e.

## Acceptance criteria
- API starts via README steps in a clean checkout; `GET /health` → 200 (rate-limit exempt).
- Full auth flow (login → refresh → suggestions) works end-to-end via curl exactly as README documents.
- Openapi final matches the frozen contract (GET /suggestions query style, Problem Details, auth endpoints, no `screening` field).
- Full Tier-1 artifact table present: README, use cases, specs, openapi, tests green, SBOM/SCA/SAST/secret-scan records, changelog, analytics plan.
- Contract corrections to openapi get TECHLEAD/QA review before the ship gate (stack record §5).

## Seam-risk requirements (debate decision)
- **Weights-override schema freeze:** the assembled `/rank` call must match the frozen contract exactly — do not "fix" weights/ranking logic here; flag drift to PM instead.
- **Auth interface pin:** assemble against the shipped `require_scope` — no signature changes.
- **Rate-limit owned by M3-A:** wire M3-A's limiter in; don't re-own it.
- **Disclaimer single-source:** e2e asserts disclaimer text comes from `compliance/disclaimer.md`.

## Implementation plan (DEV)
Serial-only. Wire routers/middleware in `main.py`, root manifests, finalize openapi, README, e2e script, run full suite.

## Test plan (TESTER)
Clean-checkout README verbatim: install, start, `GET /health`, login, refresh, suggestions call with curl; negative: bad token, no scope, 429; assert Problem Details shape and disclaimer header/body on every suggestion response.

## Report to PM at end: what shipped, task status, blockers.
