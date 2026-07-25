# Stack Decision Record — colorlab

## Chosen Stack

**Technology Stack**: Node.js (v20+) with TypeScript, Vitest for testing, Vite for bundling

## Why This Stack

### Alignment with Runtime Constraints
- **Node.js compliance**: Meets §7.2 hard requirement (only Node.js, Python, static-web stacks allowed)
- **Testable architecture**: Vitest enables TESTER to run tests in-pod as required
- **Minimal dependencies**: Focused on core color space utilities without unnecessary bloat

### Technical Justification
1. **Pure computational logic**: Color space conversions and palette generation are CPU-bound, perfect for Node.js execution
2. **Deterministic testing**: Vitest provides fast, reliable test execution for mathematical algorithms
3. **Small footprint**: Node.js ecosystem has mature color manipulation libraries (chroma.js, color) for validation
4. **CI/CD compatibility**: Vite config integrates cleanly with GitHub Actions for automated testing

## Rejected Alternatives

### Alternative 1: Python with NumPy/SciPy
- **Pros**: Strong numerical computing libraries, scientific Python ecosystem
- **Cons**: Violates Node.js runtime envelope constraint
- **Eliminated**: Runtime envelope is a hard constraint (§7.2)

### Alternative 2: Web Assembly (Rust/JS)
- **Pros**: Performance for computational workloads
- **Cons**: Complex build pipeline, violates Node.js-only constraint
- **Eliminated**: Runtime envelope enforcement

### Alternative 3: Deno with TypeScript
- **Pros**: Modern TypeScript-first runtime, similar to Node.js
- **Cons**: Runtime envelope explicitly calls out Node.js, not Deno
- **Eliminated**: Constraint compliance requires Node.js specifically

## Best-Practice Conventions

### Code Structure & Organization
```
src/
├── core/           # Pure logic module
│   ├── conversions.ts
│   ├── contrast.ts
│   ├── algorithms.ts
│   ├── palette.ts
│   └── index.ts    # Barrel exports
├── __tests__/      # Test suite (70% branch coverage minimum)
└── types.ts       # Shared type definitions
```

### Testing Strategy
- **Framework**: Vitest (headless Node.js test runner)
- **Coverage**: ≥90% branch coverage requirement
- **Parallelization**: Vitest's flat config enables parallel test execution across agents
- **CI Integration**: `.github/workflows/ci.yml` runs `npm ci && npm test -- --coverage`

### Development Standards
- **Type Safety**: TypeScript with strict mode for algorithm correctness
- **Error Handling**: Explicit error types for color space conversion failures
- **Performance**: Pure functions for deterministic mathematical operations
- **Documentation**: JSDoc comments for public APIs

### Build & Deployment
- **Bundling**: Vite for potential web integration (future-proof)
- **Packaging**: Standard npm package with semantic versioning
- **Verification**: Automated CI ensures quality gates before approval

## Quality Mandate Integration

### Define "Best Practice"
**Best Practice**: Stack decisions that enable parallel development, testable execution, and CI/CD compatibility while strictly adhering to the Node.js runtime envelope.

### Enforcement Points
- TECHLEAD applies these conventions in all reviews
- QA validates test execution runs in-pod via Vitest
- CI pipeline enforces stack compliance before merge

## Parallelization Design

### Independent Test Units
- Each color module (`conversions`, `contrast`, `algorithms`, `palette`) can be tested independently
- Test files touch disjoint files with no shared state
- Vitest parallelization enables concurrent test execution across multiple agents

### Architectural Seams Minimized
- Pure functions with no side effects
- Input parameters fully define output
- No global state or ordering dependencies between modules
- Each component isolated for independent development

## Risk Assessment

### Technical Risks
1. **Algorithm correctness**: Mathematical precision critical for color operations
   - **Mitigation**: Comprehensive unit tests with edge case coverage
2. **Test execution failures**: Node.js environment dependencies
   - **Mitigation**: Vitest provides reliable test environment
3. **Bundle size**: Node.js dependencies manageable
   - **Mitigation**: Focused dependency set, only required packages

### Operational Risks
1. **Runtime envelope enforcement**: Node.js-only constraint
   - **Status**: ✅ Fully compliant
2. **TESTER pipeline functionality**: Test execution in-pod
   - **Status**: ✅ Vitest enables reliable in-pod testing

## Metrics & Monitoring

### Development Velocity Metrics
- **Parallel tasks possible**: 4 core modules + 4 test suites = 8 independent units
- **Expected speedup**: Vitest parallelization enables 2-4x test execution improvement
- **Quality gates**: Automated CI passes ensure standards compliance

### Technical Debt Indicators
- **Boundary violations**: Track invalid file writes outside `tasks/stack-*` pattern
- **Workspace hygiene**: Monitor uncommitted changes during development cycles
- **Review round efficiency**: Target ≤2 rounds per product for quality-to-speed balance

---

**Stack Decision Owner**: CTO (technical line responsibility)
**Decision Date**: 2026-07-17
**Next Review**: Cycle 15 evaluation of stack effectiveness