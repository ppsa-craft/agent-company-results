# Use Cases: Analysis Engine Service

**Product:** vnstock-advisor  
**Component:** analysis-engine  
**Version:** 1.0  
**Status:** Draft — pending PM sign-off  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Overview

The `analysis-engine` service computes technical indicators (SMA, EMA, RSI, MACD, volume profiles), screens symbols against deterministic criteria, ranks them by a weighted composite score, and returns a ranked list with reasoning per symbol. It consumes the canonical `market_data` schema and produces analysis results for downstream consumers (API gateway, backtest runner, alerting).

---

## Actors

| Actor | Description |
|-------|-------------|
| **API Consumer** | Internal service (api-gateway) or scheduled job requesting analysis for a symbol list/date range |
| **Backtest Runner** | Batch consumer requesting historical indicator values for strategy validation |
| **Alerting System** | Consumer of screening results for trigger evaluation |
| **Data Analyst** | Ad-hoc query consumer via CLI/REPL for exploration |

---

## UC-AE-1: Compute Indicators

### Description

Compute standard technical indicators for a given list of symbols over a specified date range. Indicators: SMA, EMA, RSI, MACD, Volume Profile (VWAP, volume SMA).

### Preconditions

- `market_data` table contains OHLCV rows for requested symbols and date range
- Symbols exist in the active symbol universe
- Date range is valid (start ≤ end, not future)

### Postconditions

- Indicator values computed per specification in `specs/indicators.md`
- Results returned as structured data (JSON/Arrow/Parquet) with metadata: symbol, timestamp, indicator name, value, parameters
- Insufficient data handled per edge-case rules (return `null` with reason code)

### Main Flow

1. Consumer calls `POST /indicators/compute` with payload:
   ```json
   {
     "symbols": ["VNM", "VCB", "FPT"],
     "start_date": "2026-01-01",
     "end_date": "2026-07-30",
     "indicators": ["SMA", "EMA", "RSI", "MACD", "VOLUME_PROFILE"],
     "parameters": {
       "sma_periods": [20, 50, 200],
       "ema_periods": [12, 26],
       "rsi_period": 14,
       "macd_fast": 12,
       "macd_slow": 26,
       "macd_signal": 9,
       "volume_sma_period": 20
     }
   }
   ```
2. Service validates payload (symbols exist, dates valid, parameters within bounds)
3. For each symbol, fetch OHLCV from `market_data` where `timestamp BETWEEN start_date AND end_date` ordered ASC
4. Compute each requested indicator using exact formulas from `specs/indicators.md`
5. Return results:
   ```json
   {
     "request_id": "uuid",
     "results": [
       {
         "symbol": "VNM",
         "indicators": {
           "SMA_20": [ { "timestamp": "2026-01-20T08:00:00Z", "value": 78500.0 }, ... ],
           "EMA_12": [ ... ],
           "RSI_14": [ ... ],
           "MACD": [ { "timestamp": "...", "macd": 120.5, "signal": 95.2, "histogram": 25.3 }, ... ],
           "VOLUME_PROFILE": [ { "timestamp": "...", "vwap": 78200.0, "volume_sma_20": 1500000 }, ... ]
         },
         "metadata": { "data_points": 150, "first_date": "2026-01-02", "last_date": "2026-07-30" }
       }
     ],
     "warnings": [
       { "symbol": "ABC", "indicator": "SMA_200", "reason": "insufficient_data", "available": 50, "required": 200 }
     ]
   }
   ```

### Alternate Flows

- **Partial data:** If a symbol has gaps, compute indicators on available contiguous windows; return `null` for periods with insufficient lookback
- **Single indicator request:** Consumer may request only one indicator type
- **Default parameters:** If `parameters` omitted, use defaults from `specs/indicators.md`

### Acceptance Criteria

- AC-AE-1.1: All indicator formulas match `specs/indicators.md` exactly (tested against fixture data)
- AC-AE-1.2: Insufficient data returns `null` with reason code, not an error
- AC-AE-1.3: Response includes metadata (data points, date range) per symbol
- AC-AE-1.4: Completes within 5s for 100 symbols × 1 year daily data
- AC-AE-1.5: Deterministic output — same input produces bit-identical results

---

## UC-AE-2: Screen Symbols

### Description

Apply deterministic screening criteria to a symbol universe and return passing symbols. Criteria are versioned and configurable via environment variables.

### Preconditions

- Indicators computed (UC-AE-1) or computable on-demand for the screening date
- Screening criteria version specified (default: latest)

### Postconditions

- List of symbols passing all criteria returned with criteria evaluation detail
- Criteria version recorded in response

### Main Flow

1. Consumer calls `POST /screen` with payload:
   ```json
   {
     "symbols": ["VNM", "VCB", "FPT", "HPG", "MWG", ...],
     "date": "2026-07-30",
     "criteria_version": "v1.0"
   }
   ```
2. Service loads criteria for `criteria_version` from `specs/screening-ranking.md`
3. For each symbol, compute required indicators (SMA20, RSI14, volume SMA20) for the screening date
4. Evaluate each criterion:
   - Price > SMA20
   - RSI < 70
   - Volume > 1.5 × Volume SMA20
5. Return passing symbols with evaluation detail:
   ```json
   {
     "criteria_version": "v1.0",
     "screening_date": "2026-07-30",
     "passed": [
       {
         "symbol": "VNM",
         "evaluations": {
           "price_gt_sma20": { "pass": true, "price": 78500, "sma20": 77200 },
           "rsi_lt_70": { "pass": true, "rsi": 58.3 },
           "volume_gt_1_5x_avg": { "pass": true, "volume": 2500000, "avg_volume": 1400000 }
         }
       }
     ],
     "failed": [
       {
         "symbol": "VCB",
         "evaluations": {
           "price_gt_sma20": { "pass": false, "price": 89000, "sma20": 90500 },
           "rsi_lt_70": { "pass": true, "rsi": 62.1 },
           "volume_gt_1_5x_avg": { "pass": true, "volume": 1800000, "avg_volume": 1000000 }
         }
       }
     ],
     "errors": [
       { "symbol": "XYZ", "reason": "insufficient_data", "details": "Only 10 days available, need 20 for SMA20" }
     ]
   }
   ```

### Alternate Flows

- **Custom criteria:** Consumer may override individual thresholds via optional `overrides` field (audit-logged)
- **Batch screening:** For >500 symbols, process asynchronously with `request_id` polling

### Acceptance Criteria

- AC-AE-2.1: Criteria exactly match `specs/screening-ranking.md` for the requested version
- AC-AE-2.2: Deterministic — same input + same version = identical pass/fail
- AC-AE-2.3: Returns evaluation detail for every criterion per symbol (transparency)
- AC-AE-2.4: Handles insufficient data gracefully (moves to `errors` with reason)
- AC-AE-2.5: Criteria version is immutable — v1.0 never changes; new versions are additive

---

## UC-AE-3: Rank Symbols by Composite Score

### Description

Rank a list of symbols by a weighted composite score combining momentum, trend, volume, and volatility factors. Weights are configurable via environment variables with defaults in `specs/screening-ranking.md`.

### Preconditions

- Indicators computed for ranking date (or computable on-demand)
- Ranking algorithm version specified

### Postconditions

- Ranked list returned with composite score, component scores, and reasoning array per symbol
- Ranking version recorded

### Main Flow

1. Consumer calls `POST /rank` with payload:
   ```json
   {
     "symbols": ["VNM", "VCB", "FPT", "HPG", "MWG"],
     "date": "2026-07-30",
     "algorithm_version": "v1.0"
   }
   ```
2. Service loads algorithm config for `algorithm_version` from `specs/screening-ranking.md`
3. For each symbol, compute component scores:
   - **Momentum (40%):** Rate of change (ROC) 10-day + RSI normalization
   - **Trend (30%):** Price vs SMA20/50/200 alignment + MACD histogram slope
   - **Volume (20%):** Volume vs SMA20 ratio + OBV trend
   - **Volatility (10%):** Inverse of ATR(14) normalized (lower volatility = higher score)
4. Compute weighted composite: `score = 0.4*momentum + 0.3*trend + 0.2*volume + 0.1*volatility`
5. Sort descending by composite score
6. Return ranked list with reasoning:
   ```json
   {
     "algorithm_version": "v1.0",
     "ranking_date": "2026-07-30",
     "weights": { "momentum": 0.4, "trend": 0.3, "volume": 0.2, "volatility": 0.1 },
     "ranked": [
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
         "reasoning": [
           "Strong 10-day ROC (+4.2%) with RSI in bullish zone (58)",
           "Price above SMA20/50/200; MACD histogram expanding",
           "Volume 1.8x average; OBV trending up",
           "Moderate volatility (ATR 14 = 1.8%)"
         ]
       },
       {
         "rank": 2,
         "symbol": "FPT",
         "composite_score": 76.2,
         "components": { ... },
         "reasoning": [ ... ]
       }
     ],
     "excluded": [
       { "symbol": "XYZ", "reason": "insufficient_data", "missing": ["SMA200", "ATR14"] }
     ]
   }
   ```

### Alternate Flows

- **Weight override:** Consumer may provide custom weights (summing to 1.0) via optional `weights` field (audit-logged, not persisted)
- **Pre-screened input:** Consumer may pass only pre-screened symbols (from UC-AE-2)

### Acceptance Criteria

- AC-AE-3.1: Algorithm exactly matches `specs/screening-ranking.md` for the requested version
- AC-AE-3.2: Deterministic — same input + same version = identical ranking and scores
- AC-AE-3.3: Reasoning array provides human-readable explanation per component
- AC-AE-3.4: Weights configurable via env (`RANK_WEIGHT_MOMENTUM`, etc.) with defaults in spec
- AC-AE-3.5: Excluded symbols listed with reason (not silently dropped)

---

## UC-AE-4: Return Ranked List with Reasoning Array

### Description

Unified endpoint that runs screening (UC-AE-2) then ranking (UC-AE-3) in a single call, returning the final ranked list with full reasoning per symbol. This is the primary consumer-facing analysis endpoint.

### Preconditions

- Symbol universe provided or default (all active symbols)
- Date valid (latest trading day if omitted)

### Postconditions

- Complete analysis pipeline executed: indicators → screen → rank
- Response includes screening pass/fail, ranking, and reasoning

### Main Flow

1. Consumer calls `POST /analyze` with payload:
   ```json
   {
     "symbols": ["VNM", "VCB", "FPT", "HPG", "MWG", ...],
     "date": "2026-07-30",
     "screen_version": "v1.0",
     "rank_version": "v1.0"
   }
   ```
2. Service executes UC-AE-1 (compute indicators for all symbols)
3. Service executes UC-AE-2 (screen with `screen_version`)
4. Service executes UC-AE-3 (rank passed symbols with `rank_version`)
5. Return unified response:
   ```json
   {
     "request_id": "uuid",
     "analysis_date": "2026-07-30",
     "screen_version": "v1.0",
     "rank_version": "v1.0",
     "weights": { "momentum": 0.4, "trend": 0.3, "volume": 0.2, "volatility": 0.1 },
     "universe_size": 450,
     "screened_count": 180,
     "ranked_count": 180,
     "top_20": [
       {
         "rank": 1,
         "symbol": "VNM",
         "composite_score": 82.5,
         "components": { ... },
         "reasoning": [ ... ],
         "screening": {
           "passed": true,
           "evaluations": { ... }
         }
       },
       ...
     ],
     "excluded": [
       { "symbol": "XYZ", "stage": "screening", "reason": "price_below_sma20" },
       { "symbol": "ABC", "stage": "indicators", "reason": "insufficient_data" }
     ]
   }
   ```

### Alternate Flows

- **Streaming large results:** For universe >500, return `request_id` and stream top-N via SSE or paginated API
- **Cached indicators:** If indicators for date already computed, reuse (cache TTL configurable)

### Acceptance Criteria

- AC-AE-4.1: Pipeline executes all three stages atomically (or with clear partial-failure semantics)
- AC-AE-4.2: Response includes full traceability: screening evals + ranking components + reasoning
- AC-AE-4.3: Versions for screen and rank independently specifiable
- AC-AE-4.4: Completes within 10s for full universe (~500 symbols)
- AC-AE-4.5: Excluded symbols tracked with stage and reason (auditability)

---

## Traceability Matrix

| Use Case | AC IDs | Feeds Task |
|----------|--------|------------|
| UC-AE-1 | AC-AE-1.1–1.5 | `vnstock-advisor-5-dev-analysis-engine` (indicator computation) |
| UC-AE-2 | AC-AE-2.1–2.5 | `vnstock-advisor-5-dev-analysis-engine` (screening logic) |
| UC-AE-3 | AC-AE-3.1–3.5 | `vnstock-advisor-5-dev-analysis-engine` (ranking algorithm) |
| UC-AE-4 | AC-AE-4.1–4.5 | `vnstock-advisor-5-dev-analysis-engine` (unified endpoint) |

---

## Open Questions

1. **Caching strategy:** Should computed indicators be persisted (materialized view) or recomputed on demand? (Affects UC-AE-1/4 latency)
2. **Adjustment for splits/dividends:** Should indicators use raw or adjusted close? (Current schema has no `adj_close` — see market-data.md open questions)
3. **Intraday support:** Will analysis engine need intraday bars (1m, 5m, 1H) or daily only? (Current scope: daily only)
4. **Reasoning language:** Vietnamese or English reasoning strings? (Default: English, i18n later)

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*