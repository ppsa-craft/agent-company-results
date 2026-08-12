# Task vnstock-advisor-16 — M3-B: Suggestion API (GET /suggestions)

- **Role:** dev — **Product:** vnstock-advisor — **Assignee:** _ready (idle-first)_
- **DoD tier:** Tier 2 (use cases + tests + docs + analytics)
- **Seam:** M3-B slice per `tasks/stack-vnstock-advisor.md` §3.3 — `suggestion_api/suggestions/*`, `middleware/security_headers.py`, `middleware/error_handlers.py`, `tests/test_suggestions_*.py`, `tests/test_disclaimer.py`, suggestions half of `tests/test_owasp_security.py`. NEVER touches `suggestion_api/auth/`, `main.py`, root manifests.

## Goal
`GET /suggestions` (Bearer RS256 + `suggestions:read`): portfolio → analysis-engine `/rank` mapping → ranked suggestions with reasoning, mandatory disclaimer, RFC 7807 errors.

## Acceptance criteria (from UC-SA-1, 3, 4, 5)
- AC-SA-1.1..1.2: valid token + scope → `200 OK` ranked list with `X-Disclaimer` header, `meta.disclaimer`, `meta.generated_at`, `meta.source`.
- AC-SA-1.3: no token → 401; token missing scope → 403 (from M3-A middleware — consume, don't implement).
- AC-SA-3-1..3-3: symbols + optional weights → ranked with `rank/symbol/composite_score/components/reasoning`; excluded surfaced in `excluded[]`, never dropped.
- AC-SA-3-4: empty symbols → 400 `validation.symbols_empty`; bad weights → 422 `validation.weights_invalid`; upstream `/rank` failure → 502 `upstream.rank_failed`.
- AC-SA-4-1..4-4: every response has `X-Disclaimer` + `meta.disclaimer` (both `vi-VN`/`en-US`), text sourced from `compliance/disclaimer.md` (single source — no hardcoded duplicates); missing disclaimer fails the contract test.
- AC-SA-5-1..5-3: 429 with `Retry-After` + Problem Details when M3-A's limiter trips; all errors `application/problem+json` (type/title/status/detail/instance).

## Seam-risk requirements (debate decision)
- **Auth interface pin:** consume auth's frozen `require_scope("suggestions:read")` — no auth logic of your own; build against the pinned signature before M3-A lands.
- **Weights-override schema freeze:** use exactly the frozen `/rank` contract + weights rules (4 keys, [0,1], sum 1.0 ±0.001). If the BA contract-pin snapshot can't freeze in one round, STOP and report to PM — fallback is narrower scope.
- **Rate-limit owned by M3-A:** you only map its 429 into the RFC 7807 shape; do not implement your own limiter.
- **Disclaimer single-source:** render from `compliance/disclaimer.md`, never re-implement text.

## Implementation plan (DEV)
Touch only M3-B files. Pydantic-strict query validation (symbol pattern `^[A-Z][A-Z0-9]{0,9}$`, ≤100, default universe fallback). Call `/rank`, map `ranked[]`/`excluded[]` into the suggestion envelope, attach disclaimer from the single source, security headers + RFC 7807 error handlers.

## Test plan (TESTER)
Run after branch APPROVED, alongside M3-A's. Verbatim scenarios: (1) valid token + symbols → 200, full envelope + both disclaimer locales, text matches `disclaimer.md` exactly; (2) weights sum ≠ 1 → 422; (3) empty symbols → 400; (4) no token → 401; (5) valid token, wrong scope → 403; (6) rate-limit trip → 429 + `Retry-After` + Problem Details body; (7) `/rank` unavailable → 502; (8) excluded symbols present in response.

## Report to PM at end: what shipped, task status, blockers.
