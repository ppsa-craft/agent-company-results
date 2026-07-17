import { describe, it, expect } from 'vitest';
import { generatePalette, generateFullPalette } from '../palette.js';
import { hslToRgb } from '../conversions.js';

describe('palette.ts', () => {
  describe('generatePalette', () => {
    it('generates monochromatic palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'monochromatic', { count: 5 });
      expect(result).toHaveLength(5);
      expect(result[0].h).toBe(0);
      expect(result[0].s).toBe(100);
      expect(result[0].l).toBe(0);
      expect(result[4].l).toBe(100);
    });

    it('generates analogous palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'analogous', { count: 5, angle: 30 });
      expect(result).toHaveLength(5);
    });

    it('generates complementary palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'complementary');
      expect(result).toHaveLength(2);
    });

    it('generates triadic palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'triadic');
      expect(result).toHaveLength(3);
    });

    it('generates tetradic palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'tetradic');
      expect(result).toHaveLength(4);
    });

    it('generates split complementary palette', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generatePalette(base, 'split-complementary');
      expect(result).toHaveLength(3);
    });

    it('generates monochromatic palette with zero saturation', () => {
      const base = { h: 0, s: 0, l: 50 };
      const result = generatePalette(base, 'monochromatic', { count: 3 });
      expect(result).toHaveLength(3);
      expect(result[0].l).toBe(0);
      expect(result[2].l).toBe(100);
    });

    it('throws error for unknown algorithm', () => {
      const base = { h: 0, s: 100, l: 50 };
      expect(() => generatePalette(base, 'unknown' as any)).toThrow('Unknown palette algorithm');
    });
  });

  describe('generateFullPalette', () => {
    it('generates full palette with contrast ratings', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateFullPalette(base, 'monochromatic', { count: 5 });
      expect(result.type).toBe('monochromatic');
      expect(result.base).toEqual({ h: 0, s: 100, l: 50 });
      expect(result.colors).toHaveLength(5);
      expect(result.contrast).toHaveLength(5);
    });

    it('calculates contrast ratings for colors', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateFullPalette(base, 'complementary');
      result.contrast.forEach(contrast => {
        expect(contrast.white.ratio).toBeGreaterThanOrEqual(0);
        expect(contrast.black.ratio).toBeGreaterThanOrEqual(0);
      });
    });

    it('generates palette with correct color assignments', () => {
      const base = { h: 120, s: 70, l: 60 };
      const result = generateFullPalette(base, 'triadic');
      expect(result.colors[0]).toEqual({ h: 120, s: 70, l: 60 });
      expect(result.colors[1].h).toBe(240);
      expect(result.colors[1].s).toBe(70);
      expect(result.colors[1].l).toBe(60);
      expect(result.colors[2].h).toBe(0);
      expect(result.colors[2].s).toBe(70);
      expect(result.colors[2].l).toBe(60);
    });
  });
});