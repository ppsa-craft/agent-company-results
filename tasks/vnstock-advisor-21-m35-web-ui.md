# Task vnstock-advisor-21 — M3.5: Web UI

- **Role:** dev — **Product:** vnstock-advisor — **Assignee:** _ready (Wave 2 — POST-M3-RELEASE; no branch before M3 API ships)_
- **DoD tier:** Tier 2 (use cases + tests + docs/README + analytics)
- **Seam:** `services/web-ui/` tree (stack record M3-D seam) — builds on the M3 API contract + BA use cases (task 19).

## Goal
Browser front-end over the shipped M3 API: login (OAuth code flow via `/auth/login`), portfolio form (symbols + optional weights), ranked-suggestions display with reasoning + excluded, automatic token refresh, mandatory disclaimer rendering.

## Acceptance criteria
- UC-WUI-1..5 from `docs/use-cases/web-ui.md` (task 19) all met, traceable to AC IDs.
- All API calls authenticated (Bearer RS256); 401 → re-login; 403 scope-denied surfaced; 429 shown with retry hint.
- Disclaimer rendered from API `meta.disclaimer` — **never re-implemented text** (single-source rule); non-removable, no dismiss mechanism (UC-SA-4).
- Weights input validated client-side to the frozen rules (4 keys, [0,1], sum 1.0 ±0.001) and rejected gracefully server-side (422 surfaced).
- README for web-ui: how to run against the M3 API in a clean checkout.

## Implementation plan (DEV)
Frontend per stack record's web-ui section; UI engineering skill; consume the frozen openapi contract (GET /suggestions query style). No backend changes — all server logic lives in the shipped API.

## Test plan (TESTER — staged for wave 2)
Clean-checkout run, login, portfolio entry, results render, refresh keeps session alive, disclaimer visible on every view, 401/403/429/422 states.

## Report to PM at end: what shipped, task status, blockers.
