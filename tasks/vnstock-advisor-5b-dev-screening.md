# Task: vnstock-advisor-5b-dev-screening

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature — analysis-engine: screening module)
**Status:** ready (assign: DEV instance on `task/vnstock-advisor-5b-dev-screening`)

---

## Goal

Implement the deterministic, versioned screening module `screening.py` for the
`analysis-engine` service and wire the `POST /screen` endpoint. Screening applies
the v1.0 criteria — price > SMA20, RSI14 < 70, Volume > 1.5x Volume_SMA20 — to
select symbols from the indicator results produced by **5a**.

This is the **5b / screening slice** of `vnstock-advisor-5-dev-analysis-engine`;
it depends on the 5a `indicators.py` output and feeds no downstream slice (ranking
5c runs only on screened symbols, but is built separately).

## Acceptance Criteria (traceable to UC-AE-2; per screening-ranking.md v1.0)

- [ ] `services/analysis-engine/src/screening.py` exposes
      `screen_symbols(indicators_by_symbol, as_of_date, version="v1.0")` returning,
      per symbol, `passed` and `evaluations` (per-criterion pass + metrics) as
      specified by the screening output JSON shape.
- [ ] All three v1.0 criteria applied with AND logic; thresholds from
      `SCREEN_PRICE_GT_SMA20`, `SCREEN_RSI_MAX` (70), `SCREEN_VOLUME_RATIO_MIN`
      (1.5) with recorded effective version.
- [ ] Symbols with < 20 valid bars → `excluded` with reason `insufficient_data`.
- [ ] Deterministic: same input + same version → bit-identical output; no
      randomness.
- [ ] `POST /screen` accepts symbols/date/version, calls screening, returns
      per-symbol `passed`/`evaluations`; validates input (Pydantic); Problem
      Details errors, no stack traces.
- [ ] Tests: happy path (`screening-pass-fail.json`), insufficient-data exclusion,
      all-fail and all-pass universes; one-command suite; README updated.
- [ ] Security gate: secret-scan & SAST clean.

## Implementation Plan (for DEV)

**Architecture seam — file boundary:** this owns ONLY
`services/analysis-engine/src/screening.py`, the `screen` endpoint/router in
`src/main.py`, and `tests/test_screen*.py` + any screening fixture JSON. It
consumes `indicators.py` (5a) output — do NOT re-implement indicators here.
Touching `ranking.py` (5c) is out of scope.

Ordered subtasks (each committed):
1. Confirm 5a `indicators.py` is merged/APPROVED; otherwise flag the dependency
   as a blocker before starting.
2. Implement `screen_symbols(indicators_by_symbol, version)` per
   screening-ranking.md §1 (v1.0) with configurable thresholds. Test-first.
3. Implement insufficient-data exclusion (min 20 bars) + reason codes.
4. Add `POST /screen` endpoint + Pydantic models + version pinning.
5. Fixtures + unit tests (pass/fail, insufficient, all-pass, all-fail).
6. README run steps; security checks.

## Test Plan (for DEV and TESTER)

1. **Pass/fail matrix:** load 10-symbol `screening-pass-fail.json`; assert each
   symbol's pass/fail & fail-reason exactly matches the fixture table.
2. **Insufficient data:** symbol with <20 bars => `excluded`, reason
   `insufficient_data`, no crash.
3. **Determinism:** call `/screen` twice with same input => identical JSON.
4. **HTTP endpoint:** happy + invalid payload => clean Problem Details error.
5. **Crash-safety:** empty symbol list, malformed request => clean error.

## Dependencies

- **5a** `vnstock-advisor-5a-dev-indicators` (must be APPROVED first).
- Spec: `docs/specs/screening-ranking.md`, `docs/testing/fixtures.md`.
- Feeds: tester/QA sessions for analysis-engine.