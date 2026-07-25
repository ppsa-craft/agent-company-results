# Task: diffcheck-fix — Critical bug fixes for diffcheck

**Goal:** Fix critical blockers identified by TECHLEAD review: UI rendering bug (wrong property names), dead code, missing performance guard.

**Acceptance criteria:**
- [ ] Fix UI rendering bug: update `main.js` to use correct property names from diff algorithm:
  - `change.value` → `change.line` for added, removed, and equal lines
  - `change.old` → `change.oldLine` and `change.new` → `change.line` for changed lines
- [ ] Remove dead code: delete the unused `escapeHtml` function (lines 83-87 in main.js)
- [ ] Add performance guard: implement a line count limit (e.g., 10,000 lines total) with a warning message when exceeded, and disable the Compare button until text is reduced
- [ ] Add failing test that reproduces the UI rendering bug (TDD approach): create a test that verifies diff output renders correctly when given change objects with correct property names
- [ ] Update changelog entry (create `CHANGELOG.md` if not exists) documenting the fix

**Verification:**
- [ ] Existing diff algorithm tests still pass (6/6)
- [ ] New failing test passes after fix
- [ ] Manual verification: diffcheck UI renders diffs correctly for sample inputs (add, remove, change, equal)
- [ ] Performance guard triggers appropriately for large inputs
- [ ] Dead code removed (no unused `escapeHtml` function)
- [ ] Changelog entry added

**Dependencies:** diffcheck-dev.md (existing implementation)

**Files likely touched:**
- `workspace/apps/diffcheck/js/main.js`
- `workspace/apps/diffcheck/tests/` (new test file or addition)
- `workspace/apps/diffcheck/CHANGELOG.md` (new file)

**Estimated scope:** Small (1-3 files)

**DoD tier:** Tier 3 (Fix / maintenance)

**Notes:**
- This is a priority fix — dev-instance-1 should stop other work and focus on this task first
- Follow TDD: write failing test first, then fix code to make it pass
- Ensure all user-provided content is rendered via `textContent` (safe) — no innerHTML with dynamic content
- Performance guard should be user-friendly (clear warning, not just console.error)
- Consider adding a note about performance limitations in README if not already present