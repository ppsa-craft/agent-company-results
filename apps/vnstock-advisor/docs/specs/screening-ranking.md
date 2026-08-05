# Screening & Ranking Specifications

**Product:** vnstock-advisor  
**Component:** analysis-engine  
**Version:** 1.0  
**Status:** Draft — pending PM sign-off  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Overview

This document defines the **deterministic, versioned** screening criteria and ranking algorithm for the `analysis-engine` service. All rules are immutable per version — `v1.0` never changes. New versions are additive (e.g., `v1.1`, `v2.0`). Consumers specify the version in requests.

Weights for ranking are configurable via environment variables with defaults defined here.

---

## 1. Screening Criteria (Versioned)

### Version: `v1.0` (Current)

**Description:** Base momentum/quality screen for Vietnamese equities. Selects symbols in uptrend, not overbought, with above-average volume.

### Criteria (ALL must pass — AND logic)

| # | Criterion | Formula | Threshold | Rationale |
|---|-----------|---------|-----------|-----------|
| 1 | **Price > SMA20** | `C[t] > SMA20[t]` | Strict > | Price above short-term trend = uptrend confirmation |
| 2 | **RSI < 70** | `RSI14[t] < 70` | Strict < | Not overbought; room for further upside |
| 3 | **Volume > 1.5× Avg Volume** | `V[t] > 1.5 * Volume_SMA20[t]` | Strict > | Institutional interest / accumulation |

### Required Indicators (for screening date `t`)

| Indicator | Period | Notes |
|-----------|--------|-------|
| `SMA20` | 20 | Close prices |
| `RSI14` | 14 | Wilder's RSI |
| `Volume_SMA20` | 20 | Volume simple average |

### Minimum Data Requirements

| Indicator | Minimum Bars Required |
|-----------|----------------------|
| `SMA20` | 20 |
| `RSI14` | 15 (14 + 1 for first Δ) |
| `Volume_SMA20` | 20 |
| **Total** | **20 bars** (most restrictive) |

Symbols with `< 20` valid bars → `excluded` with reason `insufficient_data`.

### Evaluation Output (Per Symbol)

```json
{
  "symbol": "VNM",
  "passed": true,
  "evaluations": {
    "price_gt_sma20": {
      "pass": true,
      "price": 78500.0,
      "sma20": 77200.0,
      "diff_pct": 1.68
    },
    "rsi_lt_70": {
      "pass": true,
      "rsi": 58.3,
      "threshold": 70
    },
    "volume_gt_1_5x_avg": {
      "pass": true,
      "volume": 2500000,
      "avg_volume": 1400000,
      "ratio": 1.79
    }
  }
}
```

### Versioning Policy

- **`v1.0` is frozen** — will never be modified
- New criteria → new version (`v1.1`, `v2.0`)
- Versions are **independent** — consumers pin to a version
- Deprecation: Old versions supported for 12 months after replacement

### Future Versions (Planned, Not Implemented)

| Version | Planned Changes |
|---------|-----------------|
| `v1.1` | Add: Price > SMA50 (medium-term trend filter) |
| `v1.2` | Add: MACD histogram > 0 (momentum confirmation) |
| `v2.0` | Sector-relative screening (vs sector ETF/index) |

---

## 2. Ranking Algorithm (Versioned)

### Version: `v1.0` (Current)

**Description:** Weighted composite score combining four factors. Higher score = better rank.

### Weights (Configurable via Environment Variables)

| Factor | Weight | Env Var | Default | Valid Range |
|--------|--------|---------|---------|-------------|
| **Momentum** | 40% | `RANK_WEIGHT_MOMENTUM` | 0.4 | [0.0, 1.0] |
| **Trend** | 30% | `RANK_WEIGHT_TREND` | 0.3 | [0.0, 1.0] |
| **Volume** | 20% | `RANK_WEIGHT_VOLUME` | 0.2 | [0.0, 1.0] |
| **Volatility** | 10% | `RANK_WEIGHT_VOLATILITY` | 0.1 | [0.0, 1.0] |

**Constraint:** Weights must sum to 1.0 (validated at startup and on override).

### Factor Definitions

#### 2.1 Momentum (40%)

**Components (equal weight within factor):**

| Sub-factor | Formula | Normalization |
|------------|---------|---------------|
| **ROC10** | `(C[t] - C[t-10]) / C[t-10] * 100` | Percentile rank vs universe (0-100) |
| **RSI14** | `RSI14[t]` | Linear: 30→0, 50→50, 70→100, clamp [0,100] |

**Momentum Score:** `(ROC10_percentile + RSI_normalized) / 2`

**Rationale:** ROC captures absolute momentum; RSI captures relative strength vs recent history. Percentile ranking makes it cross-sectional (vs universe).

#### 2.2 Trend (30%)

**Components (equal weight):**

| Sub-factor | Formula | Scoring |
|------------|---------|---------|
| **Price > SMA20** | `C[t] > SMA20[t]` | 20 if true, 0 if false |
| **Price > SMA50** | `C[t] > SMA50[t]` | 20 if true, 0 if false |
| **Price > SMA200** | `C[t] > SMA200[t]` | 20 if true, 0 if false |
| **SMA20 > SMA50** | `SMA20[t] > SMA50[t]` | 20 if true, 0 if false |
| **SMA50 > SMA200** | `SMA50[t] > SMA200[t]` | 20 if true, 0 if false |
| **MACD Histogram > 0** | `MACD_hist[t] > 0` | 20 if true, 0 if false |
| **MACD Histogram Rising** | `MACD_hist[t] > MACD_hist[t-1]` | 20 if true, 0 if false |

**Trend Score:** Sum of passed conditions (max 140) → normalized to 0-100: `score = (passed / 7) * 100`

**Rationale:** Multiple timeframe alignment + MACD confirmation = robust trend definition.

#### 2.3 Volume (20%)

**Components (equal weight):**

| Sub-factor | Formula | Normalization |
|------------|---------|---------------|
| **Volume Ratio** | `V[t] / Volume_SMA20[t]` | Percentile rank vs universe (0-100) |
| **OBV Trend** | Slope of OBV over 20 bars (linear regression) | Percentile rank vs universe (0-100) |

**Volume Score:** `(Volume_Ratio_percentile + OBV_Trend_percentile) / 2`

**Rationale:** Current volume surge + cumulative buying pressure (OBV).

#### 2.4 Volatility (10%)

**Component:**

| Sub-factor | Formula | Normalization |
|------------|---------|---------------|
| **Inverse ATR%** | `1 / (ATR14[t] / C[t] * 100)` | Percentile rank vs universe (0-100), **inverted** (lower volatility = higher score) |

**Volatility Score:** `ATR%_percentile_inverted` (so low volatility → high score)

**Rationale:** Lower volatility = more stable trend, better risk-adjusted returns. Inverted so it aligns with "higher is better" composite.

### Composite Score Formula

```
composite = 0.4 * momentum_score
          + 0.3 * trend_score
          + 0.2 * volume_score
          + 0.1 * volatility_score
```

**Score Range:** 0-100 (each component 0-100, weighted sum preserves range)

### Required Indicators (for ranking date `t`)

| Indicator | Period | Used In |
|-----------|--------|---------|
| `SMA20`, `SMA50`, `SMA200` | 20, 50, 200 | Trend |
| `RSI14` | 14 | Momentum, Screening |
| `MACD(12,26,9)` | 12/26/9 | Trend |
| `ROC10` | 10 | Momentum |
| `Volume_SMA20` | 20 | Volume, Screening |
| `OBV` | 20 (slope) | Volume |
| `ATR14` | 14 | Volatility |

### Minimum Data Requirements

| Indicator | Minimum Bars |
|-----------|--------------|
| `SMA200` | 200 |
| `ATR14` | 15 |
| `OBV_20_slope` | 21 |
| **Total** | **200 bars** (most restrictive) |

Symbols with `< 200` valid bars → `excluded` with reason `insufficient_data` and list of missing indicators.

### Ranking Output (Per Symbol)

```json
{
  "rank": 1,
  "symbol": "VNM",
  "composite_score": 82.5,
  "components": {
    "momentum": 85.0,
    "trend": 78.0,
    "volume": 90.0,
    "volatility": 72.0
  },
  "sub_components": {
    "roc10_percentile": 88.0,
    "rsi_normalized": 82.0,
    "trend_conditions_passed": 6,
    "trend_total_conditions": 7,
    "volume_ratio_percentile": 92.0,
    "obv_trend_percentile": 88.0,
    "atr_pct_percentile_inverted": 72.0
  },
  "reasoning": [
    "Strong 10-day ROC (+4.2%) with RSI in bullish zone (58)",
    "Price above SMA20/50/200; MACD histogram expanding",
    "Volume 1.8x average; OBV trending up",
    "Moderate volatility (ATR% = 1.8%)"
  ]
}
```

### Reasoning Template (Deterministic Generation)

Each factor contributes 1-2 reasoning strings based on sub-component values:

| Factor | Condition | Reasoning String |
|--------|-----------|------------------|
| Momentum | ROC10_pctl ≥ 75 | "Strong 10-day ROC ({roc_pct:+.1f}%) with RSI in bullish zone ({rsi:.0f})" |
| Momentum | ROC10_pctl ≥ 50 | "Positive 10-day ROC ({roc_pct:+.1f}%); RSI neutral ({rsi:.0f})" |
| Momentum | ROC10_pctl < 50 | "Weak 10-day ROC ({roc_pct:+.1f}%); RSI {rsi:.0f}" |
| Trend | passed ≥ 5 | "Price above SMA20/50/200; MACD histogram expanding" |
| Trend | passed ≥ 3 | "Price above key SMAs; MACD {histogram > 0 ? 'positive' : 'negative'}" |
| Trend | passed < 3 | "Mixed trend signals; price near SMA20" |
| Volume | vol_pctl ≥ 75 | "Volume {ratio:.1f}x average; OBV trending up" |
| Volume | vol_pctl ≥ 50 | "Volume near average ({ratio:.1f}x); OBV {trend}" |
| Volume | vol_pctl < 50 | "Below-average volume ({ratio:.1f}x); OBV {trend}" |
| Volatility | atr_pctl_inv ≥ 75 | "Low volatility (ATR% = {atr_pct:.1f}%)" |
| Volatility | atr_pctl_inv ≥ 50 | "Moderate volatility (ATR% = {atr_pct:.1f}%)" |
| Volatility | atr_pctl_inv < 50 | "Elevated volatility (ATR% = {atr_pct:.1f}%)" |

**Percentile Calculation:** For each sub-component, compute percentile rank within the **current screening universe** (symbols that passed screening). Use linear interpolation (standard definition).

---

## 3. Environment Variable Configuration

### Ranking Weights

```bash
# .env or deployment config
RANK_WEIGHT_MOMENTUM=0.4
RANK_WEIGHT_TREND=0.3
RANK_WEIGHT_VOLUME=0.2
RANK_WEIGHT_VOLATILITY=0.1
```

**Validation Rules:**
- All four must be set if any is set
- Each ∈ [0.0, 1.0]
- Sum = 1.0 (tolerance: ±0.001)
- On validation failure: service fails to start (fast fail)

### Screening Thresholds (v1.0 — Immutable)

| Threshold | Env Override | Default | Note |
|-----------|--------------|---------|------|
| SMA20 comparison | `SCREEN_PRICE_GT_SMA20` | `true` | Boolean; if false, criterion disabled |
| RSI upper bound | `SCREEN_RSI_MAX` | `70` | Numeric; if null, criterion disabled |
| Volume ratio minimum | `SCREEN_VOLUME_RATIO_MIN` | `1.5` | Numeric; if null, criterion disabled |

**Warning:** Overriding screening thresholds via env creates a **de facto new version**. Audited runs must record effective thresholds.

---

## 4. Determinism Guarantees

### Requirements

1. **Same input + same version = identical output** (bit-identical JSON)
2. **No randomness** anywhere in screening/ranking pipeline
3. **Percentile calculation** uses stable algorithm (linear interpolation, fixed tie-breaking)
4. **Sort stability:** When composite scores tie, secondary sort by `symbol` (ASC) — deterministic tie-break

### Percentile Algorithm (Fixed)

```python
def percentile_rank(values: list[float], target: float) -> float:
    """Linear interpolation percentile (0-100). Matches numpy.percentile default."""
    sorted_vals = sorted(v for v in values if v is not None)
    if not sorted_vals:
        return 50.0  # neutral if no data
    n = len(sorted_vals)
    # Find position
    import bisect
    pos = bisect.bisect_left(sorted_vals, target)
    if pos == 0:
        return 0.0
    if pos == n:
        return 100.0
    # Linear interpolation between pos-1 and pos
    lower = sorted_vals[pos - 1]
    upper = sorted_vals[pos]
    if upper == lower:
        return (pos / n) * 100
    frac = (target - lower) / (upper - lower)
    return ((pos - 1 + frac) / (n - 1)) * 100
```

### Tie-Breaking Rules

| Level | Tie-Breaker |
|-------|-------------|
| Composite score | Symbol (ASC) |
| Component score | Sub-component order (fixed) |

---

## 5. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-01 | Initial: 3-criterion screen, 4-factor ranking with fixed weights |

---

## 6. Open Questions

1. **Sector neutralization:** Should ranking be sector-relative? (v2.0)
2. **Weight optimization:** Backtest-driven weight tuning? (Separate service)
3. **Screening + ranking coupling:** Should ranking only run on screened symbols? (Current: yes, UC-AE-4)
4. **Reasoning language:** English only for v1.0; Vietnamese in v1.1?
5. **ATR% vs ATR absolute:** ATR% (relative to price) better for cross-symbol comparison — confirmed.

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*