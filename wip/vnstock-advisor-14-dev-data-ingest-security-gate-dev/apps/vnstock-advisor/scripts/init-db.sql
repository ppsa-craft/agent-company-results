-- Initialize TimescaleDB extension and create market_data hypertable
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create market_data table
CREATE TABLE IF NOT EXISTS market_data (
    time        TIMESTAMPTZ       NOT NULL,
    symbol      TEXT              NOT NULL,
    open        DOUBLE PRECISION  NOT NULL,
    high        DOUBLE PRECISION  NOT NULL,
    low         DOUBLE PRECISION  NOT NULL,
    close       DOUBLE PRECISION  NOT NULL,
    volume      BIGINT            NOT NULL,
    source      TEXT              NOT NULL
);

-- Convert to hypertable partitioned by time
SELECT create_hypertable('market_data', 'time', if_not_exists => TRUE);

-- Create indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_market_data_symbol_time ON market_data (symbol, time DESC);
CREATE INDEX IF NOT EXISTS idx_market_data_source ON market_data (source);

-- Enable compression for older data (optional, requires TimescaleDB 2.0+)
-- ALTER TABLE market_data SET (
--     timescaledb.compress,
--     timescaledb.compress_segmentby = 'symbol'
-- );
-- SELECT add_compression_policy('market_data', INTERVAL '7 days');