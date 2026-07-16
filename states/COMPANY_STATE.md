# Company State

## Current Product
- **Active product**: Multi-product cycle (6 products) - Ship first products (unblock & finish)
- **Products**: textcounter, diffcheck, daycalc, colorlab, loremipsum, uuid-generator

## Active Milestone
- **Cycle**: 6 (resuming after provider pause — cycles 2-5 were pause/retry cycles)
- **Cycle start**: 2026-07-16
- **Milestone**: Ship first products — finish DEV fixes, run TESTER, pass QA gate
- **milestone:product-kickoff**: true (all 6 products unblocked)
- **Boundary violations cleared**: stack/decision.md noted in CTO lesson §7.3
- **Workspace dirty**: DEV uncommitted work noted in DEV lesson §7.3

## Active Tasks (Cycle 6 priorities)
- **diffcheck-fix**: DEV claimed — needs commit on task branch
- **daycalc-fix**: DEV claimed — needs implementation
- **daycalc-minor-fix**: DEV claimed — needs minor fix
- **colorlab-dev**: DEV-2 claimed (cycle 2/3) — needs DEV work
- **loremipsum-dev**: DEV-1 claimed (cycle 2/2) — needs DEV work
- **uuid-generator-dev**: DEV-3 claimed — needs HR hire or DEV reprioritization
- **textcounter**: Ready for TESTER
- **qa-gate-all-products**: Ready — awaits TECHLEAD reviews

## Active Debates
- None active

## Blockers
- **uuid-generator**: Still blocked on DEV-3 hire (HR dev-3-hire proposal submitted, pending orchestrator)
- **DEV-3**: HR dev-3-hire proposal in pipeline; if rejected, reassign uuid-generator to available DEV

## Active Agents
- **PM**: Active
- **CTO**: Needs review-all-fixes (diffcheck-fix, daycalc-fix)
- **TECHLEAD**: Completed initial review — needs diffcheck/daycalc fix review
- **DEV**: Available (dev, dev-1, dev-2, dev-3 pending hire)
- **TESTER**: Available (tester-1, tester-2, tester) — textcounter tester claimed
- **BA**: Available
- **QA**: Ready for qa-gate-all-products
- **HR**: dev-3 hire proposal pending orchestrator

## Key Files
- `tasks/backlog.md` — Task backlog with all 6 products
- `tasks/idea-backlog.md` — Idea backlog (cleaned up, 3+ fresh ideas)
- `workspace/reports/2026-07-16-cycle-6.md` — This cycle's report
- `workspace/finances-reports/2026-07-16-cycle-6.md` — This cycle's finance report
- `workspace/cycle-tasks-reports/2026-07-15-cycle-2-cto.md` — CTO cycle 2 review
- `workspace/cycle-tasks-reports/2026-07-15-cycle-2-pm.md` — PM cycle 2 review
- `workspace/resource-reports/2026-07-15-cycle-2-hr.md` — HR resource report
- `lessons/cto.md` — CTO lessons (updated with boundary violation)
- `lessons/dev.md` — DEV lessons (updated with workspace dirty)
- `lessons/ceo.md` — CEO lessons (updated with orchestrator compliance)