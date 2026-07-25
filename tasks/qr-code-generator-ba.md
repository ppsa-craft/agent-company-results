# Task: Business Analysis for qr-code-generator

**Goal:** Create use cases, user stories, and BA docs for qr-code-generator — generate QR codes for text/URLs with one-click copy/download, client-side only.

**Acceptance criteria:**
- [ ] Use cases / user stories documented in `tasks/qr-code-generator-use-cases.md`
- [ ] BA docs (problem statement, target user, success criteria) documented in `tasks/qr-code-generator-ba-docs.md`
- [ ] Use cases are complete, testable, and traceable to features
- [ ] BA docs are debated (§5.1) before build starts
- [ ] Analytics plan documented (what to measure, how success is judged)

**Verification:**
- [ ] Use cases cover all core functionality (text/URL input, QR generation, size options, download, copy)
- [ ] Each use case has clear acceptance criteria
- [ ] BA docs include problem statement, target user, success criteria
- [ ] Analytics plan identifies key metrics

**Dependencies:** None (can start immediately — new product, client-side only)

**Files likely touched:**
- `tasks/qr-code-generator-use-cases.md` (new file)
- `tasks/qr-code-generator-ba-docs.md` (new file)
- `workspace/analytics/qr-code-generator.md` (new file)

**Estimated scope:** Small (1-2 files)

**DoD tier:** Tier 1 (Product launch — full artifact table)

**Notes:**
- Problem: Need QR codes for links, contact info, WiFi; existing tools are ad-heavy, track usage, or require accounts
- Target user: Developers, marketers, event organizers, anyone sharing links/credentials
- Core features: text/URL input, QR code generation (qrcode.js), size/error correction options, PNG/SVG download, copy image to clipboard, dark/light mode
- Success criteria: tool generates valid QR codes instantly, works offline, zero tracking, used for real sharing scenarios
- Consider: qrcode.js or @zawgn/qrcode (ESM), canvas to blob for download, clipboard API for copy, preset types (URL, text, email, phone, WiFi, vCard)
- **BA Analysis:** Use cases and BA docs to be created. Ready for PM debate (§5.1) before build starts.
- **Analytics Plan:** Included in BA docs with metrics for generations, content types used, download vs copy, error correction level usage.