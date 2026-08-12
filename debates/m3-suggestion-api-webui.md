# M3 Debate — Suggestion API + Web UI — 2026-08-12 (cycle 22)

## Trigger (Company.md §7.1: big, expensive-to-reverse milestone → debate with CTO + PM before committing)

- M1 (data-ingest `9f1ca33`) + M2 (analysis-engine+ranking `0dcd72e`) SHIPPED on main, security-gated.
- M3 = idea-backlog rank #1: suggestion API + web UI. Staging COMPLETE (BA use cases incl. `docs/use-cases/suggestion-api.md` UC-SA-1..5, compliance disclaimer framework, CTO stack-record seams M3-A/M3-B/M3-C/M3-D, PM analytics plan) — pending this §5.1 debate to lock the build plan.
- Freeze-safe: a debate opens no branch, claims no task; its outcome lets PM open M3 tasks the cycle the PR-cap freeze lifts.

## Question

**What is the M3 build plan — slicing, ordering, and first-release scope — for the suggestion API + web UI, given the security gate (no authn/z on endpoints today; TECHLEAD flagged twice), the frozen `/rank` contract, and the parallel-build mandate?**

## Options (proposals requested from CTO + PM)

- **Option A — Auth-first sequential:** M3-A (auth + hardening, JWT RS256 per UC-SA-2) alone → then M3-B (suggestions) → M3-D (web-ui) → M3-C (assembly). Smallest risk, slowest to a runnable end-to-end demo.
- **Option B — Parallel seams:** M3-A + M3-B + M3-D build in parallel on the frozen contracts; M3-C assembly serial last. Fastest end-to-end; depends on seams holding (CTO stack record's claimed seams).
- **Option C — API-only first release:** ship the suggestion API (M3-A + M3-B + minimal M3-C) as the M3 milestone; defer web-ui to M3.5. Narrowest first release; defers the widest surface.

## Criteria (decision rubric §7.3 + owner mandates)

1. **Security gate first-class:** M3-A (authn/z) is not optional — TECHLEAD flagged twice; no public exposure without it.
2. **Parallelization:** many agents build in parallel; every live role has ready work (owner efficiency mandate).
3. **Reuse:** build on the frozen data-ingest / analysis-engine `/rank` contracts and the disclaimer framework; leave reusable assets for M4/M5.
4. **Milestone shippable on its own:** M3 as a whole must be README-runnable end-to-end with the full DoD artifact set + §7.2 security gate.
5. **Token-efficiency:** fewest review/gate round-trips; don't gold-plate.

## Decision (CEO, after proposals — cycle 22, 2026-08-12)

**Winner: Option C amended (PM) — API-first release with parallel seams; web-ui deferred to M3.5.** Both proposals converged on the core: M3-A (auth+hardening) ∥ M3-B (suggestions) build in parallel in wave 1, M3-C assembly serial last, contracts pinned first. The split was web-ui timing — CTO's amended B put M3-D in wave 2 of M3; PM's amended C makes M3.5. Adopted PM's:

- **Why:** (1) security gate runs on a small API surface and auth ships in release 1; (2) two DEV seams stay parallel while the PR cap (#155) demands SMALL merges — two small gates beat one giant gate at M3-C; (3) the API release is README-runnable (curl) alone with a full DoD artifact set; (4) UI is not built against an unassembled backend (cheapest-to-reverse, rubric 4); (5) every role has ready work in wave 1 (BA drafts M3.5 UI use cases).
- **Mandatory amendment (adopted from PM, matches TECHLEAD's twice-flagged gap):** M3-A authn/z applies to ALL existing endpoints (M1 ingest, M2 rank), not just the new `/suggestions` surface. PM to amend UC-SA-2 scope accordingly at sign-off.
- **CTO seam risks adopted as implementation requirements:** ① resolve the `/rank` weights-override schema at freeze (BA-flagged — top gate; fallback to Option C's narrower scope if it can't freeze in one round); ② pin the auth middleware interface (guard signature/header/error format) so M3-B builds before M3-A lands; ③ rate-limiting is cross-cutting middleware owned by M3-A, consumed by M3-B; ④ disclaimer text comes from `compliance/disclaimer.md` single source — M3-B exposes via API, M3.5 UI renders from data, never re-implements.

**Staged task breakdown (PM opens the cycle the freeze lifts — no branch before):**
- Wave 1 (parallel): `[dev] vnstock-advisor-15-m3a-auth-jwks` (Tier 2, app-wide authn/z + hardening); `[dev] vnstock-advisor-16-m3b-suggestion-api` (Tier 2, GET /suggestions + disclaimer + RFC 7807); `[ba] vnstock-advisor-19-m35-ui-use-cases` (M3.5 UI drafting, non-blocking); `[tester] vnstock-advisor-18-m3-api-test-pass`; `[qa] vnstock-advisor-20-m3-api-release-gate`.
- Serial: `[dev] vnstock-advisor-17-m3c-api-assembly` (Tier 1, after 15/16 merge — curl README, full artifact table).
- Wave 2 (M3.5): `[dev] vnstock-advisor-21-m35-web-ui` → `vnstock-advisor-22-m35-ui-assembly` + TESTER pass + QA gate.
- Pre-build gate: BA contract-pin snapshot (endpoint shapes, auth flow, RFC 7807 bodies, weights-override) before any DEV opens M3-D.

## Dissents

- **CTO (amended B):** would keep M3-D (web-ui) inside M3 in wave 2, overlapping A/B review-fix cycles, for the fastest full end-to-end demo. Not adopted — under the PR cap the smaller first release is the safer ship, and M3.5 follows immediately; CTO's seam risks are nonetheless all adopted as requirements above.
