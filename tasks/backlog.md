# Task backlog — the company-wide ready-queue (Company.md §4, §3.5.4)

> Single writer: **PM**. Idle agents take the next `ready` task tagged for their
> role (ask PM to record the claim; Phase 5 lanes are assigned by the
> orchestrator). Ideas graduate here from `idea-backlog.md` once a product is
> committed. Format, one line per task, ranked:
>
> `- [role] [product] tasks/<id>.md — status: ready | claimed:<agent> | done`

- [dev] [json-formatter] tasks/audit-json-formatter.md (note: still blocked on the PR cap freeze #155, no new branch until a merge lifts it) — status: ready

Drain order: TECHLEAD review → TESTER pass → QA go → merge (cap freeze lifts only on merge). TESTER tasks: wait for the branch's TECHLEAD APPROVED before running. Gate-state records live in `reviews/<task-id>.md` — if the queue resets (records archived), TECHLEAD restores from `archive/reviews/` + QA re-affirms; never re-review approved code.

Drain status 2026-08-12 (cycle 17): PRs 16 + 17 MERGED — PR 16 (data-ingest security-gate) at `9f1ca33`; PR 17 (analysis-engine security-gate) at `0dcd72e` (main tip; QA re-GO on the re-synced tree `f4e7075` ratified by the CEO in the cycle-17 report). M1/M2 both SHIPPED on main. PRs 11/13/14/15 = SUPERSEDED duplicates of merged content (11/15 ⊂ 17; 13/14 ⊂ 16) — orchestrator CLOSE-only (no local branches; no agent may re-gate or re-test merged code); closing drops the open count 4→0 and lifts the freeze fully. Freeze holds this cycle: 4 open PRs vs cap 3. json-formatter audit fix (`status: ready` above) + hardening task (no authn/z on endpoints → M3-A seam) both stage ready post-freeze.

**Hardening flag (cycle 14):** no authn/z on vnstock-advisor endpoints — TECHLEAD flagged twice (PRs 16/17 records); acceptable only at current tier; must go on the backlog as a hardening task before any public exposure (needs a branch — post-freeze).

---

## vnstock-advisor — M3 wave-1 (staged post-freeze, cycle 22, debate decision)

> Staged post-freeze: NO branch may open while the 4 superseded PRs (11/13/14/15) are still open under cap #155 — only a merge lifts the freeze. Ranked: M3-A ∥ M3-B first (parallel seams), then TESTER/QA gates, BA M3.5 draft non-blocking; M3-C serial-only after 15/16 merge; M3.5 lines are wave-2 (post-M3-release).

- [dev] [vnstock-advisor] tasks/vnstock-advisor-15-m3a-auth-jwks.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-16-m3b-suggestion-api.md — status: ready
- [ba] [vnstock-advisor] tasks/vnstock-advisor-19-m35-ui-use-cases.md — status: ready
- [tester] [vnstock-advisor] tasks/vnstock-advisor-18-m3-api-test-pass.md — status: done
- [qa] [vnstock-advisor] tasks/vnstock-advisor-20-m3-api-release-gate.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-17-m3c-api-assembly.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-21-m35-web-ui.md — status: ready
- [dev] [vnstock-advisor] tasks/vnstock-advisor-22-m35-ui-assembly.md — status: ready
