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
- [tester] vnstock-advisor tasks/vnstock-advisor-15-dev-analysis-engine-security-gate-tester.md (TESTER PASS per lane log metrics/agents/5/tester.md — F1-F4 INFO/LOW) — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-tester.md (superseded — close recommended, no run) — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-4-dev-data-ingest-tester.md (superseded — close recommended, no run) — status: done
- [tester] vnstock-advisor tasks/vnstock-advisor-5c-dev-ranking-tester.md (superseded — close recommended, no run) — status: done
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-data-ingest-ship-gate.md (PR 16 not gated — waiting on DEV fix + TESTER re-run; PRs 13/14 superseded-close) — status: done
- [qa] vnstock-advisor tasks/vnstock-advisor-qa-analysis-engine-ranking-ship-gate.md (QA GO for PR 17 — TECHLEAD APPROVED + TESTER PASS + QA GO on record; PRs 11/15 superseded-close) — status: done
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-use-cases.md — status: done
- [ba] vnstock-advisor tasks/vnstock-advisor-m3-ba-doc-disclaimer.md — status: done
- [cto] vnstock-advisor tasks/vnstock-advisor-m3-cto-stack-record.md — status: done
- [pm] vnstock-advisor tasks/vnstock-advisor-m3-pm-analytics-plan.md — status: done
- [pm] vnstock-advisor tasks/pm-cap-violation-investigation.md — status: ready
- [dev] [json-formatter] tasks/audit-json-formatter.md (note: still blocked on the PR cap freeze #155, no new branch until a merge lifts it) — status: ready

Drain order: TECHLEAD review → TESTER pass → QA go → merge (cap freeze lifts only on merge). TESTER tasks: wait for the branch's TECHLEAD APPROVED before running.

Drain status 2026-08-12 (cycle 6): all 6 PRs (11/13/14/15/16/17) TECHLEAD-APPROVED. PRs 11/13/14/15 superseded-close (identical/subset trees; orchestrator close pending — closing drops the count 6→2). Canonical PR 17 (analysis-engine security-gate, task-15): TESTER PASS + QA GO on record → orchestrator merge next (CI re-checked mechanically at merge). Canonical PR 16 (data-ingest security-gate, task-14): TESTER FAIL (F1 BLOCKING install/run, F2 HIGH DB-down crash, F3–F6) → DEV fix ready (`vnstock-advisor-14-dev-data-ingest-security-gate-fix`) → TESTER re-run → QA GO → merge. Freeze holds (6 > cap 3); only merge/close drops the count.

**Hardening flag (cycle 6):** no authn/z on vnstock-advisor endpoints — TECHLEAD flagged twice (PRs 16/17 records); acceptable only at current tier; must go on the backlog as a hardening task before any public exposure (needs a branch — post-freeze).
