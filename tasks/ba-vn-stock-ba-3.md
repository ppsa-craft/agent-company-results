# BA Task: vn-stock-ba-3

## Goal
Define comprehensive use cases for VN storage adapter (S4) for the vn-stock product.

## Status
in-progress

## Product
vn-stock

## Description
Define comprehensive use cases for the VN storage adapter (S4 layer) as defined in the vn-stock data ingestion architecture. The storage adapter provides unified persistence and retrieval for all normalized data from S2 normalizer: real-time prices, historical OHLCV, fundamentals, order books, corporate actions, symbols, trading calendar, and derived analytics.

## Use Cases (Traceable to Acceptance Criteria)

### UC-VN-STORE-001: Store Real-time Price Ticks
**Actors:** Normalizer (S2), Price Storage (S4)
**Preconditions:** UnifiedPriceEvent received from S2
**Main Flow:**
1. Storage receives UnifiedPriceEvent
2. Storage validates: symbol exists in registry, price > 0, timestamp recent (< 60s)
2. Storage writes to time-series DB (TimescaleDB/InfluxDB): measurement=prices, tags=symbol,source_count, fields=price,volume,vwap,spread,bid,ask
3. Storage updates latest-price cache (Redis): key=price:{symbol}, value={price,ts,sources}, TTL=60s
3. Storage emits PriceStoredEvent with write_latency_ms
**Postconditions:** Price persisted in TSDB, cached in Redis, event emitted
**Alternate Flows:**
- Symbol not in registry → log UnmappedSymbolWarning, write with symbol_unknown=true
- Duplicate timestamp (same ms) → upsert (last write wins), increment duplicate_counter
- TSDB write failure → retry 3x, then queue to dead letter, emit WriteFailedEvent
**Traceability:** AC-VN-STORE-001, AC-VN-STORE-002, AC-VN-STORE-003

### UC-VN-STORE-002: Store Historical OHLCV with Gap Awareness
**Actors:** Normalizer (S2), Historical Storage (S4)
**Preconditions:** UnifiedOHLCVEvent[] received, gap_filled flag present
**Main Flow:**
1. Storage receives UnifiedOHLCVEvent batch
2. Storage validates: OHLC relationships, volume ≥ 0, timestamp aligns to session close
2. Storage writes to TSDB: measurement=ohlcv, tags=symbol,source,gap_filled,session, fields=o,h,l,c,v
3. Storage updates daily aggregate cache: key=daily:{symbol}:{date}, value={o,h,l,c,v,source}
3. Storage emits OHLCVStoredEvent with count, gap_count
**Postconditions:** OHLCV persisted, daily aggregates cached
**Alternate Flows:**
- GapDetectedEvent received → write GapMarker record: measurement=gaps, tags=symbol, fields=gap_start,gap_end,reason
- Duplicate (same symbol+timestamp) → upsert, log DuplicateSuppressed
- Invalid OHLC → reject, emit ValidationErrorEvent
**Traceability:** AC-VN-STORE-004, AC-VN-STORE-005, AC-VN-STORE-006

### UC-VN-STORE-003: Store Versioned Fundamentals
**Actors:** Normalizer (S2), Fundamental Storage (S4)
**Preconditions:** UnifiedFundamentalEvent received with version_hash
**Main Flow:**
1. Storage receives UnifiedFundamentalEvent
2. Storage computes version_hash from canonical fields
2. Storage checks existing version_hash for symbol+period
3. If hash differs → insert new version: measurement=fundamentals, tags=symbol,period,version, fields=all_metrics, version_hash
3. If hash same → emit UnchangedEvent, skip write
4. Storage updates latest-fundamental cache: key=fundamental:{symbol}:latest, value={period,data,version_hash}
4. Storage emits FundamentalStoredEvent with version, is_new_version
**Postconditions:** Versioned fundamental stored, latest cache updated
**Alternate Flows:**
- Missing required fields → reject, emit ValidationErrorEvent
- Period conflict (same period, different data) → store both versions, log VersionConflictEvent
**Traceability:** AC-VN-STORE-007, AC-VN-STORE-008, AC-VN-STORE-009

### UC-VN-STORE-004: Store Order Book Snapshots
**Actors:** Normalizer (S2), Order Book Storage (S4)
**Preconditions:** UnifiedOrderBookEvent received
**Main Flow:**
1. Storage receives UnifiedOrderBookEvent
2. Storage validates: sequence increasing, spread ≥ 0, levels sorted
2. Storage writes to TSDB: measurement=orderbook, tags=symbol,source, fields=bids_json,asks_json,spread,mid_price,depth_10,imbalance,sequence
3. Storage updates L2 cache: key=orderbook:{symbol}, value={bids,asks,ts,seq}, TTL=5s
3. Storage emits OrderBookStoredEvent
**Postconditions:** Order book persisted, L2 cache updated
**Alternate Flows:**
- Sequence gap > 100 → emit SnapshotRequestedEvent for symbol
- Crossed book → store anyway, tag crossed=true
- Cache TTL expired → next request triggers snapshot fetch
**Traceability:** AC-VN-STORE-010, AC-VN-STORE-011, AC-VN-STORE-012

### UC-VN-STORE-005: Store Corporate Actions with Deduplication
**Actors:** Normalizer (S2), Corporate Action Storage (S4)
**Preconditions:** UnifiedCorporateActionEvent received
**Main Flow:**
1. Storage receives UnifiedCorporateActionEvent
2. Storage checks dedup key: symbol+action_type+ex_date+record_date
2. If exists → compare fields, merge if richer source, emit CorporateActionMergedEvent
3. If new → insert: measurement=corporate_actions, tags=symbol,action_type, fields=all, merged_sources
3. Storage updates corporate action calendar cache: key=ca_calendar:{year}:{month}, value=event[]
4. Storage emits CorporateActionStoredEvent
**Postconditions:** Corporate action stored/merged, calendar cache updated
**Alternate Flows:**
- Conflicting cash_amount → keep majority, log CashAmountConflictEvent
- Missing pay_date → infer ex_date + 10 business days (VN calendar)
**Traceability:** AC-VN-STORE-013, AC-VN-STORE-014, AC-VN-STORE-015

### UC-VN-STORE-006: Symbol Registry Management
**Actors:** Admin, Normalizer (S2), Symbol Registry (S4)
**Preconditions:** Admin provides symbol mappings CSV/API
**Main Flow:**
1. Admin loads symbol registry: canonical_symbol, aliases[], exchange, sector, lot_size, currency
2. Registry stored in PostgreSQL (symbols table) + cached in Redis (symbol:{canonical}, alias:{alias}→canonical)
2. Normalizer queries registry via cache (TTL 1h, fallback to PG)
3. Admin can add/update/deprecate symbols via API
3. Registry emits SymbolRegistryUpdatedEvent on changes
**Postconditions:** Registry loaded, cached, API available
**Alternate Flows:**
- Alias conflict (same alias → 2 canonicals) → log AliasConflictEvent, use first loaded
- Deprecated symbol → tag deprecated=true, keep for history
- Cache miss → fallback to PG, async refresh cache
**Traceability:** AC-VN-STORE-016, AC-VN-STORE-017, AC-VN-STORE-018

### UC-VN-STORE-007: Trading Calendar Management
**Actors:** Admin, Normalizer (S2), Calendar Service (S4)
**Preconditions:** VN trading calendar loaded (holidays, half-days, session times)
**Main Flow:**
1. Admin loads calendar: date, status (OPEN/HALF_DAY/CLOSED), morning_open, morning_close, afternoon_open, afternoon_close, notes
2. Calendar stored in PG (trading_calendar table) + cached in Redis (calendar:{date}→status)
2. Normalizer queries calendar for session classification
3. Calendar API: is_trading_day(date), get_session(date), get_next_trading_day(date), get_previous_trading_day(date)
3. Calendar emits CalendarUpdatedEvent on reload
**Postconditions:** Calendar loaded, API available, cache populated
**Alternate Flows:**
- Date not in calendar → assume CLOSED, log MissingCalendarDateEvent
- Half-day → adjusted session times applied
- Cache miss → PG fallback, async refresh
**Traceability:** AC-VN-STORE-019, AC-VN-STORE-020, AC-VN-STORE-021

### UC-VN-STORE-008: Query APIs for Downstream Consumers
**Actors:** Analytics (S3), API Gateway, Backfill Jobs
**Preconditions:** Data persisted in S4
**Main Flow:**
1. Consumer queries via Storage API:
   - GET /prices/latest?symbols=VNM,VIC
   - GET /ohlcv?symbol=VNM&from=2024-01-01&to=2024-01-31&gap_filled=false
   - GET /fundamentals/latest?symbol=VNM
   - GET /orderbook?symbol=VNM
   - GET /corporate-actions?symbol=VNM&from=2024-01-01
   - GET /symbols?search=VNM
   - GET /calendar?from=2024-01-01&to=2024-12-31
2. Storage routes to appropriate store: Redis for latest, TSDB for historical
2. Storage returns canonical DTOs with pagination/cursors
3. Storage emits QueryExecutedEvent with latency, row_count
**Postconditions:** Data returned in canonical format, paginated
**Alternate Flows:**
- Symbol not found → 404 with SymbolNotFoundError
- Date range too large → 400 with MaxRangeExceededError (max 1 year for OHLCV)
- Cache miss → TSDB query, async cache populate
**Traceability:** AC-VN-STORE-022, AC-VN-STORE-023, AC-VN-STORE-024

### UC-VN-STORE-009: Data Retention & Tiering
**Actors:** Storage Admin, Retention Job (S4)
**Preconditions:** Retention policies configured
**Main Flow:**
1. Retention job runs daily:
   - Real-time prices: hot (Redis) 1h, warm (TSDB) 30d, cold (S3/Parquet) 7y
   - OHLCV: warm 2y, cold 20y
   - Fundamentals: warm 5y, cold permanent
   - Order book: hot 5m, warm 1d, cold 30d
   - Corporate actions: permanent
2. Job moves data between tiers, updates catalog
2. Job emits RetentionJobCompletedEvent with stats
**Postconditions:** Data tiered per policy, catalog updated
**Alternate Flows:**
- Cold storage write failure → retry, alert on repeated failure
- Catalog inconsistency → repair job triggered
**Traceability:** AC-VN-STORE-025, AC-VN-STORE-026

### UC-VN-STORE-010: Storage Health & Metrics
**Actors:** Storage (S4), Observability (S5)
**Preconditions:** Storage running, metrics endpoint exposed
**Main Flow:**
1. Storage emits metrics: write_latency_p50/p95/p99, read_latency, error_rate, queue_lag, cache_hit_rate, disk_usage, tier_distribution
2. Health endpoint: /health → {status, writes_ok, reads_ok, cache_ok, lag_ms, disk_pct}
2. Alert rules: write_latency_p99 > 500ms, error_rate > 1%, disk > 80%, lag > 10s
**Postconditions:** Metrics exposed, alerts configured
**Alternate Flows:**
- Degraded: cache miss rate > 20% → health=degraded
- Unhealthy: write failure rate > 5% → health=unhealthy, circuit breaker
**Traceability:** AC-VN-STORE-027, AC-VN-STORE-028, AC-VN-STORE-029

## User Stories

**US-VN-STORE-001:** As a Normalizer (S2), I want to store real-time prices so that latest prices are available for trading.
- **Acceptance Criteria:** AC-VN-STORE-001, AC-VN-STORE-002, AC-VN-STORE-003

**US-VN-STORE-002:** As a Historical Store, I want gap-aware OHLCV storage so that backtests handle missing sessions correctly.
- **Acceptance Criteria:** AC-VN-STORE-004, AC-VN-STORE-005, AC-VN-STORE-006

**US-VN-STORE-003:** As a Fundamental Store, I want versioned fundamentals so that I can track changes and avoid redundant writes.
- **Acceptance Criteria:** AC-VN-STORE-007, AC-VN-STORE-008, AC-VN-STORE-009

**US-VN-STORE-004:** As an Order Book Aggregator, I want L2 order book snapshots stored so that I can reconstruct depth history.
- **Acceptance Criteria:** AC-VN-STORE-010, AC-VN-STORE-011, AC-VN-STORE-012

**US-VN-STORE-005:** As a Corporate Action Store, I want deduplicated corporate actions so that calendars are accurate.
- **Acceptance Criteria:** AC-VN-STORE-013, AC-VN-STORE-014, AC-VN-STORE-015

**US-VN-STORE-006:** As a Symbol Registry, I want canonical symbol management so that all layers use consistent symbols.
- **Acceptance Criteria:** AC-VN-STORE-016, AC-VN-STORE-017, AC-VN-STORE-018

**US-VN-STORE-007:** As a Trading Calendar, I want VN session-aware calendar so that session classification is accurate.
- **Acceptance Criteria:** AC-VN-STORE-019, AC-VN-STORE-020, AC-VN-STORE-021

**US-VN-STORE-008:** As an Analytics Consumer, I want unified query APIs so that I can fetch data without knowing storage details.
- **Acceptance Criteria:** AC-VN-STORE-022, AC-VN-STORE-023, AC-VN-STORE-024

**US-VN-STORE-009:** As a Storage Admin, I want automated tiering so that costs are optimized.
- **Acceptance Criteria:** AC-VN-STORE-025, AC-VN-STORE-026

**US-VN-STORE-010:** As Observability (S5), I want storage health metrics so that I can monitor data pipeline health.
- **Acceptance Criteria:** AC-VN-STORE-027, AC-VN-STORE-028, AC-VN-STORE-029

## Acceptance Criteria (Traceable)

**AC-VN-STORE-001:** Price written to TSDB within 50ms p99, cached in Redis TTL 60s
**AC-VN-STORE-002:** Duplicate timestamp (same ms) → upsert, duplicate_counter incremented
**AC-VN-STORE-003:** TSDB write failure → retry 3x, then dead letter queue, WriteFailedEvent emitted
**AC-VN-STORE-004:** OHLCV written with tags: symbol, source, gap_filled, session
**AC-VN-STORE-005:** GapDetectedEvent → GapMarker record written with gap_start, gap_end, reason
**AC-VN-STORE-006:** Invalid OHLC (H<O, L>C, V<0) → rejected, ValidationErrorEvent emitted
**AC-VN-STORE-007:** Fundamental version_hash (SHA256) stored, unchanged → UnchangedEvent, no write
**AC-VN-STORE-008:** Version conflict (same period, different data) → both versions stored, VersionConflictEvent
**AC-VN-STORE-009:** Latest fundamental cache key=fundamental:{symbol}:latest, TTL 24h
**AC-VN-STORE-010:** Order book written with bids_json, asks_json, sequence, spread, mid_price, depth_10, imbalance
**AC-VN-STORE-011:** Sequence gap > 100 → SnapshotRequestedEvent emitted
**AC-VN-STORE-012:** Crossed book stored with crossed=true tag
**AC-VN-STORE-013:** Corporate action dedup key: symbol+action_type+ex_date+record_date
**AC-VN-STORE-014:** Conflicting cash_amount → majority wins, CashAmountConflictEvent logged
**AC-VN-STORE-015:** Missing pay_date → inferred ex_date + 10 business days (VN calendar)
**AC-VN-STORE-016:** Symbol registry: canonical_symbol, aliases[], exchange, sector, lot_size, currency in PG + Redis cache
**AC-VN-STORE-017:** Alias conflict → AliasConflictEvent, first loaded wins
**AC-VN-STORE-018:** Deprecated symbols tagged deprecated=true, retained for history
**AC-VN-STORE-019:** Calendar: date, status, session times in PG + Redis cache calendar:{date}
**AC-VN-STORE-020:** API: is_trading_day, get_session, next_trading_day, prev_trading_day
**AC-VN-STORE-021:** Missing calendar date → CLOSED, MissingCalendarDateEvent logged
**AC-VN-STORE-022:** Query API: latest prices, historical OHLCV, latest fundamentals, order book, corporate actions, symbols, calendar
**AC-VN-STORE-023:** Pagination via cursor, max 1000 records/page, max 1 year range for OHLCV
**AC-VN-STORE-024:** Cache-first reads: Redis for latest, TSDB for historical
**AC-VN-STORE-025:** Retention: prices hot 1h/warm 30d/cold 7y; OHLCV warm 2y/cold 20y; fundamentals warm 5y/cold perm; orderbook hot 5m/warm 1d/cold 30d; corporate actions permanent
**AC-VN-STORE-026:** Tiering job daily, emits RetentionJobCompletedEvent with stats
**AC-VN-STORE-027:** Metrics: write_latency_p50/p95/p99, read_latency, error_rate, queue_lag, cache_hit_rate, disk_usage, tier_distribution
**AC-VN-STORE-028:** Health: status, writes_ok, reads_ok, cache_ok, lag_ms, disk_pct; degraded if cache_miss>20%, unhealthy if write_error>5%
**AC-VN-STORE-029:** Alerts: write_p99>500ms, error_rate>1%, disk>80%, lag>10s

## Estimated Effort
13 story points

## Assignee
BA

## DoD Tier
Tier 2 (Feature)

## Dependencies
- stack-vnstock-data-ingestion.md (S4 storage architecture, S2 normalizer events, S5 observability)
- TimescaleDB/InfluxDB for time-series, Redis for caching, PostgreSQL for relational, S3/MinIO for cold storage

## Notes
- All timestamps UTC ISO8601
- Prices VND, volumes shares
- TSDB: TimescaleDB (PostgreSQL extension) or InfluxDB
- Redis: latest prices, latest fundamentals, order book L2, symbol registry, trading calendar
- PostgreSQL: symbol registry, trading calendar, corporate actions catalog, version catalog
- Cold storage: Parquet on S3/MinIO, partitioned by symbol/year/month
- Query API: REST + GraphQL, cursor-based pagination
- Retention job: daily cron, idempotent
- Metrics: Prometheus exposition format
- Health: Kubernetes liveness/readiness probes