# Canonical Schema: market_data

**Product:** vnstock-advisor  
**Component:** data-ingest  
**Version:** 1.0  
**Status:** Approved — PM signed off 2026-08-01  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Table Definition

```sql
-- Core market data table for OHLCV bars
CREATE TABLE market_data (
    symbol          VARCHAR(20)     NOT NULL,
    timestamp       TIMESTAMPTZ     NOT NULL,
    open            NUMERIC(18,4)   NOT NULL,
    high            NUMERIC(18,4)   NOT NULL,
    low             NUMERIC(18,4)   NOT NULL,
    close           NUMERIC(18,4)   NOT NULL,
    volume          BIGINT          NOT NULL DEFAULT 0,
    source          VARCHAR(20)     NOT NULL,
    ingested_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),

    -- Primary key: one row per symbol per timestamp
    CONSTRAINT pk_market_data PRIMARY KEY (symbol, timestamp),

    -- Basic data integrity
    CONSTRAINT chk_ohlc_order CHECK (low <= open AND low <= close AND high >= open AND high >= close),
    CONSTRAINT chk_non_negative CHECK (open >= 0 AND high >= 0 AND low >= 0 AND close >= 0 AND volume >= 0),
    CONSTRAINT chk_source CHECK (source IN ('CAFEF', 'VNDIRECT', 'VIETSTOCK', 'MANUAL')),

    -- Partition by month for performance (optional, see below)
) PARTITION BY RANGE (timestamp);

-- Indexes for common query patterns
CREATE INDEX idx_market_data_symbol_time_desc ON market_data (symbol, timestamp DESC);
CREATE INDEX idx_market_data_time_symbol ON market_data (timestamp DESC, symbol);
CREATE INDEX idx_market_data_ingested_at ON market_data (ingested_at DESC);

-- Partition function (example: monthly partitions)
-- Run this once, then add partitions as needed:
-- CREATE TABLE market_data_2026_07 PARTITION OF market_data
--     FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
-- CREATE TABLE market_data_2026_08 PARTITION OF market_data
--     FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
-- ... etc.

-- Helper: auto-create monthly partitions via pg_partman (recommended)
-- Or use a maintenance job to create next 3 months ahead
```

---

## Column Reference

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `symbol` | `VARCHAR(20)` | PK, NOT NULL | Stock symbol (e.g., `VNM`, `VCB`, `FPT`). Uppercase. Matches reference data. |
| `timestamp` | `TIMESTAMPTZ` | PK, NOT NULL | Trading session timestamp. **Always 15:00:00+07 (market close) for daily bars.** Stored in UTC. |
| `open` | `NUMERIC(18,4)` | NOT NULL, ≥0 | Opening price (VND). 4 decimal places for precision (some derivatives). |
| `high` | `NUMERIC(18,4)` | NOT NULL, ≥0 | Session high price. |
| `low` | `NUMERIC(18,4)` | NOT NULL, ≥0 | Session low price. |
| `close` | `NUMERIC(18,4)` | NOT NULL, ≥0 | Closing price (last matched price). |
| `volume` | `BIGINT` | NOT NULL, DEFAULT 0 | Total matched volume (shares). 0 for suspended/untraded days. |
| `source` | `VARCHAR(20)` | NOT NULL, CHECK | Data source: `CAFEF`, `VNDIRECT`, `VIETSTOCK`, `MANUAL`. |
| `ingested_at` | `TIMESTAMPTZ` | NOT NULL, DEFAULT NOW() | When this row was last upserted. Updated on every ingest run. |

---

## Design Rationale

### 1. Primary Key: `(symbol, timestamp)`
- **Enforces idempotency** (UC-DI-4): re-ingesting same symbol/date updates the row
- **Natural partition key** for time-series access patterns
- **No surrogate ID** — saves 8 bytes/row; composite PK is the access path

### 2. `TIMESTAMPTZ` for timestamp
- Stores in UTC, displays in session timezone
- Daily bars normalized to `15:00:00+07` (HOSE/HNX close) → `08:00:00Z`
- Enables correct ordering across DST boundaries (VN doesn't observe DST, but good practice)

### 3. `NUMERIC(18,4)` for prices
- VND prices: max ~1,000,000 (1M VND) → 7 digits integer
- 4 decimals supports derivatives, warrants, future splits
- Avoids floating-point errors in financial calculations
- Storage: ~10 bytes/column vs 8 for DOUBLE PRECISION — acceptable

### 4. `BIGINT` for volume
- Max daily volume ~10B shares (theoretical) → fits in 64-bit
- `0` for no trades (not NULL — simplifies queries)

### 5. `source` CHECK constraint
- Tracks provenance for debugging/audit
- `MANUAL` for admin corrections/backfills
- Extensible: add new sources to CHECK list via migration

### 6. `ingested_at` DEFAULT NOW()
- Updated on every upsert (see Upsert SQL below)
- Enables data freshness monitoring (UC-DI-3)
- Not part of PK — allows re-ingest without PK conflict

### 7. CHECK constraints
- `chk_ohlc_order`: Catches corrupted source data (high < low, etc.)
- `chk_non_negative`: Prices/volume never negative
- `chk_source`: Prevents typos in source field

---

## Upsert Statement (UC-DI-4 Implementation)

```sql
-- Single-row upsert (used in batch)
INSERT INTO market_data (symbol, timestamp, open, high, low, close, volume, source, ingested_at)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
ON CONFLICT (symbol, timestamp) DO UPDATE SET
    open        = EXCLUDED.open,
    high        = EXCLUDED.high,
    low         = EXCLUDED.low,
    close       = EXCLUDED.close,
    volume      = EXCLUDED.volume,
    source      = EXCLUDED.source,
    ingested_at = NOW()
WHERE market_data.open        IS DISTINCT FROM EXCLUDED.open
   OR market_data.high        IS DISTINCT FROM EXCLUDED.high
   OR market_data.low         IS DISTINCT FROM EXCLUDED.low
   OR market_data.close       IS DISTINCT FROM EXCLUDED.close
   OR market_data.volume      IS DISTINCT FROM EXCLUDED.volume
   OR market_data.source      IS DISTINCT FROM EXCLUDED.source;
```

**Notes:**
- `IS DISTINCT FROM` handles NULL-safe comparison (though our columns are NOT NULL)
- `WHERE` clause avoids unnecessary writes + `ingested_at` update when data unchanged
- Batch version: use `UNNEST` arrays or `COPY` to staging table + single `INSERT ... SELECT`

---

## Partitioning Strategy (Recommended)

```sql
-- Enable pg_partman (install extension first)
CREATE EXTENSION IF NOT EXISTS pg_partman;

-- Configure monthly partitioning on timestamp
SELECT partman.create_parent(
    p_parent_table           := 'public.market_data',
    p_control                := 'timestamp',
    p_type                   := 'range',
    p_interval               := '1 month',
    p_premake                := 3,        -- Keep 3 future partitions
    p_automatic_maintenance  := 'on',
    p_jobmon                 := true
);

-- This creates:
-- market_data_p2026_07, market_data_p2026_08, market_data_p2026_09, ...
-- And a background job to create/detach partitions
```

**Benefits:**
- Query pruning: `WHERE timestamp >= '2026-07-01'` scans only relevant partition
- Maintenance: `DROP PARTITION` for old data (retention policy)
- Index locality: indexes per partition, smaller B-trees

---

## Retention Policy

| Data Type | Retention | Action |
|-----------|-----------|--------|
| Daily OHLCV | Indefinite | Keep all history |
| Intraday (if added later) | 90 days | Auto-drop partitions |

**Implementation:** pg_partman `retention` config or manual `DROP TABLE market_data_p2024_01;`

---

## Migration Checklist

- [ ] Run `CREATE TABLE` + `PARTITION BY RANGE`
- [ ] Create initial partitions (current month + 2 future)
- [ ] Create indexes (auto-created on partitions by pg_partman)
- [ ] Verify `INSERT ... ON CONFLICT` works on partitioned table
- [ ] Add `pg_partman` background job for partition maintenance
- [ ] Grant `SELECT` to `analytics_role`, `INSERT/UPDATE` to `ingest_role`

---

## Downstream Consumers

| Consumer | Access Pattern | Notes |
|----------|----------------|-------|
| `analysis-engine` | `SELECT * FROM market_data WHERE symbol = $1 AND timestamp BETWEEN $2 AND $3` | Uses `idx_market_data_symbol_time_desc` |
| `api-gateway` | `SELECT * FROM market_data WHERE symbol = $1 ORDER BY timestamp DESC LIMIT 1` | Latest price |
| `backtest-runner` | `COPY (SELECT * FROM market_data WHERE timestamp BETWEEN ... ) TO STDOUT` | Bulk export |
| `monitoring` | `SELECT max(timestamp) as latest, count(*) FROM market_data WHERE timestamp >= now() - interval '2 days'` | Freshness check |

---

## Open Questions

1. **Adjusted close:** Store split/dividend-adjusted close? (Separate column `adj_close` or separate table?)
2. **Intraday bars:** Add `resolution` column (1m, 5m, 1H, 1D) to support multiple timeframes in same table?
3. **Foreign key to symbols:** Add `symbol_ref` table with `symbol PK, exchange, status` and FK from `market_data`?

*Decision: Keep v1 minimal (daily only, no adj_close). Extend via migration when needed.*

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*