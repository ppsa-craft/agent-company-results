# BA — M3 BA doc + disclaimer spec (vnstock-advisor)

- **App:** vnstock-advisor | **DoD tier:** 2 (feature — BA docs are quality-gated like code) | **Assignee:** _ready_
- **Goal:** Produce the M3 BA doc (problem statement, target user, success criteria) plus the full disclaimer spec for every suggestion surface. Claimable during the freeze: no branch, no code.
- **Background:** BA docs must be debated (§5.1) before build starts — so the draft must exist BEFORE the freeze lifts. Flagship constraint: every suggestion surface carries a clear "informational only — not financial advice" disclaimer; this task makes that precise enough to test (exact wording, placement, visibility on API + UI).

## Acceptance criteria (BA artifact bars, §7.2)

1. Problem statement, target user, success criteria for M3 — written and recorded as the decided version after the §5.1 debate.
2. Disclaimer spec: exact wording, required placement (API response field/header; UI page location), minimum visibility (e.g., must render before/with any ranked suggestion), testable as acceptance criteria.
3. Written to `tasks/ba-vnstock-advisor-m3-doc.md` (BA-owned file), debate-ready.

## Implementation Plan (for BA)

- Load `spec-driven-development`; follow intent→skill routing.
- Problem statement from the flagship framing in `tasks/idea-backlog.md` rank 3; success criteria measurable (e.g., end-to-end README run produces ranked suggestions with disclaimer).
- Draft the disclaimer spec against both M3 surfaces (API response + web UI) and cross-check the M2 ranking contract for where suggestions first become user-visible.
- Mark debate-ready; PM schedules the §5.1 debate.

## Test Plan (for QA/TESTER validation of the artifact)

1. QA checks BA doc completeness (problem/target/success) — missing success criteria is a finding.
2. Disclaimer spec must be unambiguous enough for TESTER to verify on the shipped product: exact text, exact location, and a visibility rule.
3. Every M3 suggestion surface enumerated in the doc must carry the disclaimer requirement (no orphan surfaces).

**Report to PM at task end:** artifacts written, task status, debate readiness.
