# Task vnstock-advisor-19 — M3.5: Web-UI Use Cases (draft, non-blocking)

- **Role:** ba — **Product:** vnstock-advisor — **Assignee:** _ready_ — **DoD tier:** Tier 2 (BA artifact)
- **Status:** Wave-1 (non-blocking — does not gate M3 API release). M3.5 wave-2 work.

## Goal
Draft the M3.5 web-UI use cases so DEV (task 21) has BA-gated input the moment M3 ships. Builds on the suggestion-api use cases (UC-SA-1..5) + `compliance/disclaimer.md`.

## Deliverables (BA-owned files)
- `docs/use-cases/web-ui.md` (Draft): UC-WUI-1 login (OAuth code flow via `/auth/login`), UC-WUI-2 portfolio form → `GET /suggestions` render, UC-WUI-3 ranked-results display (reasoning, excluded), UC-WUI-4 refresh-token auto-refresh, UC-WUI-5 disclaimer rendering — **from API data, never re-implemented text** (single-source rule).
- Acceptance criteria IDs per use case, traceable to UC-SA-1..5.

## Constraints
- Disclaimer non-removable, no dismissible mechanism (UC-SA-4 guardrails).
- Authn/z comes from the shipped M3 API — UI holds tokens, never validates JWTs itself.
- Do not pre-commit UI tech choices — that is CTO/DEV's call in task 21.

## Report to PM at end: what drafted, AC IDs, task status, blockers.
