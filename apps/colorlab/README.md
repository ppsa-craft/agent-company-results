# ColorLab

A zero-dependency, client-side color palette generator with accessibility checking, export, and sharing.

## Prerequisites

- Node.js 20+

## Quick Start

```bash
# Install dependencies
npm ci

# Start development server
npm run dev

# Run tests with coverage
npm test -- --coverage
```

## Project Structure

```
workspace/apps/colorlab/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── vitest.config.ts
├── .github/workflows/ci.yml
├── README.md
├── src/
│   ├── core/
│   │   ├── types.ts           # TypeScript types: HSL, RGB, HEX, ContrastResult, Palette types
│   │   ├── conversions.ts     # Pure color space conversions (hexToHsl, hslToHex, hslToRgb, rgbToHex, rgbToHsl)
│   │   ├── contrast.ts        # WCAG 2.1 contrast ratio + AA/AAA pass/fail vs white/black
│   │   ├── algorithms.ts      # generateMonochromatic, generateAnalogous, generateComplementary
│   │   ├── palette.ts         # generatePalette dispatcher
│   │   └── index.ts           # Barrel export
│   └── core/__tests__/        # Unit tests (≥90% branch coverage on src/core/*)
│       ├── conversions.test.ts
│       ├── contrast.test.ts
│       ├── algorithms.test.ts
│       └── palette.test.ts
└── .github/workflows/ci.yml
```

## Architecture (Cycle 1)

**Zero dependencies** in `src/core/` — pure TypeScript, no external deps. Vite + Vitest only in devDependencies.

- **Color model**: Internal = HSL (h 0–360, s/l 0–100). Conversions to/from HEX/RGB are exact (round-trip safe).
- **Contrast**: WCAG 2.1 relative luminance → contrast ratio → AA/AAA pass/fail for text (≥4.5/7) and large text (≥3/4.5) against white (#FFF) and black (#000).
- **Algorithms** (pure functions, HSL-based):
  - `generateMonochromatic(base: HSL, count: number): HSL[]` — same hue, vary saturation/lightness: distribute lightness 10%→90% (or symmetric around base.l), saturation variants ±20% clamped 0–100
  - `generateAnalogous(base: HSL, count: number, angle = 30): HSL[]` — hue ±angle, ±2×angle, … up to count; clamp hue 0–360; keep s/l same as base
  - `generateComplementary(base: HSL): HSL[]` — `[base, { h: (base.h + 180) % 360, s: base.s, l: base.l }]`

## Commands

| Command | Description |
|---------|-------------|
| `npm ci` | Clean install dependencies |
| `npm run dev` | Start Vite dev server |
| `npm run build` | Type-check and build to `dist/` |
| `npm test` | Run Vitest unit tests |
| `npm test -- --coverage` | Run tests with coverage report (≥90% branches on `src/core/*`) |

## CI

GitHub Actions workflow at `.github/workflows/ci.yml` runs on push/PR:
```yaml
npm ci
npm test -- --coverage
```

Coverage threshold: **≥90% branches** on `src/core/*`.