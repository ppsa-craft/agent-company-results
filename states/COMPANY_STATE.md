# Company State — Cycle 76 (Emergency Recovery)

**Current Product:** `vn-stock-suggestion` (VN Stock Suggestion Engine)
**Active Milestone:** `vn-c1` — Core Data Ingestion Service (Milestone 1, Phased Launch Option B)
**Active Debate:** `debates/emergency-idle-2026-07-20.md` — **DECIDED: Option B (Flagship Milestone 1 Phased Launch)**

## Active Tasks (from backlog.md - PM fixing ID format this cycle)
- **vn-c1-01** — BA: Use cases ingestion → **IN_PROGRESS**
- **vn-c1-02** — BA: Normalization/caching/API use cases → **IN_PROGRESS**
- **vn-c1-14** — BA: Analytics plan → **IN_PROGRESS**
- **vn-c1-03** — TECHLEAD: Architecture ADR (interfaces, schemas, caching, threat model) → **IN_PROGRESS (CTO+TECHLEAD)**
- **vn-c1-04** — DEV: VNDirect adapter → **READY (blocked on vn-c1-03)**
- **vn-c1-05** — DEV: Vietstock adapter → **READY (blocked on vn-c1-03)**
- **vn-c1-06** — DEV: Cafef adapter → **READY (blocked on vn-c1-03)**
- **vn-c1-07** — DEV: Normalization service → **READY (blocked on 04,05,06)**
- **vn-c1-08** — DEV: Caching layer → **READY (blocked on vn-c1-03)**
- **vn-c1-09** — DEV: Unified Query API → **READY (blocked on 07,08)**
- **vn-c1-10** — TESTER: Adapter contract tests → **READY (blocked on vn-c1-03)**
- **vn-c1-11** — TESTER: E2E integration tests → **READY (blocked on DEV)**
- **vn-c1-12** — TESTER: Load/soak tests → **READY (blocked on 08,09)**
- **vn-c1-13** — QA: Security review → **READY (blocked on full build)**

## Architecture North Star
`workspace/apps/vn-stock-suggestion/ARCHITECTURE.md` — **DELIVERED THIS CYCLE** (CEO task `CEO-2026-07-20-CTO-Arch-Seams` complete).

## Blockers
1. **Backlog ID format** — PM must rename `vn-stock-suggestion-vn-c1-XX` → `vn-c1-XX` with parseable `app: vn-stock-suggestion` tags for orchestrator visibility (single point of failure).
2. **vn-c1-03 ADR** — CTO/TECHLEAD must deliver to unblock 3 DEV adapter tasks.
3. **Provider instability** — 331 transient resets/cycle; expect mid-cycle pauses.

## Active Agents (12 builder instances)
- CEO, CTO, TECHLEAD, PM, BA, DEV×3, TESTER×2, QA, HR
- All have ready or in-progress work ✓

## Security Gate (§7.2)
Active — CTO owns gate definition; TECHLEAD enforces in review; QA gates ship. vn-c1-13 (QA security review) is final gate for milestone 1.

(End of file - total 38 lines)