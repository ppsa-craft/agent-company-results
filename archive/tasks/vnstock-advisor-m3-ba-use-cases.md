# BA — M3 use cases: suggestion API + web UI (vnstock-advisor)

- **App:** vnstock-advisor | **DoD tier:** 2 (feature — BA artifacts are quality-gated like code) | **Assignee:** _ready_
- **Goal:** Produce complete, testable, traceable use cases / user stories for the M3 milestone (suggestion API + web UI) so DEV can start against them the moment the PR freeze lifts — and TESTER/QA have acceptance scenarios NOW. Claimable during the freeze: no branch, no code.
- **Background:** M3 = idea-backlog rank 3: ranked suggestions with reasoning + disclaimer, README-runnable end-to-end. Builds on data-ingest (M1) + analysis-engine/ranking (M2) contracts. Flagship constraint: **every suggestion surface must carry a clear "informational only — not financial advice" disclaimer** (BA doc requirement). These use cases feed tasks `vnstock-advisor-m3-dev-*` (staged post-freeze).

## Acceptance criteria (BA artifact bars, §7.2)

1. Complete: covers the API surfaces (suggestions list w/ reasoning, disclaimer, error handling) and the web surfaces (list view, detail view, disclaimer visibility) of M3.
2. Testable: every use case has concrete, checkable acceptance criteria (not prose vibes).
3. Traceable: every M3 feature maps to a use case; no orphans (flag any feature without a use case, any use case without acceptance criteria).
4. Written to `tasks/ba-vnstock-advisor-m3.md` (BA-owned file), ready for the §5.1 debate before M3 build starts.

## Implementation Plan (for BA)

- Load `spec-driven-development` skill; follow intent→skill routing in AGENTS.md.
- Derive surfaces from the flagship constraint + M2 contracts (analysis-engine output shape, ranking contract) — read the workspace tree `apps/vnstock-advisor/` and `tasks/stack-vnstock-advisor.md` if CTO has produced the M3 section (else note the dependency and use the M1/M2 stack record).
- Draft use cases; explicitly include failure-path use cases (invalid symbols, empty universe, API errors surfaced in UI), not just happy paths — QA gates on both flows.
- Record draft in `tasks/ba-vnstock-advisor-m3.md`; flag the debate-ready marker for PM to schedule the §5.1 debate.

## Test Plan (for QA/TESTER validation of the artifact)

1. QA checks use cases against the three bars (complete/testable/traceable) — a use case that can't be turned into a test step is a finding.
2. Every use case must name its surface (API endpoint or UI view) and its good-flow + failure-flow acceptance.
3. The disclaimer requirement must appear as an acceptance criterion on EVERY suggestion surface.

**Report to PM at task end:** artifacts written, task status, orphans flagged, debate readiness.
