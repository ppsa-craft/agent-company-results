# DataProvider Contract Specification

**Version:** 1.0.0  
**Status:** Contract Specification (Contract Spec)  
**Owner:** TECHLEAD  
**Service:** Data Ingestion Service (Provider)  
**Consumers:** TA Core Library, Backtesting Service  
**Stack:** Node.js / TypeScript (Node.js 20+, TypeScript 5.x)  
**Security Gate:** §7.2 applies — PII annotation, auth context, input validation required

---

## 1. Interface Definition (TypeScript Interfaces)

```typescript
/**
 * DataProvider — Interface implemented by Data Ingestion Service
 * Consumed by: TA Core Library, Backtesting Service
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
 * ISO 4217 currency code (3-letter alphabetic)
 * Example: "USD", "EUR", "BTC"
 */
export type CurrencyCode = string & { readonly __brand: unique symbol };

/**
 * Trading pair symbol in exchange-standard format
 * Format: "BASE/QUOTE" (e.g., "BTC/USDT", "AAPL/USD")
 */
export type TradingPair = string & { readonly __brand: unique symbol };

/**
 * Exchange identifier (lowercase, exchange-standard slug)
 * Examples: "binance", "coinbase", "kraken", "alpaca", "polygon"
 */
export type ExchangeId = string & { readonly __brand: unique symbol };

/**
 * Timeframe / resolution for OHLCV bars
 * Standard ISO 8601 duration subset + common trading intervals
 */
export type Timeframe =
  | "1s" | "5s" | "15s" | "30s"
  | "1m" | "3m" | "5m" | "15m" | "30m"
  | "1h" | "2h" | "4h" | "6h" | "8h" | "12h"
  | "1d" | "3d" | "1w" | "1M";

/**
 * OHLCV bar (Open, High, Low, Close, Volume)
 * All numeric values as string to preserve precision (decimal.js compatible)
 */
export interface OHLCVBar {
  /** Opening price — string decimal, e.g., "42150.25" */
  open: string;
  /** Highest price — string decimal */
  high: string;
  /** Lowest price — string decimal */
  low: string;
  /** Closing price — string decimal */
  close: string;
  /** Volume in base asset units — string decimal */
  volume: string;
  /** Bar timestamp (open time) — ISO 8601 UTC */
  timestamp: ISOTimestamp;
  /** Optional: number of trades in this bar */
  trades?: number;
  /** Optional: VWAP for the bar */
  vwap?: string;
}

/**
 * Ticker / 24h summary snapshot
 */
export interface TickerSnapshot {
  tradingPair: TradingPair;
  exchange: ExchangeId;
  /** Current last price */
  last: string;
  /** 24h price change (absolute) */
  change24h: string;
  /** 24h price change percent */
  changePercent24h: string;
  /** 24h volume in base asset */
  volume24h: string;
  /** 24h quote volume (quote asset volume) */
  quoteVolume24h: string;
  /** 24h high */
  high24h: string;
  /** 24 low */
  low24h: string;
  /** Best bid */
  bid: string;
  /** Best ask */
  ask: string;
  /** Timestamp of snapshot */
  timestamp: ISOTimestamp;
}

/**
 * Order book snapshot (L2 / L3)
 */
export interface OrderBookSnapshot {
  tradingPair: TradingPair;
  exchange: ExchangeId;
  /** Bids: [price, size] — price descending */
  bids: [string, string][];
  /** Asks: [price, size] — price ascending */
  asks: [string, string][];
  timestamp: ISOTimestamp;
  /** Sequence number for gap detection */
  sequence: number;
}

/**
 * Trade execution (print)
 */
export interface TradePrint {
  tradeId: string;
  tradingPair: TradingPair;
  exchange: ExchangeId;
  price: string;
  size: string;
  side: "buy" | "sell";
  timestamp: ISOTimestamp;
  /** Optional: aggressive side indicator */
  isBuyerMaker?: boolean;
}

/**
 * Pagination cursor for paginated responses
 * Opaque cursor token — treat as opaque string
 */
export type PaginationCursor = string & { readonly __brand: unique symbol };

/**
 * Pagination request parameters
 */
export interface PaginationParams {
  /** Maximum items per page (1-1000, default 100) */
  limit?: number;
  /** Cursor for next page (from previous response) */
  cursor?: PaginationCursor;
}

/**
 * Paginated response wrapper
 */
export interface PaginatedResponse<T> {
  data: T[];
  /** Cursor for next page; undefined if no more pages */
  nextCursor?: PaginationCursor;
  /** Total count if available (optional, may be expensive) */
  totalCount?: number;
}

/**
 * Time range query parameters
 */
export interface TimeRangeQuery {
  /** Start time (inclusive) — ISO 8601 UTC */
  start: ISOTimestamp;
  /** End time (exclusive) — ISO 8601 UTC */
  end: ISOTimestamp;
  /** Optional: limit max bars returned (1-10000, default 1000) */
  limit?: number;
}

/**
 * Authentication / authorization context passed by consumers
 * MUST be validated by provider on every request
 * PII: Contains user/sub identifier — treat as PII per §7.2
 */
export interface AuthContext {
  /** Authenticated subject (user ID, service account, etc.) — PII */
  sub: string;
  /** Tenant/organization ID — PII if correlates to user */
  tenantId?: string;
  /** Scopes/permissions granted (space-separated OAuth2 scopes) */
  scopes: string;
  /** Request ID for tracing (UUID v4) */
  requestId: string;
  /** Timestamp of auth validation (ISO 8601) */
  authenticatedAt: ISOTimestamp;
  /** Token expiry (ISO 8601) — provider MUST reject if expired */
  expiresAt: ISOTimestamp;
}

/**
 * DataProvider interface — implemented by Data Ingestion Service
 * All methods MUST validate AuthContext before processing.
 * All inputs MUST be validated (range checks, enum validation, SQL injection safe).
 * All timestamps MUST be validated as valid ISO 8601 UTC.
 * All string decimals MUST match ^-?\d+(\.\d+)?$ regex.
 * Rate limiting: provider MUST enforce per-tenant rate limits (configurable, default 100 req/s).
 * PII: AuthContext.sub and tenantId are PII — log only hashed (SHA-256) in audit logs.
 */
export interface DataProvider {
  /**
   * Fetch OHLCV bars for a trading pair within a time range
   * @param auth - Authenticated caller context (validated by provider)
   * @param exchange - Exchange identifier (validated against supported exchanges list)
   * @param tradingPair - Trading pair in BASE/QUOTE format
   * @param timeframe - Bar timeframe/resolution
   * @param range - Time range query (start inclusive, end exclusive)
   * @param pagination - Pagination parameters
   * @returns Paginated OHLCV bars in chronological order (oldest first)
   * @throws DataProviderError - See Error Contract
   * @precondition auth is valid, not expired, has "data:read" scope
   * @precondition exchange is in provider's supportedExchanges()
   * @precondition tradingPair is in provider's supportedPairs(exchange)
   * @precondition range.start < range.end, range ≤ 366 days
   * @postcondition Returns bars in ascending timestamp order, no gaps > timeframe
   * @postcondition Bars are exchange-authoritative (no synthetic fill by default)
   * @invariant Bars are immutable once returned for a given (exchange, pair, timeframe, timestamp)
   */
  getOHLCV(
    auth: AuthContext,
    exchange: ExchangeId,
    tradingPair: TradingPair,
    timeframe: Timeframe,
    range: TimeRangeQuery,
    pagination?: PaginationParams
  ): Promise<PaginatedResponse<OHLCVBar>>;

  /**
   * Fetch latest ticker snapshot for a trading pair
   * @param auth - Authenticated caller context
   * @param exchange - Exchange identifier
   * @param tradingPair - Trading pair
   * @returns Current ticker snapshot
   * @throws DataProviderError
   * @precondition auth valid, has "data:read" scope
   * @postcondition Timestamp within last 5 seconds (provider SLA)
   */
  getTicker(
    auth: AuthContext,
    exchange: ExchangeId,
    tradingPair: TradingPair
  ): Promise<TickerSnapshot>;

  /**
   * Fetch order book snapshot (L2 depth)
   * @param auth - Authenticated caller context
   * @param exchange - Exchange identifier
   * @param tradingPair - Trading pair
   * @param depth - Max depth levels (1-1000, default 100)
   * @returns Order book snapshot
   * @throws DataProviderError
   * @precondition auth valid, has "data:read" scope
   * @postcondition Bids sorted desc by price, asks sorted asc by price
   * @postcondition Spread >= 0 (best bid <= best ask)
   */
  getOrderBook(
    auth: AuthContext,
    exchange: ExchangeId,
    tradingPair: TradingPair,
    depth?: number
  ): Promise<OrderBookSnapshot>;

  /**
   * Fetch recent trades (prints)
   * @param auth - Authenticated caller context
   * @param exchange - Exchange identifier
   * @param tradingPair - Trading pair
   * @param limit - Max trades to return (1-1000, default 100)
   * @param startTime - Optional start time (inclusive)
   * @returns Recent trades in descending time order (newest first)
   * @throws DataProviderError
   * @precondition auth valid, has "data:read" scope
   * @postcondition Trades sorted by timestamp descending
   */
  getRecentTrades(
    auth: AuthContext,
    exchange: ExchangeId,
    tradingPair: TradingPair,
    limit?: number,
    startTime?: ISOTimestamp
  ): Promise<TradePrint[]>;

  /**
   * Get list of supported exchanges
   * @param auth - Authenticated caller context (requires "data:read" or "metadata:read")
   * @returns List of supported exchange identifiers
   * @throws DataProviderError
   */
  getSupportedExchanges(auth: AuthContext): Promise<ExchangeId[]>;

  /**
   * Get supported trading pairs for an exchange
   * @param auth - Authenticated caller context
   * @param exchange - Exchange identifier
   * @returns List of supported trading pairs
   * @throws DataProviderError
   */
  getSupportedPairs(auth: AuthContext, exchange: ExchangeId): Promise<TradingPair[]>;

  /**
   * Get supported timeframes for an exchange/pair
   * @param auth - Authenticated caller context
   * @param exchange - Exchange identifier
   * @param tradingPair - Trading pair
   * @returns Supported timeframes
   * @throws DataProviderError
   */
  getSupportedTimeframes(
    auth: AuthContext,
    exchange: ExchangeId,
    tradingPair: TradingPair
  ): Promise<Timeframe[]>;

  /**
   * Health check — lightweight liveness/readiness probe
   * @returns Health status
   * @throws DataProviderError if unhealthy
   */
  healthCheck(): Promise<DataProviderHealth>;
}

/**
 * Health check response
 */
export interface DataProviderHealth {
  status: "healthy" | "degraded" | "unhealthy";
  latencyMs: number;
  exchanges: Record<ExchangeId, { status: "up" | "down" | "degraded"; latencyMs: number }>;
  timestamp: ISOTimestamp;
}
```

---

## 2. Contract Semantics

### 2.1 Preconditions (Provider MUST validate on every request)

| Precondition | Validation | Error Code |
|--------------|------------|------------|
| `auth` present, not expired, valid signature | JWT validation (RS256/ES256), exp check, issuer validation | `AUTH_INVALID` / `AUTH_EXPIRED` |
| `auth.scopes` contains required scope (`data:read` or `metadata:read`) | Scope string contains required scope | `AUTH_INSUFFICIENT_SCOPE` |
| `exchange` in `getSupportedExchanges()` | Enum validation against cached list | `EXCHANGE_UNSUPPORTED` |
| `tradingPair` in `getSupportedPairs(exchange)` | Enum validation against cached list | `PAIR_UNSUPPORTED` |
| `timeframe` in `getSupportedTimeframes(exchange, pair)` | Enum validation | `TIMEFRAME_UNSUPPORTED` |
| `range.start < range.end` | Timestamp comparison (ISO 8601 parsed) | `INVALID_TIME_RANGE` |
| `range.end - range.start <= 366 days` | Duration check | `TIME_RANGE_TOO_LONG` |
| `range.limit <= 10000` | Numeric bound check | `LIMIT_EXCEEDED` |
| `pagination.limit <= 1000` | Numeric bound check | `LIMIT_EXCEEDED` |
| `depth <= 1000` | Numeric bound check | `DEPTH_EXCEEDED` |
| String decimals match `^-?\d+(\.\d+)?$` | Regex validation on all decimal strings | `INVALID_DECIMAL_FORMAT` |
| `auth.requestId` is valid UUID v4 | UUID v4 regex | `INVALID_REQUEST_ID` |

**All validation failures MUST return `DataProviderError` with appropriate code, HTTP 400/401/403.**

### 2.2 Postconditions (Provider MUST guarantee on success)

| Method | Postcondition |
|--------|---------------|
| `getOHLCV` | Bars sorted ascending by `timestamp`; no duplicate timestamps; gap ≤ 1 timeframe between consecutive bars (unless exchange has no data); all decimal fields valid decimal strings |
| `getTicker` | `timestamp` within 5s of provider wall clock; `bid <= ask`; all decimals valid |
| `getOrderBook` | `bids` sorted descending by price; `asks` ascending; `bids[0][0] <= asks[0][0]` (spread ≥ 0); `sequence` monotonically increasing per (exchange, pair) |
| `getRecentTrades` | Sorted descending by `timestamp`; `tradeId` unique per (exchange, pair); `side` ∈ {"buy","sell"} |
| `getSupportedExchanges` | Returns non-empty array; all values valid `ExchangeId` brand |
| `getSupportedPairs` | Returns array of valid `TradingPair` for given exchange |
| `getSupportedTimeframes` | Returns non-empty subset of `Timeframe` union |
| `healthCheck` | Returns within 100ms; `latencyMs` measured server-side |

### 2.3 Invariants (Provider MUST maintain always)

| Invariant | Description |
|-----------|-------------|
| **Immutability** | Once a bar is returned for (exchange, pair, timeframe, timestamp), it NEVER changes. Corrections are new bars with same timestamp + correction flag (future version). |
| **Monotonic Sequence** | `OrderBookSnapshot.sequence` strictly increases per (exchange, pair). Gaps indicate missed updates — consumer MUST handle. |
| **Decimal Precision** | All decimal strings preserve full exchange precision. No floating-point conversion by provider. |
| **Timezone** | All timestamps UTC, ISO 8601, millisecond precision. No timezone offsets. |
| **Rate Limit Headers** | Every response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers. |
| **Request ID Propagation** | `auth.requestId` echoed in response header `X-Request-ID` and logged. |
| **PII Handling** | `AuthContext.sub` and `tenantId` never logged in plaintext. Only SHA-256 hash in audit logs. |
| **Auth Context Propagation** | Provider MUST pass `AuthContext` to downstream exchange adapters for audit trail. |

---

## 3. Data Contracts (Exact Types)

All types defined in Section 1 are the exact data contracts. **No `any` types permitted.**

### 3.1 Decimal String Convention
All numeric values transmitted as **string decimals** matching regex `^-?\d+(\.\d+)?$`.
- Consumers MUST use `decimal.js` / `big.js` or equivalent for arithmetic.
- Providers MUST NOT use JavaScript `number` for transmission.

### 3.2 Brand Types (Nominal Typing)
Branded types (`ISOTimestamp`, `CurrencyCode`, `TradingPair`, `ExchangeId`, `PaginationCursor`) enforce compile-time distinction. Implementations MUST preserve brands through serialization (JSON reviver/replacer).

### 3.3 Pagination Contract
- Cursor-based pagination only (no offset/limit).
- Cursor is opaque base64url-encoded token containing: `{ lastTimestamp: ISOTimestamp, lastId: string, direction: "next" }`.
- Provider MUST reject tampered cursors with `INVALID_CURSOR`.

---

## 4. Error Contract

### 4.1 Error Type Hierarchy

```typescript
/**
 * Base error class for DataProvider
 * All errors include: code, message, requestId, timestamp, retryable
 */
export abstract class DataProviderError extends Error {
  abstract readonly code: DataProviderErrorCode;
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
 * Error codes — MUST match exactly for consumer error handling
 */
export type DataProviderErrorCode =
  | "AUTH_INVALID"
  | "AUTH_EXPIRED"
  | "AUTH_INSUFFICIENT_SCOPE"
  | "EXCHANGE_UNSUPPORTED"
  | "PAIR_UNSUPPORTED"
  | "TIMEFRAME_UNSUPPORTED"
  | "INVALID_TIME_RANGE"
  | "TIME_RANGE_TOO_LONG"
  | "LIMIT_EXCEEDED"
  | "INVALID_DECIMAL_FORMAT"
  | "INVALID_CURSOR"
  | "INVALID_REQUEST_ID"
  | "EXCHANGE_UNAVAILABLE"
  | "RATE_LIMIT_EXCEEDED"
  | "INTERNAL_ERROR"
  | "DATA_UNAVAILABLE"
  | "INVALID_DEPTH";

/**
 * Concrete error classes (one per code)
 */
export class AuthInvalidError extends DataProviderError {
  readonly code = "AUTH_INVALID" as const;
  readonly statusCode = 401;
  readonly retryable = false;
}
export class AuthExpiredError extends DataProviderError {
  readonly code = "AUTH_EXPIRED" as const;
  readonly statusCode = 401;
  readonly retryable = false;
}
export class AuthInsufficientScopeError extends DataProviderError {
  readonly code = "AUTH_INSUFFICIENT_SCOPE" as const;
  readonly statusCode = 403;
  readonly retryable = false;
}
export class ExchangeUnsupportedError extends DataProviderError {
  readonly code = "EXCHANGE_UNSUPPORTED" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class PairUnsupportedError extends DataProviderError {
  readonly code = "PAIR_UNSUPPORTED" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class TimeframeUnsupportedError extends DataProviderError {
  readonly code = "TIMEFRAME_UNSUPPORTED" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidTimeRangeError extends DataProviderError {
  readonly code = "INVALID_TIME_RANGE" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class TimeRangeTooLongError extends DataProviderError {
  readonly code = "TIME_RANGE_TOO_LONG" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class LimitExceededError extends DataProviderError {
  readonly code = "LIMIT_EXCEEDED" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidDecimalFormatError extends DataProviderError {
  readonly code = "INVALID_DECIMAL_FORMAT" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidCursorError extends DataProviderError {
  readonly code = "INVALID_CURSOR" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class InvalidRequestIdError extends DataProviderError {
  readonly code = "INVALID_REQUEST_ID" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
export class ExchangeUnavailableError extends DataProviderError {
  readonly code = "EXCHANGE_UNAVAILABLE" as const;
  readonly statusCode = 503;
  readonly retryable = true;
  readonly retryAfterMs = 30000;
}
export class RateLimitExceededError extends DataProviderError {
  readonly code = "RATE_LIMIT_EXCEEDED" as const;
  readonly statusCode = 429;
  readonly retryable = true;
  // retryAfterMs set from rate limit reset header
}
export class InternalError extends DataProviderError {
  readonly code = "INTERNAL_ERROR" as const;
  readonly statusCode = 500;
  readonly retryable = true;
  readonly retryAfterMs = 5000;
}
export class DataUnavailableError extends DataProviderError {
  readonly code = "DATA_UNAVAILABLE" as const;
  readonly statusCode = 404;
  readonly retryable = true;
  readonly retryAfterMs = 10000;
}
export class InvalidDepthError extends DataProviderError {
  readonly code = "INVALID_DEPTH" as const;
  readonly statusCode = 400;
  readonly retryable = false;
}
```

### 4.2 Retry Semantics

| Error Code | Retryable | Default Retry-After | Backoff Strategy |
|------------|-----------|---------------------|------------------|
| `EXCHANGE_UNAVAILABLE` | Yes | 30s | Exponential backoff (30s, 60s, 120s, max 5m) |
| `RATE_LIMIT_EXCEEDED` | Yes | Per `Retry-After` header | Honor `Retry-After` header exactly |
| `INTERNAL_ERROR` | Yes | 5s | Exponential backoff (5s, 10s, 20s, max 1m) |
| `DATA_UNAVAILABLE` | Yes | 10s | Linear backoff (10s, 20s, 30s, max 2m) |
| All 4xx codes | **No** | N/A | Do not retry — fix request |

**Consumer MUST implement:**
- Exponential backoff with jitter (±25%)
- Max 3 retries for retryable errors
- Circuit breaker per exchange (open after 5 consecutive 5xx, half-open after 30s)

### 4.3 Timeout Contracts

| Operation | Provider Timeout | Consumer Timeout | Notes |
|-----------|------------------|------------------|-------|
| `getOHLCV` | 5s | 10s | Provider must stream/chunk for large ranges |
| `getTicker` | 500ms | 2s | Cached ≤ 1s |
| `getOrderBook` | 1s | 3s | |
| `getRecentTrades` | 2s | 5s | |
| `getSupportedExchanges` | 200ms | 1s | Cached 5m |
| `getSupportedPairs` | 500ms | 2s | Cached 5m |
| `getSupportedTimeframes` | 200ms | 1s | Cached 5m |
| `healthCheck` | 100ms | 500ms | Liveness probe |

**Provider MUST** enforce its own timeout and return `INTERNAL_ERROR` (retryable) on timeout.
**Consumer MUST** enforce its timeout and treat timeout as retryable error.

---

## 5. Versioning Policy

| Version Component | Meaning | Compatibility Promise |
|-------------------|---------|----------------------|
| **MAJOR** (1.x.x → 2.0.0) | Breaking change: method removed, param added/removed/renamed, return type changed, error code added/removed/changed, precondition/postcondition weakened/strengthened | **Breaking** — consumers MUST update |
| **MINOR** (1.0.x → 1.1.0) | New method added, new optional param added, new optional field in response, new error code added (retryable only), new exchange/pair/timeframe added | **Backward compatible** — existing consumers work unchanged |
| **PATCH** (1.0.0 → 1.0.1) | Bug fix, performance improvement, internal refactor, documentation update, new exchange added (if already in supported list) | **Fully compatible** |

**Compatibility Guarantees (v1.x.x):**
- No method removal
- No required parameter addition
- No return type narrowing
- No error code removal
- No precondition strengthening
- New optional fields/parameters only

**Deprecation Policy:**
- Deprecated methods/params marked with `@deprecated` JSDoc + `X-Deprecated` response header
- Minimum 6 months (2 minor versions) before removal in next MAJOR
- Deprecation announced in `CHANGELOG.md` and `X-Deprecation-Warning` header

---

## 6. Test Contract (Contract Tests for TESTER)

**Every DataProvider implementation MUST pass these contract tests.**
Tests are written against the interface — no implementation details.

### 6.1 Authentication & Authorization Tests

| Test ID | Scenario | Expected |
|---------|----------|----------|
| `DP-AUTH-001` | Valid `AuthContext` with `data:read` scope | 200 OK, data returned |
| `DP-AUTH-002` | Missing `AuthContext` | `AUTH_INVALID` (401) |
| `DP-AUTH-003` | Expired `AuthContext` (`expiresAt` < now) | `AUTH_EXPIRED` (401) |
| `DP-AUTH-004` | Valid auth but missing `data:read` scope | `AUTH_INSUFFICIENT_SCOPE` (403) |
| `DP-AUTH-005` | Invalid `requestId` (not UUID v4) | `INVALID_REQUEST_ID` (400) |
| `DP-AUTH-006` | `AuthContext` with PII logged only as hash | Audit log contains SHA-256 hash only |

### 6.2 Input Validation Tests

| Test ID | Scenario | Expected |
|---------|----------|----------|
| `DP-VAL-001` | Unknown `exchange` | `EXCHANGE_UNSUPPORTED` (400) |
| `DP-VAL-002` | Unsupported `tradingPair` for exchange | `PAIR_UNSUPPORTED` (400) |
| `DP-VAL-003` | Unsupported `timeframe` for pair | `TIMEFRAME_UNSUPPORTED` (400) |
| `DP-VAL-004` | `range.start >= range.end` | `INVALID_TIME_RANGE` (400) |
| `DP-VAL-005` | `range.end - range.start > 366 days` | `TIME_RANGE_TOO_LONG` (400) |
| `DP-VAL-006` | `range.limit > 10000` | `LIMIT_EXCEEDED` (400) |
| `DP-VAL-007` | `pagination.limit > 1000` | `LIMIT_EXCEEDED` (400) |
| `DP-VAL-008` | `depth > 1000` | `INVALID_DEPTH` (400) |
| `DP-VAL-009` | Decimal string with scientific notation ("1e5") | `INVALID_DECIMAL_FORMAT` (400) |
| `DP-VAL-010` | Tampered pagination cursor | `INVALID_CURSOR` (400) |

### 6.3 Functional Correctness Tests

| Test ID | Method | Scenario | Expected Postconditions |
|---------|--------|----------|------------------------|
| `DP-FUNC-001` | `getOHLCV` | Valid request, data exists | Bars ascending timestamp, no duplicates, decimals valid, gap ≤ timeframe |
| `DP-FUNC-002` | `getOHLCV` | Valid request, no data in range | Empty `data` array, `nextCursor` undefined |
| `DP-FUNC-003` | `getOHLCV` | Pagination: request page 1, then page 2 via cursor | Page 2 starts after page 1 end, no overlap, no gaps |
| `DP-FUNC-004` | `getOHLCV` | Request limit=5, range has 20 bars | Returns 5 bars, `nextCursor` present, total 4 pages |
| `DP-FUNC-005` | `getTicker` | Valid pair | `timestamp` within 5s, `bid <= ask`, decimals valid |
| `DP-FUNC-006` | `getOrderBook` | Valid pair, depth=50 | Bids desc, asks asc, spread ≥ 0, sequence > 0 |
| `DP-FUNC-007` | `getOrderBook` | Depth=1 | Exactly 1 bid, 1 ask |
| `DP-FUNC-008` | `getRecentTrades` | Valid pair, limit=10 | 10 trades max, descending timestamp, unique tradeIds |
| `DP-FUNC-009` | `getSupportedExchanges` | Valid auth | Non-empty array, all valid `ExchangeId` |
| `DP-FUNC-010` | `getSupportedPairs` | Valid exchange | Non-empty array, all valid `TradingPair` |
| `DP-FUNC-011` | `getSupportedTimeframes` | Valid exchange/pair | Non-empty subset of `Timeframe` union |
| `DP-FUNC-012` | `healthCheck` | Healthy service | `status: "healthy"`, `latencyMs < 100`, all exchanges "up" |

### 6.4 Error Handling & Retry Tests

| Test ID | Scenario | Expected |
|---------|----------|----------|
| `DP-ERR-001` | Exchange returns 503 | `EXCHANGE_UNAVAILABLE` (503), `retryable=true`, `retryAfterMs=30000` |
| `DP-ERR-002` | Rate limit exceeded | `RATE_LIMIT_EXCEEDED` (429), `retryable=true`, `Retry-After` header honored |
| `DP-ERR-003` | Provider internal timeout | `INTERNAL_ERROR` (500), `retryable=true`, `retryAfterMs=5000` |
| `DP-ERR-004` | Data gap (exchange down for 1h) | `DATA_UNAVAILABLE` (404), `retryable=true`, `retryAfterMs=10000` |
| `DP-ERR-005` | Consumer retries 3x on `EXCHANGE_UNAVAILABLE` with exp backoff | All retries attempted, circuit breaker opens after 5 consecutive 5xx |

### 6.5 Contract Compliance Tests (Provider-Agnostic)

| Test ID | Description |
|---------|-------------|
| `DP-CONTRACT-001` | All decimal fields match `^-?\d+(\.\d+)?$` regex |
| `DP-CONTRACT-002` | All timestamps are valid ISO 8601 UTC with 'Z' suffix |
| `DP-CONTRACT-003` | All branded types preserved through JSON round-trip (reviver/replacer) |
| `DP-CONTRACT-004` | All responses include `X-Request-ID` = `auth.requestId` |
| `DP-CONTRACT-005` | All responses include rate limit headers |
| `DP-CONTRACT-006` | No PII in response body (sub, tenantId never in response) |
| `DP-CONTRACT-007` | Error responses never leak stack traces or internal details |
| `DP-CONTRACT-008` | All 4xx errors have `retryable: false`, all 5xx have `retryable: true` |

### 6.6 Performance / SLA Tests

| Test ID | Method | SLA | Pass Criteria |
|---------|--------|-----|---------------|
| `DP-PERF-001` | `getTicker` | p99 < 500ms | 99th percentile < 500ms over 1000 requests |
| `DP-PERF-002` | `getOHLCV` (100 bars) | p99 < 2s | 99th percentile < 2s |
| `DP-PERF-003` | `healthCheck` | p99 < 100ms | 99th percentile < 100ms |
| `DP-PERF-004` | Rate limit enforcement | 100 req/s/tenant | 101st request in 1s returns 429 |

---

## 7. Security Annotations (§7.2)

| Field / Context | Classification | Handling Requirement |
|-----------------|----------------|---------------------|
| `AuthContext.sub` | **PII** (Direct identifier) | Never log plaintext; SHA-256 hash only in audit logs; encrypt at rest |
| `AuthContext.tenantId` | **PII** (Correlatable) | Same as `sub` |
| `AuthContext.requestId` | **Operational** (Non-PII) | Log plaintext for tracing; correlate in distributed tracing |
| `AuthContext.scopes` | **AuthZ Context** | Validate on every request; never log full scope string in plaintext (hash) |
| `AuthContext.authenticatedAt` / `expiresAt` | **Auth Metadata** | Validate expiry; log only validation result (valid/expired) |
| Decimal price/volume fields | **Financial Data** (Sensitive) | Encrypt in transit (TLS 1.3), encrypt at rest; audit access |
| `TradePrint.tradeId` | **Trade Identifier** (Pseudonymous) | Treat as pseudonymous; do not log with PII correlation |
| `AuthContext` propagation | **AuthZ Context** | Must be passed to downstream exchange adapters for their audit logs |

**Input Validation Requirements (MUST):**
- All string inputs: max length 256 (except decimals: max 64 chars)
- All enums: validate against allowlist
- All timestamps: parse with strict ISO 8601, reject offsets other than Z
- All decimals: regex `^-?\d+(\.\d+)?$`, max 38 digits precision, max 18 scale
- Pagination cursor: validate base64url decode + JSON parse + schema validate
- Rate limit: enforce per `AuthContext.tenantId` (or `sub` if no tenant)

**Output Encoding:**
- JSON responses: `Content-Type: application/json; charset=utf-8`
- No JSONP, no callback parameters
- `X-Content-Type-Options: nosniff` header on all responses

---

## 8. Implementation Notes (Non-Normative)

- **Caching**: `getSupportedExchanges/Pairs/Timeframes` cached 5 min; `getTicker` cached 1s; OHLCV not cached (authoritative).
- **Exchange Adapters**: Provider wraps exchange-specific adapters (CCXT or custom). Adapter errors mapped to `DataProviderError`.
- **Gap Fill**: OHLCV gaps > timeframe returned as-is (no synthetic fill). Consumers request gap-fill via separate method (v2+).
- **Corrections**: v1.0.0 returns bars as-is. Corrections = new version (v2.0.0+).
- **WebSocket/Streaming**: Not in v1.0.0. Separate `DataStreamProvider` interface in v2.0.0.

---

**End of Contract Specification — DataProvider v1.0.0**