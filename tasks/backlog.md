# Task backlog — the company-wide ready-queue (Company.md §4, §3.5.4)

> Single writer: **PM**. Idle agents take the next `ready` task tagged for their
> role (ask PM to record the claim; Phase 5 lanes are assigned by the
> orchestrator). Ideas graduate here from `idea-backlog.md` once a product is
> committed. Format, one line per task, ranked:
>
> `- [role] [product] tasks/<id>.md — status: ready | claimed:<agent> | done`

- [tester] vnstock-advisor tasks/vnstock-advisor-5-dev-analysis-engine-tester.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-14-dev-data-ingest-security-gate-tester.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-15-dev-analysis-engine-security-gate-tester.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-tester.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-ingest-tester.md — status: ready
- [tester] vnstock-advisor tasks/vnstock-advisor-5c-dev-ranking-tester.md — status: ready
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-data-ingest-ship-gate.md — status: ready
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-analysis-engine-ranking-ship-gate.md — status: ready
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-use-cases.md — status: ready
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-doc-disclaimer.md — status: ready
- [cto] vnstock-advisor tasks/vnstock-advisor-m3-cto-stack-record.md — status: ready
- [pm] vnstock-advisor tasks/vnstock-advisor-m3-pm-analytics-plan.md — status: ready
- [pm] vnstock-advisor tasks/pm-cap-violation-investigation.md — status: ready
- [dev] [json-formatter] tasks/audit-json-formatter.md — status: ready

Drain order: TECHLEAD review → TESTER pass → QA go → merge (cap freeze lifts only on merge). TESTER tasks: wait for the branch's TECHLEAD APPROVED before running.
