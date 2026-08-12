# Task backlog — the company-wide ready-queue (Company.md §4, §3.5.4)

> Single writer: **PM**. Idle agents take the next `ready` task tagged for their
> role (ask PM to record the claim; Phase 5 lanes are assigned by the
> orchestrator). Ideas graduate here from `idea-backlog.md` once a product is
> committed. Format, one line per task, ranked:
>
> `- [role] [product] tasks/<id>.md — status: ready | claimed:<agent> | done`

- [dev] vnstock-advisor tasks/vnstock-advisor-14-dev-data-ingest-security-gate-fix.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-5-dev-analysis-engine-tester.md — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-14-dev-data-ingest-security-gate-tester.md — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-15-dev-analysis-engine-security-gate-tester.md — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-tester.md — status: superseded — close recommended (no run)
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-ingest-tester.md — status: superseded — close recommended (no run)
- [tester] vnstock-advisor tasks/vnstock-advisor-5c-dev-ranking-tester.md — status: superseded — close recommended (no run)
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-data-ingest-ship-gate.md (verdicts 0 GO / 0 NO-GO: PR 16 waiting on DEV fix + TESTER re-run, PRs 13/14 superseded-close) — status: done
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-analysis-engine-ranking-ship-gate.md (verdicts 0 GO / 0 NO-GO: PR 17 waiting on TESTER PASS, PRs 11/15 superseded-close) — status: done
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-use-cases.md — status: done
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-doc-disclaimer.md — status: done
- [cto] vnstock-advisor tasks/vnstock-advisor-m3-cto-stack-record.md — status: done
- [pm] vnstock-advisor tasks/vnstock-advisor-m3-pm-analytics-plan.md — status: done
- [pm] vnstock-advisor tasks/pm-cap-violation-investigation.md — status: ready
- [dev] [json-formatter] tasks/audit-json-formatter.md (note: still blocked on the PR cap freeze #155, no new branch until a merge lifts it) — status: ready

Drain order: TECHLEAD review → TESTER pass → QA go → merge (cap freeze lifts only on merge). TESTER tasks: wait for the branch's TECHLEAD APPROVED before running.

Drain status 2026-08-12 (cycle 5): all 6 PRs (11/13/14/15/16/17) TECHLEAD-APPROVED. PRs 11/13/14/15 are superseded duplicates (identical/subset trees) with TECHLEAD's explicit "recommend orchestrator close" ruling — NO TESTER/QA runs for them (close-candidates, not merges); QA gate verdicts for them: superseded-close (no verdict). Canonical merges: PR 16 (data-ingest security-gate, task-14) + PR 17 (analysis-engine security-gate, task-15). PR 16: TESTER FAIL (F1 BLOCKING install/run, F2 HIGH DB-down crash, F3–F6) → DEV fix task ready (`vnstock-advisor-14-dev-data-ingest-security-gate-fix`), TESTER re-run after. PR 17: TESTER run in flight (claimed:tester). QA ran both gates (0 GO / 0 NO-GO — nothing gateable yet). Merging the two canonical PRs lifts the cap freeze; superseded branches (11/13/14/15) are closed by the orchestrator, not merged.
