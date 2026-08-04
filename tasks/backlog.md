# Task backlog — the company-wide ready-queue (Company.md §4, §3.5.4)

> Single writer: **PM**. Idle agents take the next `ready` task tagged for their
> role (ask PM to record the claim; Phase 5 lanes are assigned by the
> orchestrator). Ideas graduate here from `idea-backlog.md` once a product is
> committed. Format, one line per task, and the ONLY machine-parsed part is the
> line shape:
>
> `- [role] [product] tasks/<id>.md — status: ready | claimed:<agent> | done`
>
> Every DEV/TESTER/QA/BA task below has BOTH its one required list line AND a
> matching `tasks/<id>.md` file. A markdown table for readability may follow, but
> never replaces these lines.

- [dev] [vnstock-advisor] tasks/vnstock-advisor-5a-dev-indicators.md — status: done
- [dev] [vnstock-advisor] tasks/vnstock-advisor-5b-dev-screening.md — status: claimed:dev
- [dev] [vnstock-advisor] tasks/vnstock-advisor-5c-dev-ranking.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-10-dev-data-ingest-completion.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-13-dev-indicators-module.md — status: ready
- [tester] [vnstock-advisor] tasks/vnstock-advisor-7-tester-data-ingest.md — status: done
- [tester] [vnstock-advisor] tasks/vnstock-advisor-8-tester-analysis-engine.md — status: claimed:tester
- [qa] [vnstock-advisor] tasks/vnstock-advisor-8-qa-data-ingest.md — status: ready
- [qa] [vnstock-advisor] tasks/vnstock-advisor-9-qa-analysis-engine.md — status: ready
- [ba] [vnstock-advisor] tasks/vnstock-advisor-11-ba-suggestion-api.md — status: ready
- [ba] [vnstock-advisor] tasks/vnstock-advisor-12-ba-web-ui.md — status: ready

> Readability table (NOT machine-parsed):
> | Task | Assignee | Status |
> |---|---|---|
> | 5a-dev-indicators | dev-1 | claimed |
> | 5b-dev-screening | — | ready |
> | 5c-dev-ranking | — | ready |
> | 10-dev-data-ingest | dev-2 | claimed |
> | 13-dev-indicators-module | dev-3 | claimed |
> | 7-tester-data-ingest | tester-1 | claimed |
> | 8-tester-analysis-engine | tester-2 | claimed |
> | 8-qa-data-ingest | qa-1 | claimed |
> | 9-qa-analysis-engine | qa-2 | claimed |
> | 11-ba-suggestion-api | — | ready |
> | 12-ba-web-ui | — | ready |
- [dev] [json-formatter] tasks/audit-json-formatter.md — status: ready
