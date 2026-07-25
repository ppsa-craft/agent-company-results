# BA Docs: diffcheck

## Problem Statement

Developers, writers, and other professionals frequently need to compare two pieces of text to identify differences—whether reviewing code changes, comparing document versions, or verifying content modifications. Existing online diff tools often suffer from:

- **Ad-heavy interfaces** that distract and slow down the workflow
- **Privacy concerns** as text content is uploaded to external servers
- **Performance issues** with large text inputs
- **Account requirements** for basic functionality
- **Complex UIs** that obscure the core comparison task

The diffcheck product solves this by providing a **private, local-only text diff tool** that runs entirely in the browser, with no data leaving the user's machine.

## Target User

### Primary Users
1. **Software Developers** — comparing code snippets, reviewing pull requests locally, debugging differences between versions
2. **Technical Writers** — comparing document drafts, identifying changes between revisions
3. **Content Editors** — comparing text versions for publishing workflows
4. **Quality Assurance Engineers** — comparing expected vs. actual output
5. **Students and Educators** — comparing assignments, solutions, or reference materials

### User Characteristics
- Comfortable with basic web interfaces
- Often work with text-heavy content
- Value privacy and speed over advanced features
- May use the tool frequently throughout the day
- Need quick, one-off comparisons without setup overhead

## Success Criteria

### Functional Success
1. **Diff Accuracy** — The tool correctly identifies additions, deletions, and changes with 100% accuracy for line-by-line comparisons
2. **Performance** — Handles texts up to 10,000 lines without noticeable lag (< 500ms for comparison)
3. **Cross-Browser Support** — Works consistently in Chrome, Firefox, Safari, and Edge (latest 2 versions)
4. **Responsive Design** — Usable on mobile devices (phones and tablets) as well as desktops
5. **Zero Dependencies** — No external libraries, frameworks, or CDN requirements

### User Experience Success
1. **Intuitive Interface** — New users can perform a diff within 30 seconds of opening the tool
2. **Clear Visualization** — Differences are immediately apparent through color coding and line highlighting
3. **Copy/Paste Friendly** — Easy to input text via paste, typing, or file upload (optional)
4. **No Friction** — No accounts, no ads, no pop-ups, no redirects

### Business Success
1. **Adoption** — Tool is used regularly by target users (measured by return visits)
2. **Satisfaction** — Positive feedback from users (measured via optional feedback mechanism)
3. **Retention** — Users return to the tool for future comparisons
4. **Word-of-Mouth** — Users recommend the tool to others

## Features & Use Cases

### Feature 1: Text Input
**Description:** Two separate text areas for pasting or typing the texts to compare.

#### Use Cases / User Stories

**UC-1.1: Input Text via Paste**
- *As a developer, I want to paste code snippets into two separate text areas so that I can compare them quickly.*
- **Acceptance Criteria:**
  1. Two distinct text areas are clearly labeled (e.g., "Original Text" and "Changed Text")
  2. Text can be pasted via keyboard shortcut (Ctrl+V / Cmd+V) or right-click menu
  3. Pasted text retains original formatting (line breaks, indentation)
  4. Text areas expand vertically to accommodate content (up to maximum height)
  5. Scrollbars appear when content exceeds visible area

**UC-1.2: Input Text via Typing**
- *As a writer, I want to type or edit text directly in the text areas so that I can make adjustments before comparing.*
- **Acceptance Criteria:**
  1. Text areas are editable and support standard text editing operations
  2. Undo/redo functionality works within each text area
  3. Tab key inserts tab character or spaces (configurable)
  4. Line numbers are displayed for reference

**UC-1.3: Clear Text Areas**
- *As a user, I want to clear the text areas with a single action so that I can start a new comparison quickly.*
- **Acceptance Criteria:**
  1. "Clear" button(s) are visible and accessible
  2. Clearing one area does not affect the other
  3. Confirmation dialog appears if text is present (optional, configurable)

### Feature 2: Diff Calculation
**Description:** Line-by-line comparison algorithm that identifies additions, deletions, and changes.

#### Use Cases / User Stories

**UC-2.1: Compare Two Texts**
- *As a user, I want to click a "Compare" button to see the differences between the two texts.*
- **Acceptance Criteria:**
  1. "Compare" button is prominent and clearly labeled
  2. Comparison starts immediately upon click (or with minimal delay)
  3. Progress indicator appears for large texts (if comparison takes > 100ms)
  4. Results are displayed without page refresh

**UC-2.2: View Line-by-Line Diff**
- *As a developer, I want to see which lines were added, removed, or changed so that I can understand the differences at a glance.*
- **Acceptance Criteria:**
  1. Each line from both texts is displayed in the output
  2. Lines are aligned where possible (matching lines appear in same row)
  3. Added lines are highlighted in green
  4. Deleted lines are highlighted in red
  5. Changed lines are highlighted in yellow (or different color for added/removed within line)
  6. Line numbers from original texts are displayed

**UC-2.3: Handle Large Texts**
- *As a user working with large files, I want the tool to handle texts with thousands of lines without crashing or freezing.*
- **Acceptance Criteria:**
  1. Tool remains responsive for texts up to 10,000 lines
  2. Memory usage stays within reasonable limits (< 100MB)
  3. Comparison completes within 1 second for typical texts (< 1,000 lines)
  4. Virtual scrolling or pagination for very large outputs (if needed)

### Feature 3: Diff Visualization
**Description:** Clear visual representation of differences with color coding and highlighting.

#### Use Cases / User Stories

**UC-3.1: Color-Coded Differences**
- *As a user, I want differences highlighted with distinct colors so that I can quickly identify what changed.*
- **Acceptance Criteria:**
  1. Additions (lines only in second text) are green
  2. Deletions (lines only in first text) are red
  3. Modifications (lines that differ but exist in both) are yellow
  4. Unchanged lines have no highlighting (or subtle background)
  5. Color contrast meets accessibility standards (WCAG AA)

**UC-3.2: Inline Word Diff**
- *As a developer reviewing code, I want to see exactly which words changed within modified lines.*
- **Acceptance Criteria:**
  1. Within changed lines, individual word differences are highlighted
  2. Added words are highlighted in a lighter green
  3. Removed words are highlighted in a lighter red
  4. Word diff does not obscure the overall line diff

**UC-3.3: Expand/Collapse Sections**
- *As a user comparing long documents, I want to collapse unchanged sections so that I can focus on the differences.*
- **Acceptance Criteria:**
  1. Unchanged sections can be collapsed with a click
  2. Collapsed sections show "..." or line count indicator
  3. Collapsed sections can be expanded again
  4. Total number of changes is displayed somewhere visible

### Feature 4: Privacy & Security
**Description:** All processing occurs locally in the browser with no data transmission.

#### Use Cases / User Stories

**UC-4.1: Local Processing**
- *As a user handling sensitive information, I want all comparisons to happen in my browser so that my data never leaves my device.*
- **Acceptance Criteria:**
  1. No network requests are made during or after text input
  2. No data is stored in cookies, local storage, or session storage (unless user explicitly enables)
  3. Browser's developer tools show no outgoing requests related to diff functionality
  4. Privacy statement is visible (optional but recommended)

**UC-4.2: No Account Required**
- *As a user, I want to use the tool immediately without creating an account or logging in.*
- **Acceptance Criteria:**
  1. No login/signup forms are present
  2. No prompts to create accounts
  3. No functionality is gated behind authentication
  4. Tool is fully functional on first visit

### Feature 5: User Interface
**Description:** Clean, intuitive interface that focuses on the core comparison task.

#### Use Cases / User Stories

**UC-5.1: Responsive Layout**
- *As a mobile user, I want the tool to work well on my phone or tablet so that I can compare texts on the go.*
- **Acceptance Criteria:**
  1. Layout adapts to screen size (mobile, tablet, desktop)
  2. Text areas stack vertically on small screens
  3. Buttons and controls are touch-friendly (minimum 44px touch target)
  4. No horizontal scrolling required on mobile

**UC-5.2: Keyboard Shortcuts**
- *As a power user, I want keyboard shortcuts to speed up common actions.*
- **Acceptance Criteria:**
  1. Ctrl+Enter / Cmd+Enter triggers comparison
  2. Escape clears results or closes any modals
  3. Tab moves between text areas
  4. Shortcuts are discoverable (help menu or tooltip)

**UC-5.3: Dark Mode**
- *As a user who works late, I want a dark mode option to reduce eye strain.*
- **Acceptance Criteria:**
  1. Toggle switch for light/dark mode
  2. Preference persists across sessions (localStorage)
  3. Color coding remains clear and accessible in both modes
  4. Smooth transition between modes

## Analytics Plan

### What to Measure

#### Usage Metrics
1. **Page Views** — Number of times the tool is accessed
2. **Session Duration** — Time spent on the tool per visit
3. **Comparisons per Session** — Number of diff operations performed
4. **Return Visits** — Percentage of users who return within 7/30 days
5. **Device/Browser Distribution** — Usage across platforms

#### Performance Metrics
1. **Comparison Time** — Time to calculate diff for various input sizes
2. **Input Size Distribution** — Typical text lengths (lines/characters)
3. **Error Rates** — Any JavaScript errors or failed comparisons
4. **Load Time** — Time to interactive for the page

#### User Experience Metrics
1. **Feature Usage** — Which features are used most (clear, word diff, collapse)
2. **Abandonment Rate** — Users who leave without performing a comparison
3. **Mobile vs Desktop Usage** — Platform preference
4. **Scroll Depth** — How far users scroll in results

### How to Measure

#### Implementation Methods
1. **Lightweight Analytics** — Privacy-focused analytics (e.g., Plausible, Umami) or custom event tracking
2. **Performance API** — Use browser Performance API to measure comparison times
3. **Event Tracking** — Track key actions (compare, clear, copy results) with anonymous events
4. **Local Storage** — Store usage statistics locally (with user consent) for return visit tracking

#### Success Criteria Measurement
1. **Adoption** — Track unique visitors and return visit rate
2. **Performance** — Monitor 95th percentile comparison times
3. **Satisfaction** — Optional feedback widget (star rating + comment)
4. **Error Monitoring** — Capture and log any JavaScript errors

### Data Privacy
1. **No PII Collection** — Never collect personally identifiable information
2. **Anonymous IDs** — Use random session IDs, not user accounts
3. **Local Storage** — Store analytics data locally, not on servers
4. **Transparency** — Clear privacy policy about what is/isn't tracked
5. **Opt-Out** — Easy way to disable analytics (if any are implemented)

### Success Thresholds
1. **Performance** — 95% of comparisons complete in < 1 second
2. **Adoption** — 100+ unique visitors in first month
3. **Retention** — 20% return visit rate within 30 days
4. **Satisfaction** — Average rating > 4.0/5.0 (if feedback collected)
5. **Error Rate** — < 0.1% of sessions encounter JavaScript errors

## Traceability Matrix

| Feature | Use Case | Acceptance Criteria | Test Coverage |
|---------|----------|-------------------|---------------|
| Text Input | UC-1.1, UC-1.2, UC-1.3 | Paste, typing, clear functionality | Manual testing |
| Diff Calculation | UC-2.1, UC-2.2, UC-2.3 | Compare button, line-by-line, large texts | Automated tests |
| Diff Visualization | UC-3.1, UC-3.2, UC-3.3 | Colors, word diff, collapse | Visual testing |
| Privacy & Security | UC-4.1, UC-4.2 | Local processing, no accounts | Network monitoring |
| User Interface | UC-5.1, UC-5.2, UC-5.3 | Responsive, keyboard shortcuts, dark mode | Cross-browser testing |

## Open Questions

1. **File Upload** — Should users be able to upload text files directly, or is paste/type sufficient?
2. **Export Results** — Should the diff results be exportable (e.g., as HTML, text)?
3. **Syntax Highlighting** — For code comparisons, should we add syntax highlighting?
4. **Regex/Pattern Matching** — Should users be able to ignore certain patterns (e.g., whitespace)?
5. **Side-by-Side vs Unified** — Should we support both diff views (currently planning side-by-side only)?

## Assumptions

1. Users have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
2. Users can copy/paste text
3. Primary use case is line-by-line comparison (not character-level)
4. No need for version history or saving comparisons
5. No integration with other tools (git, IDE) needed
6. Tool will be hosted as a static site (no server-side processing)