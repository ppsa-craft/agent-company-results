# Task: vnstock-advisor-7-tester-analysis-engine

**Role:** TESTER
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine service testing)
**Status:** ready

---

## Goal

Execute end-to-end testing of `analysis-engine` service per Test Plan in `vnstock-advisor-5-dev-analysis-engine.md`. Verify README works verbatim, all acceptance criteria met, edge cases covered.

---

## Acceptance Criteria (traceable to use cases)

- [ ] README verbatim run succeeds in clean checkout
- [ ] All Test Plan scenarios pass (indicators, screening, ranking, determinism, reasoning)
- [ ] Automated test suite runs via one command (`pytest`) and passes
- [ ] Coverage includes BOTH happy path AND failure/edge paths
- [ ] No critical defects blocking ship
- [ ] Findings reported with exact reproduction steps, expected vs actual, severity

---

## Test Plan (for TESTER) — from DEV task

**Scenario: Indicator computation accuracy**
- Steps: Load fixture data, call `/indicators/compute` for known symbols/range, compare output to expected values
- Expected: All indicators match expected values within floating-point tolerance

**Scenario: Insufficient data handling**
- Steps: Request indicators for symbol with < required periods of data
- Expected: Returns appropriate error/empty result per spec (not crash)

**Scenario: Screening filters correctly**
- Steps: Load fixture data where some symbols pass/fail criteria, call `/screen`
- Expected: Returns only passing symbols with correct filter metadata

**Scenario: Ranking determinism**
- Steps: Call `/rank` twice with same input data
- Expected: Identical ranked output (same order, same scores, same reasoning)

**Scenario: Ranking weights configurable**
- Steps: Call `/rank` with custom weights via env/config
- Expected: Ranking reflects custom weights

**Scenario: Reasoning array per symbol**
- Steps: Inspect `/rank` response
- Expected: Each symbol has `reasoning` array explaining score components

**Exploratory edge cases (beyond Test Plan):**
- Empty symbol list
- Single data point
- All NaN values in data
- Weekend/holiday gaps in data
- Stock splits/adjustments in historical data
- Extreme values (very high volume, zero volume)
- Mixed pass/fail symbols in screening