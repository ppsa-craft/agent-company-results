# Idea Backlog — Cycle 144

**Ranked by strategic priority (flagship first, then reuse potential)**

---

## 1. [app: vn-stock-suggestion] M2 — Technical Analysis Engine (vn-c2)
**Reuse rank:** ★★★★★ (core analytics library shared across all downstream)
**Description:** Consumes canonical prices from S1 unified API, produces a composable indicator library (RSI, MACD, Bollinger Bands, MA crossovers, volume profiles) as a reusable Python/Numba package. Standardized indicator interface for backtesting, screener, and alerting to call into.
**Architecture:** Package `vn_indicators` with `IndicatorEngine.calculate(symbol, indicators[], timeframe)`.
**Why flagship:** Natural next milestone after S1-S4 data pipeline — the engine that powers all signal generation.

---

## 2. [app: crypto-screener] Crypto Market Screener (NEW app)
**Reuse rank:** ★★★★★ (reuses every reusable asset from vn-stock)
**Description:** Identical architecture pattern as vn-stock-suggestion but for crypto markets. Reuses: adapter pattern (Binance, Coinbase, Kraken adapters), canonical schemas (same 6 types), normalization pipeline, caching layer. Builds the same S1-S4 stack for a different asset class.
**Why now:** The VN stock flagship is near M1 completion. Its adapter pattern + canonical schemas were designed for reuse. Crypto is the fastest path to a second product — drop in new adapters, everything downstream is already built.
**Risk:** API rate limits on exchange data are tighter; need dedicated rate-limit handling.

---

## 3. [app: shared] Unified Data Emitter — Reusable Export Layer
**Reuse rank:** ★★★★★ (pays for itself across every product)
**Description:** A generic export/streaming layer that any service can emit canonical data through: CSV/Parquet for data scientists, JSON/SSE for dashboards, Protobuf/gRPC for internal services, WebSocket for real-time. One emitter config, multiple output formats.
**Architecture:** Go service consuming from Redis pub/sub, emitting to configurable sinks.
**Why valuable:** Every product the company builds needs to export data. Building it once as a shared service eliminates duplication.

---

**Current flagship:** VN Stock Suggestion System (M1: S1-S4 services in progress)
**Next after M1 ships:** M2 Technical Analysis Engine
**Backlog health:** 6 viable ideas, 5 with high reuse rank. Good.

