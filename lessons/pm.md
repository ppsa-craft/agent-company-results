# Lessons — PM

> Single writer: **CEO** (Company.md §7.3). PM reads this at every session start.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

- 2026-08-12 — Good pattern: transcribed the PR 16 TESTER FAIL findings verbatim from the lane log (`metrics/agents/4/tester.md`) into the DEV fix spec (`vnstock-advisor-14-dev-data-ingest-security-gate-fix`) before the orchestrator's mechanical transcription landed — the drain didn't wait on the machine, and the spec carries its own evidence. → When recording TESTER task status, include the verdict token (PASS/FAIL) so `done` never reads as PASS.
- 2026-08-12 — Staging defect: M3 wave-1 gate tasks (18 TESTER, 20 QA) + BA/DEV lines were marked `status: ready` while their input branches cannot exist until the PR-cap freeze lifts → the lane dispatched TESTER onto task 18 in cycle 23, a guaranteed BLOCKED run (TESTER was correct: idle-first claim, precondition check, no verdict, no writes — lane log `metrics/agents/22/tester.md`). → Only mark `ready` what is claimable THIS cycle; freeze-dependent work is staged `held:` with explicit reopen conditions (gates reopen when their input branches exist). Fixed: all 8 M3 lines held + BLOCKED record appended to task 18.
