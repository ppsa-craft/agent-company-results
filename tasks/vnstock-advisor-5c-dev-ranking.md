# Task: vnstock-advisor-5c-dev-ranking

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature — analysis-engine: ranking module)
**Status:** ready (assign: DEV instance on `task/vnstock-advisor-5c-dev-ranking`)

---

## Goal

Implement the deterministic, versioned ranking module `ranking.py` for the
`analysis-engine` service and wire the `POST /rank` endpoint. Ranking computes a
weighted composite score (momentum 40% / trend 30% / volume 20% / volatility 10%)
per symbol from the indicator results produced by **5a**, and returns a ranked
list with a per-symbol reasoning array (UC-AE-3 / UC-AE-4).

This is the **5c / ranking slice** of `vnstock-advisor-5-dev-analysis-engine`;
ranking runs only on the screened universe, but is implemented self-contained of
the 5b code (it ingests indicators + a screened-symbol set).

## Analysis Ranking Criteria (traceable per screening-ranking.md v1.0)

- [ ] `services/analysis-engine/src/ranking.py` exposes
      `rank_symbols(indicators_by_symbol, screened_symbols, weights, version)` →
      ranked list with `rank`, `symbol`, `composite_score`, `components`
      (momentum/trend/volume/volatility), `sub_components`, `reasoning[]`.
- [ ] Composite uses configurable weights (env `RANK_WEIGHT_*`, defaults
      0.4/0.3/0.2/0.1) that validate to sum 1.0 (tolerance ±0.001).
- [ ] Momentum = (ROC10 percentile + RSI normalized)/2; Trend = passed/7
      conditions normalized; Volume = (vol-ratio pctl + OBV trend pctl)/2;
      Volatility = inverted ATR% percentile — all per spec tables.
- [ ] Percentile via the fixed linear-interpolation `percentile_rank` algorithm.
- [ ] Symbols with < 200 valid bars → `excluded` with reason `insufficient_data`
      + missing-indicator list.
- [ ] Determinism: same input+version → bit-identical JSON; tie-break by symbol ASC.
- [ ] Reasoning strings deterministic per the reasoning-template table.
- [ ] `POST /rank` endpoint accepts symbols/date/version; Pydantic validation;
      Problem Details errors; one-command suite; README updated.
- [ ] Security gate: secret-scan & SAST clean.

## Implementation Plan (for DEV)

**Architecture seam — file boundary:** this owns ONLY
`services/analysis-engine/src/ranking.py`, `src/main.py`, and
`tests/test_rank*.py`. Ingest `indicators.py` (5a) + screening output (5b) as
inputs; do NOT re-implement them.

Ordered subtasks (each committed):
1. Confirm 5a `indicators.py` is merged/APPROVED; otherwise flag dependency blocker.
2. Implement percentile helper (`percentile_rank` per spec §4) + factor scores
   (momentum/trend/volume, determinism). Test-first.
3. Implement composite weighting + validation (sum 1.0) + ranking sort + symbol
   tie-break.
4. Implement deterministic reasoning generation per template table.
5. Add `POST /rank` endpoint + Pydantic models + version pinning.
6. Fixtures + unit tests (`ranking-deterministic.json`, insufficient-data
   exclusion, weight validation, determinism).
7. README run steps; security checks.

## Test Plan (for DEV and TESTER)

1. **Deterministic order:** `ranking-deterministic.json` => expected rank order
   1..5 exactly (VNM, MWG, FPT, CCC, AAA); call twice => identical JSON.
2. **Reasoning:** each ranked symbol has a reasoning array with values matching
   the component bands.
3. **Weight validation:** invalid weight sets (partial, non-sum-1) rejected;
   custom weights change ordering deterministically.
4. **Insufficient data:** <200-bar symbol `excluded: insufficient_data`.
5. **HTTP endpoint:** happy + invalid payload => clean Problem Details error.
6. **Crash-safety:** empty universe, empty indicators => clean result/no crash.

## Dependencies

- **5a** `vnstock-advisor-5a-dev-indicators` (must be APPROVED first).
- **5b** `vnstock-advisor-5b-dev-screening` provides the universe (may be
  optional/dependency-injected).
- Spec: `docs/specs/screening-ranking.md` §2-5, `docs/testing/fixtures.md`.