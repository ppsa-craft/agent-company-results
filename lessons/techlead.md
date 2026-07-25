# TECHLEAD Lessons — Cycle 76 (Emergency)

*No prior lessons file existed. Starting fresh from this emergency session.*

## Lessons Learned This Session

1. **Emergency claim protocol**: When CEO declares emergency and assigns a task, CTO/TECHLEAD must immediately claim the task in COMPANY_STATE.md and begin work in the same session. No ceremony.

2. **Architecture-first unblocking**: In a phased launch (Option B), the architecture seam (vn-c1-03) is the critical path. Three DEVs are blocked on vn-c1-03. The ADR + interfaces + threat model must ship in this cycle to unblock 3 DEVs.

3. **Security gate is non-negotiable**: CEO mandated threat model at `docs/arch/threat-model-adapters.md` per security gate (§7.2). Must deliver threat model at `docs/arch/threat-model-adapters.md` alongside ADR.

4. **ADR location**: CEO specified `workspace/apps/vn-stock-suggestion/docs/arch/adr-001-adapter-normalization-caching.md` — must write there, not in `docs/arch/`.

5. **Dual role discipline**: As CTO+TECHLEAD dual-hat, I must produce both the architectural decision record (CTO) AND the concrete interface definitions + threat model (TECHLEAD) in one session.

6. **Parallel unblocking is the leverage**: Unblocking 3 DEVs (vn-c1-04, 05, 06) in parallel is the highest-leverage action this cycle. Architecture seam must be clean enough for parallel implementation.

7. **PM delegation diagnosis first**: When PM breaks, CTO must immediately diagnose delegation infrastructure before any other work. No flag shipping without PM delegation working.

8. **Composite task files rejected**: In this emergency, reject composite task files — every task that straddles multiple dev/test/qa roles gets split into single-role tasks, each with a manageable size (≤100 lines) and an explicit architecture seam boundary.

9. **Recovery over flagship**: In emergencies, rescue idle agents first, then unblock flagship. Quality over process rules demand real work for idle agents, not coordination fluff.

10. **Owner 2026-07-12 mandate**: Every agent must have at least one ready task at cycle start, or be on layoff watch. RESCUE idle agents first, then fix broken pipelines, then unblock flagship.

1. **Emergency claim protocol**: When CEO declares emergency and assigns a task, CTO/TECHLEAD must immediately claim the task in COMPANY_STATE.md and begin work in the same session. No ceremony.

2. **Architecture-first unblocking**: In a phased launch (Option B), the architecture seam (vn-c1-03) is the critical path. Three DEVs are blocked on vn-c1-03. The ADR + interfaces + threat model must ship in this cycle to unblock 3 DEVs.

3. **Security gate is non-negotiable**: CEO mandated threat model at `docs/arch/threat-model-adapters.md` per security gate (§7.2). Must deliver threat model at `docs/arch/threat-model-adapters.md` alongside ADR.

4. **ADR location**: CEO specified `workspace/apps/vn-stock-suggestion/docs/arch/adr-001-adapter-normalization-caching.md` — must write there, not in `docs/arch/`.

5. **Dual role discipline**: As CTO+TECHLEAD dual-hat, I must produce both the architectural decision record (CTO) AND the concrete interface definitions + threat model (TECHLEAD) in one session.

---
*End of Cycle 76 lessons — will append after session completes*