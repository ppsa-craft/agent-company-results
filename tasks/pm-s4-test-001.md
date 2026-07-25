# Task: pm-s4-test-001 — S4 Web UI Tests (Playwright E2E + Vitest Unit)

## Metadata
- **ID**: pm-s4-test-001
- **Role**: TESTER
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1-S4
- **Assignee**: tester-3
- **Depends on**: pm-s4-002 (API Client + Auth + WS), pm-s4-001 (S4 Scaffold)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
S4 Web UI: End-to-End User Flow Tests + Component Unit Tests + Accessibility

## Description
Test the S4 React application: authentication flows, dashboard interactions, real-time signal updates via WebSocket, and accessibility compliance.

## Acceptance Criteria
- [ ] Playwright E2E: login → dashboard → signal selection → real-time update visible
- [ ] Playwright E2E: token refresh during session, logout, session expiry handling
- [ ] Playwright E2E: WebSocket disconnect/reconnect simulation, data consistency
- [ ] Vitest unit tests: auth context, API client hooks, WebSocket hook
- [ ] Accessibility: axe-core scan on all pages, WCAG 2.1 AA compliance
- [ ] Visual regression: Chromatic/Playwright screenshot comparison for key views
- [ ] Performance: Lighthouse CI budgets (LCP < 2.5s, TBT < 200ms, CLS < 0.1)

## Verification
- All tests pass in CI with Playwright trace artifacts on failure
- Accessibility report generated and archived
- Visual regression baseline approved
- Lighthouse scores tracked in CI

## Security Notes
- Test with invalid/expired tokens
- Verify no XSS in signal data rendering (sanitize WebSocket messages)
- CSP headers validated in E2E