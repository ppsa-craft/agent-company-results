# Code Review: daycalc-dev

| Field | Value |
|-------|-------|
| **Task** | daycalc-dev |
| **DEV** | dev-1 |
| **Date** | 2026-07-13 |
| **Reviewer** | TECHLEAD |
| **Files reviewed** | `js/datecalc.js`, `js/main.js`, `tests/datecalc.test.js`, `index.html`, `css/style.css`, `README.md` |

---

## Verdict: REQUEST CHANGES

Section 5.1: All **Major** items must be resolved before this can be APPROVED.

---

## Review Comments

### Blocker

None.

### Major

1. **Broken invalid-date error handling** (`js/main.js` + `js/datecalc.js`)
   The try/catch blocks in all three handlers assume `daysBetween`/`dayOfWeek`/`addDays` throw on invalid input, but they do not. Given an invalid date string (e.g. `"2025-13-01"`), `new Date(...)` produces an Invalid Date, `getTime()` returns `NaN`, and the functions return `NaN` or `"Invalid Date"` strings — no exception is thrown. The error UI is therefore dead code against invalid input. The spec requires *"clear error messages for invalid dates"*; this is unmet.
   **Fix:** Validate dates at the top of each function and throw a `RangeError` for invalid input, or validate in `main.js` before calling the library functions.

2. **Missing package.json** (`apps/daycalc/`)
   The README instructs users to run `npm test`, `npm run build`, and `npm install` from the project directory, but no `package.json` exists in `apps/daycalc/`. These commands fail if run in the project root. `npm test` works only from the workspace root via `npx vitest run apps/daycalc/tests/`.
   **Fix:** Add a `package.json` with `test` and `build` scripts that delegate to the workspace tooling, or correct the README instructions to match the actual workflow.

### Minor

3. **Result text is awkward for negative differences** (`js/main.js:40`)
   When `end` precedes `start`, the output reads e.g. `"-5 day(s) between 2025-01-10 and 2025-01-05"`. The word "between" paired with a negative number is confusing.
   **Suggestion:** Use a phrase like `"5 day(s) from 2025-01-10 to 2025-01-05 (before)"` or swap operands to keep results non-negative and indicate direction separately.

4. **No input validation in exported functions** (`js/datecalc.js`)
   While the browser date input constrains valid formatting, the three functions in `datecalc.js` are public API and accept any string. Empty strings, malformed dates, or non-date strings silently produce `NaN`/`"Invalid Date"` results.
   **Suggestion:** Add input validation that throws descriptive errors, strengthening the module's contract for any future consumer.

5. **`hidden` attribute may not be fully styled** (`js/main.js`, `index.html`)
   The `.result` and `.error` divs use the `hidden` HTML attribute, which has inconsistent styling in older browsers. The project targets modern browsers per the README, so this is acceptable — but a utility class (e.g. `.hidden { display: none }`) would be more robust and explicit.

---

## What's Done Well

- **Clean separation of concerns:** Pure date logic in `datecalc.js`, UI binding in `main.js`. Makes the module testable and reusable.
- **UTC-safe date handling:** Concatenating `"T00:00:00Z"` avoids all local-timezone and DST edge cases — a common pitfall in date libraries.
- **Good test coverage:** 12 tests covering same-day, positive/negative differences, month boundaries, leap years, day-of-week lookup, and add/subtract with boundary cases. All pass.
- **Security:** No `innerHTML`, no `eval`, no external network requests. Results are set via `textContent`. No XSS vector.
- **Accessibility:** Semantic HTML with `<label>` elements, `focus-visible` indicators, proper heading hierarchy, and `sr-only` utility class.
- **Dark mode:** Respects `prefers-color-scheme` with a dark theme — zero-effort for the user.
- **Responsive design:** Fluid layout with `max-width: 800px` container, mobile-friendly breakpoint at 768px.
- **Keyboard shortcut:** `Ctrl+Enter` to trigger calculation in the focused card improves power-user experience.
- **Minimal dependencies:** Vanilla JS with no external libraries — aligns with spec requirement.
- **Comprehensive README:** Covers how to run, project structure, test commands, API docs, accessibility, and privacy.

---

## Verification Story

| Check | Result |
|-------|--------|
| **Tests run** | `npx vitest run apps/daycalc/tests/` |
| **Test files** | 1 passed |
| **Test cases** | 12 passed, 0 failed |
| **Build** | No build step (vanilla JS modules) |
| **Security scan** | No XSS, no eval, no external requests, no storage |
| **Spec compliance** | 8/10 AC met; 2 Major issues (broken error handling, missing package.json) |
| **Browser compatibility** | Modern browsers only; ES modules, `<input type="date">`, CSS custom properties |
