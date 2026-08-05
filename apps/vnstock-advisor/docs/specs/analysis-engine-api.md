# Analysis-Engine API Contract

**Product:** vnstock-advisor  
**Component:** analysis-engine  
**Version:** 1.0  
**Status:** Frozen — PM sign-off required before DEV starts screening/ranking  
**PM Sign-off:** ✅ Approved by PM (cycle 42)

---

## Overview

This document defines the **exact, frozen request/response contracts** for the `analysis-engine` service endpoints that screening (`/screen`), ranking (`/rank`), and data-ingest consumers depend on. These contracts are **immutable per version** — `v1.0` never changes. New versions are additive (`v1.1`, `v2.0`). Consumers pin to a version in requests.

**Base URL:** `http://analysis-engine:8002` (docker-compose internal)  
**Content-Type:** `application/json`  
**Error Format:** RFC 7807 Problem Details (`application/problem+json`)

---

## 1. Endpoint: `POST /indicators/compute`

**Purpose:** Compute all 12 indicator families over an OHLCV series for a single symbol. This is the **primary contract** consumed by screening and ranking modules.

### Request

```json
{
  "symbol": "VNM",
  "ohlcv": [
    {
      "time": "2025-01-02T08:00:00Z",
      "open": 75100.0,
      "high": 75500.0,
      "low": 74900.0,
      "close": 75300.0,
      "volume": 1450000,
      "source": "FIXTURE"
    }
  ],
  "algorithm_version": "v1.0",
  "volume_sma_period": 20
}
```

#### Request Schema (Pydantic: `IndicatorComputeRequest`)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `symbol` | string | Yes | `minLength: 1, maxLength: 20` | Stock symbol (VN ticker) |
| `ohlcv` | array[OHLCV] | Yes | `minItems: 1, maxItems: 10000` | Chronological ascending (oldest first) |
| `algorithm_version` | string | Yes | `pattern: "^v\\d+\\.\\d+$"` | Must be `v1.0` (frozen) |
| `volume_sma_period` | integer | No | `minimum: 2, maximum: 200, default: 20` | Period for Volume SMA / VWAP window |

#### OHLCV Item Schema

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `time` | string (ISO 8601) | Yes | — | Timestamp of the bar (UTC) |
| `open` | number | Yes | `gt: 0` | Opening price |
| `high` | number | Yes | `gt: 0` | Highest price |
| `low` | number | Yes | `gt: 0` | Lowest price |
| `close` | number | Yes | `gt: 0` | Closing price |
| `volume` | integer | Yes | `ge: 0` | Trading volume |
| `source` | string | Yes | `minLength: 1, maxLength: 50` | Data source identifier (e.g., `CAFEF`, `VNDIRECT`, `FIXTURE`) |

### Response (200 OK)

```json
{
  "symbol": "VNM",
  "algorithm_version": "v1.0",
  "computed_at": "2026-08-05T10:30:00Z",
  "bars_processed": 250,
  "indicators": {
    "sma20": [null, null, ..., 75250.1234],
    "sma50": [null, ..., 74800.5678],
    "sma200": [null, ..., 72100.9012],
    "ema12": [null, ..., 75320.1111],
    "ema26": [null, ..., 74950.2222],
    "ema9": [null, ..., 75180.3333],
    "rsi14": [null, ..., 58.30],
    "macd": [null, ..., {"macd": 120.5000, "signal": 95.2000, "histogram": 25.3000}],
    "vwap": [null, ..., 75150.4444],
    "volume_sma": [null, ..., 1450000],
    "volume_ratio": [null, ..., 1.25],
    "roc10": [null, ..., 4.20],
    "atr14": [null, ..., 1250.6789],
    "obv": [null, ..., 125000000]
  },
  "warnings": [
    "insufficient_data (SMA200: need 200, have 150)"
  ],
  "last": {
    "sma20": 75250.1234,
    "sma50": 74800.5678,
    "sma200": 72100.9012,
    "ema12": 75320.1111,
    "ema26": 74950.2222,
    "ema9": 75180.3333,
    "rsi14": 58.30,
    "macd": {"macd": 120.5000, "signal": 95.2000, "histogram": 25.3000},
    "vwap": 75150.4444,
    "volume_sma": 1450000,
    "volume_ratio": 1.25,
    "roc10": 4.20,
    "atr14": 1250.6789,
    "obv": 125000000
  }
}
```

#### Response Schema (Pydantic: `IndicatorComputeResponse`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | Yes | Echo of request symbol |
| `algorithm_version` | string | Yes | Echo of request version |
| `computed_at` | string (ISO 8601) | Yes | Server timestamp of computation |
| `bars_processed` | integer | Yes | Number of OHLCV bars received |
| `indicators` | IndicatorsResult | Yes | All 12 indicator families as aligned arrays |
| `warnings` | array[string] | Yes | Non-fatal warnings (e.g., insufficient data) |
| `last` | IndicatorsSnapshot | Yes | Compact snapshot of last computable bar |

#### IndicatorsResult Schema

Each array is **aligned to input bars** (index `i` corresponds to `ohlcv[i]`). `null` means not computable at that index (insufficient data or gap).

| Indicator Family | Array Type | Rounding | Notes |
|------------------|------------|----------|-------|
| `sma20` | `number \| null`[] | 4 decimals | SMA(20) |
| `sma50` | `number \| null`[] | 4 decimals | SMA(50) |
| `sma200` | `number \| null`[] | 4 decimals | SMA(200) |
| `ema12` | `number \| null`[] | 4 decimals | EMA(12, Wilder) |
| `ema26` | `number \| null`[] | 4 decimals | EMA(26, Wilder) |
| `ema9` | `number \| null`[] | 4 decimals | EMA(9, Wilder) |
| `rsi14` | `number \| null`[] | 2 decimals | Wilder RSI(14) |
| `macd` | `MacdValue \| null`[] | 4 decimals | MACD(12,26,9) object per bar |
| `vwap` | `number \| null`[] | 4 decimals | Rolling VWAP(20) |
| `volume_sma` | `number \| null`[] | 0 decimals | Volume SMA(20) |
| `volume_ratio` | `number \| null`[] | 4 decimals | `V[t] / Volume_SMA[t]` |
| `roc10` | `number \| null`[] | 2 decimals | Rate of Change(10), percent |
| `atr14` | `number \| null`[] | 4 decimals | ATR(14, Wilder) |
| `obv` | `integer \| null`[] | 0 decimals | On-Balance Volume |

#### MacdValue Schema

```json
{
  "macd": 120.5000,
  "signal": 95.2000,
  "histogram": 25.3000
}
```

#### IndicatorsSnapshot Schema (the `last` field)

Compact snapshot of the **last computable bar** (rightmost non-null index across all indicators). Used by screening/ranking for the "as of now" evaluation.

### Error Responses

| Status | Code | Title | Detail Example |
|--------|------|-------|----------------|
| 400 | `INVALID_INPUT` | Request validation failed | `ohlcv must have at least 1 item` |
| 400 | `UNSUPPORTED_VERSION` | Algorithm version not supported | `v2.0 not supported; supported: [v1.0]` |
| 422 | `COMPUTATION_ERROR` | Indicator computation failed | `MACD requires at least 34 bars (slow=26 + signal=9 - 1)` |
| 500 | `INTERNAL_ERROR` | Unexpected server error | `Internal computation error` |

**Problem Details Format (all errors):**

```json
{
  "type": "https://vnstock-advisor.com/errors/INVALID_INPUT",
  "title": "Request validation failed",
  "status": 400,
  "detail": "ohlcv must have at least 1 item",
  "instance": "/indicators/compute",
  "errors": [
    {"field": "ohlcv", "message": "must have at least 1 item"}
  ]
}
```

---

## 2. Endpoint: `POST /analyze`

**Purpose:** Higher-level analysis endpoint that accepts a single `MarketDataCreate` (from data-ingest) and returns a summary analysis including trend, signals, and strength. This is the **data-ingest consumer contract** — data-ingest calls this after each successful ingestion.

### Request

```json
{
  "time": "2025-01-02T08:00:00Z",
  "symbol": "VNM",
  "open": 75100.0,
  "high": 75500.0,
  "low": 74900.0,
  "close": 75300.0,
  "volume": 1450000,
  "source": "CAFEF"
}
```

#### Request Schema (Pydantic: `MarketDataCreate` — from `vnstock_shared`)

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `time` | string (ISO 8601) | Yes | — | Timestamp of the market data point |
| `symbol` | string | Yes | `minLength: 1, maxLength: 20` | Stock symbol |
| `open` | number | Yes | `gt: 0` | Opening price |
| `high` | number | Yes | `gt: 0` | Highest price |
| `low` | number | Yes | `gt: 0` | Lowest price |
| `close` | number | Yes | `gt: 0` | Closing price |
| `volume` | integer | Yes | `ge: 0` | Trading volume |
| `source` | string | Yes | `minLength: 1, maxLength: 50` | Data source identifier |

### Response (200 OK)

```json
{
  "symbol": "VNM",
  "timeframe": "1D",
  "analysis": {
    "indicators": {
      "ma_20": 75250.1234,
      "ma_50": 74800.5678,
      "rsi": 58.30,
      "volume": 1450000,
      "macd": {"macd": 120.5000, "signal": 95.2000, "histogram": 25.3000},
      "vwap": 75150.4444
    },
    "signals": ["price_above_sma20", "rsi_bullish", "macd_positive"],
    "trend": "BULLISH",
    "strength": 0.72
  },
  "timestamp": "2026-08-05T10:30:00Z"
}
```

#### Response Schema (Pydantic: `AnalyzeResponse`)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | Yes | Echo of request symbol |
| `timeframe` | string | Yes | Fixed to `"1D"` (daily bars) |
| `analysis` | AnalysisSummary | Yes | Computed analysis summary |
| `timestamp` | string (ISO 8601) | Yes | Server timestamp |

#### AnalysisSummary Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `indicators` | object | Yes | Key indicators at latest bar (subset of full indicator set) |
| `signals` | string[] | Yes | List of triggered signal names (see Signal Catalog below) |
| `trend` | string | Yes | One of: `BULLISH`, `BEARISH`, `SIDEWAYS` |
| `strength` | number | Yes | Trend strength 0.0–1.0 |

#### Signal Catalog (v1.0)

| Signal | Trigger Condition |
|--------|-------------------|
| `price_above_sma20` | `close > SMA20` |
| `price_below_sma20` | `close < SMA20` |
| `price_above_sma50` | `close > SMA50` |
| `price_below_sma50` | `close < SMA50` |
| `rsi_bullish` | `RSI14 > 50` |
| `rsi_bearish` | `RSI14 < 50` |
| `rsi_overbought` | `RSI14 >= 70` |
| `rsi_oversold` | `RSI14 <= 30` |
| `macd_positive` | `MACD_histogram > 0` |
| `macd_negative` | `MACD_histogram < 0` |
| `macd_rising` | `MACD_histogram[t] > MACD_histogram[t-1]` |
| `macd_falling` | `MACD_histogram[t] < MACD_histogram[t-1]` |
| `volume_surge` | `volume_ratio > 1.5` |
| `volume_dry` | `volume_ratio < 0.5` |

#### Trend Logic (v1.0)

```
BULLISH   if (close > SMA20) and (close > SMA50) and (MACD_histogram > 0)
BEARISH   if (close < SMA20) and (close < SMA50) and (MACD_histogram < 0)
SIDEWAYS  otherwise
```

#### Strength Calculation (v1.0)

```
strength = (
    (close > SMA20 ? 1 : 0) +
    (close > SMA50 ? 1 : 0) +
    (MACD_histogram > 0 ? 1 : 0) +
    (RSI14 > 50 ? 1 : 0) +
    (volume_ratio > 1.0 ? 1 : 0)
) / 5.0
```

### Error Responses

| Status | Code | Title | Detail Example |
|--------|------|-------|----------------|
| 400 | `INVALID_INPUT` | Request validation failed | `close must be greater than 0` |
| 422 | `INSUFFICIENT_HISTORY` | Not enough historical data for analysis | `Need at least 50 bars for SMA50; have 10` |
| 500 | `INTERNAL_ERROR` | Unexpected server error | `Internal computation error` |

---

## 3. Endpoint: `POST /screen`

**Purpose:** Screening endpoint — applies versioned criteria to a universe of symbols. **Consumes `/indicators/compute` output internally.** Defined here for contract completeness; detailed spec in `screening-ranking.md`.

### Request

```json
{
  "symbols": ["VNM", "VCB", "FPT", "HPG", "MWG"],
  "as_of_date": "2025-07-30",
  "criteria_version": "v1.0"
}
```

### Response (200 OK)

```json
{
  "criteria_version": "v1.0",
  "as_of_date": "2025-07-30",
  "screened_at": "2026-08-05T10:30:00Z",
  "results": [
    {
      "symbol": "VNM",
      "passed": true,
      "evaluations": {
        "price_gt_sma20": {"pass": true, "price": 82000.0, "sma20": 80000.0, "diff_pct": 2.50},
        "rsi_lt_70": {"pass": true, "rsi": 58.3, "threshold": 70},
        "volume_gt_1_5x_avg": {"pass": true, "volume": 2500000, "avg_volume": 1400000, "ratio": 1.79}
      }
    },
    {
      "symbol": "VCB",
      "passed": false,
      "evaluations": {
        "price_gt_sma20": {"pass": false, "price": 88000.0, "sma20": 89000.0, "diff_pct": -1.12},
        "rsi_lt_70": {"pass": true, "rsi": 62.0, "threshold": 70},
        "volume_gt_1_5x_avg": {"pass": true, "volume": 3200000, "avg_volume": 3000000, "ratio": 1.07}
      }
    }
  ],
  "excluded": [
    {"symbol": "ABC", "reason": "insufficient_data", "missing_indicators": ["SMA20", "RSI14", "Volume_SMA20"]}
  ]
}
```

---

## 4. Endpoint: `POST /rank`

**Purpose:** Ranking endpoint — computes weighted composite scores for screened symbols. **Consumes `/indicators/compute` output + screening output internally.** Defined here for contract completeness; detailed spec in `screening-ranking.md`.

### Request

```json
{
  "symbols": ["VNM", "MWG", "FPT", "CCC", "AAA"],
  "as_of_date": "2025-07-30",
  "algorithm_version": "v1.0",
  "weights": {
    "momentum": 0.4,
    "trend": 0.3,
    "volume": 0.2,
    "volatility": 0.1
  }
}
```

### Response (200 OK)

```json
{
  "algorithm_version": "v1.0",
  "as_of_date": "2025-07-30",
  "ranked_at": "2026-08-05T10:30:00Z",
  "weights_used": {"momentum": 0.4, "trend": 0.3, "volume": 0.2, "volatility": 0.1},
  "ranked": [
    {
      "rank": 1,
      "symbol": "VNM",
      "composite_score": 82.5,
      "components": {"momentum": 85.0, "trend": 78.0, "volume": 90.0, "volatility": 72.0},
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
  ],
  "excluded": [
    {"symbol": "XYZ", "reason": "insufficient_data", "missing_indicators": ["SMA200", "ATR14"]}
  ]
}
```

---

## 5. Endpoint: `GET /health`

**Purpose:** Health check for orchestration and load balancers.

### Response (200 OK)

```json
{
  "status": "healthy",
  "service": "analysis-engine",
  "version": "0.1.0",
  "timestamp": "2026-08-05T10:30:00Z",
  "checks": [
    {"name": "database", "status": "ok"},
    {"name": "indicators_module", "status": "ok"}
  ]
}
```

---

## 6. Versioning & Compatibility Policy

| Aspect | Rule |
|--------|------|
| **Algorithm versions** | `v1.0` frozen; `v1.1` additive; consumers pin version in request |
| **Breaking changes** | Never in same major version; `v2.0` = new contract |
| **Deprecation** | Old versions supported 12 months after replacement |
| **Response additions** | New fields allowed (non-breaking); consumers must ignore unknown fields |
| **Error codes** | Stable per version; new codes only in new versions |

---

## 7. Rate Limiting & Timeouts

| Endpoint | Rate Limit | Timeout |
|----------|------------|---------|
| `/indicators/compute` | 100 req/min per IP | 30s |
| `/analyze` | 200 req/min per IP | 10s |
| `/screen` | 50 req/min per IP | 60s |
| `/rank` | 50 req/min per IP | 60s |
| `/health` | Unlimited | 5s |

---

## 8. Security Requirements

- All endpoints: Input validation via Pydantic; no stack traces in errors (Problem Details only)
- `/screen`, `/rank`, `/indicators/compute`: Require API key header `X-API-Key` (enforced at API gateway)
- `/analyze`: Internal-only (data-ingest → analysis-engine); not exposed externally
- CORS: Restricted to known origins; no credentials
- Security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy: default-src 'none'`

---

## 9. Implementation Notes for DEV

1. **File boundary:** This contract owns `services/analysis-engine/src/main.py` (endpoints) and `services/analysis-engine/src/schemas.py` (Pydantic models). The indicator computation lives in `indicators.py` (task 5a).
2. **Dependency:** `/analyze` must fetch historical bars from data-ingest / database to compute indicators (minimum 200 bars for full analysis). Implement a `get_history(symbol, bars=200)` client call.
3. **Determinism:** Same input + same version → bit-identical JSON. No randomness anywhere.
4. **Testing:** Use fixtures from `docs/testing/fixtures.md` — `normal-trading.json` for happy path, `insufficient-data.json` for edge cases.

---

## 10. Open Questions (Requires CTO/TECHLEAD Decision)

1. **Historical data source for `/analyze`:** Should analysis-engine query the database directly, or call data-ingest's (future) `/bars` endpoint? **Decision needed before DEV starts 5b/5c.**
2. **`/analyze` timeframe parameter:** Currently fixed to `1D`. Support `1W`, `1M` via resampling? **Defer to v1.1.**
3. **Batch `/indicators/compute`:** Support multiple symbols in one request? **Defer to v1.1.**

---

*Document status: Frozen — PM sign-off required. DEV may begin implementation against this contract.*