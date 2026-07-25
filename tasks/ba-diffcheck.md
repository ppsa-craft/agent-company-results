# BA Record: diffcheck

## Product Overview
**Product:** diffcheck — private, local-only text diff tool. Paste two texts, see line-by-line diff. No ads, no accounts, no data leaves the browser.

## Problem Statement
Developers and writers constantly need to compare two pieces of text (code, config, prose) to spot differences. Existing solutions are bloated web apps with ads, trackers, account requirements, or send data to servers. There's no simple, privacy-first, zero-dependency tool that runs entirely in the browser.

## Target User
- **Primary:** Developers comparing code snippets, config files, logs
- **Secondary:** Writers/editors comparing document versions
- **Tertiary:** Anyone needing a quick diff without leaving the browser or compromising privacy

## Success Criteria
1. **Privacy-first:** Zero network requests — all diffing happens client-side
2. **Zero dependencies:** Single HTML file, no build step, no npm install
3. **Line-by-line diff:** Side-by-side or unified view with clear add/delete/modify highlighting
4. **Performance:** Handles 10,000+ lines smoothly in browser
5. **Accessibility:** WCAG 2.1 AA compliant (keyboard navigation, color contrast, screen reader labels)
6. **Offline-capable:** Works fully offline after first load (Service Worker optional)
7. **Copy/paste UX:** One-click copy for each diff hunk, "copy all changes" button

## Use Cases / User Stories

| ID | User Story | Acceptance Criteria | Traceability |
|----|------------|---------------------|--------------|
| UC-01 | As a developer, I want to paste two code snippets and see a line-by-line diff so I can spot changes quickly | - Two text areas accept paste/typing<br>- Diff renders in <500ms for 1000 lines<br>- Added lines highlighted green, removed red, modified yellow<br>- Line numbers shown | FEAT-DIFF-01 |
| UC-02 | As a user, I want to switch between side-by-side and unified diff views so I can choose my preferred format | - Toggle button switches view mode<br>- State persists in localStorage<br>- Both views show same diff data | FEAT-DIFF-02 |
| UC-03 | As a privacy-conscious user, I want zero network requests so my data never leaves my browser | - No fetch/XHR/websocket calls on load or diff<br>- No external resources (fonts, CDN, analytics)<br>- Works offline after first load | FEAT-PRIVACY-01 |
| UC-04 | As a keyboard user, I want full keyboard navigation so I can use the tool without a mouse | - Tab navigation between textareas, toggle, copy buttons<br>- Arrow keys navigate diff hunks<br>- Enter/Space activates buttons<br>- Focus indicators visible | FEAT-A11Y-01 |
| UC-05 | As a user, I want to copy individual hunks or all changes so I can apply fixes elsewhere | - "Copy" button per hunk copies unified diff format<br>- "Copy All" copies full unified diff<br>- Toast confirmation on copy | FEAT-COPY-01 |
| UC-06 | As a user on mobile, I want a responsive layout so I can diff on any device | - Side-by-side stacks vertically on <768px<br>- Textareas stack, diff view scrolls horizontally<br>- Touch-friendly tap targets (44px min) | FEAT-RESPONSIVE-01 |
| UC-07 | As a user, I want to clear inputs and start fresh with one click | - "Clear" button empties both textareas and diff view<br>- Focus returns to first textarea | FEAT-CLEAR-01 |

## Traceability Matrix
| Feature | Use Cases | Test Cases (TESTER) |
|---------|-----------|---------------------|
| Core diff algorithm | UC-01 | diffcheck-tester.md TC-01..TC-05 |
| View modes | UC-02 | diffcheck-tester.md TC-06..TC-07 |
| Privacy/offline | UC-03 | diffcheck-tester.md TC-08..TC-10 |
| Accessibility | UC-04 | diffcheck-tester.md TC-11..TC-14 |
| Copy functionality | UC-05 | diffcheck-tester.md TC-15..TC-17 |
| Responsive design | UC-06 | diffcheck-tester.md TC-18..TC-19 |
| Clear/reset | UC-07 | diffcheck-tester.md TC-20 |

## Open Questions for §5.1 Debate
1. **Diff algorithm:** Myers O(ND) vs. simple line-by-line — trade accuracy for code size?
2. **View default:** Side-by-side vs. unified — which default serves more users?
3. **Color scheme:** High-contrast only, or themeable (light/dark)?
4. **Large file handling:** Virtual scrolling vs. simple truncation warning?
5. **Copy format:** Unified diff only, or also side-by-side text?

## Debate Status
- **Status:** Not started
- **Debate file:** `debates/diffcheck-ba.md` (to be created)
- **Decision owner:** PM (BA docs debated per §5.1 before build)
- **Participants:** BA (proposer), CTO (technical), PM (business), TECHLEAD (review)

## BA Artifacts Delivered
- [x] Problem statement
- [x] Target user
- [x] Success criteria
- [x] Use cases / user stories (complete, testable, traceable)
- [x] Traceability matrix
- [ ] §5.1 debate initiated
- [ ] §5.1 debate concluded
- [ ] BA docs approved (PM sign-off post-debate)