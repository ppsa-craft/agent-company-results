# JSON Formatter — TESTER Onboarding Guide

> **Welcome!** This guide gets you productive on the json-formatter test suite from day one. Read it end-to-end before writing your first test.

---

## 1. Project Overview

### What is json-formatter?

A **client-side JSON processing tool** for developers that provides:
- **Validation** — Real-time JSON syntax validation with detailed error messages (line, column, suggestions)
- **Pretty-printing** — Configurable indentation (2–8 spaces), preserves key order, handles Unicode
- **Minification** — Strips all whitespace, produces smallest valid JSON
- **Error Highlighting** — Visual error location with context snippets and fix suggestions
- **Copy to Clipboard** — One-click copy with cross-browser fallback, user feedback

### Target Users
| Tier | Audience | Primary Need |
|------|----------|--------------|
| Primary | Backend/Frontend/Full-stack developers | Fast, ad-free JSON formatting & validation |
| Secondary | API testers, Technical writers, Data analysts | Readable output, tree view, error diagnosis |
| Tertiary | DevOps, DBAs | Large file handling, CLI-friendly output |

### Tech Stack
| Layer | Technology |
|-------|------------|
| **Runtime** | Node.js v20+ (dev), browser (prod) |
| **Test Framework** | **Vitest** with `jsdom` environment |
| **Module System** | ES Modules (`import`/`export`) |
| **Coverage Target** | **≥90% branches** (enforced by stack decision) |
| **Lint/Format** | ESLint + Prettier (run via `npm run lint`) |
| **Architecture** | Modular, event-driven, zero external deps for core logic |

### Key Files at a Glance
```
workspace/apps/json-formatter/
├── src/
│   ├── validator.js      # JSON validation & error details
│   ├── printer.js        # Pretty-printing (2–8 space indent)
│   ├── minifier.js       # Minification + round-trip validation
│   ├── highlighter.js    # Error location, context, suggestions
│   ├── clipboard.js      # Clipboard API + textarea fallback
│   ├── core.js           # Event-driven orchestrator (EventEmitter)
│   └── ui.js             # UI component wiring (browser only)
├── tests/                # ← YOUR DOMAIN
│   ├── validator.test.js
│   ├── printer.test.js
│   ├── minifier.test.js
│   ├── highlighter.test.js
│   ├── clipboard.test.js
│   ├── setup.js          # Global test utilities/mocks
│   └── integration.test.js (planned)
├── vitest.config.js      # Coverage thresholds, jsdom, reporters
├── package.json          # Scripts: test, test:coverage, lint, build
└── README.md             # Run instructions (must work verbatim)
```

---

## 2. Architecture Summary (Core Modules)

| Module | Exports | Responsibility | Key Functions |
|--------|---------|----------------|---------------|
| **validator** | `validateJSON`, `validateLargeJSON`, `getLineNumber`, `getColumnNumber`, `getExpectedToken`, `getErrorSuggestion` | Syntax validation, detailed error objects with position, line/col, suggestions | `validateJSON(jsonString)` → `{ valid, parsed, errors[] }` |
| **printer** | `printJSON`, `formatJSON`, `formatArray`, `formatObject`, `escapeString`, `validateIndentLevel`, `formatWithComments` | Recursive pretty-print with configurable indent (2–8), string escaping, comment preservation | `printJSON(jsonString, indent)` → formatted string |
| **minifier** | `minifyJSON`, `minifyLargeJSON`, `removeWhitespace`, `roundTripValidation`, `minifyEmptyStructures`, `minifyWithKeyOrder` | Whitespace removal, round-trip validation (minify→format→compare) | `minifyJSON(jsonString)` → compact string |
| **highlighter** | `highlightErrors`, `getErrorContext`, `identifyErrorType`, `calculateCursorPositions`, `getErrorSeverity`, `incrementalParsing`, `generateVisualMarkers`, `batchHighlight` | Error location → context snippet, cursor positions, severity, visual markers for UI | `highlightErrors(jsonString, validationResult)` → `{ errors[], highlighted, message }` |
| **clipboard** | `copyToClipboard`, `isModernClipboardAvailable`, `copyWithModernAPI`, `copyWithTextarea`, `copyWithFallback`, `showCopyFeedback`, `copyLargeJSON`, `checkClipboardPermission`, `readFromClipboard` | Clipboard API + textarea fallback, feedback UI, progress for large payloads | `copyToClipboard(text, options)` → `{ success, method, timestamp, textLength }` |
| **core** | `JSONFormatterCore` (class, extends `EventEmitter`) | Orchestrates all modules via events: `process:input`, `process:format`, `process:validate`, `process:copy` | `.format()`, `.validate()`, `.copy()` return Promises |
| **ui** | `JSONFormatterUI` (class, extends `EventEmitter`) | Binds DOM elements, wires events, manages state (input, validity, processing, result) | `.setInputComponent()`, `.setOutputComponent()`, `.setCopyButton()`, etc. |

### Event Flow (Core)
```
UI Input → core.emit('process:input') 
  → validation (validator) 
    → if valid: format:pretty | format:minify (printer/minifier)
    → if invalid: highlight:errors (highlighter)
  → UI receives 'format:complete' | 'error' | 'validation:complete'
```

---

## 3. Development Setup

### Prerequisites
- **Node.js ≥ 20** (check: `node --version`)
- **npm ≥ 9** (bundled with Node)

### Install & Verify
```bash
cd /data/workspace/apps/json-formatter
npm install              # installs vitest, jsdom, eslint, prettier
npm test                 # runs all tests in watch mode (Ctrl+C to exit)
npm test -- --coverage   # single run with coverage report
npm run lint             # ESLint + Prettier check
```

### Key npm Scripts (from `package.json`)
| Script | Command | Use When |
|--------|---------|----------|
| `test` | `vitest` | Dev loop — watch mode, fast feedback |
| `test:run` | `vitest run` | CI / pre-commit — single run, exit code |
| `test:coverage` | `vitest run --coverage` | Coverage gate (≥90% branches) |
| `test:ui` | `vitest --ui` | Visual test runner (browser) |
| `lint` | `eslint src/ tests/` | Code style check |
| `build` | `node src/core.js` | Smoke test core module loads |

### Running a Single Test File
```bash
npm test -- tests/validator.test.js        # one file
npm test -- -t "validates empty object"    # by test name pattern
npm test -- --grep "validation"            # by describe/it text
```

---

## 4. Testing Guidelines

### Test Structure & Naming Conventions

**File naming**: `<module>.test.js` (mirrors `src/<module>.js`)

**Describe block hierarchy**:
```javascript
// tests/validator.test.js
import { describe, it, expect, beforeEach } from 'vitest'
import { validateJSON, getLineNumber, getErrorSuggestion } from '../src/validator.js'

describe('validator.js', () => {
  describe('validateJSON()', () => {
    describe('valid JSON', () => {
      it('parses simple object', () => { ... })
      it('parses nested objects', () => { ... })
    })
    describe('invalid JSON', () => {
      it('rejects missing quotes', () => { ... })
      it('rejects trailing comma', () => { ... })
    })
  })
  describe('getLineNumber()', () => { ... })
})
```

**Test naming pattern**: `it('<expected behavior> when <condition>', () => { ... })`
- Good: `it('returns line 3 column 5 for error at position 42', () => { ... })`
- Bad: `it('test line number', () => { ... })`

### Coverage Expectations (Enforced by Stack Decision)

| Metric | Threshold | Enforced By |
|--------|-----------|-------------|
| **Branches** | **≥90%** | `vitest.config.js` + CI gate |
| **Functions** | ≥90% | Same |
| **Lines** | ≥90% | Same |
| **Statements** | ≥90% | Same |

> **Do not lower thresholds.** The CTO stack decision (§7.2) mandates ≥90% branch coverage. TECHLEAD and QA will reject PRs that don't meet it.

### What to Test (Per Module)

| Module | Critical Test Areas |
|--------|---------------------|
| **validator** | Valid/invalid JSON, error position accuracy, line/col calculation, Unicode, large input streaming, suggestion quality |
| **printer** | Indent levels 2/4/6/8, special chars (`\n`, `\t`, `\"`, `\\`), Unicode, empty objects/arrays, key order preservation, comment handling |
| **minifier** | Whitespace removal, already-minified input, empty structures, round-trip (minify→validate→format), Unicode preservation |
| **highlighter** | Error context snippet (before/after), cursor position accuracy, error type classification, severity levels, batch processing |
| **clipboard** | Modern API success, textarea fallback, permission denied handling, large text (>64KB), feedback UI callbacks |
| **core** | Event emission order, promise resolution/rejection, timeout handling, option propagation |
| **ui** | DOM wiring, state transitions, input→validation→output flow, copy button feedback |

### Test Utilities (`tests/setup.js`)
```javascript
// Global test helpers — import automatically via vitest.config.js setupFiles
export function makeValidJSON(depth = 2, breadth = 3) { ... }
export function makeInvalidJSON(type = 'trailingComma') { ... }
export function createMockClipboard() { ... }
export function waitFor(ms) { return new Promise(r => setTimeout(r, ms)) }
```
> Add helpers here instead of duplicating across test files.

### Async Testing Patterns
```javascript
// Promise-returning functions (core, clipboard)
it('resolves with formatted result', async () => {
  const result = await core.format('{"a":1}', { format: 'pretty' })
  expect(result.result).toBe('{\n  "a": 1\n}')
})

// Event-based (core emits events)
it('emits validation:complete', () => {
  return new Promise((resolve) => {
    core.on('validation:complete', (result) => {
      expect(result.valid).toBe(true)
      resolve()
    })
    core.emit('process:validate', { input: '{}' })
  })
})
```

---

## 5. Code Review Process (What TECHLEAD/QA Look For)

### TECHLEAD Review Checklist (from `techlead-review-json-formatter.md`)
| Category | Must-Pass Items |
|----------|-----------------|
| **Architecture** | Module boundaries respected, no circular deps, event contracts honored |
| **Code Quality** | ESLint clean, Prettier formatted, JSDoc on exported functions, no `console.log` in prod code |
| **Security** | No `eval`, no `innerHTML` with user input, clipboard sanitization, XSS-safe error display |
| **Performance** | No O(n²) loops on large input, streaming for >1MB, memory <50MB peak |
| **Test Coverage** | **≥90% branches** on changed files, new tests for new behavior, edge cases covered |

### QA Gate Checklist (from `qa-gate-json-formatter.md`)
| Gate | Requirement |
|------|-------------|
| **Test Suite** | 100% passing (250+ cases planned) |
| **Coverage** | ≥90% branches, functions, lines, statements |
| **Performance** | <500ms for 10KB JSON, <50MB memory |
| **Cross-Browser** | Chrome, Firefox, Safari, Edge (latest 2) |
| **Accessibility** | WCAG 2.1 AA (keyboard, ARIA, contrast) |
| **Security** | OWASP guidelines, no critical vulns |
| **Docs** | README runs verbatim, API docs complete |

### Common Rejection Reasons (Learn These)
1. **Coverage drop** — New code without tests, or deleted tests without replacement
2. **Missing error paths** — Happy path only; no tests for `catch` blocks, timeouts, permission denials
3. **Flaky tests** — Timing-dependent, shared state, no cleanup in `afterEach`
4. **Browser-only APIs in Node tests** — `navigator.clipboard`, `document` without `jsdom` mock
5. **Magic numbers** — Hardcoded positions, timeouts, sizes without constants

---

## 6. File Ownership Map

| Path | Owner | TESTER Access |
|------|-------|---------------|
| `src/*.js` | **DEV** | **Read-only** — write tests against these |
| `tests/*.test.js` | **TESTER** | **Full ownership** — create, modify, delete |
| `tests/setup.js` | **TESTER** | **Full ownership** |
| `vitest.config.js` | **TESTER** (config) / **TECHLEAD** (approval) | Propose changes, TECHLEAD merges |
| `package.json` | **DEV** (deps) / **TESTER** (scripts) | Test scripts only |
| `README.md` | **DEV** | Report inaccuracies |
| `docs/architecture/*.md` | **CTO/TECHLEAD** | Read for context |
| `tasks/json-formatter-*.md` | **PM/BA/CTO/HR** | Read for requirements traceability |

> **Rule**: TESTER never edits `src/`. If you find a bug, write a failing test first, then report to DEV via PM.

---

## 7. Common Workflows

### Workflow A: Claim Task → Write Tests → Run → Report

```mermaid
graph TD
    A[PM assigns task in backlog.md] --> B[TESTER claims task]
    B --> C[Read BA doc & use cases for requirements]
    C --> D[Read source module (src/x.js) to understand API]
    D --> E[Write failing tests first (TDD)]
    E --> F[Run: npm test -- tests/x.test.js]
    F --> G{All pass?}
    G -- No --> H[Debug / refine tests]
    H --> F
    G -- Yes --> I[Run full suite: npm test -- --coverage]
    I --> J{Coverage ≥90%?}
    J -- No --> K[Add missing branch tests]
    K --> I
    J -- Yes --> L[Report to PM: task done + coverage %]
```

### Workflow B: Regression Test for Bug Report

1. PM files bug → creates task `json-formatter-tester-bug-N`
2. TESTER reads bug, identifies affected module
3. Write **minimal failing test** reproducing the bug
4. Run test → confirm failure
5. Assign to DEV (via PM) with test file reference
6. DEV fixes → TESTER re-runs → confirms pass
7. Add **edge-case tests** around the fix
8. Full suite + coverage → report done

### Workflow C: New Feature Test Development

1. BA doc + use cases → identify acceptance criteria
2. Map each AC to a test case (traceability)
3. Write tests **before** DEV implements (TDD)
4. Tests fail → DEV implements → tests pass
5. Integration test for end-to-end flow
6. Performance test if >10KB input involved

---

## 8. Key Reference Links

| Document | Location | Purpose |
|----------|----------|---------|
| **Backlog Task** | `/data/tasks/backlog.md` | Your assigned tasks |
| **BA Docs** | `/data/tasks/json-formatter-ba-docs.md` | Problem, users, success criteria, features |
| **Use Cases** | `/data/tasks/json-formatter-use-cases.md` | UC1–UC6, US1–US6, acceptance criteria |
| **CTO Architecture** | `/data/tasks/stack-json-formatter.md` | Stack rationale, module diagram, parallelization |
| **Test Plan** | `/data/tasks/json-formatter-tester-1.md` | 250+ test cases, coverage targets, config |
| **QA Gate** | `/data/tasks/qa-gate-json-formatter.md` | Launch criteria, test execution process |
| **TECHLEAD Review** | `/data/tasks/techlead-review-json-formatter.md` | What reviewers check |
| **DEV Spec** | `/data/tasks/json-formatter-dev-1.md` | Implementation acceptance criteria |
| **Company Rules** | `/data/AGENTS.md` | Org chart, file ownership, workflow rules |

---

## 9. Your First Day Checklist

- [ ] `cd /data/workspace/apps/json-formatter && npm install`
- [ ] `npm test -- --coverage` — verify baseline passes (≥90% branches)
- [ ] Open `tests/validator.test.js` — study existing patterns
- [ ] Read `json-formatter-use-cases.md` UC1 (Validation) + US1
- [ ] Read `json-formatter-tester-1.md` Test 1 (Validation Tests)
- [ ] Pick first task from backlog → claim in `backlog.md`
- [ ] Write your first test → run → pass → report to PM

---

## 10. Escalation Path

| Issue | Escalate To | Via |
|-------|-------------|-----|
| Blocked by missing DEV implementation | **PM** | Task comment / Slack |
| Coverage gate failing on unrelated code | **TECHLEAD** | Review record |
| Unclear acceptance criteria | **BA** | Task reference |
| Architecture question | **CTO/TECHLEAD** | Debate file if needed |
| Process/policy question | **HR** | This doc / lessons/hr.md |

---

**Welcome to the team. Write tests that catch bugs before users do.** 🧪