# Task: Testing for textcounter

**Goal:** Test textcounter — count words, characters, sentences, paragraphs, reading time.

**Acceptance criteria:**
- [ ] Test cases documented in `tasks/textcounter-test-cases.md`
- [ ] Functional testing: counting accuracy
- [ ] Functional testing: reading time estimation
- [ ] UI testing: responsive design, usability
- [ ] Performance testing: large text handling
- [ ] Cross-browser testing: Chrome, Firefox, Safari
- [ ] Test report with pass/fail status
- [ ] Defects documented with reproduction steps

**Verification:**
- [ ] All test cases executed
- [ ] Core functionality works correctly
- [ ] UI is responsive and usable
- [ ] No critical defects remain
- [ ] Test report is complete

**Dependencies:** textcounter-dev.md, review-all-products.md

**Files likely touched:**
- `tasks/textcounter-test-cases.md`
- `tasks/textcounter-test-report.md`

**Estimated scope:** Small (1-2 files)

**DoD tier:** Tier 1 (Product launch — full artifact table)

**Notes:**
- Load test-engineer persona
- Load browser-testing-with-devtools skill
- Test with various text inputs (empty, single word, paragraphs, large text)
- Test counting accuracy against manual counts
- Test reading time estimation against known values
- Test responsive design on different screen sizes
- Document any defects found