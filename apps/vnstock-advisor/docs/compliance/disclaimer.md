# Disclaimer Framework

**Product:** vnstock-advisor  
**Component:** compliance  
**Version:** 1.0  
**Status:** Approved — PM signed off 2026-08-01  
**PM Sign-off:** ✅ Approved by PM (cycle 13)

---

## Purpose

This document defines the mandatory "informational only — not financial advice" disclaimer framework for **vnstock-advisor**. It specifies:
1. Exact disclaimer text (VN/EN)
2. Mandatory placement rules (every suggestion surface)
3. Localization strategy
4. Implementation requirements for DEV

---

## Disclaimer Text

### Vietnamese (Primary)
```
⚠️ **Thông tin chỉ mang tính chất tham khảo, không phải lời khuyên đầu tư.**

Dữ liệu và phân tích trên vnstock-advisor được cung cấp nhằm mục đích thông tin và nghiên cứu cá nhân. Chúng tôi không đảm bảo tính chính xác, đầy đủ hoặc kịp thời của dữ liệu. Mọi quyết định đầu tư dựa trên thông tin này đều do bạn tự chịu rủi ro. Vui lòng tham khảo ý kiến chuyên gia tài chính độc lập trước khi đầu tư.
```

### English (Secondary)
```
⚠️ **Information for reference only — not financial advice.**

Data and analysis on vnstock-advisor are provided for informational and personal research purposes only. We do not guarantee the accuracy, completeness, or timeliness of the data. All investment decisions based on this information are at your own risk. Please consult a qualified independent financial advisor before investing.
```

### Short Variant (Space-Constrained UI)
```
⚠️ Tham khảo בלבד — Không phải lời khuyên đầu tư. / Reference only — Not financial advice.
```

---

## Placement Rules (MANDATORY)

### 1. Every Suggestion Surface
**Definition:** Any UI/component that presents:
- Buy/sell/hold signals
- Target prices
- Risk/reward ratios
- Portfolio recommendations
- "Top picks" / "Screened results"
- Algorithmic scores (momentum, value, quality, etc.)
- Backtest-derived suggestions

**Rule:** Disclaimer **must** be visible without scrolling (above the fold) on every such surface.

### 2. Specific Placement Requirements

| Surface Type | Placement | Variant |
|--------------|-----------|---------|
| **Dashboard / Landing** | Top banner, persistent | Full VN + EN (toggle) |
| **Symbol Detail Page** | Below header, above first signal | Full VN (default), EN on locale switch |
| **Screener Results** | Above results table, sticky | Short variant |
| **Portfolio Suggestion** | Inline, before each recommendation block | Short variant |
| **API Response (JSON)** | `disclaimer` field in every response payload | Full VN + EN |
| **Email / Notification** | Footer of every message | Short variant |
| **PDF / Export Report** | Cover page + footer every page | Full VN |
| **Widget / Embed** | Bottom of widget, non-removable | Short variant |

### 3. No Exceptions
- **No A/B testing** without disclaimer
- **No "dismissible"** — user cannot hide
- **No "premium removes disclaimer"** — applies to all tiers
- **Cached pages** must include disclaimer in HTML (not injected via JS only)

---

## Localization Strategy

### Supported Locales
| Locale | Code | Disclaimer Text | Default |
|--------|------|-----------------|---------|
| Vietnamese | `vi-VN` | Full VN (primary) | ✅ |
| English | `en-US` | Full EN | — |

### Implementation
```typescript
// Shared constant (single source of truth)
const DISCLAIMER = {
  'vi-VN': {
    full: `⚠️ **Thông tin chỉ mang tính chất tham khảo, không phải lời khuyên đầu tư.**\n\nDữ liệu và phân tích trên vnstock-advisor được cung cấp nhằm mục đích thông tin và nghiên cứu cá nhân. Chúng tôi không đảm bảo tính chính xác, đầy đủ hoặc kịp thời của dữ liệu. Mọi quyết định đầu tư dựa trên thông tin này đều do bạn tự chịu rủi ro. Vui lòng tham khảo ý kiến chuyên gia tài chính độc lập trước khi đầu tư.`,
    short: `⚠️ Tham khảo בלבד — Không phải lời khuyên đầu tư.`
  },
  'en-US': {
    full: `⚠️ **Information for reference only — not financial advice.**\n\nData and analysis on vnstock-advisor are provided for informational and personal research purposes only. We do not guarantee the accuracy, completeness, or timeliness of the data. All investment decisions based on this information are at your own risk. Please consult a qualified independent financial advisor before investing.`,
    short: `⚠️ Reference only — Not financial advice.`
  }
} as const;

// Usage
function getDisclaimer(locale: 'vi-VN' | 'en-US', variant: 'full' | 'short' = 'full'): string {
  return DISCLAIMER[locale][variant];
}
```

### Locale Detection Priority
1. User preference (account setting)
2. `Accept-Language` header
3. Default: `vi-VN`

---

## API Contract

### Every Suggestion Endpoint Response
```json
{
  "data": { ... },
  "meta": {
    "generated_at": "2026-07-31T08:00:00Z",
    "source": "analysis-engine-v1.2",
    "disclaimer": {
      "vi-VN": "⚠️ Thông tin chỉ mang tính chất tham khảo...",
      "en-US": "⚠️ Information for reference only..."
    }
  }
}
```

### Required Fields
- `meta.disclaimer` object with **both** locales (client chooses)
- `meta.generated_at` — timestamp for freshness
- `meta.source` — model/engine version for traceability

---

## Frontend Implementation (DEV Checklist)

- [ ] **Shared component:** `<Disclaimer locale="vi-VN" variant="full" />`
- [ ] **Layout wrapper:** Auto-injects disclaimer in suggestion routes (HOC or layout.tsx)
- [ ] **Non-dismissible:** No close button, no localStorage hide flag
- [ ] **SSR/SEO:** Disclaimer rendered in initial HTML (not client-only)
- [ ] **Accessibility:** `role="alert"`, `aria-live="polite"`, sufficient contrast
- [ ] **Print/PDF:** Disclaimer included in `@media print` styles
- [ ] **Widget/Embed:** Disclaimer in shadow DOM or iframe (parent cannot strip)

---

## Backend Implementation (DEV Checklist)

- [ ] **Middleware:** Auto-append `meta.disclaimer` to all `/api/v1/suggestions/*` responses
- [ ] **Validation:** Integration test fails if response missing `meta.disclaimer`
- [ ] **Logging:** Audit log every suggestion response (user_id, endpoint, disclaimer_included: true)
- [ ] **Rate limit:** Disclaimer text not counted toward response size limits

---

## Compliance Checklist (QA Gate)

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Disclaimer present on all suggestion pages | Automated crawl (playwright) | 100% pages with suggestion content have disclaimer |
| Disclaimer in API responses | Contract test | All `/suggestions/*` endpoints return `meta.disclaimer` |
| No dismissible/hide mechanism | Code review + manual test | No `onDismiss`, `localStorage.hideDisclaimer`, etc. |
| Both locales available | i18n test | `vi-VN` and `en-US` keys exist in all variants |
| SSR rendered | View source check | Disclaimer text in raw HTML |
| Accessibility | axe-core scan | No violations on disclaimer element |
| Print styles | Manual print preview | Disclaimer visible on printed page |

---

## Legal Notes

1. **Not a substitute for regulated advice:** This disclaimer does not constitute legal compliance for regulated financial advisory activities. If vnstock-advisor evolves to provide personalized advice, engage legal counsel.

2. **Data source attribution:** Disclaimer complements (not replaces) data source ToS requirements (see `docs/research/data-sources.md` — CAFEF/VNDIRECT/Vietstock terms).

3. **Jurisdiction:** Vietnamese law applies. English version is courtesy translation; Vietnamese is authoritative.

4. **Versioning:** Any text change requires PM + Legal sign-off. Track in git history.

---

## Open Questions

1. **Mobile app:** Same rules apply? (Yes — WebView or native must render disclaimer)
2. **Third-party embeds:** If another site embeds our widget, can they style the disclaimer? (No — non-removable, minimum font size 12px, contrast 4.5:1)
3. **Voice/Chat interfaces:** How to surface? (Read full disclaimer at session start + before each suggestion)

---

*Document status: Draft — awaiting PM sign-off. PM to add sign-off line above when approved.*