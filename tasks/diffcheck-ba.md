# Task: Business Analysis for diffcheck

**Goal:** Create use cases, user stories, and BA docs for diffcheck — a private, local-only text diff tool.

**Acceptance criteria:**
- [x] Use cases / user stories documented in `tasks/diffcheck-use-cases.md`
- [x] BA docs (problem statement, target user, success criteria) documented in `tasks/diffcheck-ba-docs.md`
- [x] Use cases are complete, testable, and traceable to features
- [x] BA docs are debated (§5.1) before build starts — **DECIDED 2026-07-12: approved as-is**
- [x] Analytics plan documented (what to measure, how success is judged)

**Verification:**
- [x] Use cases cover all core functionality
- [x] Each use case has clear acceptance criteria
- [x] BA docs include problem statement, target user, success criteria
- [x] Analytics plan identifies key metrics

**Dependencies:** None (can start immediately)

**Files likely touched:**
- `tasks/diffcheck-use-cases.md` (new file)
- `tasks/diffcheck-ba-docs.md` (new file)

**Estimated scope:** Small (1-2 files)

**DoD tier:** Tier 1 (Product launch — full artifact table)

**Notes:**
- Problem: Developers need to compare text snippets quickly without ad-heavy online tools
- Target user: Developers, writers, anyone who needs to compare text
- Core features: paste two texts, see line-by-line diff, highlight additions/deletions/changes
- Success criteria: tool is used, positive feedback, solves real pain point
- Consider: local-only (no data leaves browser), no accounts needed, fast performance