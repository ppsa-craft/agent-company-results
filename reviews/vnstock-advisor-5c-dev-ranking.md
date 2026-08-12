# Code Review: vnstock-advisor-5c-dev-ranking

- Task: vnstock-advisor-5c-dev-ranking (ranking slice)
- Branch: `task/vnstock-advisor-5c-dev-ranking-dev`
- PR: 15 (https://github.com/ppsa-craft/agent-company-results/pull/15)
- DEV: dev
- Date: 2026-08-12
- Reviewer: TECHLEAD

## Round 1 — TECHLEAD comments

**Superseded branch (canonical-lineage ruling, cycle 231).** This branch's tree
is byte-identical to `task/vnstock-advisor-5-dev-analysis-engine-dev` (PR11) —
`git diff --stat origin/task/vnstock-advisor-5-dev-analysis-engine-dev
origin/task/vnstock-advisor-5c-dev-ranking-dev` is EMPTY. Both are superseded by
the canonical analysis-engine tree on `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev`
(PR17), which carries this analysis-engine subtree verbatim plus the security
gate, docs, and the data-ingest service. No further comment rounds are
warranted for this branch — its content lives on in PR17.

## Scope check (§6.2, decision #133)

CLEAN — `git diff --name-only origin/main...origin/<branch>` contains ZERO files
outside `apps/` (verified 2026-08-12).

## CI note

CI status unknown (ci: none per pr-queue.json 2026-08-12 16:06; orchestrator ship gate mechanically re-checks CI at merge time).

## Supersession evidence

- `git diff --stat origin/task/vnstock-advisor-5-dev-analysis-engine-dev origin/task/vnstock-advisor-5c-dev-ranking-dev` → empty (identical trees).
- PR17's analysis-engine subtree is blob-identical to this branch's analysis-engine files.

## Verdict

APPROVED — identical tree to PR11, superseded by task-15 (PR17) per canonical-lineage ruling; recommend orchestrator close PR 15.
