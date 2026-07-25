# BA Task: vn-stock-ba-5

## Goal
Define comprehensive analytics plan for VN stock data in the vn-stock product, including business intelligence, signal generation, and alert-driven insights.

## Status
in-progress

## Product
vn-stock

## Description
Define comprehensive analytics plan for VN stock data covering: business intelligence dashboards, technical/fundamental signal generation, anomaly detection, alert systems, and automated report generation based on unified data from S2-S4.

## Use Cases (Traceable to Acceptance Criteria)

### UC-VN-ANALYTICS-001: Real-time Price Dashboard
**Actors:** Trader, Risk Manager, Portfolio Manager
**Preconditions:** Historical real-time price data stored in S4, current prices cached in S4
**Main Flow:**
1. Dashboard user selects symbol (VNM, VCI, VND, TCBS, SSI)
2. System loads latest price from S4 cache (/prices/latest)
3. System enriches with last 10 real-time ticks from S4 time-series
4. System computes: current_price, change_pct, volume, vwap, bid_ask_spread, order_book_imbalance
5. System displays real-time price chart with volume bars
6. System emits to alerts if price volatility > threshold
**Postconditions:** Real-time dashboard displayed with computed metrics and alerts
**Alternate Flows:**
- S4 cache miss → fallback to S3 aggregated price
- Missing symbol → show error, suggest similar symbols from registry
- Network timeout → show stale indicator, retry every 30s
**Traceability:** AC-VN-ANALYTICS-001, AC-VN-ANALYTICS-002, AC-VN-ANALYTICS-003

### UC-VN-ANALYTICS-002: Technical Analysis Engine
**Actors:** Quantitative Analyst, Algo Trader
**Preconditions:** OHLCV data stored in S4 with daily/monthly aggregates
**Main Flow:**
1. User selects symbol, timeframe (1min, 5min, 1hr, daily), indicators
2. System queries S4 OHLCV with grouping window
3. System computes technical indicators: SMA, EMA, RSI, MACD, Bollinger Bands, Stochastic Oscillator, ADX, Volume Profile
4. System applies VN market session adjustments (different overnight behavior)
5. System generates technical signals based on crossovers, threshold breaches
6. System outputs signals with confidence scores and timestamps
**Postconditions:** Technical analysis report with indicators and signals generated
**Alternate Flows:**
- Insufficient data (< 20 periods) → show insufficient data warning
- Invalid indicator combination → show error, suggest valid combinations
- Compute timeout (>2s) → use cached results from previous run
**Traceability:** AC-VN-ANALYTICS-004, AC-VN-ANALYTICS-005, AC-VN-ANALYTICS-006

### UC-VN-ANALYTICS-003: Fundamental Analysis Dashboard
**Actors:** Fundamental Analyst, Portfolio Manager
**Preconditions:** Versioned fundamentals stored in S4, current period available
**Main Flow:**
1. User selects symbol and rating period
2. System retrieves fundamentals from S4 (/fundamentals/:symbol?period=:period)
3. System normalizes across sources (VNM: profile only, VCI: ratios, VND: full)
4. System computes derived metrics: beta (vs VN index), PEG ratio, EV/EBITDA, FCF yield
5. System applies sector/peer benchmarks (VN sector averages)
6. System generates fundamental scores (growth, profitability, valuation, financial health)
**Postconditions:** Fundamental analysis report with scores and recommendations
**Alternate Flows:**
- Historical fundamentals available → show trend analysis (YoY, QoQ)
- Data incomplete → show missing data warnings, use available data
- Scoring timeout → use cached scores
**Traceability:** AC-VN-ANALYTICS-007, AC-VN-ANALYTICS-008, AC-VN-ANALYTICS-009

### UC-VN-ANALYTICS-004: Corporate Actions Calendar
**Actors:** Investor, Compliance Officer, Dividend Advisor
**Preconditions:** Corporate actions stored in S4 with deduplication applied
**Main Flow:**
1. User selects symbol and date range
2. System queries S4 corporate actions (/corporate-actions/:symbol?from=...:to=...)
3. System filters by action type (dividend, split, bonus, rights, merger)
4. System enriches with implied value (dividend yield calculation)
5. System computes ex-dividend dates and record dates
6. System generates calendar view with summary statistics
**Postconditions:** Corporate actions calendar displayed with summary stats
**Alternate Flows:**
- No corporate actions → show calendar with no events marker
- Conflicting corporate actions → show resolved event with discrepancy note
- Upcoming data not yet available → show forecast based on historical patterns
**Traceability:** AC-VN-ANALYTICS-010, AC-VN-ANALYTICS-011

### UC-VN-ANALYTICS-005: Sentiment & News Correlation
**Actors:** Market Analyst, Sentiment Modeler
**Preconditions:** Sentiment data available from external APIs, news feeds configured
**Main Flow:**
1. System collects news sentiment for selected symbols (last 24h, 7d, 30d)
2. System processes sentiment through VN language model (Vietnamese sentiment analysis)
3. System correlates sentiment scores with price movements
4. System computes sentiment vs price momentum correlation (PNC)
5. System generates alerts for sentiment-price divergences
**Postconditions:** Sentiment analysis report with correlations and alerts
**Alternate Flows:**
- No news for symbol → show null sentiment trend
- Sentimental model unavailable → fallback to proxy (social media mentions)
- High latency → use cached sentiment from previous 30m
**Traceability:** AC-VN-ANALYTICS-012, AC-VN-ANALYTICS-013, AC-VN-ANALYTICS-014

### UC-VN-ANALYTICS-006: Multi-Asset Correlation Matrix
**Actors:** Portfolio Manager, Risk Analyst
**Preconditions:** Historical price data available for multiple symbols
**Main Flow:**
1. User selects portfolio of symbols (VN stocks + relevant indices)
2. System retrieves historical OHLCV from S4 with rolling window (default 1y)
3. System computes rolling correlation matrix (daily returns)
4. System normalizes correlations by VN market regime (bull/bear/flat)
5. System identifies clusters and outlier correlations
6. System outputs heat map with correlation arrows and risk scores
**Postconditions:** Correlation matrix and risk analysis generated
**Alternate Flows:**
- Insufficient data (< 3 months) → use available window with warning
- High correlation clusters detected → highlight for portfolio rebalancing
- Real-time update requested → use latest prices if available
**Traceability:** AC-VN-ANALYTICS-015, AC-VN-ANALYTICS-016, AC-VN-ANALYTICS-017

### UC-VN-ANALYTICS-007: Automated Alert & Notification System
**Actors:** Risk Manager, Portfolio Manager, Compliance Officer
**Preconditions:** Alert configuration stored in S4, alert engine running
**Main Flow:**
1. Alert engine monitors various triggers:
   - Price volatility > 5% per minute
   - Technical signal generation
   - Fundamental deviation alerts
   - Corporate action calendar events
   - Sentiment-price divergence > 2x
2. Engine evaluates alert conditions every 30s
3. Engine applies user alert preferences (symbol, condition, delivery channel)
4. Engine triggers notifications (in-app, email, SMS)
5. Engine logs alert for analytics and audit
**Postconditions:** Alerts delivered according to user preferences
**Alternate Flows:**
- Alert failure → retry with backoff, eventually queue for manual review
- Duplicate alerts → deduplicate within 5m window
- User disables/alert silences → respect preferences
**Traceability:** AC-VN-ANALYTICS-018, AC-VN-ANALYTICS-019, AC-VN-ANALYTICS-020

### UC-VN-ANALYTICS-008: Automated Report Generator
**Actors:** Portfolio Manager, Institutional Investor
**Preconditions:** Scheduled generation configured, market data available
**Main Flow:**
1. Scheduler triggers report generation for configured users
2. System builds comprehensive report including:
   - Performance summary (price trends, volume analysis)
   - Technical indicators (latest signals, chart patterns)
   - Fundamental analysis (scores, recommendations)
   - Risk metrics (correlation, volatility, beta)
   - Corporate actions and earnings calendar
3. System formats report as HTML/PDF
4. System emails report to recipients
5. System archives generated reports in S4
**Postconditions:** Scheduled report distributed and archived
**Alternate Flows:**
- Data unavailable for date range → include only available data with note
- Email delivery fails → queue for retry, alert admin
- Report generation timeout → retry with subset of sections
**Traceability:** AC-VN-ANALYTICS-021, AC-VN-ANALYTICS-022

### UC-VN-ANALYTICS-009: VN Market Regime Detection
**Actors:** Market Strategist, Macro Analyst
**Preconditions:** Historical VN market data, regime detection model configured
**Main Flow:**
1. System analyzes VN market indicators:
   - Price momentum (VN index)
   - Volume trends
   - Volatility (VN30 volatility index)
   - Interest rates (SBV policy)
   - Inflation data (GSO)
2. System classifies regime: Bull, Bear, Neutral, Volatility
3. System applies regime-specific settings to analytics
4. System adjusts signal thresholds based on regime
5. System updates UI components with regime indicators
**Postconditions:** Current market regime detected and applied
**Alternate Flows:**
- Model training required → use last known regime
- Outlier market events → adjust regime classification with warning
- Manual override → respect user selection
**Traceability:** AC-VN-ANALYTICS-023, AC-VN-ANALYTICS-024

### UC-VN-ANALYTICS-010: Analytics Health Monitor
**Actors:** DevOps, System Admin
**Preconditions:** System monitoring configured, metrics endpoint exposed
**Main Flow:**
1. Health monitor queries analytics service health:
   - Service availability (/health)
   - Data freshness (last event timestamps)
   - Performance metrics (p50, p95, p99 latency)
   - Error rates and alert counts
2. Monitor applies VN working hour window (UTC+7)
3. Monitor generates health reports
4. Monitor triggers alerts for degradation
**Postconditions:** Health monitoring active with alerts
**Alternate Flows:**
- Service unavailable → trigger critical alert, send page
- Health metrics timeout → use previous health status
- Manual health check → display immediate status
**Traceability:** AC-VN-ANALYTICS-025, AC-VN-ANALYTICS-026

## User Stories

**US-VN-ANALYTICS-001:** As a Trader, I want real-time price dashboards so that I can make instant trading decisions.
- **Acceptance Criteria:** AC-VN-ANALYTICS-001, AC-VN-ANALYTICS-002, AC-VN-ANALYTICS-003

**US-VN-ANALYTICS-002:** As a Quantitative Analyst, I want technical analysis with VN market adjustments so that strategies are regime-aware.
- **Acceptance Criteria:** AC-VN-ANALYTICS-004, AC-VN-ANALYTICS-005, AC-VN-ANALYTICS-006

**US-VN-ANALYTICS-003:** As a Fundamental Analyst, I want multi-source fundamental analysis with scoring so that investment decisions are data-driven.
- **Acceptance Criteria:** AC-VN-ANALYTICS-007, AC-VN-ANALYTICS-008, AC-VN-ANALYTICS-009

**US-VN-ANALYTICS-004:** As a Corporate Action Advisor, I want a consolidated calendar with computed values so that dividend and split planning is accurate.
- **Acceptance Criteria:** AC-VN-ANALYTICS-010, AC-VN-ANALYTICS-011

**US-VN-ANALYTICS-005:** As a Market Analyst, I want sentiment analysis with Vietnamese language support so that local news is captured.
- **Acceptance Criteria:** AC-VN-ANALYTICS-012, AC-VN-ANALYTICS-013, AC-VN-ANALYTICS-014

**US-VN-ANALYTICS-006:** As a Portfolio Manager, I want correlation analysis with VN regime adjustments so that risk is properly measured.
- **Acceptance Criteria:** AC-VN-ANALYTICS-015, AC-VN-ANALYTICS-016, AC-VN-ANALYTICS-017

**US-VN-ANALYTICS-007:** As a Risk Manager, I want automated alerts with multi-channel delivery so that timely actions are taken.
- **Acceptance Criteria:** AC-VN-ANALYTICS-018, AC-VN-ANALYTICS-019, AC-VN-ANALYTICS-020

**US-VN-ANALYTICS-008:** As an Institutional Investor, I want scheduled analytics reports so that I have regular market summaries.
- **Acceptance Criteria:** AC-VN-ANALYTICS-021, AC-VN-ANALYTICS-022

**US-VN-ANALYTICS-009:** As a Market Strategist, I want VN market regime detection so that strategies are adapted to market conditions.
- **Acceptance Criteria:** AC-VN-ANALYTICS-023, AC-VN-ANALYTICS-024

**US-VN-ANALYTICS-010:** As a System Admin, I want analytics health monitoring so that issues are detected early.
- **Acceptance Criteria:** AC-VN-ANALYTICS-025, AC-VN-ANALYTICS-026

## Acceptance Criteria (Traceable)

**AC-VN-ANALYTICS-001:** Dashboard loads within 2s, shows latest price within 1s, updates real-time within 3s
**AC-VN-ANALYTICS-002:** Computes 5 technical indicators within 500ms, signals generated for crossovers
**AC-VN-ANALYTICS-003:** 95%+ fundamental data coverage for each symbol, scores computed across 5 dimensions
**AC-VN-ANALYTICS-004:** Corporate actions deduplicated, no duplicate events across sources, warnings for conflicts
**AC-VN-ANALYTICS-005:** Sentiment pipeline processes 100+ Vietnamese news articles per minute, correlation computed
**AC-VN-ANALYTICS-006:** Correlation matrix computed for up to 20 symbols within 30s, cluster detection included
**AC-VN-ANALYTICS-007:** Alerts sent within 30s of trigger, respects user preferences, deduplication applied
**AC-VN-ANALYTICS-008:** Scheduled reports generated daily/weekly, PDFs emailed within 10s of generation
**AC-VN-ANALYTICS-009:** Regime classified based on 15+ VN indicators, updates every hour
**AC-VN-ANALYTICS-010:** Analytics health endpoints exposed, metrics exported to S5 monitoring, automated alerts
**AC-VN-ANALYTICS-011:** Alert thresholds configurable per user, notification types validated, delivery status tracked
**AC-VN-ANALYTICS-012:** Report data completeness >95%, sections optional based on user role, archival quality verified
**AC-VN-ANALYTICS-013:** Vietnamese language support for sentiment analysis, local keywords configured
**AC-VN-ANALYTICS-014:** S5 observability for analytics, health checks every 30s, SLA monitoring
**AC-VN-ANALYTICS-015:** Analytics unhealthy → trigger alert, page admin, create incident in dashboard
**AC-VN-ANALYTICS-016:** Alert delivery success/failure logged, read receipts for email/SMS when available
**AC-VN-ANALYTICS-017:** Budget limits for alerts enforced, per-user alert quotas respected
**AC-VN-ANALYTICS-018:** Report generation timeout < 30s for standard reports, < 60s for comprehensive reports
**AC-VN-ANALYTICS-019:** Automated report scheduling configured, delivery status tracked, retry logic with backoff
**AC-VN-ANALYTICS-020:** Current VN regime detected from 15+ indicators, updates during market hours
**AC-VN-ANALYTICS-021:** Generated reports archived in S4 with integrity verification, searchable by user/date
**AC-VN-ANALYTICS-022:** Reports delivered to configured recipients, delivery confirmations logged, manual delivery fallback

## Estimated Effort
12 story points

## Assignee
BA

## DoD Tier
Tier 2 (Feature)

## Dependencies
- stack-vnstock-data-ingestion.md (VN-specific analytics design, regime detection, Vietnamese sentiment)
- S5 observability for health monitoring
- External VN sentiment APIs and news feeds
- Trading calendar and holiday data (S4 trading calendar)
- VN financial data providers for benchmark data

## Notes
- All timestamps in VN time (UTC+7) with ability to toggle to UTC
- All financial values in Vietnamese Dong (VND)
- Analytics supports both retail (trader dashboards) and institutional (scheduled reports)
- Vietnamese language support required for sentiment analysis and notifications
- Market regime detection includes VN-specific indicators (SBV rates, inflation, forex)
- Alert system supports multiple channels with rate limiting to prevent spam
- Analytics pipelines are asynchronous and can be scaled independently
- Each analytics module can operate independently with shared data from S4
- Reports include both tabular data and visualizations with export functionality