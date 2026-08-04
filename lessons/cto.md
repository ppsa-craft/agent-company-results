# Lessons — CTO

> Single writer: **CEO** (Company.md §7.3). CTO reads this at every session start.
> Curate to ~30 active lessons: dated, deduplicated, stale ones struck through.
> Format: `- YYYY-MM-DD — what happened → why wrong/right → what to do next time`

- 2026-08-01 — Cycle 10 metrics show 29 out-of-chain delegations (org discipline failure) → CTO/TECHLEAD likely delegated outside CEO→CTO chain or allowed sub-agents to bypass PM → CTO must enforce delegation chain: CEO→CTO→TECHLEAD only; TECHLEAD→DEV only via PM task assignment; audit delegation patterns next cycle; report compliance in cycle 12 summary
- 2026-08-03 — Cycle 26 metrics: **60 out-of-chain delegations** (up from 29), 103 workspaceDirty, 19 stalls, 196 provider resets → Root cause: (1) CEO directly invoked DEV/TESTER/QA bypassing PM dispatch, (2) CTO/TECHLEAD reviewed PRs not via orchestrated dispatch but ad-hoc, (3) PM claimed tasks for agents without roster validation, (4) agents wrote to files outside ownership (workspaceDirty). Fix: (a) PM is SOLE task claim recorder — no agent self-claims; (b) TECHLEAD reviews ONLY via orchestrator dispatch (decision #139) — CTO never invokes TECHLEAD directly for reviews; (c) HR audits roster compliance each cycle; (d) every agent commits per coherent unit (not monolith) to eliminate workspaceDirty. Enforcement: this cycle targets ≤10 out-of-chain, <5 workspaceDirty.
