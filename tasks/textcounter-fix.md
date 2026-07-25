# Task: textcounter-fix — Fix blockers from TECHLEAD review

**Goal:** Fix 3 major blockers and 2 minor issues from TECHLEAD review of textcounter-dev.

**Acceptance criteria:**
- [ ] Add debounce (150-300ms) to input handler for performance — avoid recalculating on every keystroke
- [ ] Improve sentence counting regex or document limitation prominently:
  - Current regex fails on abbreviations (e.g., "Dr. Smith", "U.S.A."), decimal numbers, ellipsis
  - Fix regex OR add prominent "Known Limitations" section in README with concrete examples
- [ ] Add `package.json` with name, version, scripts (test, build), and devDependencies
- [ ] Fix reading time format consistency:
  - Current: "1 min read", "2 mins read" (inconsistent pluralization)
  - Fix to consistent format (e.g., "1 min", "2 mins" or "1 minute", "2 minutes")
- [ ] Fix copy-paste test error in `textcounter.test.js` line 125:
  - Test "whitespace only" calls `countSentences('   ')` instead of `countParagraphs('   ')`
  - Fix test to call correct function

**Verification:**
- [ ] Debounce implemented and verified (no calculation on every keystroke)
- [ ] Sentence counting improved OR limitation documented with examples in README
- [ ] `package.json` exists with valid scripts and devDependencies
- [ ] Reading time format is consistent across all values
- [ ] Test line 125 calls `countParagraphs` not `countSentences`
- [ ] All existing tests still pass
- [ ] Build works via `npm run build`
- [ ] Tests pass via `npm test`

**Dependencies:** textcounter-dev.md (completed implementation in `workspace/apps/textcounter/`)

**Files likely touched:**
- `workspace/apps/textcounter/index.html` (input handler debounce)
- `workspace/apps/textcounter/js/counter.js` (sentence counting, reading time format)
- `workspace/apps/textcounter/tests/textcounter.test.js` (test fix line 125)
- `workspace/apps/textcounter/package.json` (new file)
- `workspace/apps/textcounter/README.md` (if documenting sentence counting limitation)

**Estimated scope:** Small (1-3 files)

**DoD tier:** Tier 3 (Fix / maintenance)

**Notes:**
- Priority: Assign to dev-instance-1 after diffcheck-fix completes
- DoD Tier 3: failing-test-first fix + changelog + README if run steps changed
- Add changelog entry in `CHANGELOG.md` (create if not exists)
- For sentence counting: if fixing regex, add test cases for abbreviations/decimals; if documenting, make limitation prominent in README "Known Limitations" section with examples like "Dr. Smith counted as 2 sentences"
- Debounce: 150-300ms recommended; avoid blocking rapid typing feel
- package.json: include `name`, `version`, `scripts: {test, build}`, `devDependencies` (esbuild, jest/vitest)