# Review: diffcheck

**Task:** diffcheck-dev  
**DEV:** dev-instance-1  
**Date:** 2026-07-12  
**Reviewer:** TECHLEAD  

## Round 1 — TECHLEAD comments

1. **Blocker: UI rendering references wrong property names.** In `js/main.js` lines 114, 130, 146, the code uses `change.value` but the diff algorithm (`js/diff.js`) returns `change.line`. Similarly, line 146 uses `change.old` and `change.new` but the algorithm returns `change.oldLine` and `change.line`. This mismatch will cause the diff display to show `undefined` for all lines, making the tool non-functional. **Required fix:** Update `main.js` to use the correct property names (`line`, `oldLine`). Alternatively, adjust the diff algorithm's output to match the expected interface.

2. **Blocker: Missing `escapeHtml` usage.** The `escapeHtml` function is defined (line 83) but never called. While `textContent` is used for line content (safe), the "No differences found" message uses `innerHTML` with a static string (line 93). However, the `escapeHtml` function appears to be dead code. If the intent was to sanitize user input before inserting into HTML, it's not being used. **Required explanation:** Either remove the unused function or integrate it where needed. Confirm that all user-provided content is rendered via `textContent` (safe) and no `innerHTML` is used with dynamic content.

3. **Major: No error handling for large inputs.** The LCS algorithm has O(mn) complexity. For texts with >10,000 lines, this may freeze the browser. The stack decision (section 6.1) mentions "performance for large texts" as a consideration. **Required explanation:** Add a guard (e.g., limit line count, show warning) or document the limitation in README.

4. **Major: Inconsistent line numbering display.** The diff algorithm returns `oldLineNum` and `newLineNum` for each change, but the UI displays only symbols (+, -, ~) instead of line numbers. The task acceptance criteria require "line-by-line diff display with color coding" but not necessarily line numbers; however, the DEV's report mentions "line numbers and diff statistics". **Required explanation:** Clarify whether line numbers are intended. If not, remove the `oldLineNum`/`newLineNum` properties from the diff output to reduce confusion.

5. **Minor: Unused `escapeHtml` function.** Dead code should be removed to keep the codebase clean. **Suggested fix:** Delete the `escapeHtml` function (lines 83-87) unless it's needed for future XSS protection.

6. **Minor: Missing package.json for diffcheck.** The stack decision (section 4.1) specifies each tool should have its own `package.json`. The workspace uses npm workspaces, but the absence of a tool-specific package.json deviates from the convention. **Suggested fix:** Add a minimal `package.json` with tool-specific scripts (e.g., `build`, `test`) even if they delegate to the root.

7. **Minor: CSS color variables not shared across tools.** The diffcheck CSS defines its own color variables (`--bg`, `--text`, etc.) rather than using the shared design system mentioned in the stack decision (section 2.4). This reduces consistency across tools. **Suggested fix:** Consider extracting common CSS variables into a shared stylesheet or use the same variable names as other tools.

## What's Done Well

- Clean separation of concerns (diff algorithm, UI logic, styling).
- Good use of CSS custom properties for theming (dark mode support).
- Responsive design with mobile breakpoints.
- Keyboard shortcuts (Ctrl+Enter, Escape) improve UX.
- Tests for the diff algorithm are present and cover basic cases.
- README is accurate and includes development instructions.

## Verification Story

- Tests reviewed: Yes, diff algorithm tests pass (6/6).
- Build verified: Yes, esbuild produces bundle.js.
- Security checked: Yes, `textContent` used for dynamic content; no innerHTML with user input.

## Verdict

**REQUEST CHANGES** — Two blockers must be fixed before merge. The UI rendering bug makes the tool non-functional; the unused `escapeHtml` function is dead code that should be removed or integrated.