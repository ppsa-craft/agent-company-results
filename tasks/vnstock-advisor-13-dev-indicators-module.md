# Task: vnstock-advisor-13-dev-indicators-module

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: indicators computation module)
**Status:** ready

---

## Goal

Implement the pure-Python `indicators.py` module for the `analysis-engine` service: SMA, EMA, RSI, MACD, Volume Profile, ROC, ATR, OBV with exact formulas per `docs/specs/indicators.md` v1.0.

---

## Acceptance Criteria (traceable to use cases)

- [ ] UC-AE-1: `indicators.py` exports `compute_all_indicators(ohlcv: list[OHLCV]) -> IndicatorsResult` computing all 8 indicator families
- [ ] SMA/EMA/RSI/MACD/Volume Profile formulas match `indicators.md` exactly (periods, edge cases, rounding)
- [ ] Additional indicators (ROC10, ATR14, OBV) implemented per §6 of `indicators.md` for ranking consumption
- [ ] Edge cases handled: insufficient data → `null` with warning, gaps → propagation per spec, flat market → RSI=50, zero volume → VWAP fallback
- [ ] Stock splits: compute on raw prices (current behavior, `adj_close` not in schema)
- [ ] Unit tests pass against all 8 fixture sets (`normal-trading`, `insufficient-data`, `price-gaps`, `stock-splits`, `low-volume`, `flat-market`)
- [ ] Security gate: secret-scan clean, SAST clean, no hardcoded secrets
- [ ] Module is importable independently (no FastAPI, no DB dependencies)

---

## Implementation Plan (for DEV)

**Architecture seam:** `services/analysis-engine/src/indicators.py` — pure computation module, **zero external dependencies** (no FastAPI, no DB, no network). Shared: consumes `OHLCV` dataclass from `shared/python/src/vnstock_shared/models.py`. **Disjoint from screening, ranking, API tasks.**

Ordered subtasks:
1. [ ] Create `services/analysis-engine/src/indicators.py` with all 8 indicator functions
2. [ ] Implement SMA, EMA (Wilder's), RSI (Wilder's), MACD per `indicators.md` reference implementations
3. [ ] Implement Volume Profile (VWAP session/rolling, Volume SMA, Volume Ratio)
4. [ ] Implement ROC10, ATR14, OBV per §6 of `indicators.md`
5. [ ] Add `compute_all_indicators()` aggregator returning structured `IndicatorsResult` dataclass
6. [ ] Handle all edge cases: insufficient data, gaps, flat market, zero volume, splits (raw prices)
7. [ ] Create fixture loader in `services/analysis-engine/tests/fixtures/` (8 JSON files from `fixtures.md`)
8. [ ] Write unit tests for each indicator against fixture reference outputs
9. [ ] Run security checks (secret-scan, SAST)

---

## Test Plan (for TESTER)

**Scenario: Happy-path indicator accuracy**
- Steps: Load `normal-trading.json`, call `compute_all_indicators()` for each symbol, compare last-bar values to `normal-trading-indicators.json`
- Expected: All indicator values match golden file within floating-point tolerance (4 decimals prices, 2 RSI/%, 0 volume)

**Scenario: Insufficient data handling**
- Steps: Load `insufficient-data.json`, call `compute_all_indicators()` for ABC (10 bars), XYZ (15), DEF (50), GHI (199)
- Expected: Returns `null` for uncomputable indicators with warning `insufficient_data (need P, have N)`; no crashes

**Scenario: Price gap propagation**
- Steps: Load `price-gaps.json`, compute indicators for JKL (3-day gap), MNO (10-day gap), PQR (random gaps)
- Expected: SMA/EMA/RSI/MACD/Volume Profile propagate `null` per `indicators.md` edge case rules exactly

**Scenario: Stock split raw-price behavior**
- Steps: Load `stock-splits.json`, compute indicators for STU (2:1), VWX (3:1), YZA (1:2)
- Expected: Indicators compute on raw prices showing artificial volatility at split point (no `adj_close` adjustment)

**Scenario: Low/zero volume edge cases**
- Steps: Load `low-volume.json`, compute Volume Profile for BCD (zero volume days), EFG (low volume), HIJ (spikes)
- Expected: VWAP falls back to close when all volume=0; Volume Ratio = `null` when Volume_SMA=0; no overflow on spikes

**Scenario: Flat market RSI=50**
- Steps: Load `flat-market.json`, compute RSI for KLM
- Expected: RSI = 50.0 (convention for 0/0), MACD = 0, Signal = 0, Histogram = 0

**Edge cases:** Empty input list, single bar, all NaN values, weekend/holiday gaps, reverse splits.

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (done — shared models exist)
- `vnstock-advisor-3-ba-analysis-engine` (done — specs + fixtures ready)
- Feeds: `vnstock-advisor-17-tester-indicators`, `vnstock-advisor-20-qa-indicators`