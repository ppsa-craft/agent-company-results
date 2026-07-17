import { RGB, ContrastResult } from './types.js';

/**
 * Calculate relative luminance of an RGB color per WCAG 2.1
 */
function getLuminance(rgb: RGB): number {
  const srgb = [rgb.r / 255, rgb.g / 255, rgb.b / 255].map(c => {
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * srgb[0] + 0.7152 * srgb[1] + 0.0722 * srgb[2];
}

/**
 * Calculate contrast ratio between two RGB colors per WCAG 2.1
 */
export function contrastRatio(fg: RGB, bg: RGB): number {
  const l1 = getLuminance(fg);
  const l2 = getLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if contrast ratio passes WCAG AA
 */
export function passesAa(fg: RGB, bg: RGB, largeText: boolean): boolean {
  const ratio = contrastRatio(fg, bg);
  return largeText ? ratio >= 3 : ratio >= 4.5;
}

/**
 * Check if contrast ratio passes WCAG AAA
 */
export function passesAaa(fg: RGB, bg: RGB, largeText: boolean): boolean {
  const ratio = contrastRatio(fg, bg);
  return largeText ? ratio >= 4.5 : ratio >= 7;
}

export type ContrastRating = {
  ratio: number;
  aa: { normal: boolean; large: boolean };
  aaa: { normal: boolean; large: boolean };
};

/**
 * Get detailed contrast rating between two colors
 */
export function getContrastRating(fg: RGB, bg: RGB): ContrastRating {
  const ratio = contrastRatio(fg, bg);
  return {
    ratio: Number(ratio.toFixed(2)),
    aa: {
      normal: passesAa(fg, bg, false),
      large: passesAa(fg, bg, true)
    },
    aaa: {
      normal: passesAaa(fg, bg, false),
      large: passesAaa(fg, bg, true)
    }
  };
}