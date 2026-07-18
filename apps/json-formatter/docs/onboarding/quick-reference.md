# JSON Formatter — TESTER Quick Reference

> **One-page cheat sheet** — keep this open while working.

---

## 🚀 Quick Commands

| Action | Command |
|--------|---------|
| Install deps | `cd /data/workspace/apps/json-formatter && npm install` |
| Watch-mode tests | `npm test` |
| Single run + coverage | `npm test -- --coverage` |
| One test file | `npm test -- tests/validator.test.js` |
| Filter by name | `npm test -- -t "validates empty object"` |
| Visual UI | `npm test -- --ui` |
| Lint check | `npm run lint` |

---

## 📁 File Map (Your Domain = `tests/`)

```
tests/
├── validator.test.js      # validateJSON, line/col, suggestions
├── printer.test.js        # printJSON, indent 2-8, escapes, Unicode
├── minifier.test.js       # minifyJSON, round-trip, edge cases
├── highlighter.test.js    # highlightErrors, context, severity
├── clipboard.test.js      # copyToClipboard, fallbacks, feedback
├── setup.js               # Global helpers, mocks (auto-loaded)
└── integration.test.js    # (planned) E2E workflows
```

---

## 🎯 Coverage Gate (Non-Negotiable)

| Metric | Minimum | Config |
|--------|---------|--------|
| **Branches** | **90%** | `vitest.config.js` |
| Functions | 90% | enforced in CI |
| Lines | 90% | enforced in CI |
| Statements | 90% | enforced in CI |

> **Fail = no merge.** Add tests for every branch.

---

## 🧪 Test Patterns (Copy-Paste)

### Basic Unit Test
```javascript
import { describe, it, expect } from 'vitest'
import { validateJSON } from '../src/validator.js'

describe('validator.js → validateJSON()', () => {
  it('returns valid=true for simple object', () => {
    const result = validateJSON('{"key": "value"}')
    expect(result.valid).toBe(true)
    expect(result.parsed).toEqual({ key: 'value' })
  })

  it('returns errors with position for trailing comma', () => {
    const result = validateJSON('{"key": "value",}')
    expect(result.valid).toBe(false)
    expect(result.errors[0]).toMatchObject({
      type: 'syntax',
      position: expect.any(Number),
      line: expect.any(Number),
      column: expect.any(Number)
    })
  })
})
```

### Async / Promise Test
```javascript
import { JSONFormatterCore } from '../src/core.js'

it('format() resolves with pretty output', async () => {
  const core = new JSONFormatterCore()
  const result = await core.format('{"a":1}', { format: 'pretty' })
  expect(result.result).toBe('{\n  "a": 1\n}')
})
```

### Event-Based Test (Core)
```javascript
it('emits validation:complete', () => {
  const core = new JSONFormatterCore()
  return new Promise((resolve) => {
    core.on('validation:complete', (result) => {
      expect(result.valid).toBe(true)
      resolve()
    })
    core.emit('process:validate', { input: '{}' })
  })
})
```

### Clipboard Mock (jsdom)
```javascript
// In test file or setup.js
Object.defineProperty(navigator, 'clipboard', {
  value: { writeText: vi.fn().mockResolvedValue(undefined) },
  writable: true
})
```

---

## 🔑 Module APIs (What You're Testing Against)

| Module | Key Exports | Input → Output |
|--------|-------------|----------------|
| **validator** | `validateJSON(str)` | string → `{ valid, parsed, errors[] }` |
| | `getLineNumber(str, pos)` | → `{ line, column }` |
| | `getErrorSuggestion(msg)` | → string suggestion |
| **printer** | `printJSON(str, indent?)` | → formatted string (indent 2–8) |
| | `escapeString(str)` | → JSON-escaped string |
| **minifier** | `minifyJSON(str)` | → compact string |
| | `roundTripValidation(str, minify, format)` | → boolean |
| **highlighter** | `highlightErrors(str, result)` | → `{ errors[], highlighted, message }` |
| | `getErrorContext(str, error)` | → `{ snippet, before, after, errorOffset }` |
| **clipboard** | `copyToClipboard(text, opts)` | → `{ success, method, timestamp, textLength }` |
| **core** | `new JSONFormatterCore(opts)` | `.format()`, `.validate()`, `.copy()` → Promises |
| **ui** | `new JSONFormatterUI(opts)` | `.setInputComponent()`, `.setOutputComponent()`... |

---

## 📋 Traceability: Use Cases → Tests

| Use Case | User Story | Test File | Key Cases |
|----------|------------|-----------|-----------|
| **UC1: Validation** | US1 | `validator.test.js` | Valid/invalid, line/col, suggestions |
| **UC2: Pretty-Print** | US2 | `printer.test.js` | Indent 2/4/6/8, Unicode, escapes |
| **UC3: Minification** | US3 | `minifier.test.js` | Whitespace removal, round-trip |
| **UC4: Error Highlight** | US4 | `highlighter.test.js` | Position, type, severity, context |
| **UC5: Tree View** | US5 | *(UI integration)* | Not in core modules yet |
| **UC6: Copy** | US6 | `clipboard.test.js` | Modern API, fallback, feedback |

---

## ⚠️ Common Pitfalls (Don't Do These)

| Pitfall | Fix |
|---------|-----|
| Testing private functions | Test **exported** API only |
| No `await` on async test | Add `async` + `await` |
| Shared state between tests | Use `beforeEach`/`afterEach`, fresh imports |
| `console.log` in tests | Remove — clutters CI output |
| Magic numbers (position 42) | Use `getLineNumber()` / constants |
| Browser APIs without mock | Add mock in `setup.js` or test file |
| Skipping error paths | Test **every** `catch` block |

---

## 📊 Current Test Targets (from `json-formatter-tester-1.md`)

| Suite | Target Cases | Status |
|-------|--------------|--------|
| Validation | 45+ | 🎯 Write first |
| Pretty-Print | 50+ | 📝 Next |
| Minification | 40+ | 📝 Next |
| Error Highlight | 35+ | 📝 Next |
| Clipboard | 30+ | 📝 Next |
| Integration | 20+ | 📅 Later |
| Performance | 10+ | 📅 Later |
| Security | 10+ | 📅 Later |
| Accessibility | 15+ | 📅 Later |
| **Total** | **250+** | |

---

## 🔗 Essential Links

| Doc | Path |
|-----|------|
| Backlog (claim tasks) | `/data/tasks/backlog.md` |
| BA Docs (requirements) | `/data/tasks/json-formatter-ba-docs.md` |
| Use Cases (AC traceability) | `/data/tasks/json-formatter-use-cases.md` |
| CTO Stack Decision | `/data/tasks/stack-json-formatter.md` |
| Test Plan (this project) | `/data/tasks/json-formatter-tester-1.md` |
| QA Gate (launch criteria) | `/data/tasks/qa-gate-json-formatter.md` |
| TECHLEAD Review Criteria | `/data/tasks/techlead-review-json-formatter.md` |
| AGENTS.md (company rules) | `/data/AGENTS.md` |

---

## 🆘 Stuck? Escalate

| Problem | Who | How |
|---------|-----|-----|
| Unclear acceptance criteria | **BA** | Comment on task |
| Module not implemented yet | **PM → DEV** | Task dependency |
| Coverage failing on old code | **TECHLEAD** | Review record |
| Architecture question | **CTO/TECHLEAD** | Debate file |

---

**Remember**: Red → Green → Refactor. Every test you write is a bug that won't ship. 🧪