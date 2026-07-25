# Flagship Horizontal Analytics Sync (vn-stock-analytics-sync)

**Description:** 
Lightweight horizontal analytics sync for flagship - enables analytics across flagship products while preserving existing data pipelines. Integrates with existing flagship products and provides cross-product analytics integration.

**Acceptance Criteria:**
- [ ] Define analytics integration contract between flagship products (vn-stock, json-formatter, qr-code-generator, day-calculator)
- [ ] Implement basic sync service that aggregates key metrics from flagship products
- [ ] Add analytics middleware to central factory with dependency tracking
- [ ] Create integration tests for sync functionality across flagship products
- [ ] Update flagship README with analytics endpoint documentation
- [ ] Add analytics monitoring for flagship pipeline performance

**Verification:**
- [ ] Tests pass: `npm test -- --grep "analytics-sync"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: Analytics endpoints return integrated metrics

**Dependencies:** None - independent task on existing flagship codebase

**Files likely touched:**
- `src/products/flagship-analytics.ts`
- `src/flagship-metrics.ts`
- `src/flagship-middleware.ts`
- `tests/flagship-analytics.test.ts`
- `README.md` (flagship analytics section)

**Estimated scope:** Medium (4-5 files)