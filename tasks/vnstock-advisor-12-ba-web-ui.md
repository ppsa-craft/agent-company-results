# Task: vnstock-advisor-12-ba-web-ui

**Role:** BA
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: web-ui use cases + UX specs)
**Status:** ready

---

## Goal

Produce BA documentation for `web-ui` service: use cases, user flows, component design, disclaimer placement, responsive breakpoints, and accessibility requirements.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Use case document: `workspace/apps/vnstock-advisor/docs/use-cases/web-ui.md` covering:
  - UC-WUI-1: Unauthenticated user lands on homepage, sees disclaimer, can view public market overview
  - UC-WUI-2: Authenticated user logs in via JWT (redirect to suggestion-api `/auth/login`), sees personalized dashboard
  - UC-WUI-3: User views ranked suggestions with reasoning cards (symbol, score, indicator breakdown, disclaimer)
  - UC-WUI-4: User filters suggestions (by sector, market cap, score range)
  - UC-WUI-5: User views symbol detail page with chart (price + indicators) and full reasoning
  - UC-WUI-6: Responsive layout works on mobile (375px), tablet (768px), desktop (1440px)
- [ ] UI/UX specification: `workspace/apps/vnstock-advisor/docs/specs/ui-ux.md` — wireframe descriptions, component hierarchy, state management (TanStack Query + Zustand), color palette (Tailwind), typography
- [ ] Component design: `workspace/apps/vnstock-advisor/docs/specs/components.md` — reusable components (SuggestionCard, ReasoningBadge, DisclaimerBanner, ChartWrapper, FilterBar, LoadingSkeleton, ErrorBoundary)
- [ ] Disclaimer integration: exact placement rules per `docs/compliance/disclaimer.md` — banner on every suggestion surface, footer on all pages, VN/EN localization
- [ ] Accessibility spec: `workspace/apps/vnstock-advisor/docs/specs/accessibility.md` — WCAG 2.1 AA targets, keyboard navigation, ARIA labels, color contrast, focus management
- [ ] All docs reviewed and approved by PM

---

## Implementation Plan (for BA)

1. Define use cases with actors, preconditions, postconditions, error flows
2. Design user flows (auth, suggestions list, symbol detail, filtering)
3. Specify component hierarchy and reusable component props
4. Define responsive breakpoints and Tailwind color palette
5. Specify disclaimer placement on every suggestion surface (header banner + card footer + page footer)
6. Define accessibility requirements (WCAG 2.1 AA)
7. Get PM sign-off

---

## Test Plan (for TESTER)

**Scenario: Use case completeness**
- Steps: Verify each UC has actor, precondition, postcondition, error flow
- Expected: No gaps; all suggestion surfaces include disclaimer mandate

**Scenario: Component spec completeness**
- Steps: Verify each component has props, states (loading/error/empty), accessibility props
- Expected: All components specified; DisclaimerBanner has VN/EN variants

**Scenario: Accessibility spec**
- Steps: Verify WCAG 2.1 AA criteria mapped to components
- Expected: Color contrast ratios, keyboard flows, ARIA patterns documented

---

## Dependencies

- `vnstock-advisor-2-ba-data-ingest` (needs disclaimer framework)
- `vnstock-advisor-11-ba-suggestion-api` (needs API contract for integration points)
- Output feeds: `vnstock-advisor-14-dev-web-ui-scaffold`, `vnstock-advisor-16-dev-web-ui-core`, future TESTER/QA tasks