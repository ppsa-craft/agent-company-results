# Task vnstock-advisor-18 — M3 API Test Pass

- **Role:** tester — **Product:** vnstock-advisor — **Assignee:** _ready_
- **DoD tier:** Tier 2 (supports 15/16) — gate task, runs after the branches' TECHLEAD APPROVED.

## Goal
End-to-end test the assembled M3 API per the Test Plans in tasks 15/16/17 — README verbatim in a clean checkout. Merged M1 (`9f1ca33`) + M2 (`0dcd72e`) are the base.

## Scope (execute the verbatim scenarios)
- **Auth (15):** login → 200; no token → 401; wrong scope → 403; expired → 401; refresh rotation + reuse → 409 + family revoked; `alg:none` → 401; `/health` exempt from rate limit; M1 ingest + M2 rank reject unauthenticated calls (amended UC-SA-2 scope).
- **Suggestions (16):** valid → 200 full envelope; disclaimer header + both locales matching `compliance/disclaimer.md` exactly; empty symbols → 400; bad weights → 422; upstream `/rank` down → 502; rate-limit → 429 + `Retry-After`; excluded surfaced.
- **Assembly (17):** clean-checkout README verbatim — install, start, health, login, refresh, suggestions via curl.

## Method
Per AC, one scenario at a time, state running verdict per scenario as you go. Defects: report only, never fix. Include repro steps + expected-vs-actual.

## Seam-risk focus
Weights-override behavior matches the frozen schema (4 keys, [0,1], sum 1.0 ±0.001); disclaimer text byte-matches the single source; RFC 7807 bodies on every error.

## Report to PM at end: per-scenario verdicts (PASS/FAIL), defect list, overall verdict.
