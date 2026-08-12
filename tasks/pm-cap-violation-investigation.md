# PM — cap-violation investigation + lesson (#160)

- **App:** vnstock-advisor (the violation is on flagship branches) | **DoD tier:** 3 (process/lesson work, no code) | **Assignee:** _ready_
- **Goal:** Identify which agent opened a task branch in-session DESPITE the PR-cap freeze (a lane queue cannot do this by itself — some agent created/opened a branch), and record the §7.3 lesson so it cannot recur. Branch stays; cap is not optional.
- **Background:** Debate file `debates/emergency-idle-2026-08-12.md` line 14 flags: "a task branch was opened in-session DESPITE the freeze (lane queue cannot do this) → find which agent, record lesson." Two of the 6 open PRs (13 `vnstock-advisor-4-dev-data` / 14 `vnstock-advisor-4-dev-data-ingest`) look like a duplicate pair opened ~simultaneously by different authors (`ingest` vs `dev`) — a likely violation locus. This is claimable by PM during the freeze: reads logs/reports, writes a lesson; no branch.

## Acceptance criteria

1. Investigation performed: trace branch creation + authorship from `logs/`, `workspace/reports/` (cycle reports 2026-08-10..12), orchestrator artifacts, and the PR metadata in `.orchestrator/pr-queue.json`/`state.json` (author fields, openedAt, title mismatches).
2. Culprit named (or "unresolvable — evidence insufficient" honestly stated with what IS known) in the task output.
3. Dated lesson appended to `lessons/dev.md` (and `lessons/pm.md` note if PM's own breakdown contributed) per §7.3, `- YYYY-MM-DD — what happened → why wrong → what to do next time`.
4. If PR 13/14 are confirmed duplicates, flag for CEO/TECHLEAD whether closing the superseded one as hygiene (not cap-gaming) is appropriate.

## Implementation Plan (for PM)

- Read `logs/orchestrator.log`, `logs/debug-trace.log`, recent cycle reports for 2026-08-10..12, and the PR metadata (author fields: `ingest` vs `dev`, `openedAt` within 3s of each other for PR 13/14).
- Cross-check against the freeze chronology in `debates/emergency-idle-2026-08-12.md` and decision #160.
- Record the lesson; report findings + recommendation to CEO.

## Test Plan (verification of the lesson loop)

1. Lesson is dated, concrete, and actionable — not a platitude ("don't open branches during a freeze" without the how-to-prevent).
2. If a duplicate PR is confirmed, the CEO's decision to close/keep it is recorded in the cycle report.
3. No branch was created or pushed by this task (cap absolute).

**Report to CEO at task end:** culprit + evidence, lesson written, duplicate-PR recommendation, status.
