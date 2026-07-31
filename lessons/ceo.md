# Lessons — CEO

> Writers: **CEO (self)** + **owner** (Company.md §7.3). The only self-written
> lessons file, kept honest by the code-computed KPIs in `metrics/`.
> Entries marked `[OWNER]` come from the owner — NEVER prune or contradict them.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

- 2026-07-31 — CTO and PM agents completed complex task invocations but returned empty output (no task result content) → agent prompt handling issue for multi-step prompts → validate agent outputs immediately after each delegation; if empty, re-delegate with simpler prompt or do the work directly as CEO; escalate to HR if persistent