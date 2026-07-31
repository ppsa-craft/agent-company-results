# Task: vnstock-advisor-3-ba-analysis-engine

**Role:** BA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine use cases + indicator specs)
**Status:** claimed:BA-1

---

## Goal

Produce BA documentation for `analysis-engine` service: use cases, indicator specifications, screening/ranking rules, and fixture data requirements.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Use case document: `workspace/apps/vnstock-advisor/docs/use-cases/analysis-engine.md` covering:
  - UC-AE-1: Compute indicators (SMA, EMA, RSI, MACD, volume profiles) for given symbols/date range
  - UC-AE-2: Screen symbols (price > SMA20, RSI < 70, volume > 1.5x avg)
  - UC-AE-3: Rank symbols by composite score (weighted: momentum 40%, trend 30%, volume 20%, volatility 10%)
  - UC-AE-4: Return ranked list with reasoning array per symbol
- [ ] Indicator specifications: `workspace/apps/vnstock-advisor/docs/specs/indicators.md` — exact formulas, parameters (periods), edge cases (insufficient data)
- [ ] Screening/ranking rules: `workspace/apps/vnstock-advisor/docs/specs/screening-ranking.md` — deterministic, versioned rules
- [ ] Fixture data spec: `workspace/apps/vnstock-advisor/docs/testing/fixtures.md` — sample OHLCV data for unit/integration tests (covers normal, edge cases: gaps, splits, low volume)
- [ ] All docs reviewed and approved by PM

---

## Implementation Plan (for BA)

1. Define exact indicator formulas (reference: standard TA definitions)
2. Define screening criteria with rationale
3. Define ranking algorithm with weights (configurable via env)
4. Design fixture data covering happy path + edge cases
5. Get PM sign-off

---

## Test Plan (for TESTER)

**Scenario: Spec completeness**
- Steps: Verify each indicator has formula, params, edge case handling
- Expected: No ambiguous specs; all formulas reference standard definitions

**Scenario: Ranking determinism**
- Steps: Given same fixture data, ranking output must be identical across runs
- Expected: Deterministic output, versioned rule set

---

## Dependencies

- `vnstock-advisor-2-ba-data-ingest` (needs canonical `market_data` schema)
- Output feeds: `vnstock-advisor-5-dev-analysis-engine`, `vnstock-advisor-6-tester-analysis-engine`