# Use Cases / User Stories: diffcheck

## Overview

This document contains user stories and use cases for diffcheck, a private, local-only text diff tool. Each user story follows the format: "As a [role], I want [feature] so that [benefit]." Acceptance criteria define testable conditions for completion.

## Epic 1: Text Input

### US-1.1: Paste Text into Input Areas
**As a developer, I want to paste code snippets into two separate text areas so that I can compare them quickly.**

**Acceptance Criteria:**
1. Two distinct text areas are clearly labeled (e.g., "Original Text" and "Changed Text")
2. Text can be pasted via keyboard shortcut (Ctrl+V / Cmd+V) or right-click menu
3. Pasted text retains original formatting (line breaks, indentation)
4. Text areas expand vertically to accommodate content (up to maximum height)
5. Scrollbars appear when content exceeds visible area
6. Maximum text size limit is clearly communicated (if any)

**Test Scenarios:**
- Paste single line text
- Paste multi-line text with formatting
- Paste large text (>1000 lines)
- Paste empty text
- Paste text with special characters

### US-1.2: Type/Edit Text in Input Areas
**As a writer, I want to type or edit text directly in the text areas so that I can make adjustments before comparing.**

**Acceptance Criteria:**
1. Text areas are editable and support standard text editing operations
2. Undo/redo functionality works within each text area (Ctrl+Z / Ctrl+Y)
3. Tab key inserts tab character or spaces (configurable)
4. Line numbers are displayed for reference
5. Current line is highlighted
6. Auto-scroll follows cursor position

**Test Scenarios:**
- Type new text from scratch
- Edit existing text
- Undo/redo operations
- Tab indentation
- Line number accuracy

### US-1.3: Clear Text Areas
**As a user, I want to clear the text areas with a single action so that I can start a new comparison quickly.**

**Acceptance Criteria:**
1. "Clear" button(s) are visible and accessible for each text area
2. Clearing one area does not affect the other
3. Confirmation dialog appears if text is present (optional, configurable)
4. Clear action is reversible via undo (within session)
5. Clear button has appropriate hover/focus states

**Test Scenarios:**
- Clear single text area
- Clear both text areas
- Clear with confirmation dialog
- Clear then undo
- Clear with large text

## Epic 2: Diff Calculation

### US-2.1: Compare Two Texts
**As a user, I want to click a "Compare" button to see the differences between the two texts.**

**Acceptance Criteria:**
1. "Compare" button is prominent and clearly labeled
2. Comparison starts immediately upon click (or with minimal delay)
3. Progress indicator appears for large texts (if comparison takes > 100ms)
4. Results are displayed without page refresh
5. Button is disabled during comparison to prevent duplicate requests
6. Error handling for empty inputs or identical texts

**Test Scenarios:**
- Compare two different texts
- Compare identical texts
- Compare empty texts
- Compare very large texts (>5000 lines)
- Click compare multiple times rapidly

### US-2.2: View Line-by-Line Diff
**As a developer, I want to see which lines were added, removed, or changed so that I can understand the differences at a glance.**

**Acceptance Criteria:**
1. Each line from both texts is displayed in the output
2. Lines are aligned where possible (matching lines appear in same row)
3. Added lines (only in second text) are highlighted in green
4. Deleted lines (only in first text) are highlighted in red
5. Changed lines (exist in both but differ) are highlighted in yellow
6. Line numbers from original texts are displayed
7. Unchanged lines have no highlighting (or subtle background)
8. Total number of changes is displayed

**Test Scenarios:**
- Compare texts with additions only
- Compare texts with deletions only
- Compare texts with modifications only
- Compare texts with mixed changes
- Compare texts with no changes
- Verify line alignment

### US-2.3: Handle Large Texts Efficiently
**As a user working with large files, I want the tool to handle texts with thousands of lines without crashing or freezing.**

**Acceptance Criteria:**
1. Tool remains responsive for texts up to 10,000 lines
2. Memory usage stays within reasonable limits (< 100MB)
3. Comparison completes within 1 second for typical texts (< 1,000 lines)
4. Virtual scrolling or pagination for very large outputs (if needed)
5. User is warned if input exceeds recommended size
6. Performance degrades gracefully with very large inputs

**Test Scenarios:**
- Compare 100-line texts (should be instant)
- Compare 1,000-line texts (<500ms)
- Compare 5,000-line texts (<2s)
- Compare 10,000-line texts (<5s)
- Monitor memory usage during large comparisons

## Epic 3: Diff Visualization

### US-3.1: Color-Coded Differences
**As a user, I want differences highlighted with distinct colors so that I can quickly identify what changed.**

**Acceptance Criteria:**
1. Additions (lines only in second text) are green (#d4edda or similar)
2. Deletions (lines only in first text) are red (#f8d7da or similar)
3. Modifications (lines that differ but exist in both) are yellow (#fff3cd or similar)
4. Unchanged lines have no highlighting (or subtle #f8f9fa background)
5. Color contrast meets accessibility standards (WCAG AA - 4.5:1 ratio)
6. Colors are distinguishable for color-blind users (use patterns/icons in addition)

**Test Scenarios:**
- Verify color coding for each change type
- Test color contrast with accessibility tools
- Test with color-blind simulation
- Verify colors in dark mode

### US-3.2: Inline Word Diff
**As a developer reviewing code, I want to see exactly which words changed within modified lines.**

**Acceptance Criteria:**
1. Within changed lines, individual word differences are highlighted
2. Added words are highlighted in a lighter green (#c3e6cb)
3. Removed words are highlighted in a lighter red (#f5c6cb)
4. Word diff does not obscure the overall line diff
5. Word boundaries are correctly identified (whitespace, punctuation)
6. Toggle option to show/hide word-level diff

**Test Scenarios:**
- Compare lines with single word change
- Compare lines with multiple word changes
- Compare lines with punctuation changes
- Compare lines with whitespace changes
- Toggle word diff on/off

### US-3.3: Expand/Collapse Unchanged Sections
**As a user comparing long documents, I want to collapse unchanged sections so that I can focus on the differences.**

**Acceptance Criteria:**
1. Unchanged sections of 3+ lines can be collapsed with a click
2. Collapsed sections show "..." or line count indicator (e.g., "15 unchanged lines")
3. Collapsed sections can be expanded again
4. Total number of changes is displayed prominently
5. Collapse/expand all sections option available
6. Collapsed state persists during session

**Test Scenarios:**
- Collapse single unchanged section
- Expand collapsed section
- Collapse all unchanged sections
- Verify line count accuracy
- Test with many small unchanged sections

## Epic 4: Privacy & Security

### US-4.1: Local-Only Processing
**As a user handling sensitive information, I want all comparisons to happen in my browser so that my data never leaves my device.**

**Acceptance Criteria:**
1. No network requests are made during or after text input
2. No data is stored in cookies, local storage, or session storage (unless user explicitly enables)
3. Browser's developer tools show no outgoing requests related to diff functionality
4. Privacy statement is visible (optional but recommended)
5. No analytics that transmit text content
6. Tool works offline after initial load

**Test Scenarios:**
- Monitor network requests during use
- Check browser storage for text content
- Verify offline functionality
- Inspect privacy policy (if present)

### US-4.2: No Account Required
**As a user, I want to use the tool immediately without creating an account or logging in.**

**Acceptance Criteria:**
1. No login/signup forms are present
2. No prompts to create accounts
3. No functionality is gated behind authentication
4. Tool is fully functional on first visit
5. No third-party authentication integrations
6. No prompts to save progress or create accounts

**Test Scenarios:**
- First visit experience
- No login prompts
- Full functionality without accounts
- No third-party redirects

## Epic 5: User Interface

### US-5.1: Responsive Design
**As a mobile user, I want the tool to work well on my phone or tablet so that I can compare texts on the go.**

**Acceptance Criteria:**
1. Layout adapts to screen size (mobile, tablet, desktop)
2. Text areas stack vertically on small screens (<768px)
3. Buttons and controls are touch-friendly (minimum 44px touch target)
4. No horizontal scrolling required on mobile
5. Text remains readable without zooming
6. Virtual keyboard doesn't obscure input areas

**Test Scenarios:**
- Test on iPhone SE (375px)
- Test on iPad (768px)
- Test on desktop (1920px)
- Test landscape orientation
- Test with virtual keyboard open

### US-5.2: Keyboard Shortcuts
**As a power user, I want keyboard shortcuts to speed up common actions.**

**Acceptance Criteria:**
1. Ctrl+Enter / Cmd+Enter triggers comparison
2. Escape clears results or closes any modals
3. Tab moves between text areas
4. Shortcuts are discoverable (help menu or tooltip)
5. Shortcuts don't conflict with browser defaults
6. Shortcut list accessible via ? key or menu

**Test Scenarios:**
- Test all documented shortcuts
- Verify no browser conflicts
- Test shortcut discoverability
- Test on different operating systems

### US-5.3: Dark Mode Support
**As a user who works late, I want a dark mode option to reduce eye strain.**

**Acceptance Criteria:**
1. Toggle switch for light/dark mode
2. Preference persists across sessions (localStorage)
3. Color coding remains clear and accessible in both modes
4. Smooth transition between modes (CSS transition)
5. System preference detection (prefers-color-scheme)
6. All UI elements have appropriate dark mode styles

**Test Scenarios:**
- Toggle dark mode on/off
- Verify persistence across page reloads
- Test color accessibility in dark mode
- Test system preference detection
- Verify all elements have dark styles

## Epic 6: Results Management

### US-6.1: Copy Diff Results
**As a user, I want to copy the diff results to clipboard so that I can share them elsewhere.**

**Acceptance Criteria:**
1. "Copy" button available for diff results
2. Copied text includes line numbers and change indicators
3. Format is readable as plain text
4. Clipboard API used (with fallback for older browsers)
5. Visual feedback when copy succeeds/fails
6. Copy includes only visible results (respecting collapsed sections)

**Test Scenarios:**
- Copy single change
- Copy multiple changes
- Copy with collapsed sections
- Test clipboard permissions
- Test on mobile devices

### US-6.2: Share Diff Results (Optional)
**As a user, I want to generate a shareable link to the diff results so that I can send them to colleagues.**

**Acceptance Criteria:**
1. "Share" button generates a URL with encoded diff (if feasible)
2. URL contains all necessary data to reconstruct the diff
3. No server-side storage required
4. URL length is reasonable (consider compression)
5. Shared view is read-only
6. Privacy warning when sharing sensitive content

**Test Scenarios:**
- Generate shareable link
- Open shared link in new browser
- Verify no server requests
- Test URL length limits
- Test with large diffs

## Traceability Matrix

| User Story | Feature | Acceptance Criteria | Test Coverage |
|------------|---------|-------------------|---------------|
| US-1.1 | Text Input | Paste functionality | Manual testing |
| US-1.2 | Text Input | Edit functionality | Manual testing |
| US-1.3 | Text Input | Clear functionality | Manual testing |
| US-2.1 | Diff Calculation | Compare button | Automated tests |
| US-2.2 | Diff Calculation | Line-by-line diff | Automated tests |
| US-2.3 | Diff Calculation | Performance | Performance tests |
| US-3.1 | Diff Visualization | Color coding | Visual testing |
| US-3.2 | Diff Visualization | Word diff | Manual testing |
| US-3.3 | Diff Visualization | Collapse sections | Manual testing |
| US-4.1 | Privacy | Local processing | Network monitoring |
| US-4.2 | Privacy | No accounts | Manual testing |
| US-5.1 | UI | Responsive design | Cross-browser testing |
| US-5.2 | UI | Keyboard shortcuts | Manual testing |
| US-5.3 | UI | Dark mode | Visual testing |
| US-6.1 | Results | Copy functionality | Manual testing |
| US-6.2 | Results | Share functionality | Manual testing |

## Priority Matrix

| Priority | User Stories | Rationale |
|----------|--------------|-----------|
| P0 (Must Have) | US-1.1, US-2.1, US-2.2, US-3.1, US-4.1, US-4.2 | Core functionality - tool doesn't work without these |
| P1 (Should Have) | US-1.2, US-1.3, US-2.3, US-3.2, US-5.1 | Important for usability and performance |
| P2 (Nice to Have) | US-3.3, US-5.2, US-5.3, US-6.1 | Enhances user experience |
| P3 (Future) | US-6.2 | Optional advanced feature |

## Dependencies

1. **Tech Stack Decision** — Final implementation depends on CTO's stack decision
2. **Diff Algorithm** — Choice of algorithm affects performance and accuracy
3. **Browser APIs** — Clipboard API availability affects copy functionality
4. **Accessibility Standards** — WCAG compliance affects color choices

## Open Questions

1. Should we support file drag-and-drop for text input?
2. Should we add syntax highlighting for code comparisons?
3. Should we support regex-based ignore patterns?
4. Should we add a unified diff view (in addition to side-by-side)?
5. Should we integrate with browser extensions for developer tools?

## Assumptions

1. Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
2. Users can copy/paste text
3. Primary use case is line-by-line comparison (not character-level)
4. No need for version history or saving comparisons
5. No integration with other tools (git, IDE) needed
6. Tool will be hosted as a static site (no server-side processing)
7. Text input is manual (no API integrations)