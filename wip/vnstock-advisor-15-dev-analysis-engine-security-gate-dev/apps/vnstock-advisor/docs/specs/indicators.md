# Indicator Specifications

**Product:** vnstock-advisor  
**Component:** analysis-engine  
**Version:** 1.0  
**Status:** Draft — pending PM sign-off  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Overview

This document defines exact formulas, parameters, and edge-case handling for all technical indicators computed by the `analysis-engine` service. All formulas reference standard Technical Analysis definitions (Wilder, Murphy, standard TA literature). Implementations must produce bit-identical results to the reference test fixtures in `testing/fixtures.md`.

**Versioning:** Indicator formulas are versioned. This document is `v1.0`. Any change to a formula creates a new version (e.g., `v1.1`). Consumers specify the version in requests.

---

## Conventions

| Convention | Definition |
|------------|------------|
| `C[t]` | Close price at timestamp `t` (current bar) |
| `H[t]` | High price at timestamp `t` |
| `L[t]` | Low price at timestamp `t` |
| `V[t]` | Volume at timestamp `t` |
| `O[t]` | Open price at timestamp `t` |
| `t` | Current index (0 = oldest, N-1 = most recent) |
| `N` | Total number of bars in the input series |
| `P` | Period (lookback window) |
| `null` | Insufficient data — not computable (distinct from 0) |
| **Rounding** | Final values rounded to 4 decimal places for prices, 2 for RSI/percentages, 0 for volume |

**Data Ordering:** Input OHLCV arrays are **chronological ascending** (oldest first). All formulas assume this ordering.

---

## 1. Simple Moving Average (SMA)

### Formula

```
SMA[t, P] = (1/P) * Σ_{i=t-P+1}^{t} C[i]    for t ≥ P-1
SMA[t, P] = null                              for t < P-1
```

### Parameters

| Parameter | Default | Valid Range | Description |
|-----------|---------|-------------|-------------|
| `period` | 20 | [2, 500] | Number of periods (bars) |

### Standard Periods (Pre-configured)

- `SMA_20` — Short-term trend (default)
- `SMA_50` — Medium-term trend
- `SMA_200` — Long-term trend

### Edge Cases

| Condition | Behavior |
|-----------|----------|
| `N < P` | All outputs `null`; warning: `insufficient_data (need P, have N)` |
| `P ≤ 1` | Validation error (reject request) |
| `P > N` | Same as `N < P` |
| Missing `C[i]` (gap) | Treat as `null` — if any input in window is `null`, output `null` for that `t` |

### Reference Implementation (Python)

```python
def sma(closes: list[float], period: int) -> list[float | None]:
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result = [None] * n
    if n < period:
        return result
    # First computable index is period-1
    window_sum = sum(closes[:period])
    result[period - 1] = round(window_sum / period, 4)
    for t in range(period, n):
        window_sum += closes[t] - closes[t - period]
        result[t] = round(window_sum / period, 4)
    return result
```

---

## 2. Exponential Moving Average (EMA)

### Formula

Uses **Wilder's Smoothing** (standard in TA, not the simple EMA formula):

```
α = 1 / P
EMA[t, P] = C[t] * α + EMA[t-1, P] * (1 - α)    for t ≥ P-1
EMA[t, P] = SMA[t, P]                            for t = P-1 (seed)
EMA[t, P] = null                                 for t < P-1
```

**Note:** The seed at `t = P-1` is the SMA of the first `P` closes. This matches TradingView, vnstock, and standard TA libraries.

### Parameters

| Parameter | Default | Valid Range | Description |
|-----------|---------|-------------|-------------|
| `period` | 12 | [2, 500] | Number of periods |
| `alpha` | `1/period` | (0, 1] | Override smoothing factor (optional) |

### Standard Periods (Pre-configured)

- `EMA_12` — MACD fast line
- `EMA_26` — MACD slow line
- `EMA_9` — MACD signal line (also used standalone)

### Edge Cases

| Condition | Behavior |
|-----------|----------|
| `N < P` | All outputs `null`; warning |
| `P ≤ 1` | Validation error |
| Missing `C[i]` | If seed window has gaps → all `null`; if gap after seed → propagate `null` forward until `P` valid bars accumulate |

### Reference Implementation (Python)

```python
def ema(closes: list[float], period: int, alpha: float | None = None) -> list[float | None]:
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result = [None] * n
    if n < period:
        return result
    alpha = alpha or (1.0 / period)
    # Seed with SMA of first P closes
    seed = sum(closes[:period]) / period
    result[period - 1] = round(seed, 4)
    for t in range(period, n):
        if closes[t] is None or result[t - 1] is None:
            result[t] = None
        else:
            result[t] = round(closes[t] * alpha + result[t - 1] * (1 - alpha), 4)
    return result
```

---

## 3. Relative Strength Index (RSI)

### Formula

**Wilder's RSI** (standard 14-period):

```
Δ[t] = C[t] - C[t-1]                    for t ≥ 1
Gain[t] = max(Δ[t], 0)
Loss[t] = max(-Δ[t], 0)

AvgGain[t, P] = SMA(Gain, P)[t]         for t = P (first computable)
AvgLoss[t, P] = SMA(Loss, P)[t]         for t = P (first computable)

AvgGain[t, P] = (AvgGain[t-1, P]*(P-1) + Gain[t]) / P    for t > P (Wilder smoothing)
AvgLoss[t, P] = (AvgLoss[t-1, P]*(P-1) + Loss[t]) / P   for t > P

RS[t] = AvgGain[t] / AvgLoss[t]         if AvgLoss[t] > 0 else INF
RSI[t] = 100 - (100 / (1 + RS[t]))      if AvgLoss[t] > 0 else 100
RSI[t] = 0                              if AvgGain[t] == 0 and AvgLoss[t] == 0
```

**Key:** The first `P` periods use simple average (SMA) for Gain/Loss; subsequent periods use Wilder's smoothing (equivalent to EMA with α=1/P).

### Parameters

| Parameter | Default | Valid Range | Description |
|-----------|---------|-------------|-------------|
| `period` | 14 | [2, 100] | Lookback period |

### Standard Period

- `RSI_14` — Default (only period supported in v1.0)

### Edge Cases

| Condition | Behavior |
|-----------|----------|
| `N ≤ P` | All outputs `null` (need `P+1` closes for first Δ) |
| `AvgLoss == 0` | RSI = 100 (all gains, no losses) |
| `AvgGain == 0` | RSI = 0 (all losses, no gains) |
| Flat market (no price change) | RSI = 50 (by convention: 0/0 → 50) |
| Missing `C[i]` | Gap in Δ → `null` propagates; need `P` valid Δs after gap |

### Reference Implementation (Python)

```python
def rsi(closes: list[float], period: int = 14) -> list[float | None]:
    if period < 2:
        raise ValueError("period must be >= 2")
    n = len(closes)
    result = [None] * n
    if n <= period:
        return result
    # Compute deltas
    deltas = [None] + [closes[i] - closes[i-1] for i in range(1, n)]
    gains = [max(d, 0) if d is not None else None for d in deltas]
    losses = [max(-d, 0) if d is not None else None for d in deltas]
    # First avg gain/loss at index P (using first P deltas: indices 1..P)
    first_idx = period
    valid_gains = [g for g in gains[1:first_idx+1] if g is not None]
    valid_losses = [l for l in losses[1:first_idx+1] if l is not None]
    if len(valid_gains) < period or len(valid_losses) < period:
        return result
    avg_gain = sum(valid_gains) / period
    avg_loss = sum(valid_losses) / period
    # Compute RSI at first_idx
    if avg_loss == 0:
        result[first_idx] = 100.0 if avg_gain > 0 else 50.0
    else:
        rs = avg_gain / avg_loss
        result[first_idx] = round(100 - 100 / (1 + rs), 2)
    # Wilder smoothing for subsequent
    for t in range(first_idx + 1, n):
        if gains[t] is None or losses[t] is None:
            result[t] = None
            continue
        avg_gain = (avg_gain * (period - 1) + gains[t]) / period
        avg_loss = (avg_loss * (period - 1) + losses[t]) / period
        if avg_loss == 0:
            result[t] = 100.0 if avg_gain > 0 else 50.0
        else:
            rs = avg_gain / avg_loss
            result[t] = round(100 - 100 / (1 + rs), 2)
    return result
```

---

## 4. Moving Average Convergence Divergence (MACD)

### Formula

Three components computed from close prices:

```
EMA_fast[t] = EMA(C, fast_period)[t]
EMA_slow[t] = EMA(C, slow_period)[t]
MACD_line[t] = EMA_fast[t] - EMA_slow[t]              (both must be non-null)
Signal_line[t] = EMA(MACD_line, signal_period)[t]     (EMA of MACD line)
Histogram[t] = MACD_line[t] - Signal_line[t]
```

**Default periods (standard):** `fast=12`, `slow=26`, `signal=9`

### Parameters

| Parameter | Default | Valid Range | Description |
|-----------|---------|-------------|-------------|
| `fast_period` | 12 | [2, 100] | Fast EMA period |
| `slow_period` | 26 | [fast+1, 200] | Slow EMA period (must be > fast) |
| `signal_period` | 9 | [2, 100] | Signal line EMA period |

### Standard Configuration

- `MACD(12, 26, 9)` — Only configuration in v1.0

### Edge Cases

| Condition | Behavior |
|-----------|----------|
| `N < slow_period + signal_period - 1` | All outputs `null` (need enough data for slow EMA + signal EMA seed) |
| `fast_period ≥ slow_period` | Validation error |
| Missing `C[i]` | Propagates through EMA → MACD → Signal → Histogram |

### Output Structure

Each computable timestamp returns an object:

```json
{
  "timestamp": "2026-07-30T08:00:00Z",
  "macd": 120.5000,
  "signal": 95.2000,
  "histogram": 25.3000
}
```

### Reference Implementation (Python)

```python
def macd(closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> list[dict | None]:
    if fast >= slow:
        raise ValueError("fast_period must be < slow_period")
    n = len(closes)
    result = [None] * n
    if n < slow + signal - 1:
        return result
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    # MACD line
    macd_line = [None] * n
    for t in range(n):
        if ema_fast[t] is not None and ema_slow[t] is not None:
            macd_line[t] = round(ema_fast[t] - ema_slow[t], 4)
    # Signal line (EMA of MACD line)
    # Filter out None values for EMA seeding
    valid_macd = [(i, v) for i, v in enumerate(macd_line) if v is not None]
    if len(valid_macd) < signal:
        return result
    # Compute EMA on MACD line values only, then map back
    macd_values = [v for _, v in valid_macd]
    signal_ema = ema(macd_values, signal)
    # Map back to original indices
    signal_line = [None] * n
    for (idx, _), sig in zip(valid_macd[signal-1:], signal_ema[signal-1:]):
        signal_line[idx] = round(sig, 4)
    # Histogram
    for t in range(n):
        if macd_line[t] is not None and signal_line[t] is not None:
            result[t] = {
                "macd": macd_line[t],
                "signal": signal_line[t],
                "histogram": round(macd_line[t] - signal_line[t], 4)
            }
    return result
```

---

## 5. Volume Profile

### Components

| Component | Formula | Description |
|-----------|---------|-------------|
| **VWAP** | `Σ_{i=0}^{t} (TypicalPrice[i] * V[i]) / Σ_{i=0}^{t} V[i]` | Volume-Weighted Average Price (session or rolling) |
| **Volume SMA** | `SMA(V, volume_period)[t]` | Simple moving average of volume |
| **Volume Ratio** | `V[t] / Volume_SMA[t]` | Current volume vs average |

**Typical Price:** `(H + L + C) / 3` for daily bars. For rolling VWAP, use rolling window.

### Parameters

| Parameter | Default | Valid Range | Description |
|-----------|---------|-------------|-------------|
| `volume_sma_period` | 20 | [2, 200] | Period for Volume SMA |
| `vwap_window` | `session` | `session`, `rolling:N` | VWAP reset: per session (daily) or rolling N bars |

### Standard Configuration (v1.0)

- `Volume_SMA_20` — 20-period volume average
- `VWAP_session` — Session VWAP (resets each trading day)
- `Volume_Ratio` — `V[t] / Volume_SMA_20[t]`

### Formulas

**Session VWAP (daily reset):**
```
TypicalPrice[t] = (H[t] + L[t] + C[t]) / 3
Cumulative_Volume[t] = Σ_{i=session_start}^{t} V[i]
Cumulative_PV[t] = Σ_{i=session_start}^{t} TypicalPrice[i] * V[i]
VWAP[t] = Cumulative_PV[t] / Cumulative_Volume[t]    if Cumulative_Volume[t] > 0 else C[t]
```

**Rolling VWAP (window P):**
```
VWAP_rolling[t, P] = Σ_{i=t-P+1}^{t} (TypicalPrice[i] * V[i]) / Σ_{i=t-P+1}^{t} V[i]
```

### Edge Cases

| Condition | Behavior |
|-----------|----------|
| `V[t] == 0` for all bars in window | VWAP = `C[t]` (fallback to close) |
| `Volume_SMA == 0` | Volume Ratio = `null` (not 0, not INF) |
| `N < volume_sma_period` | Volume SMA = `null`; Volume Ratio = `null` |
| Missing `V[i]` | Treat as 0 for VWAP numerator/denominator; `null` for Volume SMA |

### Reference Implementation (Python)

```python
def volume_profile(
    highs: list[float],
    lows: list[float],
    closes: list[float],
    volumes: list[int],
    volume_sma_period: int = 20
) -> list[dict | None]:
    n = len(closes)
    result = [None] * n
    if n < volume_sma_period:
        return result
    # Typical price
    typical = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
    # Session VWAP (assumes daily bars, each bar = one session)
    # For daily data, session VWAP = typical price (single bar per session)
    # Rolling VWAP over volume_sma_period bars
    vwap = [None] * n
    vol_sma = sma([float(v) for v in volumes], volume_sma_period)
    for t in range(volume_sma_period - 1, n):
        # Rolling VWAP
        pv_sum = sum(typical[i] * volumes[i] for i in range(t - volume_sma_period + 1, t + 1))
        v_sum = sum(volumes[i] for i in range(t - volume_sma_period + 1, t + 1))
        vwap[t] = round(pv_sum / v_sum, 4) if v_sum > 0 else closes[t]
    # Volume ratio
    vol_ratio = [None] * n
    for t in range(n):
        if vol_sma[t] is not None and vol_sma[t] > 0:
            vol_ratio[t] = round(volumes[t] / vol_sma[t], 4)
    # Build output
    for t in range(n):
        if vol_sma[t] is not None:
            result[t] = {
                "vwap": vwap[t],
                "volume_sma": round(vol_sma[t], 0),
                "volume_ratio": vol_ratio[t]
            }
    return result
```

---

## 6. Additional Indicators for Ranking (UC-AE-3)

These are computed internally for ranking; not directly exposed via `/indicators/compute` but documented for completeness.

### 6.1 Rate of Change (ROC)

```
ROC[t, P] = (C[t] - C[t-P]) / C[t-P] * 100    for t ≥ P
ROC[t, P] = null                               for t < P
```

- Default `P = 10` (10-day ROC)
- Used in **Momentum** component

### 6.2 Average True Range (ATR)

**True Range:**
```
TR[t] = max(H[t] - L[t], |H[t] - C[t-1]|, |L[t] - C[t-1]|)
```

**ATR (Wilder smoothing, period 14):**
```
ATR[t, 14] = SMA(TR, 14)[t]              for t = 14 (seed)
ATR[t, 14] = (ATR[t-1] * 13 + TR[t]) / 14   for t > 14
```

- Used in **Volatility** component (inverse normalized)

### 6.3 On-Balance Volume (OBV)

```
OBV[0] = V[0]
OBV[t] = OBV[t-1] + V[t]     if C[t] > C[t-1]
OBV[t] = OBV[t-1] - V[t]     if C[t] < C[t-1]
OBV[t] = OBV[t-1]            if C[t] == C[t-1]
```

- OBV trend (slope over 20 bars) used in **Volume** component

### 6.4 Price vs SMA Alignment (Trend Component)

```
Trend_Score = (Price > SMA20) * 1 + (Price > SMA50) * 1 + (Price > SMA200) * 1
              + (SMA20 > SMA50) * 1 + (SMA50 > SMA200) * 1
```
Normalized to 0-100 scale (max 5 conditions → each = 20 points)

---

## 7. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-01 | Initial release: SMA, EMA, RSI, MACD, Volume Profile, ROC, ATR, OBV |

---

## 8. Open Questions

1. **Adjusted prices:** Should indicators use split/dividend-adjusted close? (Current schema: no `adj_close` column)
2. **Intraday VWAP:** For future intraday support, session VWAP needs proper session boundary detection
3. **RSI smoothing variant:** Some libraries use simple EMA for Gain/Loss after seed; we use Wilder's. Confirm with PM.
4. **MACD histogram precision:** 4 decimals sufficient? (VND prices up to ~1M, MACD differences small)

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*