# BA Task: vn-stock-ba-2

## Goal
Define comprehensive use cases for VN stock normalizer (S2) for the vn-stock product.

## Status
in-progress

## Product
vn-stock

## Description
Define comprehensive use cases for the VN stock normalizer (S2 layer) as defined in the vn-stock data ingestion architecture. The normalizer transforms source-specific DTOs from S1 adapters (VNM, VCI, VND, TCBS, SSI) into canonical unified domain models, handles conflicts, deduplication, enrichment, and emits normalized events to S3/S4.

## Use Cases (Traceable to Acceptance Criteria)

### UC-VN-NORM-001: Normalize Real-time Price from Multiple Sources
**Actors:** Normalizer (S2), Price Aggregator (S3)
**Preconditions:** At least one S1 adapter returns valid PriceDTO
**Main Flow:**
1. Normalizer receives PriceDTO[] from multiple adapters (VNM, VCI, TCBS)
2. Normalizer validates each DTO: required fields, timestamp freshness (< 5s), price > 0
3. Normalizer groups by symbol
4. Normalizer applies conflict resolution: median price for price, sum for volume, latest timestamp
5. Normalizer enriches with: vwap (volume-weighted), spread (ask-bid), source_count
6. Normalizer emits UnifiedPriceEvent to S3
**Postconditions:** UnifiedPriceEvent emitted with: symbol, price, volume, vwap, spread, bid, ask, timestamp_utc, sources[], source_count
**Alternate Flows:**
- Single source → emit with source_count=1, spread=null
- Stale data (>5s) → exclude, log warning, emit with remaining sources
- All sources stale → emit StalePriceEvent with staleness_ms
- Price variance > 5% → emit PriceDiscrepancyEvent, use median
**Traceability:** AC-VN-NORM-001, AC-VN-NORM-002, AC-VN-NORM-003, AC-VN-NORM-004

### UC-VN-NORM-002: Normalize Historical OHLCV with Gap Detection
**Actors:** Normalizer (S2), Historical Store (S4)
**Preconditions:** OHLCVDTO[] from one or more adapters for date range
**Main Flow:**
1. Normalizer receives OHLCVDTO[] from adapter(s) for symbol + date range
2. Normalizer validates each record: OHLC relationship (H≥O,C≥L), volume ≥ 0, timestamp aligns to session
3. Normalizer sorts by timestamp, detects gaps (missing trading sessions)
4. Normalizer applies source priority: VCI > VNM > TCBS for OHLCV
5. Normalizer fills single-session gaps with previous close (configurable)
6. Normalizer emits UnifiedOHLCVEvent per record
**Postconditions:** UnifiedOHLCVEvent[] emitted with: symbol, open, high, low, close, volume, timestamp_utc, source, gap_filled=bool, session_type
**Alternate Flows:**
- Multi-source conflict → use priority source, log discrepancy event
- Gap > 1 session → emit GapDetectedEvent, don't fill
- Invalid OHLC relationship → reject record, emit ValidationErrorEvent
**Traceability:** AC-VN-NORM-005, AC-VN-NORM-006, AC-VN-NORM-007, AC-VN-NORM-008

### UC-VN-NORM-003: Normalize Fundamentals with Versioning
**Actors:** Normalizer (S2), Fundamental Store (S4)
**Preconditions:** FundamentalDTO from VND (primary), fallback to VCI
**Main Flow:**
1. Normalizer receives FundamentalDTO from VND adapter
2. Normalizer validates required fields: symbol, period, revenue, net_income
3. Normalizer computes derived: pe_ratio, pb_ratio, roe, roa, debt_to_equity if missing
4. Normalizer versions: creates FundamentalVersion with version_hash, effective_date
5. Normalizer emits UnifiedFundamentalEvent
**Postconditions:** UnifiedFundamentalEvent with: symbol, period, revenue, net_income, pe, pb, roe, roa, debt_to_equity, version_hash, source, fetched_at
**Alternate Flows:**
- Missing derived fields → compute if inputs available, else null
- Version hash unchanged → emit UnchangedEvent, skip store write
- Source conflict (VND vs VCI) → prefer VND, log discrepancy
**Traceability:** AC-VN-NORM-009, AC-VN-NORM-010, AC-VN-NORM-011

### UC-VN-NORM-004: Normalize Order Book with Level Aggregation
**Actors:** Normalizer (S2), Order Book Aggregator (S3)
**Preconditions:** OrderBookDTO from TCBS (primary), VNM (fallback)
**Main Flow:**
1. Normalizer receives OrderBookDTO from primary source
2. Normalizer validates: sequence increasing, bid < ask, levels sorted
3. Normalizer aggregates levels: combine same-price levels, sort bid desc, ask asc
4. Normalizer computes: spread, mid_price, bid_depth_10, ask_depth_10, imbalance
5. Normalizer emits UnifiedOrderBookEvent
**Postconditions:** UnifiedOrderBookEvent: symbol, bids[][{price, volume}], asks[][{price, volume}], spread, mid_price, bid_depth_10, ask_depth_10, imbalance, sequence, timestamp_utc, source
**Alternate Flows:**
- Primary source stale → fallback to secondary, emit SourceSwitchedEvent
- Crossed book (bid ≥ ask) → emit CrossedBookEvent, use mid_price
- Sequence gap > 100 → emit SequenceGapEvent, request snapshot
**Traceability:** AC-VN-NORM-012, AC-VN-NORM-013, AC-VN-NORM-014

### UC-VN-NORM-005: Normalize Corporate Actions with Deduplication
**Actors:** Normalizer (S2), Corporate Action Store (S4)
**Preconditions:** CorporateActionDTO[] from SSI, VND
**Main Flow:**
1. Normalizer receives CorporateActionDTO[] from multiple sources
2. Normalizer normalizes action_type enum: DIVIDEND, SPLIT, BONUS, RIGHTS, MERGER
3. Normalizer deduplicates by: symbol, action_type, ex_date, record_date
4. Normalizer merges: prefer source with more fields populated
5. Normalizer emits UnifiedCorporateActionEvent
**Postconditions:** UnifiedCorporateActionEvent: symbol, action_type, ex_date, record_date, pay_date, ratio, cash_amount, currency="VND", source_priority, merged_sources[]
**Alternate Flows:**
- Conflicting cash amounts → use majority, log DiscrepancyEvent
- Missing pay_date → infer from ex_date + 10 business days (VN standard)
- Duplicate detection → emit DuplicateSuppressedEvent
**Traceability:** AC-VN-NORM-015, AC-VN-NORM-016, AC-VN-NORM-017

### UC-VN-NORM-006: Normalizer Health & Metrics Emission
**Actors:** Normalizer (S2), Observability (S5)
**Preconditions:** Normalizer running, metrics endpoint exposed
**Main Flow:**
1. Normalizer emits metrics per normalization: records_in, records_out, validation_errors, conflicts, gaps_filled, source_switches
2. Normalizer emits latency histogram: p50, p95, p99 normalization latency
3. Normalizer emits source health: records_per_source, error_rate_per_source
4. Normalizer health endpoint returns: status, last_event_ts, lag_ms, error_rate
**Postconditions:** Metrics exposed on /metrics, health on /health
**Alternate Flows:**
- Lag > 10s → health degraded
- Error rate > 5% → health unhealthy
**Traceability:** AC-VN-NORM-018, AC-VN-NORM-019, AC-VN-NORM-020

### UC-VN-NORM-007: Symbol Mapping & Canonicalization
**Actors:** Normalizer (S2), Symbol Registry (S4)
**Preconditions:** Symbol registry loaded with canonical symbols and aliases
**Main Flow:**
1. Normalizer receives DTO with source-specific symbol
2. Normalizer looks up canonical symbol in registry
3. Normalizer replaces source symbol with canonical symbol
4. Normalizer emits normalized events with canonical symbol
**Postconditions:** All emitted events use canonical symbols
**Alternate Flows:**
- Unknown symbol → emit UnmappedSymbolEvent, use source symbol with warning
- Alias conflict → emit AliasConflictEvent, use first registered
**Traceability:** AC-VN-NORM-021, AC-VN-NORM-022

## User Stories

**US-VN-NORM-001:** As a Price Aggregator (S3), I want unified prices from multiple sources so that I get the best available price.
- **Acceptance Criteria:** AC-VN-NORM-001, AC-VN-NORM-002, AC-VN-NORM-003, AC-VN-NORM-004

**US-VN-NORM-002:** As a Historical Store (S4), I want gap-aware OHLCV so that backtests handle missing sessions correctly.
- **Acceptance Criteria:** AC-VN-NORM-005, AC-VN-NORM-006, AC-VN-NORM-007, AC-VN-NORM-008

**US-VN-NORM-003:** As a Fundamental Store (S4), I want versioned fundamentals so that I can track changes and avoid redundant writes.
- **Acceptance Criteria:** AC-VN-NORM-009, AC-VN-NORM-010, AC-VN-NORM-011

**US-VN-NORM-004:** As an Order Book Aggregator (S3), I want normalized L2 order books so that depth aggregation works across sources.
- **Acceptance Criteria:** AC-VN-NORM-012, AC-VN-NORM-013, AC-VN-NORM-014

**US-VN-NORM-005:** As a Corporate Action Store (S4), I want deduplicated corporate actions so that calendars are accurate.
- **Acceptance Criteria:** AC-VN-NORM-015, AC-VN-NORM-016, AC-VN-NORM-017

**US-VN-NORM-006:** As Observability (S5), I want normalizer metrics so that I can monitor pipeline health.
- **Acceptance Criteria:** AC-VN-NORM-018, AC-VN-NORM-019, AC-VN-NORM-020

**US-VN-NORM-007:** As a Symbol Registry, I want canonical symbols so that all layers use consistent identifiers.
- **Acceptance Criteria:** AC-VN-NORM-021, AC-VN-NORM-022

## Acceptance Criteria (Traceable)

**AC-VN-NORM-001:** Normalizer emits UnifiedPriceEvent with fields: symbol, price (median), volume (sum), vwap, spread, bid, ask, timestamp_utc (latest), sources[], source_count within 10ms p99
**AC-VN-NORM-002:** Price variance > 5% across sources → PriceDiscrepancyEvent emitted with source prices
**AC-VN-NORM-003:** Stale data (>5s) excluded, StalePriceEvent emitted if all sources stale with max_staleness_ms
**AC-VN-NORM-004:** Single source → spread=null, vwap=price, source_count=1
**AC-VN-NORM-005:** UnifiedOHLCVEvent: symbol, open, high, low, close, volume, timestamp_utc, source, gap_filled, session_type (MORNING/AFTERNOON)
**AC-VN-NORM-006:** Gap detection: missing trading session → GapDetectedEvent with gap_start, gap_end, expected_sessions
**AC-VN-NORM-007:** Single session gap → gap_filled=true, filled with prev_close; multi-session → gap_filled=false
**AC-VN-NORM-008:** Source priority for OHLCV: VCI > VNM > TCBS; conflict → DiscrepancyEvent logged
**AC-VN-NORM-009:** UnifiedFundamentalEvent: symbol, period, revenue, net_income, pe, pb, roe, roa, debt_to_equity, version_hash, source, fetched_at
**AC-VN-NORM-010:** Version hash = SHA256 of all fields; unchanged hash → UnchangedEvent, no store write
**AC-VN-NORM-011:** Derived fields computed if inputs present: pe=price/eps, pb=price/bvps, roe=ni/equity, roa=ni/assets, d2e=debt/equity
**AC-VN-NORM-012:** UnifiedOrderBookEvent: symbol, bids[][{price,volume}], asks[][{price,volume}], spread, mid_price, bid_depth_10, ask_depth_10, imbalance, sequence, timestamp_utc, source
**AC-VN-NORM-013:** Level aggregation: same price → sum volume; bids sorted desc, asks sorted asc
**AC-VN-NORM-014:** Source switch → SourceSwitchedEvent; crossed book → CrossedBookEvent; sequence gap>100 → SequenceGapEvent
**AC-VN-NORM-015:** UnifiedCorporateActionEvent: symbol, action_type, ex_date, record_date, pay_date, ratio, cash_amount, currency="VND", source_priority, merged_sources[]
**AC-VN-NORM-016:** Dedup key: symbol+action_type+ex_date+record_date; merge prefers more complete source
**AC-VN-NORM-017:** Cash conflict → majority wins (or VND > SSI), CashConflictEvent; missing pay_date → ex_date + 10 business days (VN calendar)
**AC-VN-NORM-018:** Metrics: records_in_total, records_out_total, validation_errors_total, conflicts_total, gaps_filled_total, source_switches_total
**AC-VN-NORM-019:** Latency histogram: normalize_latency_ms_bucket (p50<5ms, p95<15ms, p99<50ms)
**AC-VN-NORM-020:** Source health: records_per_source, error_rate_per_source, last_success_ts_per_source
**AC-VN-NORM-021:** All emitted events use canonical_symbol from registry
**AC-VN-NORM-022:** Unknown symbol → UnmappedSymbolEvent{symbol, source}, canonical_symbol=source_symbol, warning logged

## Estimated Effort
8 story points

## Assignee
BA

## DoD Tier
Tier 2 (Feature)

## Dependencies
- stack-vnstock-data-ingestion.md (S2 normalizer architecture, S1 adapter contracts, S3/S4 event consumers, S5 observability)
- S1 adapter DTO contracts (PriceDTO, OHLCVDTO, FundamentalDTO, OrderBookDTO, CorporateActionDTO)

## Notes
- All timestamps UTC ISO8601
- All prices VND, volumes shares
- Normalizer is stateless, horizontally scalable
- Events emitted to Kafka/Redis Streams (S3 consumers)
- Version hashing uses SHA256 of canonical field values
- VN trading sessions: Morning 09:00-11:30, Afternoon 13:00-14:30 (UTC+7)
- Business days follow VN trading calendar (S4)
- Gap filling configurable: default=true for single session, false for multi-session
- Source priority: Price (VNM=VCI>TCBS), OHLCV (VCI>VNM>TCBS), Fundamentals (VND>VCI), OrderBook (TCBS>VNM), CorporateActions (VND>SSI)