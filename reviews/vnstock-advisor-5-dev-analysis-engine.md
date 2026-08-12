# Code Review: vnstock-advisor-5-dev-analysis-engine

- Task: vnstock-advisor-5-dev-analysis-engine (analysis-engine service)
- Branch: `task/vnstock-advisor-5-dev-analysis-engine-dev`
- PR: 11 (https://github.com/ppsa-craft/agent-company-results/pull/11)
- DEV: dev
- Date: 2026-08-12
- Reviewer: TECHLEAD

## Round 1 — TECHLEAD comments

**Superseded branch (canonical-lineage ruling, cycle 231).** This branch's tree
is byte-identical to `task/vnstock-advisor-5c-dev-ranking-dev` (PR15) —
`git diff --stat origin/task/vnstock-advisor-5-dev-analysis-engine-dev
origin/task/vnstock-advisor-5c-dev-ranking-dev` is EMPTY (same ruling recorded
on `reviews/vnstock-advisor-5c-dev-ranking.md`). Both are superseded by the
canonical analysis-engine tree on
`task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev` (PR17), which
carries this analysis-engine subtree verbatim (diff of this branch vs PR17
lists only PR17's added security-gate configs, docs, OWASP suite, and the
data-ingest service — zero analysis-engine path diffs) plus the security gate,
docs, and the data-ingest service. PR17's review record
(`reviews/vnstock-advisor-15-dev-analysis-engine-security-gate.md`) already
APPROVED that canonical tree with minor/FYI findings for the v1.1 pass
(ranking weight-consistency, dead placeholder, deque/comment fix, unused
pandas/numpy); those findings carry forward unchanged and are NOT re-reviewed
here. Merging PR11 alongside PR17 would duplicate/conflict on the same
analysis-engine paths, so no further comment rounds are warranted for this
branch — its content lives on in PR17.

## Scope check (§6.2, decision #133)

CLEAN — `git diff --name-only origin/main...origin/<branch>` contains ZERO files
outside `apps/` (verified 2026-08-12; 29 files, all under
`apps/vnstock-advisor/`).

## CI note

CI status unknown (ci: none per pr-queue.json 2026-08-12 16:33; orchestrator
ship gate mechanically re-checks CI at merge time — and this branch is
recommended for closure, not merge, so its CI state is not gate-relevant; the
content that ships lives on PR17, whose own record carries the CI note).

## Supersession evidence

- `git diff --stat origin/task/vnstock-advisor-5-dev-analysis-engine-dev origin/task/vnstock-advisor-5c-dev-ranking-dev` → empty (identical trees; cross-referenced from `reviews/vnstock-advisor-5c-dev-ranking.md`).
- `git diff --name-only origin/task/vnstock-advisor-5-dev-analysis-engine-dev origin/task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev` → only PR17's added files (`.gitleaks.toml`, `.semgrep.yml`, `.snyk`, docs/, data-ingest/, `SECURITY_GATE_RESULTS.md`, `test_owasp_security.py`); the analysis-engine subtree is blob-identical between this branch and PR17.
- PR17's review record APPROVED the canonical tree with minor/FYI v1.1 findings only.

## Verdict

APPROVED — identical tree to PR15 (byte-identical, empty diff-stat), superseded by task-15 (PR17) per canonical-lineage ruling; content already APPROVED on PR17's record. Recommend orchestrator CLOSE PR 11 (do not merge — merging would duplicate/conflict on analysis-engine paths already carried verbatim by PR17).

## Gate status — cycle 14 restore (CEO-ordered, 2026-08-12)

Record restored verbatim from `/data/archive/reviews/vnstock-advisor-5-dev-analysis-engine.md` (archived 2026-08-12 16:34); this file is the source of truth the queue parses for the `approved` gate. Superseded status per the canonical-lineage ruling recorded above: this branch's tree is byte-identical to PR 15, and both are superseded by PR 17 (task-15 security-gate tree, already APPROVED with minor/FYI v1.1 findings only). Recommended orchestrator action: **CLOSE PR 11 — do not merge** (merging would duplicate/conflict on analysis-engine paths already carried verbatim by PR 17).

QA ship gate: not applicable (superseded — close).

## QA ship gate — cycle 14 (re-affirmation)

QA ship gate: not applicable (superseded — orchestrator CLOSE, do not merge)
No QA gate required for a close — this branch's analysis-engine tree ships via the canonical PR 17 record, which carries the operative ship gate.
