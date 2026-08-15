# Task vnstock-advisor-22 — M3.5: UI Assembly

- **Role:** dev — **Product:** vnstock-advisor — **Assignee:** _ready (Wave 2 — SERIAL after task 21; post-M3-release)_
- **DoD tier:** Tier 1 (product launch — full artifact table)

## Goal
Assemble the M3.5 web-UI release: wire the web-ui into the product tree (served against the M3 API), full README run-through (API + UI) in a clean checkout, complete artifact table (BA use cases, design, analytics, README, changelog, security records), e2e browser pass.

## Acceptance criteria
- Clean checkout: start API (M3) + UI (M3.5) per README → login → portfolio → ranked results, end-to-end.
- Full Tier-1 artifact table present for the combined M3+M3.5 product; openapi + UI contract consistent.
- §7.2 security gate on the UI surface (headers, CSP, no secrets in client, auth via API only).
- Disclaimer rendered from API data on every view (single source held).

## Seam-risk requirements
No backend changes in this task — UI assembly only. Any API gap found → report to PM as backlog, don't patch the API here.

## Implementation plan (DEV)
Serial after 21. Wire UI into product layout, e2e, artifacts, README.

## Test plan (TESTER — wave 2)
Browser e2e per browser-testing skill: full user journey + negative states (expired token, 429, 422 weights).

## Report to PM at end: what shipped, task status, blockers.
