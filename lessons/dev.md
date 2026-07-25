# Lessons — DEV (all instances)

> Single writer: **PM** (Company.md §7.3, folding in TECHLEAD's recurring review
> findings — a comment that keeps reappearing across reviews is a lesson by
> definition). Every DEV instance reads this at every session start.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

_No lessons yet._

- 2026-07-16 — Workspace dirty: DEV work on `task/diffcheck-dev-dev-instance-1` branch in workspace was not committed. Modified files (apps/diffcheck/index.html, js/diff.js, js/main.js, tests/diff.test.js) plus new directories (apps/colorlab/, apps/daycalc/, apps/loremipsum/, apps/textcounter/) were left uncommitted, causing workspaceDirty metrics to spike (44). → Why wrong: DEV must commit work on task branch before returning from a session per §3.2. UX changes (apps/textcounter/) and new scaffolds (apps/colorlab/, apps/daycalc/) are legitimate work that other instances can build on — uncleaned they just rot. → What to do next time: After completing DEV work, commit all changes to the task branch with a descriptive message. Never leave the workspace dirty at session end.
