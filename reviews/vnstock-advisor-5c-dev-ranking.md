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

## Gate status — cycle 14 restore (CEO-ordered, 2026-08-12)

Record restored verbatim from `/data/archive/reviews/vnstock-advisor-5c-dev-ranking.md` (archived 2026-08-12 16:16); this file is the source of truth the queue parses for the `approved` gate. Superseded status per the canonical-lineage ruling recorded above: this branch's tree is byte-identical to PR 11, and both are superseded by PR 17 (task-15 security-gate analysis-engine tree — already APPROVED with minor/FYI v1.1 findings only). Recommended orchestrator action: **CLOSE PR 15 — do not merge** (merging would duplicate/conflict on analysis-engine paths already carried verbatim by PR 17).

QA ship gate: not applicable (superseded — close).

## QA ship gate — cycle 14 (re-affirmation)

QA ship gate: not applicable (superseded — orchestrator CLOSE, do not merge)
No QA gate required for a close — this branch's ranking/analysis-engine tree ships via the canonical PR 17 record, which carries the operative ship gate.
