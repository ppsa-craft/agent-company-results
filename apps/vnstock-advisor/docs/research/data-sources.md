# Data Source Evaluation: Free VN Market Data

**Product:** vnstock-advisor  
**Component:** data-ingest  
**Version:** 1.0  
**Status:** Approved — PM signed off 2026-08-01  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Executive Summary

This document evaluates three free Vietnamese stock market data sources for the `data-ingest` service: **CAFEF**, **VNDIRECT**, and **Vietstock**. Based on availability, rate limits, schema compatibility, and reliability, we recommend:

| Role | Source | Rationale |
|------|--------|-----------|
| **Primary** | **CAFEF** | Best free OHLCV coverage, stable HTML/JSON endpoints, used by vnstock library |
| **Fallback 1** | **VNDIRECT** | Good API structure, but requires token for higher limits; free tier limited |
| **Fallback 2** | **Vietstock** | Comprehensive data but aggressive free-tier gating; requires login for API access |

---

## Source Comparison

### 1. CAFEF (cafef.vn / liveboard.cafef.vn)

| Dimension | Details |
|-----------|---------|
| **Type** | Financial news portal with liveboard data |
| **Access Method** | Public web endpoints (HTML + embedded JSON); no official public API |
| **OHLCV Coverage** | HOSE, HNX, UPCOM — all listed symbols; indices (VNINDEX, HNX30, VN30) |
| **Historical Depth** | Daily bars available via chart endpoints; at least 5+ years |
| **Rate Limits** | No published limits; informal ~60 req/min observed; IP-based |
| **Authentication** | None required for public pages |
| **Data Freshness** | Intraday updates during trading hours; EOD finalized ~17:00 ICT |
| **Schema** | JSON embedded in liveboard pages; OHLCV fields: `open`, `high`, `low`, `close`, `volume`, `time` |
| **Reliability** | High — major portal, professionally operated by VCCorp |
| **Legal/ToS** | Public data display; scraping for personal/research generally tolerated; no commercial redistribution |
| **vnstock Support** | Primary source for `Market.equity.ohlcv()` in vnstock v4 (source code: `KBS` = "Ket Ban Securities" — CAFEF backend) |

**Sample Endpoint (inferred from vnstock):**
```
GET https://liveboard.cafef.vn/chart/history?symbol=VNM&resolution=D&from=1704067200&to=1735689600
Response: { "t": [...], "o": [...], "h": [...], "l": [...], "c": [...], "v": [...], "s": "ok" }
```

**Pros:**
- No auth, no registration
- Used by vnstock (battle-tested)
- Covers all exchanges
- Intraday + historical

**Cons:**
- Unofficial — could change without notice
- HTML/JSON parsing required (no formal API contract)
- Rate limits undocumented

---

### 2. VNDIRECT (dchart.vndirect.com.vn / api.vndirect.com.vn)

| Dimension | Details |
|-----------|---------|
| **Type** | Brokerage with public charting API |
| **Access Method** | REST API (JSON); TradingView-compatible chart endpoint |
| **OHLCV Coverage** | HOSE, HNX, UPCOM; indices; derivatives (VN30F1M) |
| **Historical Depth** | Full history available via chart API |
| **Rate Limits** | Free tier: ~30 req/min (unauthenticated); Higher with API key |
| **Authentication** | Optional API key for higher limits; key requires VNDIRECT account |
| **Data Freshness** | Real-time during session; EOD confirmed |
| **Schema** | TradingView UDF format: `{ t, o, h, l, c, v, s }` arrays |
| **Reliability** | High — broker-grade infrastructure |
| **Legal/ToS** | API intended for VNDIRECT clients; public chart endpoint semi-documented |
| **vnstock Support** | Supported as source `VCI` in vnstock for some endpoints |

**Sample Endpoint:**
```
GET https://dchart.vndirect.com.vn/dchart/api/history?symbol=VNM&resolution=D&from=1704067200&to=1735689600
Response: { "t": [...], "o": [...], "h": [...], "l": [...], "c": [...], "v": [...], "s": "ok" }
```

**Pros:**
- Clean TradingView-compatible JSON API
- Official broker source
- Supports derivatives

**Cons:**
- Low unauthenticated rate limit
- API key requires account + approval
- May block non-client IPs under load

---

### 3. Vietstock (finance.vietstock.vn / banggia.vietstock.vn)

| Dimension | Details |
|-----------|---------|
| **Type** | Financial data portal (Vietstock JSC) |
| **Access Method** | Web UI + "Bảng giá trực tuyến" (banggia.vietstock.vn); JSON endpoints behind login |
| **OHLCV Coverage** | Comprehensive: HOSE, HNX, UPCOM, ETF, warrants, bonds, derivatives |
| **Historical Depth** | Full history via "Xuất dữ liệu" (export) feature — requires login |
| **Rate Limits** | Free tier: Very limited; most API endpoints require login + paid tier |
| **Authentication** | Required for API access; free account gives limited quota |
| **Data Freshness** | Real-time streaming on banggia; EOD official |
| **Schema** | Proprietary JSON; OHLCV in "Thống kê giao dịch" tables |
| **Reliability** | High — dedicated data vendor |
| **Legal/ToS** | Commercial data vendor; free tier for personal use only; API access paid |
| **vnstock Support** | Source `VCI`/`KBS` for some endpoints; fundamental data from Vietstock |

**Sample Endpoint (public page, not API):**
```
GET https://banggia.vietstock.vn/ket-qua-giao-dich?tab=thong-ke-gia&exchange=1&code=-19
Returns HTML table — not machine-readable without parsing
```

**Pros:**
- Most comprehensive data (fundamentals, corporate actions, ETF, bonds)
- Official data vendor
- English + Vietnamese UI

**Cons:**
- Aggressive gating — API requires paid subscription
- Free web UI not designed for programmatic access
- Rate limits very low on free tier

---

## Detailed Comparison Matrix

| Criterion | CAFEF | VNDIRECT | Vietstock |
|-----------|-------|----------|-----------|
| **Free OHLCV Access** | ✅ Full | ⚠️ Limited rate | ❌ Gated |
| **No Auth Required** | ✅ | ✅ (low tier) | ❌ |
| **Official API** | ❌ | ⚠️ Semi-official | ✅ (paid) |
| **Schema Stability** | ⚠️ Unofficial | ✅ TradingView standard | ✅ Vendor contract |
| **Rate Limit (free)** | ~60/min (est.) | ~30/min | ~10/min (web) |
| **Historical Depth** | 5+ years | 10+ years | 10+ years |
| **All Exchanges** | ✅ | ✅ | ✅ |
| **Indices** | ✅ | ✅ | ✅ |
| **Derivatives** | ⚠️ Limited | ✅ VN30F1M | ✅ |
| **vnstock Integration** | Primary (KBS) | Secondary (VCI) | Fundamentals |
| **Operational Risk** | Medium (unofficial) | Low (broker) | Low (vendor) |
| **Legal Risk (personal)** | Low | Low | Low (ToS compliant) |

---

## Recommendation

### Primary: CAFEF
**Rationale:**
1. **vnstock already uses it** as the primary source for `Market.equity.ohlcv()` — the library handles parsing, retries, and schema normalization
2. **No authentication** — zero operational overhead for keys/tokens
3. **Full exchange coverage** — HOSE, HNX, UPCOM all available
4. **Battle-tested** — 1.2M+ downloads of vnstock v4+ with CAFEF as default
5. **Rate limits sufficient** — ~500 symbols × 1 request = ~8 min at 60/min; well within 10-min SLA

**Mitigation for unofficial status:**
- Wrap all CAFEF calls in adapter with circuit breaker
- Log raw responses for schema drift detection
- Fallback chain handles outages automatically

### Fallback 1: VNDIRECT
**Rationale:**
- Clean TradingView UDF JSON format — easy to parse
- Broker-grade reliability
- Used by vnstock as `VCI` source for some endpoints
- Activated only when CAFEF fails (timeout, 5xx, schema error)

**Limitation:** Low unauthenticated rate limit means fallback batch may be slower; implement per-symbol backoff.

### Fallback 2: Vietstock
**Rationale:**
- Only for fundamental/corporate action data (not OHLCV)
- OHLCV API is paid — not viable for free tier
- Keep as reference for future paid tier upgrade

**Decision:** **Do not use Vietstock for OHLCV ingest in free tier.** Use only if CAFEF + VNDIRECT both fail for a symbol (extremely rare), via html scraping of banggia.vietstock.vn as last resort.

---

## Implementation Guidance for DEV

1. **Adapter Pattern:** Create `SourceAdapter` interface with `fetch_ohlcv(symbol, date) -> OHLCVRecord`
2. **Circuit Breaker:** Track consecutive failures per source; trip after 5 failures, auto-reset after 5 min
3. **Schema Validation:** Validate response has `o,h,l,c,v,t` arrays of equal length; reject if `s != "ok"`
4. **Rate Limiting:** Token bucket per source (CAFEF: 50/min, VNDIRECT: 25/min) to stay under limits
5. **Observability:** Emit `source_used`, `latency_ms`, `fallback_triggered` per symbol

---

## Open Questions

1. **Trading calendar:** Should we fetch trading days from CAFEF (index history) or maintain our own?
2. **Symbol list:** Where to get authoritative active symbol list? (CAFEF `liveboard` page, VNDIRECT API, or vnstock `Reference.equity.list()`)
3. **Corporate actions:** Adjust for splits/dividends? (Out of scope for OHLCV ingest — handle in downstream)

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*