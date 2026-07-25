# ColorLab Cycle 1 Implementation Task

## Task Overview

Implement the core color space conversion and palette generation library for ColorLab Cycle 1. The scaffold exists at `workspace/apps/colorlab/` with package.json, tsconfig.json, vite.config.ts, vitest.config.ts, .github/workflows/ci.yml, README.md, and src/core/types.ts.

## Missing Files to Create

### Core Implementation Files (src/core/)

1. **src/core/conversions.ts** - Pure color space conversions:
   - `hexToHsl(hex: string): HslColor`
   - `hslToHex(hsl: HslColor): string`
   - `hslToRgb(hsl: HslColor): RgbColor`
   - `rgbToHex(rgb: RgbColor): string`
   - `rgbToHsl(rgb: RgbColor): HslColor`

2. **src/core/contrast.ts** - WCAG 2.1 contrast ratio + AA/AAA pass/fail:
   - `contrastRatio(fg: RgbColor, bg: RgbColor): number`
   - `passesAa(fg: RgbColor, bg: RgbColor, largeText: boolean): boolean`
   - `passesAaa(fg: RgbColor, bg: RgbColor, largeText: boolean): boolean`
   - `getContrastRating(fg: RgbColor, bg: RgbColor): ContrastRating`

3. **src/core/algorithms.ts** - Palette generation algorithms:
   - `generateMonochromatic(base: HslColor, count: number): HslColor[]`
   - `generateAnalogous(base: HslColor, count: number, angle?: number): HslColor[]`
   - `generateComplementary(base: HslColor): HslColor[]`
   - `generateTriadic(base: HslColor): HslColor[]`
   - `generateTetradic(base: HslColor): HslColor[]`
   - `generateSplitComplementary(base: HslColor): HslColor[]`

4. **src/core/palette.ts** - Palette generation dispatcher:
   - `PaletteAlgorithm` type: 'monochromatic' | 'analogous' | 'complementary' | 'triadic' | 'tetradic' | 'split-complementary'
   - `generatePalette(base: HslColor, algorithm: PaletteAlgorithm, count?: number): HslColor[]`

5. **src/core/index.ts** - Barrel export exporting all public APIs from conversions, contrast, algorithms, palette, and types

### Test Files (src/core/__tests__/)

6. **src/core/__tests__/conversions.test.ts** - ≥90% branch coverage on conversions.ts
2. **src/core/__tests__/contrast.test.ts** - ≥90% branch coverage on contrast.ts
3. **src/core/__tests__/algorithms.test.ts** - ≥90% branch coverage on algorithms.ts
4. **src/core/__tests__/palette.test.ts** - ≥90% branch coverage on palette.ts

## Definition of Done (Tier 2 for Cycle 1)

- `npm ci && npm test -- --coverage` passes with **≥90% branch coverage** on `src/core/*`
- All algorithms implemented per spec in this task file
- CI workflow runs `npm ci && npm test -- --coverage`

## Verification

Run `npm ci && npm test -- --coverage` in `workspace/apps/colorlab/` to verify.

## Files Already Present (Scaffold)

- package.json
- tsconfig.json
- vite.config.ts
- vitest.config.ts
- .github/workflows/ci.yml
- README.md
- src/core/types.ts