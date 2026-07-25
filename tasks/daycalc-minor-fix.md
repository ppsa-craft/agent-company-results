# Task: Minor Fix for daycalc

**Goal:** Fix the negative diff wording in daycalc.

**Acceptance criteria:**
- [ ] Fix line 40 in `workspace/apps/daycalc/js/main.js`
- [ ] Current: `${diff} day(s) between ${start} and ${end}` — confusing for negative diffs
- [ ] Fix to show proper wording for negative values (e.g., "5 days before" or "-5 days → 5 days before")
- [ ] Test the fix works correctly

**Verification:**
- [ ] Tool works in browser without any server
- [ ] Negative diff shows clear, non-confusing wording
- [ ] Positive diff still works correctly
- [ ] README instructions work verbatim in clean checkout
- [ ] Tests pass

**Dependencies:** daycalc-dev.md (done)

**Files likely touched:**
- `workspace/apps/daycalc/js/main.js` (line 40)

**Estimated scope:** Tiny (1 line change)

**DoD tier:** Tier 3 (Fix DoD — failing-test-first fix + changelog + README if run steps changed)

**Notes:**
- The issue: when start date > end date, diff is negative (e.g., -5), and the text reads "-5 day(s) between 2025-01-10 and 2025-01-05" which is confusing
- Fix: Show absolute value with clear direction (e.g., "5 days before" or "5 days earlier")
- Update CHANGELOG.md with the fix