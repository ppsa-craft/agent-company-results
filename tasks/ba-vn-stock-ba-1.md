# BA Task: vn-stock-ba-1

## Goal
Define comprehensive use cases for VN stock data adapters (VNM, VCI, VND, TCBS, SSI) for the vn-stock product.

## Status
in-progress

## Product
vn-stock

## Description
Define comprehensive use cases for the 5 VN stock data adapters (VNM - Vinamilk/Vietcombank, VCI - VCI Securities, VND - VNDirect, TCBS - Techcom Securities, SSI - SSI Securities) as defined in the vn-stock data ingestion architecture (S1 adapters layer). Each adapter must handle source-specific authentication, rate limiting, data formats, and error handling.

## Use Cases (Traceable to Acceptance Criteria)

### UC-VN-ADAPTER-001: VNM Adapter - Fetch Real-time Stock Prices
**Actors:** Data Ingestion Pipeline (S1)
**Preconditions:** VNM adapter configured with valid credentials, market is open
**Main Flow:**
1. Pipeline requests real-time price for VNM symbol
2. Adapter authenticates with VNM API using configured credentials
3. Adapter respects VNM rate limits (max 60 req/min)
4. Adapter fetches real-time price data (price, volume, bid/ask)
5. Adapter normalizes timestamp to UTC
6. Adapter returns normalized price DTO
**Postconditions:** Normalized price DTO returned with source metadata
**Alternate Flows:**
- 429 Too Many Requests → exponential backoff, retry after Retry-After header
- 401 Unauthorized → refresh token, retry once
- 404 Not Found → return NotFound error with symbol
- Network timeout → retry with exponential backoff (max 3 retries)
**Traceability:** AC-VN-ADAPTER-001, AC-VN-ADAPTER-002, AC-VN-ADAPTER-003

### UC-VN-ADAPTER-002: VCI Adapter - Fetch Historical OHLCV Data
**Actors:** Data Ingestion Pipeline (S1), Backfill Job
**Preconditions:** VCI adapter configured, date range valid, market was open
**Main Flow:**
1. Pipeline requests OHLCV for VCI symbol over date range
2. Adapter chunks request per VCI API limits (max 1000 records/request)
3. Adapter fetches paginated OHLCV data
4. Adapter normalizes each record to canonical OHLCV DTO
5. Adapter returns paginated results with cursor
**Postconditions:** Complete OHLCV dataset returned with pagination cursor
**Alternate Flows:**
- Partial data returned → return partial with next cursor
- Invalid symbol → return SymbolNotFound error
- Market holiday → return empty array with holiday flag
**Traceability:** AC-VN-ADAPTER-004, AC-VN-ADAPTER-005, AC-VN-ADAPTER-006

### UC-VN-ADAPTER-003: VND Adapter - Fetch Company Fundamentals
**Actors:** Fundamental Data Pipeline (S1)
**Preconditions:** VND adapter configured, company symbol valid
**Main Flow:**
1. Pipeline requests fundamentals for VND symbol
2. Adapter fetches company profile, financial ratios, financial statements
3. Adapter normalizes to canonical FundamentalDTO
4. Adapter returns normalized fundamentals
**Postconditions:** Normalized FundamentalDTO returned
**Alternate Flows:**
- Data not available → return PartialData with available fields
- Rate limit exceeded → queue with backoff
**Traceability:** AC-VN-ADAPTER-007, AC-VN-ADAPTER-008

### UC-VN-ADAPTER-004: TCBS Adapter - Fetch Market Depth / Order Book
**Actors:** Market Data Pipeline (S1)
**Preconditions:** TCBS adapter configured, market open
**Main Flow:**
1. Pipeline requests order book for TCBS symbol
2. Adapter fetches Level 2 order book (bid/ask levels)
3. Adapter normalizes to canonical OrderBookDTO
4. Adapter returns order book with sequence number
**Postconditions:** Normalized OrderBookDTO returned
**Alternate Flows:**
- WebSocket disconnection → reconnect with exponential backoff
- Stale sequence → request snapshot, resume streaming
**Traceability:** AC-VN-ADAPTER-009, AC-VN-ADAPTER-010

### UC-VN-ADAPTER-005: SSI Adapter - Fetch Dividend & Corporate Actions
**Actors:** Corporate Actions Pipeline (S1)
**Preconditions:** SSI adapter configured, symbol valid
**Main Flow:**
1. Pipeline requests corporate actions for SSI symbol
2. Adapter fetches dividends, splits, bonus shares, rights issues
3. Adapter normalizes to canonical CorporateActionDTO
4. Adapter returns paginated results
**Postconditions:** Normalized CorporateActionDTO list returned
**Alternate Flows:**
- No corporate actions → return empty array
- Partial data → return available with missing field indicators
**Traceability:** AC-VN-ADAPTER-011, AC-VN-ADAPTER-012

### UC-VN-ADAPTER-006: Adapter Health Check & Circuit Breaker
**Actors:** Observability (S5), Circuit Breaker
**Preconditions:** Adapter registered with health check endpoint
**Main Flow:**
1. S5 calls adapter health endpoint every 30s
2. Adapter performs self-check: connectivity, auth, rate limit status
3. Adapter returns health status (healthy/degraded/unhealthy)
4. Circuit breaker updates state based on health
**Postconditions:** Health status reported, circuit breaker state updated
**Alternate Flows:**
- 3 consecutive unhealthy → circuit opens
- Circuit open → fail fast, return cached/stale data with staleness header
**Traceability:** AC-VN-ADAPTER-013, AC-VN-ADAPTER-014, AC-VN-ADAPTER-015

### UC-VN-ADAPTER-007: Adapter Rate Limit Compliance
**Actors:** Rate Limiter (S1), All Adapters
**Preconditions:** Rate limiter configured per adapter specs
**Main Flow:**
1. Adapter receives request
2. Adapter checks rate limiter token bucket
3. If tokens available → proceed, consume token
4. If no tokens → wait or reject with Retry-After
**Postconditions:** Request processed within rate limits
**Alternate Flows:**
- Burst allowance used → queue request
- Sustained limit → return 429 with Retry-After
**Traceability:** AC-VN-ADAPTER-016, AC-VN-ADAPTER-017

### UC-VN-ADAPTER-008: Adapter Error Normalization
**Actors:** All Adapters, Error Handler (S1)
**Preconditions:** Adapter encounters error
**Main Flow:**
1. Adapter catches source-specific error
2. Adapter maps to canonical AdapterError (timeout, auth, notfound, ratelimit, upstream, unknown)
3. Adapter enriches with source, symbol, timestamp, request_id
4. Adapter returns canonical error
**Postconditions:** Canonical AdapterError returned
**Traceability:** AC-VN-ADAPTER-018, AC-VN-ADAPTER-019

## User Stories

**US-VN-ADAPTER-001:** As a Data Ingestion Pipeline, I want to fetch real-time VNM prices so that downstream normalizer receives timely price data.
- **Acceptance Criteria:** AC-VN-ADAPTER-001, AC-VN-ADAPTER-002, AC-VN-ADAPTER-003

**US-VN-ADAPTER-002:** As a Backfill Job, I want to fetch historical OHLCV from VCI so that historical database is populated.
- **Acceptance Criteria:** AC-VN-ADAPTER-004, AC-VN-ADAPTER-005, AC-VN-ADAPTER-006

**US-VN-ADAPTER-003:** As a Fundamental Data Pipeline, I want normalized fundamentals from VND so that fundamental analysis works across sources.
- **Acceptance Criteria:** AC-VN-ADAPTER-007, AC-VN-ADAPTER-008

**US-VN-ADAPTER-004:** As a Market Data Pipeline, I want normalized order book from TCBS so that order book aggregation works across sources.
- **Acceptance Criteria:** AC-VN-ADAPTER-009, AC-VN-ADAPTER-010

**US-VN-ADAPTER-005:** As a Corporate Actions Pipeline, I want normalized corporate actions from SSI so that corporate action calendar is accurate.
- **Acceptance Criteria:** AC-VN-ADAPTER-011, AC-VN-ADAPTER-012

**US-VN-ADAPTER-006:** As Observability (S5), I want adapter health checks so that circuit breakers protect downstream.
- **Acceptance Criteria:** AC-VN-ADAPTER-013, AC-VN-ADAPTER-014, AC-VN-ADAPTER-015

**US-VN-ADAPTER-007:** As a Rate Limiter, I want adapters to respect source rate limits so that we don't get banned.
- **Acceptance Criteria:** AC-VN-ADAPTER-016, AC-VN-ADAPTER-017

**US-VN-ADAPTER-008:** As an Error Handler, I want normalized adapter errors so that retry/alert logic is source-agnostic.
- **Acceptance Criteria:** AC-VN-ADAPTER-018, AC-VN-ADAPTER-019

## Acceptance Criteria (Traceable)

**AC-VN-ADAPTER-001:** VNM adapter returns PriceDTO with fields: symbol, price, volume, bid, ask, timestamp_utc, source="VNM" within 500ms P99
**AC-VN-ADAPTER-002:** VNM adapter returns 429 with Retry-After header when rate limited, retries with exponential backoff max 3x
**AC-VN-ADAPTER-003:** VNM adapter returns NotFoundError with symbol when symbol not found
**AC-VN-ADAPTER-004:** VCI adapter returns paginated OHLCVDTO[] with cursor, each DTO: symbol, open, high, low, close, volume, timestamp_utc, source="VCI"
**AC-VN-ADAPTER-005:** VCI adapter handles pagination transparently, returns next_cursor for pagination
**AC-VN-ADAPTER-006:** VCI adapter returns empty array with holiday flag for market holidays
**AC-VN-ADAPTER-007:** VND adapter returns FundamentalDTO with: symbol, company_name, sector, pe_ratio, pb_ratio, roe, roa, debt_to_equity, revenue, net_income, source="VND"
**AC-VN-ADAPTER-008:** VND adapter returns PartialData when some fields unavailable, with missing_fields list
**AC-VN-ADAPTER-009:** TCBS adapter returns OrderBookDTO: symbol, bids[][{price, volume}], asks[][{price, volume}], sequence, timestamp_utc, source="TCBS"
**AC-VN-ADAPTER-010:** TCBS adapter reconnects WebSocket with exponential backoff on disconnect, resumes from sequence
**AC-VN-ADAPTER-011:** SSI adapter returns CorporateActionDTO[]: symbol, action_type, ex_date, record_date, pay_date, ratio, cash_amount, source="SSI"
**AC-VN-ADAPTER-012:** SSI adapter returns empty array with has_data=false when no corporate actions
**AC-VN-ADAPTER-013:** Adapter health endpoint returns {status, source, latency_ms, rate_limit_remaining, last_success_ts}
**AC-VN-ADAPTER-014:** Circuit breaker opens after 3 consecutive unhealthy checks
**AC-VN-ADAPTER-015:** Circuit open returns stale data with staleness_ms header
**AC-VN-ADAPTER-016:** Adapter respects source rate limits (VNM: 60/min, VCI: 100/min, VND: 30/min, TCBS: 100/min WS, SSI: 50/min)
**AC-VN-ADAPTER-017:** Adapter returns 429 with Retry-After when rate limited
**AC-VN-ADAPTER-018:** All adapters return AdapterError{code, source, symbol, timestamp, request_id, details}
**AC-VN-ADAPTER-019:** Error codes are canonical: TIMEOUT, AUTH_FAILED, NOT_FOUND, RATE_LIMITED, UPSTREAM_ERROR, UNKNOWN

## Estimated Effort
8 story points

## Assignee
BA

## DoD Tier
Tier 2 (Feature)

## Dependencies
- stack-vnstock-data-ingestion.md (S1 adapters architecture)
- stack-vnstock-data-ingestion.md (S5 observability for health checks)

## Notes
- Each adapter must implement the unified Adapter interface from S1
- Rate limits per source: VNM=60/min, VCI=100/min, VND=30/min, TCBS=100/min (WS), SSI=50/min
- All timestamps normalized to UTC ISO8601
- All prices in VND, volumes in shares
- Circuit breaker state persisted in Redis (S5)
- Health checks every 30s, circuit opens after 3 consecutive failures
- Stale data served with `X-Stale-Data: true` and `X-Staleness-Ms` headers when circuit open
- All timestamps normalized to UTC ISO8601
- All monetary values in VND (Vietnamese Dong)
- Volumes in shares (not lots)