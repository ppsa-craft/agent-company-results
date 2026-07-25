# Task: Implementation for textcounter

**Goal:** Implement textcounter — count words, characters, sentences, paragraphs, reading time.

**Acceptance criteria:**
- [x] Product implemented in `workspace/apps/textcounter/`
- [x] Single HTML file with embedded CSS and JavaScript (or minimal files)
- [x] Text area for input
- [x] Real-time counting of: words, characters, sentences, paragraphs
- [x] Reading time estimate (based on average reading speed)
- [x] Clear display of all counts
- [x] No external dependencies (pure vanilla JS)
- [x] Responsive design for mobile and desktop
- [x] README with how-to-run instructions
- [x] Tests for counting logic

**Verification:**
- [x] Tool works in browser without any server
- [x] Counts are accurate
- [x] Reading time estimate is reasonable
- [x] UI is intuitive and responsive
- [x] README instructions work verbatim in clean checkout
- [x] Tests pass

**Dependencies:** stack-decision.md, textcounter-ba.md

**Files likely touched:**
- `workspace/apps/textcounter/index.html`
- `workspace/apps/textcounter/README.md`
- `workspace/apps/textcounter/tests/`

**Estimated scope:** Small (1-3 files)

**DoD tier:** Tier 1 (Product launch — full artifact table)

**Notes:**
- Follow CTO's tech stack decision
- Use regex or string splitting for counting
- Consider: average reading speed (200-300 words per minute)
- Include clear, real-time updates as user types
- Consider: character count with/without spaces