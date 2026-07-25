# Stack Decision Record — qr-code-generator

## Product Overview
**qr-code-generator** — A client-side QR code generator web tool supporting text, URLs, WiFi, vCard, and custom data encoding. Built for Static Web runtime compliance with emphasis on parallel development and zero-dependency core.

## Chosen Stack

**Technology Stack**: Static Web — Vite + Vanilla TypeScript (ES Modules), Vitest for testing, QR code library (qrcode or @zaxing/encoder) as single runtime dependency.

### Core Technology Components
- **Runtime**: Static Web (browser-only, no server) — meets §7.2 hard constraint
- **Build Tool**: Vite (fast dev server, optimized production build)
- **Language**: TypeScript (strict mode, ES modules)
- **QR Library**: `qrcode` (npm, ~30KB gzipped) or `@zaxing/encoder` (smaller, no Canvas deps)
- **Testing**: Vitest (unit) + Playwright (E2E) — TESTER runs in-pod via static server
- **Styling**: Vanilla CSS with CSS Custom Properties (themes)
- **Deploy**: Static files (Vite build output) — works on any static host

## Rationale for Stack Choice

### Alignment with Runtime Constraints (§7.2)
1. **Static Web Compliance**: Runs entirely in browser, zero server dependencies
2. **TESTER Ready**: `npx serve dist` + Playwright = full E2E in clean pod
3. **Node.js Dev Only**: Vite/Vitest run in Node dev environment, production is static files
4. **Parallelism Optimized**: Module boundaries enable 8+ independent DEV tasks

### Performance & Quality Objectives
1. **Bundle Size**: < 50KB gzipped (QR lib ~30KB + app ~15KB)
2. **Cold Load**: < 1.5s LCP on 3G (Lighthouse CI gate)
3. **Generation Speed**: < 50ms for typical QR codes
4. **Offline-First**: Service worker optional, works fully offline

## Rejected Alternatives

### Alternative 1: React/Vue/Svelte + Vite
- **Pros**: Component model, ecosystem
- **Cons**: Bundle bloat (React ~40KB), build complexity, overkill for single-page tool
- **Eliminated**: Violates "static web preference" for quick wins

### Alternative 2: Node.js Backend + Frontend
- **Pros**: Server-side generation for complex codes
- **Cons**: Violates static-web envelope; QR generation is purely client-side
- **Eliminated**: Unnecessary server infrastructure

### Alternative 3: Python (pyqrcode) + Web Frontend
- **Pros**: Mature Python QR libraries
- **Cons**: Violates Node/Python/Static-Web constraint (requires Python runtime for TESTER)
- **Eliminated**: Stack constraint is hard

### Alternative 4: Pure Canvas API (no library)
- **Pros**: Zero dependencies
- **Cons**: QR encoding is complex (Reed-Solomon, mask patterns); reinventing = bugs
- **Eliminated**: Security/correctness risk outweighs dep cost

## Best-Practice Conventions (Owner Mandate §7.2)

### Code Structure & Organization
```
workspace/apps/qr-code-generator/
├── src/
│   ├── core/                 # Pure logic (0 deps except QR lib)
│   │   ├── encoder.ts        # QR encoding logic, options validation
│   │   ├── formats.ts        # Formatters: text, url, wifi, vcard, email, sms
│   │   ├── types.ts          # TypeScript types for options, formats
│   │   └── index.ts          # Barrel export
│   ├── web/                  # Web UI
│   │   ├── index.html        # Entry HTML
│   │   ├── main.ts           # Bootstrap, wiring
│   │   ├── ui-form.ts        # Dynamic form per format type
│   │   ├── ui-canvas.ts      # Canvas rendering + download
│   │   ├── ui-options.ts     # Error correction, size, colors, logo
│   │   └── styles.css        # Themed, responsive
│   └── sw.ts                 # Optional service worker (workbox)
├── tests/
│   ├── core/                 # Vitest unit tests
│   │   ├── encoder.test.ts
│   │   ├── formats.test.ts
│   │   └── types.test.ts
│   └── e2e/                  # Playwright E2E
│       ├── generate.spec.ts
│       ├── formats.spec.ts
│       └── a11y.spec.ts
├── package.json
├── tsconfig.json
├── vite.config.ts
├── vitest.config.ts
├── playwright.config.ts
└── README.md
```

### Development Standards

#### Module Design
- **Pure Core**: `src/core/*` has zero DOM dependencies — unit testable in Node (Vitest)
- **Single Responsibility**: Each module owns one concern (encoding, formats, rendering, options)
- **Type-Safe Boundaries**: Zod schemas for format options → validated at UI boundary
- **Error Boundaries**: `Result<T, E>` pattern (neverthrow) for encoding failures

#### Testing Strategy
- **Unit**: Vitest on `src/core/*` — >95% branch coverage, pure functions
- **E2E**: Playwright — generate each format, verify QR decodes, download PNG/SVG, a11y
- **Contract**: Zod schemas tested as validation boundaries
- **Parallel**: All core modules test independently; E2E scenarios run in parallel

#### Code Quality
- **TypeScript**: Strict mode, `exactOptionalPropertyTypes`, no `any`
- **Lint/Format**: Biome (fast, unified) — `biome check --apply`
- **Bundle Analysis**: `vite-bundle-analyzer` in CI, gate at 50KB gzipped
- **Security**: CSP headers in `index.html` meta, no `eval`, sanitize logo uploads

## Parallelization Design

### Independent Development Units (DEV Tasks)

| Module | File | Responsibility | DEV Task ID | Dependencies |
|--------|------|----------------|-------------|--------------|
| **Core: Types & Schemas** | `src/core/types.ts` | Zod schemas for all formats, TypeScript types | `qr-core-types` | None |
| **Core: Encoder** | `src/core/encoder.ts` | QR code generation, error correction, options | `qr-core-encoder` | `qr-core-types` |
| **Core: Formatters** | `src/core/formats.ts` | Text/URL/WiFi/vCard/Email/SMS formatters | `qr-core-formats` | `qr-core-types` |
| **Web: Form UI** | `src/web/ui-form.ts` | Dynamic form per format, validation, preview | `qr-web-form` | `qr-core-types`, `qr-core-formats` |
| **Web: Canvas Renderer** | `src/web/ui-canvas.ts` | Draw QR to canvas, logo overlay, export PNG/SVG | `qr-web-canvas` | `qr-core-encoder` |
| **Web: Options Panel** | `src/web/ui-options.ts` | Error correction, size, colors, margin, logo | `qr-web-options` | `qr-core-types` |
| **Web: Main + Wiring** | `src/web/main.ts` | Bootstrap, event wiring, state management | `qr-web-main` | All above |
| **Web: Styles** | `src/web/styles.css` | Theming, responsive, print styles | `qr-web-styles` | None |

### Independent TESTER Units

| Test Suite | File | Scope | Parallelism |
|------------|------|-------|-------------|
| Unit: Types | `tests/core/types.test.ts` | Schema validation, type guards | Independent |
| Unit: Encoder | `tests/core/encoder.test.ts` | QR generation, error levels, sizes | Independent |
| Unit: Formatters | `tests/core/formats.test.ts` | All format encoders, edge cases | Independent |
| E2E: Core Generate | `tests/e2e/generate.spec.ts` | Text → QR → decode verify | Independent |
| E2E: Formats | `tests/e2e/formats.spec.ts` | WiFi/vCard/Email/SMS roundtrip | Independent |
| E2E: Options | `tests/e2e/options.spec.ts` | Size/color/logo/EC level changes | Independent |
| E2E: Export | `tests/e2e/export.spec.ts` | PNG/SVG download, clipboard | Independent |
| E2E: A11y | `tests/e2e/a11y.spec.ts` | axe-core audit, keyboard nav | Independent |

**Total Parallel DEV Tasks: 8** (after `qr-core-types` completes, 7 run in parallel)
**Total Parallel TESTER Suites: 8** (all independent, run concurrently in Vitest/Playwright)

### Architectural Seams Minimization
- **No Shared State**: Core is pure functions; UI modules communicate via explicit props/events
- **Clear Dependency DAG**: `types` → `encoder`/`formats` → UI modules → `main.ts`
- **Single Direction**: Core never imports UI; UI imports core
- **Test Isolation**: Each test file imports only its module under test

## Quality Mandate Integration

### Best Practice Definition
**Best Practice**: Static-web stack decisions that enable parallel development, in-pod TESTER execution, zero-server deployment, and <50KB bundles while strictly adhering to Static Web runtime constraint.

### Enforcement Points
- **TECHLEAD**: Validates module boundaries, pure core, bundle size gate, TypeScript strictness
- **QA**: Verifies Vitest + Playwright run in clean pod (`npx serve dist` + `npx playwright test`)
- **CI**: `biome check`, `tsc --noEmit`, `vitest run --coverage`, `playwright test`, bundle size gate

### Parallelization Metrics
- **Max Independent DEV Tasks**: 8 (1 seed + 7 parallel)
- **Max Independent TESTER Suites**: 8 (fully parallel)
- **Expected Speedup**: 5-7x with 2 DEV + 2 TESTER agents
- **Critical Path**: `qr-core-types` → (`qr-core-encoder` + `qr-core-formats`) → UI modules

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| QR library bundle size > budget | Low | Medium | Use `@zaxing/encoder` (no Canvas) or `qrcode` with tree-shaking; CI gate |
| Canvas API differences (Safari) | Medium | Low | Test cross-browser in Playwright; fallback to SVG |
| Logo overlay complexity | Medium | Low | Scope to M2; M1 = core generation only |
| TESTER pod lacks browser | Low | Critical | Playwright installs Chromium; document in README |
| Accessibility gaps | Low | Medium | axe-core in CI; semantic HTML from start |

## Metrics & Monitoring

### Development Velocity
- **Parallel Tasks**: 8 DEV + 8 TESTER = 16 units
- **Expected Speedup**: 5-7x with current agent capacity
- **Quality Gates**: Automated (Biome, TSC, Vitest, Playwright, Bundle)

### Technical Debt Indicators
- **Bundle Size**: Track gzipped size in CI (gate: 50KB)
- **TypeScript Strictness**: `tsc --noEmit` must pass
- **Test Coverage**: >95% branches on core
- **Review Rounds**: Target ≤2 per product

## Integration with Quick Wins Portfolio

### Shared Stack Conventions (All 3 Quick Wins)
| Convention | json-formatter | qr-code-generator | base64-tool |
|------------|----------------|-------------------|-------------|
| **Build** | Vite + TS | Vite + TS | Vite + TS |
| **Test Unit** | Vitest | Vitest | Vitest |
| **Test E2E** | Playwright | Playwright | Playwright |
| **Lint/Format** | Biome | Biome | Biome |
| **Deploy** | Static (dist/) | Static (dist/) | Static (dist/) |
| **Core Pattern** | Pure TS modules | Pure TS modules | Pure TS modules |
| **TESTER Cmd** | `npx serve dist` | `npx serve dist` | `npx serve dist` |

**TESTER Efficiency**: Single test infrastructure (Vite + Vitest + Playwright config template) shared across all 3 quick wins.

---

**Stack Decision Owner**: CTO (technical line responsibility)
**Decision Date**: 2026-07-19 (Cycle 65 Emergency Meeting)
**Next Review**: Portfolio requalification or Cycle 66
**Emergency Status**: ACTIVE — Supports immediate parallel execution

(End of file)