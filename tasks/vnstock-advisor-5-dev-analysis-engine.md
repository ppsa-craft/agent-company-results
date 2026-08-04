# Task: vnstock-advisor-5-dev-analysis-engine

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine service)
**Status:** OPEN (in-progress) — SPLIT into sub-tasks 5a/5b/5c below. Do NOT mark
`done`. The umbrella remains open until 5a (indicators), 5b (screening), 5c
(ranking) are all APPROVED. BA docs complete (indicators.md, screening-ranking.md,
fixtures.md), PM sign-off done.

---

## Goal

Implement the `analysis-engine` service per BA docs: compute indicators (SMA, EMA, RSI, MACD, volume profiles), screen symbols, rank by composite score, return ranked list with reasoning.

**This task is now split into three disjoint sub-tasks (see links):**
- `vnstock-advisor-5a-dev-indicators` — indicators.py + `POST /indicators/compute`
- `vnstock-advisor-5b-dev-screening` — screening.py + `POST /screen` (dep: 5a)
- `vnstock-advisor-5c-dev-ranking` — ranking.py + `POST /rank` (dep: 5a, 5b)

---

## Acceptance Criteria (traceable to use cases)

- [ ] UC-AE-1: `POST /indicators/compute` computes SMA, EMA, RSI, MACD, volume profiles for given symbols/date range
- [ ] UC-AE-2: `POST /screen` screens symbols (price > SMA20, RSI < 70, volume > 1.5x avg)
- [ ] UC-AE-3: `POST /rank` ranks symbols by composite score (momentum 40%, trend 30%, volume 20%, volatility 10%)
- [ ] UC-AE-4: Ranked list returns reasoning array per symbol
- [ ] Indicator formulas match `docs/specs/indicators.md` exactly (periods, edge cases) — BLOCKED on BA
- [ ] Screening/ranking rules match `docs/specs/screening-ranking.md` (deterministic, versioned) — BLOCKED on BA
- [ ] Fixture data per `docs/testing/fixtures.md` used in tests (normal + edge cases) — BLOCKED on BA
- [ ] Tests pass (unit + integration), README works verbatim — only basic health test exists
- [ ] Security gate: secret-scan clean, SAST clean, no hardcoded secrets

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/analysis-engine/` — isolated FastAPI service with pure-Python indicator computation, screening, and ranking logic. Touches: `services/analysis-engine/src/main.py` (API), new `services/analysis-engine/src/indicators.py`, `services/analysis-engine/src/screening.py`, `services/analysis-engine/src/ranking.py`, `services/analysis-engine/tests/`. Shared: reads `market_data` from DB via `shared/python/src/vnstock_shared/models/`. **No overlap with data-ingest.**

Ordered subtasks:
1. [ ] Implement indicator computation module (SMA, EMA, RSI, MACD, volume profiles) with exact formulas
2. [ ] Implement screening module (price > SMA20, RSI < 70, volume > 1.5x avg)
3. [ ] Implement ranking module (composite score with configurable weights)
4. [ ] Add API endpoints: `/indicators/compute`, `/screen`, `/rank`
5. [ ] Add DB read layer for `market_data` (reuse shared models)
6. [ ] Add comprehensive tests using fixture data (happy path + edge cases: insufficient data, gaps, splits, low volume)
7. [ ] Write README with exact run steps
8. [ ] Run security checks

---

## Test Plan (for TESTER)

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

**Edge cases:** Empty symbol list, single data point, all NaN values, weekend/holiday gaps in data, stock splits

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (done)
- `vnstock-advisor-3-ba-analysis-engine` (done — specs + fixtures ready)
- `vnstock-advisor-2-ba-data-ingest` (done — needs market_data schema)
- Feeds: `vnstock-advisor-7-tester-analysis-engine`, `vnstock-advisor-9-qa-analysis-engine`