# Stack Decision Record: diffcheck

## Product
**diffcheck** — Private, local-only text diff tool running entirely in the browser

## Chosen Stack: Static Web (Vanilla HTML/CSS/JS)

### Decision
**Static web stack with vanilla JavaScript (ES modules), no framework, no build step required for core functionality.**

### Rationale
| Factor | Assessment |
|--------|------------|
| **Runtime envelope (§7.2)** | ✅ Static web — runs in any browser, TESTER can run in-pod via static server |
| **Product requirements** | ✅ Local-only processing, zero dependencies, < 500ms for 10k lines, no account, no ads |
| **Performance** | ✅ Vanilla JS avoids framework overhead; diff algorithm in pure JS meets perf targets |
| **Privacy** | ✅ No network requests possible with static files; no build step eliminates supply-chain risk |
| **Maintainability** | ✅ Single HTML file deployable; easy to audit; no version-lock to framework |
| **Parallelization** | ✅ Disjoint modules: diff engine, UI rendering, input handling, visualization — independent |

### Alternatives Rejected

| Alternative | Why Rejected |
|-------------|--------------|
| **React/Vue/Svelte + Vite** | Adds build step, bundle size, framework learning curve; overkill for a single-page diff tool; violates "zero dependencies" success criterion |
| **Node.js backend** | Unnecessary — product explicitly requires local-only processing; adds server complexity, deployment, privacy risk |
| **Python (Flask/FastAPI + frontend)** | Same as Node — server-side not needed; outside static-web envelope for core product |
| **WebAssembly (Rust/C++ diff)** | Premature optimization; vanilla JS diff (Myers/LCS) handles 10k lines in < 100ms; adds toolchain complexity |
| **TypeScript + build** | Adds compilation step; for a ~500 LOC tool, type safety ROI is low; JSDoc provides adequate hints |

---

## Architecture for Parallelization

The product is decomposed into **four independent modules** with clear interfaces — DEV tasks can run in parallel:

```
┌─────────────────────────────────────────────────────────────┐
│                      index.html (entry)                     │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  diff-engine │  ui-input    │  ui-diff     │  ui-controls   │
│  (pure JS)   │  (DOM + events)│ (rendering) │  (dark mode,   │
│              │              │              │   shortcuts)    │
└──────────────┴──────────────┴──────────────┴────────────────┘
       │            │             │               │
       ▼            ▼             ▼               ▼
   Exports:     Exports:      Exports:         Exports:
   diff(a,b)→   initInputs()  renderDiff()     initControls()
   DiffResult   getTexts()    updateView()     toggleTheme()
```

| Module | File | Responsibility | DEV Task |
|--------|------|----------------|----------|
| **diff-engine** | `js/diff-engine.js` | Myers diff algorithm, line/word diff, returns structured `DiffResult` | `diffcheck-diff-engine` |
| **ui-input** | `js/ui-input.js` | Two textareas, paste/typing/clear, line numbers, sync scroll | `diffcheck-ui-input` |
| **ui-diff** | `js/ui-diff.js` | Side-by-side rendering, color coding, inline word diff, collapse sections | `diffcheck-ui-diff` |
| **ui-controls** | `js/ui-controls.js` | Compare button, dark mode toggle, keyboard shortcuts, copy/export | `diffcheck-ui-controls` |

**No shared state** — modules communicate via:
- `diff-engine` → pure function, no side effects
- `ui-input` → exposes `getTexts()` returning `{ original, changed }`
- `ui-diff` → receives `DiffResult`, renders to container
- `ui-controls` → orchestrates: calls `getTexts()` → `diff()` → `renderDiff()`

**Parallelization verdict:** 4 DEV tasks can run simultaneously. Speedup justifies 2-4 DEV instances.

---

## Best-Practice Conventions (Enforced by TECHLEAD/QA)

### Project Structure
```
/workspace/apps/diffcheck/
├── index.html              # Single entry point
├── css/
│   ├── variables.css       # CSS custom properties (colors, spacing)
│   ├── reset.css           # Minimal reset
│   ├── layout.css          # Grid/flex layout, responsive breakpoints
│   ├── diff-view.css       # Diff-specific styles (colors, collapse)
│   └── themes.css          # Light/dark mode variables
├── js/
│   ├── diff-engine.js      # Pure diff algorithm (exported)
│   ├── ui-input.js         # Input handling
│   ├── ui-diff.js          # Diff rendering
│   ├── ui-controls.js      # App orchestration + controls
│   └── main.js             # Bootstraps modules, wires events
├── tests/
│   ├── diff-engine.test.js # Unit tests for diff algorithm
│   └── integration.test.js # E2E via Playwright (if needed)
├── README.md               # How-to-run (verbatim works in clean checkout)
└── package.json            # Optional: only for dev tooling (lint, test)
```

### Code Conventions
- **ES Modules** — `type: "module"` in package.json or `<script type="module">`
- **JSDoc** — All exported functions typed with JSDoc (no TS build)
- **Naming** — `camelCase` for functions/vars, `PascalCase` for classes, `UPPER_SNAKE` for constants
- **No global pollution** — IIFE or module scope only
- **Error handling** — Try/catch at module boundaries; user-facing errors via toast/notification, not `alert()`

### Linting & Formatting
- **ESLint** with `eslint:recommended` + `plugin:eslint-plugin-jsdoc/recommended`
- **Prettier** — single quotes, 2 spaces, trailing commas, printWidth 100
- **Command:** `npm run lint && npm run format:check` (in CI)

### Testing
| Layer | Tool | Scope |
|-------|------|-------|
| Unit | Vitest (or Node `test:run`) | `diff-engine.js` — 100% coverage on diff algorithm |
| Integration | Playwright | Smoke: load page, paste, compare, verify colors, dark mode |
| Visual | Playwright + pixelmatch | Diff rendering snapshots (optional, post-MVP) |
| Privacy | Manual / Playwright | DevTools Network tab — zero requests on diff |

**Minimum DoD:** Unit tests pass, integration smoke passes, no console errors, README runs verbatim.

### Security Basics (OWASP Static Web)
- **CSP header** — `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'` (inline styles for themes)
- **No `eval`/`new Function`** — diff algorithm uses pure iteration
- **No `innerHTML` with user data** — use `textContent` or `createElement`; sanitize if HTML ever needed
- **Subresource Integrity** — if any CDN used (not planned)
- **Referrer-Policy** — `strict-origin-when-cross-origin`

### Performance Budgets
| Metric | Budget | Measurement |
|--------|--------|-------------|
| Initial load (LCP) | < 1.5s | Lighthouse CI |
| Diff 1k lines | < 100ms | Performance API in `diff-engine` |
| Diff 10k lines | < 500ms | Performance API in `diff-engine` |
| Bundle size (gzipped) | < 30 KB | `index.html` + CSS + JS |
| Memory (10k lines) | < 50 MB | DevTools heap snapshot |

### Accessibility (WCAG AA)
- Semantic HTML (`<main>`, `<section>`, `<label>`, `<button>`)
- Color contrast ≥ 4.5:1 (tested in both themes)
- Focus visible, keyboard operable
- ARIA labels for icon-only buttons
- `prefers-reduced-motion` respected

---

## Stack Decision Log
- **2026-07-14** — Initial decision: Static web (vanilla JS). Recorded by CTO.
- Next review: Portfolio requalification (§7.1) or if product scope changes.

---

## Appendix: Diff Algorithm Choice
**Myers O(ND) algorithm** — Industry standard for line diff (used by Git, diffutils).
- Time: O((N+M)D) where D = edit distance
- Space: O(N+M)
- Handles 10k lines in ~50ms in V8
- Implementation: ~150 lines pure JS, well-tested, no deps
- Word diff: Post-process line diff with word-level Myers on changed lines