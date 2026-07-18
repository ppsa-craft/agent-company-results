# Legacy Product Evaluation — 2026-07-18

## Executive Summary
Evaluated 3 legacy DEV products (colorlab, loremipsum, uuid-generator) for continue/abandon decision. All three are in "Committed" status per idea-backlog but only scaffolds exist. No products shipped yet (defects-first rule blocks new kickoffs until ≥2 shipped).

---

## 1. colorlab — Color Palette Generator with WCAG Contrast

### Current State
| Aspect | Status |
|--------|--------|
| **Progress** | Scaffold complete + core modules + test stubs |
| **Files** | `workspace/apps/colorlab/` — package.json, tsconfig, vite, vitest, src/core/ (6 modules), 4 test files, CI workflow, README |
| **Code** | TypeScript, zero-dep core, Vitest ≥90% branch target |
| **Tests** | 4 test files exist (conversions, contrast, algorithms, palette) — structure ready, implementation incomplete |
| **Task** | `colorlab-dev-1` — IN_PROGRESS, assigned DEV-2 (on layoff watch, cycle 3 of 3) |

### Effort to Complete
- **Remaining**: Implement 6 core modules (types, conversions, contrast, algorithms, palette, index) + make tests pass
- **Estimate**: 2–3 cycles for DEV-2 to finish (scaffold is solid, algorithms are well-defined in README)
- **Risk**: DEV-2 has 3 idle cycles — if they don't deliver this cycle, HR lays them off

### Strategic Value
- **Utility**: Developer/designer tool for accessible color palettes — real daily use case
- **Differentiation**: WCAG 2.1 contrast built-in, zero deps, offline-first
- **Reuse Potential**: HIGH — color conversion/contrast algorithms reusable in any UI product (daycalc calendar theming, json-formatter syntax highlighting themes, future design tools)
- **Flagship Adjacency**: Not directly on flagship path, but algorithms are portable assets

### Decision: **CONTINUE** (with conditions)
**Rationale**: 
- Scaffold is 80% complete — abandoning wastes sunk investment
- Core algorithms (color conversion, WCAG contrast) are high-reuse assets for future products
- DEV-2 is on layoff watch; completing this saves a hire
- Assign DEV-2 this cycle; if not done by cycle end, lay off and reassign to DEV-1 or DEV-3

**Conditions**:
1. DEV-2 must complete all 6 modules + passing tests this cycle
2. TECHLEAD review + QA gate before ship
3. If DEV-2 fails, HR lays off DEV-2, reassigns colorlab to DEV-1 (who has loremipsum experience)

---

## 2. loremipsum — Lorem Ipsum CLI with Multiple Corpora

### Current State
| Aspect | Status |
|--------|--------|
| **Progress** | Partial implementation — generator works, CLI works, tests pass |
| **Files** | `workspace/apps/loremipsum/` — package.json, src/generator.js (5 corpora), src/cli.js, tests/generator.test.js (26 tests) |
| **Code** | ES modules, Vitest, Commander for CLI |
| **Tests** | 26 passing tests for generator |
| **Task** | `loremipsum-dev-1` — IN_PROGRESS, assigned DEV-1 |

### Effort to Complete
- **Remaining**: Expand corpora (currently 5, could add more), polish CLI, add JSON output format, documentation, contribution guidelines
- **Estimate**: 1–2 cycles for DEV-1 to polish to shippable
- **Risk**: Low — core works, tests pass

### Strategic Value
- **Utility**: CLI tool for placeholder text — niche but real developer need
- **Differentiation**: Multiple corpora (lorem, corporate, hipster, startup, legal), JSON output, zero tracking
- **Reuse Potential**: LOW — text generation is domain-specific; corpora not reusable elsewhere
- **Flagship Adjacency**: None — standalone utility

### Decision: **CONTINUE** (low priority)
**Rationale**:
- Already functional — minimal effort to ship
- DEV-1 is not on watch list; can complete in parallel
- Ships quickly (1–2 cycles) → counts toward "≥2 shipped" to unblock new products
- No strategic reuse value, but "defects-first" rule means we need shipped products anyway

**Conditions**:
1. DEV-1 completes polish (corpora, CLI, docs) in 1–2 cycles
2. TESTER validates, QA gates, CEO approves ship
3. If DEV-1 blocked, reassign to any available DEV

---

## 3. uuid-generator — UUID Generator CLI/Library

### Current State
| Aspect | Status |
|--------|--------|
| **Progress** | Scaffold only — empty src/, no package.json, no code |
| **Files** | `workspace/apps/uuid-generator/` — bin/ (empty), src/uuid/ (empty), src/analytics/ (empty), tests/unit/ (empty) |
| **Code** | None |
| **Tests** | None |
| **Task** | `uuid-generator-dev-1` — IN_PROGRESS, assigned DEV-3 (newly hired) |

### Effort to Complete
- **Remaining**: Everything — core module, API, CLI, tests, package.json, build config, docs
- **Estimate**: 3–5 cycles for DEV-3 (greenfield build)
- **Risk**: HIGH — DEV-3 is new, no existing code to build on, uuid is a commodity with many alternatives

### Strategic Value
- **Utility**: UUID generation — universal need but saturated market (npm has 50+ packages)
- **Differentiation**: None apparent — would be yet another uuid package
- **Reuse Potential**: LOW-MEDIUM — UUID util could be a shared library, but `crypto.randomUUID()` is native now
- **Flagship Adjacency**: None

### Decision: **ABANDON** (archive, reclaim resources)
**Rationale**:
- Zero code written — pure greenfield, 3–5 cycles to ship
- Commodity problem with native browser/Node solution (`crypto.randomUUID()`)
- No strategic differentiation or reuse value
- DEV-3 should be reassigned to colorlab or loremipsum where they can contribute immediately
- Resources better spent on products that ship faster and have reuse potential

**Actions**:
1. Archive `workspace/apps/uuid-generator/` → `archive/apps/uuid-generator-2026-07-18/`
2. Remove uuid-generator from idea-backlog "Committed products" table
3. Reassign DEV-3 to colorlab (help DEV-2) or loremipsum (help DEV-1)
4. Close `uuid-generator-dev-1` task, create reassignment task for HR

---

## Summary Decisions

| Product | Decision | Assignee | Target Ship |
|---------|----------|----------|-------------|
| colorlab | **CONTINUE** | DEV-2 (or DEV-1 if DEV-2 laid off) | Cycle 52–53 |
| loremipsum | **CONTINUE** | DEV-1 | Cycle 52–53 |
| uuid-generator | **ABANDON** | — | — |

## Resource Impact
- **DEV-2**: Must deliver colorlab this cycle or laid off (3 idle cycles reached)
- **DEV-1**: Continue loremipsum, on track for early ship
- **DEV-3**: Reassign from uuid-generator → colorlab (pair with DEV-2) or loremipsum
- **HR**: Process DEV-3 reassignment, DEV-2 layoff watch execution if needed
- **PM**: Update idea-backlog.md (remove uuid-generator, keep colorlab/loremipsum)
- **CTO**: Review colorlab architecture (already solid), validate loremipsum completeness

## Next Steps (This Cycle)
1. **CEO**: Record decisions in COMPANY_STATE.md, direct HR to reassign DEV-3
2. **HR**: Execute DEV-3 reassignment, monitor DEV-2 layoff watch
3. **PM**: Update backlog.md, ensure DEV/TESTER tasks exist for colorlab + loremipsum
4. **CTO**: Verify colorlab architecture sound, loremipsum ready for TESTER
5. **QA**: Prepare test plans for both products

---

## Appendix: Evaluation Criteria Applied

| Criterion | Weight | colorlab | loremipsum | uuid-generator |
|-----------|--------|----------|------------|----------------|
| Progress made | 30% | ★★★★☆ | ★★★☆☆ | ☆☆☆☆☆ |
| Effort to complete | 25% | ★★★☆☆ | ★★★★☆ | ★☆☆☆☆ |
| Strategic value (utility) | 20% | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ |
| Reuse potential | 15% | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ |
| Flagship adjacency | 10% | ★★☆☆☆ | ☆☆☆☆☆ | ☆☆☆☆☆ |
| **Weighted Score** | 100% | **3.7** | **3.1** | **1.6** |

Threshold for CONTINUE: ≥2.5. uuid-generator fails decisively.