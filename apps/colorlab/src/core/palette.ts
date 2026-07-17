import { HSL, Palette, PaletteAlgorithm, PaletteOptions, RGB } from './types.js';
import {
  generateMonochromatic,
  generateAnalogous,
  generateComplementary,
  generateTriadic,
  generateTetradic,
  generateSplitComplementary
} from './algorithms.js';
import { getContrastRating } from './contrast.js';

/**
 * Generate palette based on algorithm
 */
export function generatePalette(base: HSL, algorithm: PaletteAlgorithm, options: PaletteOptions = {}): HSL[] {
  const count = options.count ?? 5;

  switch (algorithm) {
    case 'monochromatic':
      return generateMonochromatic(base, count);
    case 'analogous':
      return generateAnalogous(base, count, options.angle ?? 30);
    case 'complementary':
      return generateComplementary(base);
    case 'triadic':
      return generateTriadic(base);
    case 'tetradic':
      return generateTetradic(base);
    case 'split-complementary':
      return generateSplitComplementary(base);
    default:
      throw new Error(`Unknown palette algorithm: ${algorithm}`);
  }
}

/**
 * Generate full palette with contrast ratings against white and black
 */
export function generateFullPalette(base: HSL, algorithm: PaletteAlgorithm, options: PaletteOptions = {}): Palette {
  const colors = generatePalette(base, algorithm, options);
  const white: import('./types.js').RGB = { r: 255, g: 255, b: 255 };
  const black: import('./types.js').RGB = { r: 0, g: 0, b: 0 };

  const contrast = colors.map(color => {
    const rgb = {
      r: Math.round(hslToRgb(color).r),
      g: Math.round(hslToRgb(color).g),
      b: Math.round(hslToRgb(color).b)
    };
    return {
      white: getContrastRating(rgb, white),
      black: getContrastRating(rgb, black)
    };
  });

  return {
    type: algorithm,
    base,
    colors,
    contrast
  };
}

/**
 * Convert HSL to RGB (internal helper)
 */
function hslToRgb(hsl: HSL): { r: number; g: number; b: number } {
  const h = hsl.h / 360;
  const s = hsl.s / 100;
  const l = hsl.l / 100;

  let r, g, b;

  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };

    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;

    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }

  return { r: r * 255, g: g * 255, b: b * 255 };
}