# Task: daycalc-fix — Major fixes for daycalc from TECHLEAD review

**Goal:** Fix 2 major blockers identified by TECHLEAD review: (1) Broken invalid-date error handling in datecalc.js/main.js, (2) Incomplete package.json (missing devDependencies).

## Acceptance criteria:
- [ ] Fix invalid-date error handling consistency:
  - datecalc.js throws `RangeError("Invalid date: please enter a valid date")`
  - main.js catches and shows `"Invalid date format. Please use YYYY-MM-DD."` — messages inconsistent
  - Fix: Align error messages. Option A: Update datecalc.js to throw "Invalid date format. Please use YYYY-MM-DD." OR Option B: Update main.js to show the original error message. Choose Option A for consistency (throw user-friendly message from library).
  - Also fix dayOfWeek bug: line 39 uses `abbrevDays` and `fullDays` but variables are `abbrevDays` (line 38) and `fullDays` (lines 29-37) — these ARE defined correctly. Wait — re-checking: line 39 `return abbreviated ? abbrevDays[dayIndex] : fullDays[dayIndex];` — `abbrevDays` (line 38) and `fullDays` (lines 29-37) both exist. But the CEO said "Broken invalid-date error handling" — the issue is likely the inconsistent error messages between library and UI.
  - Add tests for invalid date inputs in datecalc.test.js (TDD: failing test first)
- [ ] Fix package.json: add `devDependencies` with `vitest` and `esbuild` (required for `npm test` and `npm run build` to work in clean checkout)
- [ ] Update CHANGELOG.md with fix entries

## Verification:
- [ ] Invalid date input shows consistent, user-friendly error message in UI
- [ ] `npm test` passes in clean checkout (devDependencies installed)
- [ ] `npm run build` works (if build script exists — daycalc uses ES modules directly, may not need build)
- [ ] New tests for invalid dates pass
- [ ] Existing tests still pass
- [ ] CHANGELOG.md updated

## Dependencies: daycalc-dev.md (completed), daycalc-minor-fix.md (separate task)

## Files likely touched:
- `workspace/apps/daycalc/js/datecalc.js` (error message consistency)
- `workspace/apps/daycalc/js/main.js` (error handling alignment)
- `workspace/apps/daycalc/tests/datecalc.test.js` (new invalid-date tests)
- `workspace/apps/daycalc/package.json` (add devDependencies)
- `workspace/apps/daycalc/CHANGELOG.md` (new file or update)

## Estimated scope: Small (1-3 files)

## DoD tier: Tier 3 (Fix / maintenance — failing-test-first fix + changelog + README if run steps changed)

## Notes:
- DoD Tier 3: Write failing test for invalid date handling first, then fix code to make it pass
- Error message should be consistent between library (datecalc.js) and UI (main.js)
- package.json devDependencies: at minimum `vitest` for test, `esbuild` if build script kept
- daycalc uses native ES modules (no bundle.js), so build step may not be needed — verify README run steps still work
- The dayOfWeek function variable names (fullDays, abbrevDays) ARE correctly defined — the bug is purely error message inconsistency