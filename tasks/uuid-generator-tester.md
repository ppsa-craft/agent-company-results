# Task: Testing for uuid-generator

**Goal:** Test uuid-generator — generate UUIDs (v4, v5) with one-click copy.

**Acceptance criteria:**
- [ ] Test cases documented in `tasks/uuid-generator-test-cases.md`
- [ ] Functional testing: UUID v4 generation
- [ ] Functional testing: UUID v5 generation
- [ ] Functional testing: copy to clipboard
- [ ] Functional testing: UUID format validation
- [ ] UI testing: responsive design, usability
- [ ] Cross-browser testing: Chrome, Firefox, Safari
- [ ] Test report with pass/fail status
- [ ] Defects documented with reproduction steps

**Verification:**
- [ ] All test cases executed
- [ ] Core functionality works correctly
- [ ] UI is responsive and usable
- [ ] No critical defects remain
- [ ] Test report is complete

**Dependencies:** uuid-generator-dev.md, review-all-products.md

**Files likely touched:**
- `tasks/uuid-generator-test-cases.md`
- `tasks/uuid-generator-test-report.md`

**Estimated scope:** Small (1-2 files)

**DoD tier:** Tier 1 (Product launch — full artifact table)

**Notes:**
- Load test-engineer persona
- Load browser-testing-with-devtools skill
- Test UUID v4 format (128-bit random)
- Test UUID v5 format (namespace + name)
- Test copy to clipboard functionality
- Test responsive design on different screen sizes
- Document any defects found