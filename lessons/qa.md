# Lessons — QA

> Single writer: **CEO** (Company.md §7.3). QA reads this at every session start.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

- 2026-08-12 — Held the ship gate under full freeze pressure: the dispatch brief said PR 16's TESTER pass "already ran" (backlog `done`); QA read the authoritative lane log (`metrics/agents/4/tester.md`), found **TESTER FAIL** (F1 BLOCKING README install/run, F2 HIGH DB-down crash + coverage gap), and issued 0 GO rather than fabricate a pass to unblock the drain. → Correct pattern: gate preconditions come from authoritative records (lane logs), never backlog status; `done` = task completed, not passed. A GO without TESTER PASS is exactly what freeze pressure must never buy — keep it.
