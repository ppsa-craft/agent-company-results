# Fixture Data Specifications

**Product:** vnstock-advisor  
**Component:** analysis-engine  
**Version:** 1.0  
**Status:** Approved — PM signed off (cycle 13)  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Overview

This document defines the **canonical fixture datasets** for unit and integration testing of the `analysis-engine` service. All tests must use these fixtures to ensure deterministic, repeatable results. Fixtures cover happy-path scenarios and edge cases (gaps, splits, low volume, insufficient data).

**Format:** JSON arrays of OHLCV objects matching the `MarketDataSchema` from `shared/typescript/src/index.ts`.

**Location:** Tests load from `services/analysis-engine/tests/fixtures/` (to be created by DEV-2).

---

## 1. Happy-Path Dataset: `normal-trading.json`

**Description:** 250 trading days of synthetic data for 5 symbols (VNM, VCB, FPT, HPG, MWG) with realistic Vietnamese market characteristics. Covers uptrend, downtrend, sideways phases.

**Symbols & Profiles:**

| Symbol | Profile | Start Price | Volatility | Volume Pattern |
|--------|---------|-------------|------------|----------------|
| VNM | Large-cap, steady uptrend | 75000 | Low (1.5% daily) | Stable, 1.5M avg |
| VCB | Large-cap, sideways | 89000 | Very low (1% daily) | High, 3M avg |
| FPT | Mid-cap, volatile uptrend | 55000 | Medium (2.5% daily) | Growing, 800K→2M |
| HPG | Cyclical, downtrend then recovery | 32000 | High (3.5% daily) | Spiky, 500K-5M |
| MWG | Growth, strong uptrend | 45000 | Medium (2% daily) | Steady growth, 1M→3M |

**Data Generation Rules (deterministic, seed=42):**
- Daily bars, chronological ascending (oldest first)
- No gaps (continuous trading days)
- OHLC relationships: `L ≤ O,C ≤ H`; `O,C ∈ [L,H]`
- Volume: log-normal distribution around symbol's avg
- Trends implemented via drift component in price random walk

**Minimum Bars:** 250 per symbol (exceeds all indicator requirements: SMA200 needs 200, ATR14 needs 15, OBV slope needs 21)

**File Structure:**
```json
[
  {"time": "2025-01-02T08:00:00Z", "symbol": "VNM", "open": 75100, "high": 75500, "low": 74900, "close": 75300, "volume": 1450000, "source": "FIXTURE"},
  {"time": "2025-01-02T08:00:00Z", "symbol": "VCB", "open": 89200, "high": 89500, "low": 88900, "close": 89100, "volume": 3100000, "source": "FIXTURE"},
  ...
]
```

**Reference Outputs (for test validation):**
- `normal-trading-indicators.json` — expected indicator values at day 249 (last bar)
- `normal-trading-screening.json` — expected screening pass/fail at day 249
- `normal-trading-ranking.json` — expected ranked list at day 249

---

## 2. Edge Case: `insufficient-data.json`

**Description:** Symbols with fewer bars than required for various indicators. Tests that engine returns `null` with reason codes, not errors.

**Cases:**

| Symbol | Bars | Missing Indicators | Expected Behavior |
|--------|------|-------------------|-------------------|
| ABC | 10 | SMA20, SMA50, SMA200, RSI14, Volume_SMA20, MACD, ATR14, OBV | All indicators `null`; screening `excluded: insufficient_data`; ranking `excluded: insufficient_data` |
| XYZ | 15 | SMA20, SMA50, SMA200, Volume_SMA20, MACD, ATR14, OBV | RSI14 computable (needs 15); others `null` |
| DEF | 50 | SMA50, SMA200, ATR14 (needs 15 ✓), OBV slope (needs 21 ✓) | SMA20, RSI14, Volume_SMA20, MACD computable |
| GHI | 199 | SMA200 | All except SMA200 computable |

**File Structure:** Same OHLCV format, 4 symbols with varying lengths.

---

## 3. Edge Case: `price-gaps.json`

**Description:** Data with missing trading days (gaps) to test gap handling in indicators.

**Cases:**
- **Gap of 3 days:** Symbol JKL has bars for days 1-10, then 14-20 (days 11-13 missing — weekend + holiday)
- **Gap of 10 days:** Symbol MNO has bars for days 1-5, then 16-25 (10-day gap)
- **Single-day gaps:** Symbol PQR has random single-day gaps throughout

**Expected Behavior (per `indicators.md` edge cases):**
- SMA/EMA: If any input in window is `null` (gap), output `null` for that `t`
- RSI: Gap in Δ → `null` propagates; need `P` valid Δs after gap
- MACD: Propagates through EMA → MACD → Signal → Histogram
- Volume Profile: Missing `V[i]` → treat as 0 for VWAP; `null` for Volume SMA

**File Structure:** OHLCV with non-contiguous timestamps; missing days simply absent from array.

---

## 4. Edge Case: `stock-splits.json`

**Description:** Data simulating stock splits (price discontinuity, volume adjustment).

**Cases:**
- **2:1 split:** Symbol STU at day 100: close drops from ~100000 to ~50000, volume doubles
- **3:1 split:** Symbol VWX at day 150: close drops from ~90000 to ~30000, volume triples
- **Reverse split (1:2):** Symbol YZA at day 200: close jumps from ~20000 to ~40000, volume halves

**Note:** Current `market_data` schema has no `adj_close` column (see `indicators.md` open question #1). Fixtures use **raw prices** — split handling is an open question for v1.1. Tests verify current behavior (indicators compute on raw prices, showing artificial volatility at split point).

**File Structure:** OHLCV with price/volume discontinuities at split dates.

---

## 5. Edge Case: `low-volume.json`

**Description:** Symbols with very low or zero volume to test volume-profile edge cases.

**Cases:**
- **Zero volume days:** Symbol BCD has 5 days with `volume = 0` (trading halt)
- **Consistently low volume:** Symbol EFG has avg volume ~1000 (vs typical 1M+)
- **Volume spikes:** Symbol HIJ has 3 days with volume 100x avg (news-driven)

**Expected Behavior (per `indicators.md` edge cases):**
- VWAP: `V[t] == 0` for all bars in window → VWAP = `C[t]` (fallback to close)
- Volume SMA: `Volume_SMA == 0` → Volume Ratio = `null` (not 0, not INF)
- Volume Ratio: Handles extreme ratios without overflow

---

## 6. Edge Case: `flat-market.json`

**Description:** Symbol with nearly constant price (flat market) to test RSI edge case.

**Case:**
- Symbol KLM: 50 days with `open ≈ high ≈ low ≈ close ≈ 50000`, minor noise (±10)

**Expected Behavior (per `indicators.md` RSI edge cases):**
- RSI = 50 (by convention: 0/0 → 50) when `AvgGain == 0 and AvgLoss == 0`
- SMA/EMA = constant price
- MACD = 0, Signal = 0, Histogram = 0
- Volume Ratio = 1.0 (if volume constant)

---

## 7. Screening & Ranking Fixtures

### 7.1 `screening-pass-fail.json`

**Description:** 10 symbols at a single date (day 249 of normal-trading) with known pass/fail outcomes.

| Symbol | Price | SMA20 | RSI | Volume | AvgVol | Pass? | Fail Reason |
|--------|-------|-------|-----|--------|--------|-------|-------------|
| VNM | 82000 | 80000 | 58 | 2.5M | 1.5M | ✅ | — |
| VCB | 88000 | 89000 | 62 | 3.2M | 3.0M | ❌ | price_below_sma20 |
| FPT | 62000 | 60000 | 72 | 1.8M | 1.2M | ❌ | rsi_ge_70 |
| HPG | 28000 | 30000 | 45 | 800K | 2.0M | ❌ | price_below_sma20, volume_low |
| MWG | 58000 | 55000 | 65 | 4.0M | 2.5M | ✅ | — |
| AAA | 10000 | 10500 | 55 | 500K | 400K | ❌ | price_below_sma20 |
| BBB | 25000 | 24000 | 68 | 100K | 200K | ❌ | volume_low |
| CCC | 40000 | 38000 | 40 | 3.0M | 1.5M | ✅ | — |
| DDD | 15000 | 16000 | 75 | 2.0M | 1.0M | ❌ | price_below_sma20, rsi_ge_70 |
| EEE | 30000 | 28000 | 50 | 500K | 600K | ❌ | volume_low |

### 7.2 `ranking-deterministic.json`

**Description:** 5 symbols with pre-computed indicator values at a single date, designed to produce a **known, fixed ranking order** for determinism testing.

| Symbol | ROC10% | RSI | Trend Conds | Vol Ratio | OBV Slope | ATR% | Expected Rank |
|--------|--------|-----|-------------|-----------|-----------|------|---------------|
| VNM | +4.2% | 58 | 6/7 | 1.8 | +0.15 | 1.8% | 1 |
| MWG | +3.8% | 62 | 5/7 | 2.1 | +0.20 | 2.1% | 2 |
| FPT | +5.1% | 72 | 4/7 | 1.5 | +0.10 | 3.5% | 3 |
| CCC | +2.5% | 40 | 3/7 | 2.0 | -0.05 | 1.2% | 4 |
| AAA | -1.2% | 55 | 2/7 | 1.2 | -0.10 | 2.8% | 5 |

**Determinism Test:** Call `/rank` twice with identical input → bit-identical JSON output (same order, scores, reasoning).

---

## 8. Test Matrix (Traceability)

| Fixture | Tests Indicator | Tests Screening | Tests Ranking | Tests Edge Case |
|---------|-----------------|-----------------|---------------|-----------------|
| normal-trading.json | ✅ All | ✅ v1.0 | ✅ v1.0 | — |
| insufficient-data.json | ✅ null handling | ✅ excluded | ✅ excluded | Insufficient data |
| price-gaps.json | ✅ gap propagation | — | — | Gaps |
| stock-splits.json | ✅ raw price behavior | — | — | Splits |
| low-volume.json | ✅ VWAP/Volume SMA | — | — | Zero/low volume |
| flat-market.json | ✅ RSI=50, MACD=0 | — | — | Flat market |
| screening-pass-fail.json | — | ✅ v1.0 criteria | — | — |
| ranking-deterministic.json | — | — | ✅ v1.0 deterministic | Determinism |

---

## 9. Implementation Notes for DEV-2

1. **Fixture Loading:** Create `services/analysis-engine/tests/fixtures/` and place all 8 JSON files there. Load via `json.load()` in test setup.
2. **Reference Outputs:** Generate `normal-trading-indicators.json`, `normal-trading-screening.json`, `normal-trading-ranking.json` by running the implemented engine against `normal-trading.json` **once**, then commit those outputs as golden files. Future runs must match exactly.
3. **Determinism:** Set `random.seed(42)` and `numpy.random.seed(42)` in test setup if any stochasticity exists (should not, but defensive).
4. **Percentile Algorithm:** Use the exact `percentile_rank` function from `screening-ranking.md` §4 in tests to validate ranking outputs.
5. **Version Pinning:** All tests must specify `criteria_version: "v1.0"` and `algorithm_version: "v1.0"` in requests.

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-01 | Initial: 8 fixture sets covering happy path + 6 edge cases + screening/ranking validation |

---

*Document status: Approved — PM signed off (cycle 13). Ready for DEV-2 implementation.*