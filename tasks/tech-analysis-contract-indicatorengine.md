# IndicatorEngine Contract Specification

**Version:** 1.0.0  
**Status:** Contract Specification (Contract Spec)  
**Owner:** TECHLEAD  
**Service:** TA Core Library (Provider)  
**Consumers:** Alerting Service, Backtesting Service  
**Stack:** Node.js / TypeScript (Node.js 20+, TypeScript 5.x)  
**Security Gate:** §7.2 applies — input validation, no PII in indicators, auth context for audit

---

## 1. Interface Definition (TypeScript Interfaces)

```typescript
/**
 * IndicatorEngine — Interface implemented by TA Core Library
 * Consumed by: Alerting Service, Backtesting Service
 * Version: 1.0.0
 * Semantic Versioning: MAJOR.MINOR.PATCH — breaking changes = MAJOR bump
 */

/**
 * Standardized timestamp in ISO 8601 UTC (ISO 8601:2019, RFC 3339)
 * Must be UTC, millisecond precision, 'Z' suffix.
 * Example: "2026-07-24T14:30:00.123Z"
 */
export type ISOTimestamp = string & { readonly __brand: unique symbol };

/**
 * Trading pair symbol in exchange-standard format
 * Format: "BASE/QUOTE" (e.g., "BTC/USDT", "AAPL/USD")
 */
export type TradingPair = string & { readonly __brand: unique symbol };

/**
 * Timeframe / resolution for indicator calculation
 * Standard ISO 8601 duration subset + common trading intervals
 */
export type Timeframe =
  | "1s" | "5s" | "15s" | "30s"
  | "1m" | "3m" | "5m" | "15m" | "30m"
  | "1h" | "2h" | "4h" | "6h" | "8h" | "12h"
  | "1d" | "3d" | "1w" | "1M";

/**
 * OHLCV bar input for indicator calculation
 * All numeric values as precision-preserving strings
 */
export interface OHLCVBar {
  open: string;
  high: string;
  low: string;
  close: string;
  volume: string;
  timestamp: ISOTimestamp;
  trades?: number;
  vwap?: string;
}

/**
 * Indicator parameter definition (for introspection/validation)
 */
export interface IndicatorParameter {
  /** Parameter name (camelCase) */
  name: string;
  /** Human-readable description */
  description: string;
  /** JSON Schema type: "number" | "integer" | "string" | "boolean" */
  type: "number" | "integer" | "string" | "boolean";
  /** Required parameter */
  required: boolean;
  /** Default value if optional */
  default?: unknown;
  /** Minimum value (for numbers/integers) */
  minimum?: number;
  /** Maximum value (for numbers/integers) */
  maximum?: number;
  /** Allowed enum values (for strings) */
  enum?: string[];
  /** Regex pattern (for strings) */
  pattern?: string;
}

/**
 * Indicator metadata for discovery/introspection
 */
export interface IndicatorMetadata {
  /** Unique indicator identifier (lowercase, kebab-case) */
  id: string;
  /** Human-readable name */
  name: string;
  /** Category for grouping */
  category: "trend" | "momentum" | "volatility" | "volume" | "oscillator" | "custom";
  /** Description of what the indicator computes */
  description: string;
  /** Required input data types */
  inputs: ("open" | "high" | "low" | "close" | "volume" | "vwap" | "trades")[];
  /** Output series produced by this indicator */
  outputs: IndicatorOutputSpec[];
  /** Configurable parameters with validation schema */
  parameters: IndicatorParameter[];
  /** Minimum bars required for first valid output */
  minBars: number;
  /** Whether indicator produces values for every input bar (after warmup) */
  producesEveryBar: boolean;
  /** Version of this indicator implementation */
  version: string;
}

/**
 * Output series specification
 */
export interface IndicatorOutputSpec {
  /** Output series name (e.g., "macd", "signal", "histogram") */
  name: string;
  /** Description of what this output represents */
  description: string;
  /** Type of output values */
  type: "line" | "histogram" | "level" | "signal" | "bool";
  /** For "level" type: reference levels (e.g., [70, 30] for RSI) */
  levels?: number[];
}

/**
 * Indicator parameter values provided by caller
 * Values validated against IndicatorParameter schema
 */
export type IndicatorParameters = Record<string, unknown>;

/**
 * Single indicator output value at a timestamp
 */
export interface IndicatorValue {
  /** Timestamp of this value (matches input bar timestamp) */
  timestamp: ISOTimestamp;
  /** Named output values for this timestamp */
  values: Record<string, string | number | boolean | null>;
  /** Whether this value is "warmed up" (reliable) or still in warmup period */
  isWarmedUp: boolean;
}

/**
 * Complete indicator calculation result
 */
export interface IndicatorResult {
  /** Indicator metadata (echoed from request) */
  indicator: IndicatorMetadata;
  /** Parameters used for this calculation */
  parameters: IndicatorParameters;
  /** Input data range */
  inputRange: {
    start: ISOTimestamp;
    end: ISOTimestamp;
    barCount: number;
  };
  /** Computed values — one per input bar (including warmup) */
  values: IndicatorValue[];
  /** Calculation metadata */
  meta: {
    /** Calculation timestamp (when computation completed) */
    calculatedAt: ISOTimestamp;
    /** Computation time in milliseconds */
    computeTimeMs: number;
    /** Number of bars in warmup period */
    warmupBars: number;
    /** Warnings (e.g., "insufficient data for reliable signal") */
    warnings?: string[];
  };
}

/**
 * Batch calculation request for multiple indicators on same data
 */
export interface BatchIndicatorRequest {
  /** Indicators to compute */
  indicators: Array<{
    id: string;
    parameters?: IndicatorParameters;
  }>;
  /** Shared input data */
  bars: OHLCVBar[];
  /** Optional: only compute last N bars (for streaming/incremental) */
  lastNBars?: number;
}

/**
 * Batch calculation result
 */
export interface BatchIndicatorResult {
  /** Results keyed by indicator ID */
  results: Record<string, IndicatorResult>;
  /** Overall computation time */
  totalComputeTimeMs: number;
  /** Warnings aggregated across all indicators */
  warnings?: string[];
}

/**
 * Authentication / authorization context
 * Passed by consumers for audit trail
 * PII: Contains sub (user ID) — treat as PII per §7.2
 */
export interface AuthContext {
  /** Authenticated subject (user ID, service account) — PII */
  sub: string;
  /** Tenant/organization ID — PII if correlatable */
  tenantId?: string;
  /** Scopes/permissions (space-separated) */
  scopes: string;
  /** Request ID for tracing (UUID v4) */
  requestId: string;
  /** Auth validation timestamp */
  authenticatedAt: ISOTimestamp;
  /** Token expiry */
  expiresAt: ISOTimestamp;
}

/**
 * IndicatorEngine interface — implemented by TA Core Library
 * All methods MUST validate inputs before computation.
 * All numeric computations MUST use arbitrary-precision decimal (decimal.js).
 * No PII in indicator inputs/outputs — only market data.
 * AuthContext passed for audit trail only.
 */
export interface IndicatorEngine {
  /**
   * Get metadata for all available indicators
   * @param auth - Authenticated caller context (requires "indicators:read" scope)
   * @returns Map of indicator ID to metadata
   * @throws IndicatorEngineError
   * @precondition auth valid, has "indicators:read" scope
   * @postcondition Returns all registered indicators with complete metadata
   */
  getAvailableIndicators(auth: AuthContext): Promise<Map<string, IndicatorMetadata>>;

  /**
   * Get metadata for a specific indicator
   * @param auth - Authenticated caller context
   * @param indicatorId - Indicator identifier (from getAvailableIndicators)
   * @returns Indicator metadata
   * @throws IndicatorEngineError
   * @precondition auth valid, has "indicators:read" scope
   * @precondition indicatorId exists in registry
   */
  getIndicatorMetadata(auth: AuthContext, indicatorId: string): Promise<IndicatorMetadata>;

  /**
   * Compute a single indicator on OHLCV data
   * @param auth - Authenticated caller context (requires "indicators:compute" scope)
   * @param indicatorId - Indicator identifier
   * @param parameters - Parameter values (validated against metadata schema)
   * @param bars - OHLCV bars in chronological order (oldest first)
   * @returns Computed indicator values for each bar
   * @throws IndicatorEngineError
   * @precondition auth valid, has "indicators:compute" scope
   * @precondition indicatorId exists
   * @precondition parameters valid per indicator's parameter schema
   * @precondition bars.length >= indicator.minBars
   * @precondition bars sorted ascending by timestamp, no duplicate timestamps
   * @postcondition Returns IndicatorResult with values.length === bars.length
   * @postcondition First `warmupBars` values have isWarmedUp = false
   * @postcondition All decimal outputs as strings matching ^-?\d+(\.\d+)?$
   * @invariant Deterministic: same inputs + same parameters + same version = identical outputs
   * @invariant No side effects — pure computation
   */
  computeIndicator(
    auth: AuthContext,
    indicatorId: string,
    parameters: IndicatorParameters,
    bars: OHLCVBar[]
  ): Promise<IndicatorResult>;

  /**
   * Compute multiple indicators on the same data (batch optimization)
   * @param auth - Authenticated caller context (requires "indicators:compute" scope)
   * @param request - Batch request with indicators and shared data
   * @returns Batch results
   * @throws IndicatorEngineError
   * @precondition auth valid, has "indicators:compute" scope
   * @precondition All indicatorIds exist
   * @precondition All parameters valid for their indicators
   * @precondition bars.length >= max(indicator.minBars)
   * @postcondition All results have values.length === bars.length
   * @postcondition totalComputeTimeMs = sum of individual compute times (within 10%)
   */
  computeBatch(auth: AuthContext, request: BatchIndicatorRequest): Promise<BatchIndicatorResult>;

  /**
   * Validate indicator parameters without computing
   * @param auth - Authenticated caller context
   * @param indicatorId - Indicator identifier
   * @param parameters - Parameters to validate
   * @returns Validation result
   * @throws IndicatorEngineError
   * @precondition auth valid
   * @postcondition Returns valid=true iff parameters pass schema validation
   */
  validateParameters(
    auth: AuthContext,
    indicatorId: string,
    parameters: IndicatorParameters
  ): Promise<{ valid: boolean; errors: ValidationError[] }>;

  /**
   * Get engine version and build info
   * @returns Version information
   */
  getEngineInfo(): Promise<EngineInfo>;
}

/**
 * Engine version and build information
 */
export interface EngineInfo {
  version: string; // semver
  buildTimestamp: ISOTimestamp;
  gitCommit: string;
  indicatorsCount: number;
  supportedTimeframes: Timeframe[];
}
```

---

## 2. Contract Semantics

### 2.1 Preconditions (Engine MUST validate on every request)

| Precondition | Validation | Error Code |
|--------------|------------|------------|
| `auth` present, not expired, valid signature | JWT validation (RS256/ES256), exp check | `AUTH_INVALID` / `AUTH_EXPIRED` |
| `auth.scopes` contains required scope | Scope string contains required scope | `AUTH_INSUFFICIENT_SCOPE` |
| `indicatorId` exists in registry | Registry lookup | `INDICATOR_NOT_FOUND` |
| `parameters` valid per indicator's JSON Schema | AJV validation against parameter schema | `INVALID_PARAMETERS` |
| `bars.length >= indicator.minBars` | Array length check | `INSUFFICIENT_DATA` |
| `bars` sorted ascending by timestamp | Adjacent timestamp comparison | `INVALID_DATA_ORDER` |
| No duplicate timestamps in `bars` | Set size check | `DUPLICATE_TIMESTAMPS` |
| All bar decimals match `^-?\d+(\.\d+)?$` | Regex on each field | `INVALID_DECIMAL_FORMAT` |
| Bar timestamps align with declared timeframe | Modulo check on timestamp | `TIMEFRAME_MISMATCH` |
| `auth.requestId` valid UUID v4 | UUID v4 regex | `INVALID_REQUEST_ID` |
| `lastNBars` (if provided) <= bars.length | Numeric check | `INVALID_LAST_N_BARS` |

**All validation failures MUST return `IndicatorEngineError` with appropriate code, HTTP 400/401/403.**

### 2.2 Postconditions (Engine MUST guarantee on success)

| Method | Postcondition |
|--------|---------------|
| `getAvailableIndicators` | Returns Map with all registered indicators; each has complete `IndicatorMetadata` |
| `getIndicatorMetadata` | Returns metadata matching registered indicator; `version` matches engine version |
| `computeIndicator` | `values.length === bars.length`; first `warmupBars` have `isWarmedUp=false`; all output decimals as strings; `computeTimeMs > 0` |
| `computeBatch` | All results satisfy individual `computeIndicator` postconditions; `totalComputeTimeMs` ≈ sum |
| `validateParameters` | `valid=true` iff parameters pass JSON Schema; `errors` array details each violation |
| `getEngineInfo` | Returns current engine version, build info, indicator count |

### 2.3 Invariants (Engine MUST maintain always)

| Invariant | Description |
|-----------|-------------|
| **Determinism** | Same inputs (bars, parameters, indicator version) → bitwise identical outputs. No randomness, no external state. |
| **Purity** | `computeIndicator` / `computeBatch` have NO side effects. No I/O, no cache mutation, no logging of market data. |
| **Decimal Precision** | All calculations use `decimal.js` (or equivalent) with 38 digits precision, 18 scale. No IEEE 754 float. |
| **Warmup Consistency** | `warmupBars` = `minBars - 1` for standard indicators. First valid index = `warmupBars`. |
| **Timestamp Alignment** | Output `IndicatorValue.timestamp` === input `OHLCVBar.timestamp` for same index. |
| **Parameter Immutability** | Input `parameters` object never mutated. |
| **Auth Context Audit** | `auth.requestId` logged (hashed) with computation metadata for audit trail. |
| **No PII in Output** | Indicator results contain ONLY market data derivatives. No `sub`, `tenantId`, `requestId` in output. |
| **Version Pinning** | Indicator `version` in metadata = engine version at registration. Breaking change = new indicator ID. |

---

## 3. Data Contracts (Exact Types)

All types defined in Section 1 are exact data contracts. **No `any` types.**

### 3.1 Decimal String Contract
- All numeric inputs/outputs as strings matching `^-?\d+(\.\d+)?$`
- Consumers MUST use `decimal.js` for arithmetic
- Engine internally uses `decimal.js` with `Decimal.set({ precision: 38, rounding: 4 })` (ROUND_HALF_UP)

### 3.2 Indicator Registry (Built-in Indicators v1.0.0)

| Indicator ID | Name | Category | minBars | Outputs |
|--------------|------|----------|---------|---------|
| `sma` | Simple Moving Average | trend | period | `sma` (line) |
| `ema` | Exponential Moving Average | trend | period | `ema` (line) |
| `rsi` | Relative Strength Index | momentum | period | `rsi` (level, levels: [70,30]) |
| `macd` | MACD | momentum | slowPeriod | `macd`, `signal`, `histogram` (line, line, histogram) |
| `bbands` | Bollinger Bands | volatility | period | `upper`, `middle`, `lower` (line, line, line) |
| `atr` | Average True Range | volatility | period | `atr` (line) |
| `stoch` | Stochastic Oscillator | momentum | kPeriod | `k`, `d` (level, levels: [80,20]) |
| `adx` | Average Directional Index | trend | period | `adx`, `plusDi`, `minusDi` (line, line, line) |
| `obv` | On-Balance Volume | volume | 1 | `obv` (line) |
| `vwap` | Volume Weighted Average Price | volume | 1 | `vwap` (line) |

**Parameter Schemas (JSON Schema Draft 2020-12):**
Each indicator's `parameters` array defines exact validation schema. Example for `rsi`:
```json
{
  "name": "period",
  "description": "RSI period",
  "type": "integer",
  "required": true,
  "default": 14,
  "minimum": 2,
  "maximum": 200
}
```

### 3.3 Batch Request Contract
- All indicators in batch share same `bars` array
- `lastNBars` (optional): compute only last N bars (for streaming updates)
- If `lastNBars` provided: `bars.length >= max(minBars) + lastNBars` (warmup + requested)

---

## 4. Error Contract

### 4.1 Error Type Hierarchy

```typescript
/**
 * Base error for IndicatorEngine
 */
export abstract class IndicatorEngineError extends Error {
  abstract readonly code: IndicatorEngineErrorCode;
  abstract readonly statusCode: number;
  readonly requestId: string;
  readonly timestamp: ISOTimestamp;
  readonly retryable: boolean;
  readonly retryAfterMs?: number;
  readonly details?: Record<string, unknown>;

  constructor(message: string, requestId: string, options?: {
    retryable?: boolean;
    retryAfterMs?: number;
    details?: Record<string, unknown>;
  }) {
    super(message);
    this.name = this.constructor.name;
    this.requestId = requestId;
    this.timestamp = new Date().toISOString() as ISOTimestamp;
    this.retryable = options?.retryable ?? false;
    this.retryAfterMs = options?.retryAfterMs;
    this.details = options?.details;
  }
}

/**
 * Error codes — exact match required for consumer handling
 */
export type IndicatorEngineErrorCode =
  | "AUTH_INVALID"
  | "AUTH_EXPIRED"
  | "AUTH_INSUFFICIENT_SCOPE"
  | "INDICATOR_NOT_FOUND"
  | "INVALID_PARAMETERS"
  | "INSUFFICIENT_DATA"
  | "INVALID_DATA_ORDER"
  | "DUPLICATE_TIMESTAMPS"
  | "INVALID_DECIMAL_FORMAT"
  | "TIMEFRAME_MISMATCH"
  | "INVALID_REQUEST_ID"
  | "INVALID_LAST_N_BARS"
  | "COMPUTATION_ERROR"
  | "INTERNAL_ERROR";

/**
 * Concrete error classes
 */
export class AuthInvalidError extends IndicatorEngineError {
  readonly code = "AUTH_INVALID" as const;
  readonly statusCode = 401;
  readonly retryable = false;
}
export class AuthExpiredError extends IndicatorEngineError {
  readonly code = "AUTH_EXPIRED" as const;
  readonly statusCode = 401;
  readonly retryable = false;
}
export class AuthInsufficientScopeError extends IndicatorEngineError {
  readonly code = "AUTH_INSUFFICIENT_SCOPE" as const;
  readonly statusCode = 403;
  readonly retryable = false;
}
export class IndicatorNotFoundError extends IndicatorEngineError {
  readonly code = "INDICATOR_NOT_FOUND" as const;
  readonly statusCode = 404;
  readonly retryable = false;
}
export class InvalidParametersError extends IndicatorEngineError {
  readonly code = "INVALID_PARAMETERS" as const;
  readonly statusCode = 400;
  readonly retryable = false;
  readonly details: { errors: ValidationError[] };
  constructor(message: string, requestId: string, errors: ValidationError[]) {
    super(message, requestId, { details: { errors } });
    this.details = { errors };
  }
}
export class InsufficientDataError extends IndicatorEngineError {
  readonly code = "INSUFFICIENT_DATA" as const;
  readonly statusCode = 400;
  readonly retryable = false;
  readonly details: { required: number; provided: number };
  constructor(message: string, requestId: string, required: number, provided: number) {
    super(message, requestId, { details: { required, provided } });
    this.details = { required, provided };
  }
}
export class InvalidDataOrderError extends IndicatorEngineError {
  readonly code = "INVALID_DATA_ORDER" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class DuplicateTimestampsError extends IndicatorEngineError {
  readonly code = "DUPLICATE_TIMESTAMPS" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidDecimalFormatError extends IndicatorEngineError {
  readonly code = "INVALID_DECIMAL_FORMAT" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class TimeframeMismatchError extends IndicatorEngineError {
  readonly code = "TIMEFRAME_MISMATCH" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidRequestIdError extends IndicatorEngineError {
  readonly code = "INVALID_REQUEST_ID" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidLastNBarsError extends IndicatorEngineError {
  readonly code = "INVALID_LAST_N_BARS" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class ComputationError extends IndicatorEngineError {
  readonly code = "COMPUTATION_ERROR" as const;
  readonly statusCode = 500;
  readonly retryable = true;
  readonly retryAfterMs = 1000;
}
export class InternalError extends IndicatorEngineError {
  readonly code = "INTERNAL_ERROR" as const;
  readonly statusCode = 500;
  readonly retryable = true;
  readonly retryAfterMs = 5000;
}

/**
 * Parameter validation error detail
 */
export interface ValidationError {
  parameter: string;
  message: string;
  received: unknown;
  expected: string;
}
```

### 4.2 Retry Semantics

| Error Code | Retryable | Retry-After | Backoff |
|------------|-----------|-------------|---------|
| `COMPUTATION_ERROR` | Yes | 1s | Exponential (1s, 2s, 4s, max 30s) |
| `INTERNAL_ERROR` | Yes | 5s | Exponential (5s, 10s, 20s, max 2m) |
| All 4xx codes | **No** | N/A | Do not retry |

**Consumer MUST:** Max 3 retries, exponential backoff with jitter (±25%), circuit breaker after 5 consecutive 5xx.

### 4.3 Timeout Contracts

| Operation | Engine Timeout | Consumer Timeout |
|-----------|----------------|------------------|
| `getAvailableIndicators` | 100ms | 500ms |
| `getIndicatorMetadata` | 50ms | 200ms |
| `computeIndicator` (1000 bars) | 2s | 5s |
| `computeBatch` (5 indicators, 1000 bars) | 5s | 10s |
| `validateParameters` | 50ms | 200ms |
| `getEngineInfo` | 10ms | 100ms |

---

## 5. Versioning Policy

| Version Component | Meaning | Compatibility |
|-------------------|---------|---------------|
| **MAJOR** (1.x.x → 2.0.0) | Breaking: method removed, param changed, return type changed, error code changed, indicator ID changed/removed, output schema changed | **Breaking** — consumers must update |
| **MINOR** (1.0.x → 1.1.0) | New indicator added, new optional parameter, new optional output field, new error code (retryable only), new optional method | **Backward compatible** |
| **PATCH** (1.0.0 → 1.0.1) | Bug fix, performance, doc update, internal refactor | **Fully compatible** |

**v1.x.x Guarantees:**
- No indicator ID removal
- No required parameter addition
- No output field removal
- No error code removal
- Determinism preserved
- Decimal precision preserved

**Indicator Versioning:**
- Each indicator has own `version` in metadata
- Breaking change to indicator = new indicator ID (e.g., `rsi` → `rsi-v2`)
- Old indicator retained for 2 minor versions (deprecation period)

---

## 6. Test Contract (Contract Tests for TESTER)

**Every IndicatorEngine implementation MUST pass these tests.**

### 6.1 Authentication & Authorization

| Test ID | Scenario | Expected |
|---------|----------|----------|
| `IE-AUTH-001` | Valid auth with `indicators:compute` | 200 OK, result returned |
| `IE-AUTH-002` | Missing auth | `AUTH_INVALID` (401) |
| `IE-AUTH-003` | Expired auth | `AUTH_EXPIRED` (401) |
| `IE-AUTH-004` | Valid auth, missing `indicators:compute` scope | `AUTH_INSUFFICIENT_SCOPE` (403) |
| `IE-AUTH-005` | `getAvailableIndicators` requires `indicators:read` | 403 without scope |
| `IE-AUTH-006` | Invalid `requestId` (not UUID v4) | `INVALID_REQUEST_ID` (400) |
| `IE-AUTH-007` | PII in auth logged only as hash | Audit log shows SHA-256(sub) only |

### 6.2 Input Validation

| Test ID | Method | Scenario | Expected |
|---------|--------|----------|----------|
| `IE-VAL-001` | `computeIndicator` | Unknown indicatorId | `INDICATOR_NOT_FOUND` (404) |
| `IE-VAL-002` | `computeIndicator` | Missing required parameter | `INVALID_PARAMETERS` (400), details list missing param |
| `IE-VAL-003` | `computeIndicator` | Parameter out of range (e.g., period=0) | `INVALID_PARAMETERS` (400), details show min violation |
| `IE-VAL-004` | `computeIndicator` | Parameter wrong type (string for number) | `INVALID_PARAMETERS` (400) |
| `IE-VAL-005` | `computeIndicator` | bars.length < minBars | `INSUFFICIENT_DATA` (400), details {required, provided} |
| `IE-VAL-006` | `computeIndicator` | bars not sorted ascending | `INVALID_DATA_ORDER` (400) |
| `IE-VAL-007` | `computeIndicator` | Duplicate timestamps in bars | `DUPLICATE_TIMESTAMPS` (400) |
| `IE-VAL-008` | `computeIndicator` | Decimal with scientific notation | `INVALID_DECIMAL_FORMAT` (400) |
| `IE-VAL-009` | `computeIndicator` | Bar timestamps don't align with timeframe | `TIMEFRAME_MISMATCH` (400) |
| `IE-VAL-010` | `computeBatch` | One indicator invalid params | `INVALID_PARAMETERS` for whole batch (atomic) |
| `IE-VAL-011` | `validateParameters` | Valid params | `{ valid: true, errors: [] }` |
| `IE-VAL-012` | `validateParameters` | Invalid params | `{ valid: false, errors: [...] }` |

### 6.3 Functional Correctness (Determinism & Accuracy)

| Test ID | Indicator | Scenario | Expected |
|---------|-----------|----------|----------|
| `IE-FUNC-001` | `sma` | period=10, 100 bars | `values.length=100`, first 9 `isWarmedUp=false`, 10th `true`, SMA values match reference implementation (decimal.js) |
| `IE-FUNC-002` | `ema` | period=14, 100 bars | First 13 `isWarmedUp=false`, EMA matches reference (wilders smoothing) |
| `IE-FUNC-003` | `rsi` | period=14, 100 bars | RSI values in [0,100], first 13 not warmed up, levels 70/30 in metadata |
| `IE-FUNC-004` | `macd` | fast=12, slow=26, signal=9 | Three outputs: macd, signal, histogram; histogram = macd - signal |
| `IE-FUNC-005` | `bbands` | period=20, stdDev=2 | Upper > middle > lower for all warmed bars; middle = SMA(20) |
| `IE-FUNC-006` | `atr` | period=14 | ATR > 0 for all warmed bars; uses true range (high-low, high-prevClose, prevClose-low) |
| `IE-FUNC-007` | `stoch` | kPeriod=14, dPeriod=3 | %K and %D in [0,100]; %D = SMA(%K, 3) |
| `IE-FUNC-008` | `adx` | period=14 | ADX, +DI, -DI all >= 0; ADX = smoothed DX |
| `IE-FUNC-009` | `obv` | 50 bars | OBV cumulative; up days add volume, down days subtract |
| `IE-FUNC-010` | `vwap` | 50 bars with volume | VWAP = sum(volume*price)/sum(volume); uses typical price (H+L+C)/3 |
| `IE-FUNC-011` | All | Determinism: same inputs twice | Bitwise identical outputs (JSON stringify equal) |
| `IE-FUNC-012` | All | Warmup: first `minBars-1` bars have `isWarmedUp=false` | Exactly `minBars-1` false, rest true |
| `IE-FUNC-013` | `computeBatch` | 3 indicators on same 500 bars | All 3 results returned, `totalComputeTimeMs` ≈ sum |

### 6.4 Error Handling & Retry

| Test ID | Scenario | Expected |
|---------|----------|----------|
| `IE-ERR-001` | Engine throws during computation (e.g., division by zero in custom indicator) | `COMPUTATION_ERROR` (500), `retryable=true`, `retryAfterMs=1000` |
| `IE-ERR-002` | Consumer retries 3x on `COMPUTATION_ERROR` with exp backoff | All retries attempted, circuit breaker logic not triggered (only 3 5xx) |
| `IE-ERR-003` | 5 consecutive `INTERNAL_ERROR` | Circuit breaker opens (consumer responsibility) |

### 6.5 Contract Compliance

| Test ID | Description |
|---------|-------------|
| `IE-CONTRACT-001` | All decimal outputs match `^-?\d+(\.\d+)?$` |
| `IE-CONTRACT-002` | All timestamps valid ISO 8601 UTC with 'Z' |
| `IE-CONTRACT-003` | Branded types preserved through JSON round-trip |
| `IE-CONTRACT-004` | `X-Request-ID` response header = `auth.requestId` |
| `IE-CONTRACT-005` | No PII in any response body (sub, tenantId absent) |
| `IE-CONTRACT-006` | Error responses no stack traces, no internal details |
| `IE-CONTRACT-007` | 4xx errors have `retryable=false`, 5xx have `retryable=true` |
| `IE-CONTRACT-008` | `computeIndicator` pure: no file I/O, no network, no global mutation |

### 6.6 Performance / SLA

| Test ID | Operation | SLA | Pass Criteria |
|---------|-----------|-----|---------------|
| `IE-PERF-001` | `computeIndicator` (SMA, 1000 bars) | p99 < 500ms | 99th percentile < 500ms over 100 runs |
| `IE-PERF-002` | `computeBatch` (5 indicators, 1000 bars) | p99 < 2s | 99th percentile < 2s |
| `IE-PERF-003` | `getAvailableIndicators` | p99 < 100ms | < 100ms |
| `IE-PERF-004` | Memory: 1000 bars, 10 indicators | < 100MB heap | Heap delta < 100MB |

---

## 7. Security Annotations (§7.2)

| Field / Context | Classification | Handling |
|-----------------|----------------|----------|
| `AuthContext.sub` | **PII** | Hash (SHA-256) in audit logs; never in response |
| `AuthContext.tenantId` | **PII** (Correlatable) | Same as `sub` |
| `AuthContext.requestId` | **Operational** | Log plaintext for tracing; correlate in distributed tracing |
| `AuthContext.scopes` | **AuthZ** | Validate; log hash only |
| `OHLCVBar` fields | **Market Data** (Sensitive) | TLS 1.3 in transit; encrypt at rest; audit access |
| `IndicatorResult` outputs | **Derived Market Data** | Same as market data; no PII |
| `IndicatorParameters` | **Configuration** (Non-sensitive) | Log for audit (no PII) |

**Input Validation (MANDATORY):**
- All strings: max 256 chars (decimals: 64 chars)
- All enums: allowlist validation
- Timestamps: strict ISO 8601 UTC parse, reject non-Z offsets
- Decimals: regex `^-?\d+(\.\d+)?$`, max precision 38, max scale 18
- Arrays: max 10000 bars per request (configurable, default 5000)
- Parameters: JSON Schema validation (AJV) against indicator metadata

**Output Encoding:**
- `Content-Type: application/json; charset=utf-8`
- `X-Content-Type-Options: nosniff`
- No JSONP, no callbacks

---

## 8. Implementation Notes (Non-Normative)

- **Computation Engine**: Use `technicalindicators` library or pure `decimal.js` implementations. No TA-Lib (native binding issues).
- **Streaming/Incremental**: v1.0.0 is batch-only. `lastNBars` supports incremental but recomputes warmup. v2.0.0: `IncrementalIndicatorEngine` interface.
- **Custom Indicators**: Registration API not in v1.0.0. Custom = separate engine instance or v2.0.0 plugin system.
- **Caching**: Metadata cached 5 min. Computation results NOT cached (deterministic = cacheable by consumer).
- **Parallelism**: `computeBatch` should parallelize independent indicators (worker threads or Promise.all).

---

**End of Contract Specification — IndicatorEngine v1.0.0**