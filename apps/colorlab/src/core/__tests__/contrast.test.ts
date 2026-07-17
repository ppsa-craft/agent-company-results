import { describe, it, expect } from 'vitest';
import { contrastRatio, passesAa, passesAaa, getContrastRating } from '../contrast.js';

describe('contrast.ts', () => {
  describe('contrastRatio', () => {
    it('calculates contrast ratio between black and white', () => {
      const result = contrastRatio({ r: 0, g: 0, b: 0 }, { r: 255, g: 255, b: 255 });
      expect(result).toBe(21);
    });

    it('calculates contrast ratio between red and white', () => {
      const result = contrastRatio({ r: 255, g: 0, b: 0 }, { r: 255, g: 255, b: 255 });
      expect(result).toBeCloseTo(3.998, 2);
    });

    it('calculates contrast ratio between red and black', () => {
      const result = contrastRatio({ r: 255, g: 0, b: 0 }, { r: 0, g: 0, b: 0 });
      expect(result).toBeCloseTo(5.252, 2);
    });
  });

  describe('passesAa', () => {
    it('fails AA for normal text with red on white', () => {
      const result = passesAa({ r: 255, g: 0, b: 0 }, { r: 255, g: 255, b: 255 }, false);
      expect(result).toBe(false); // red on white has ratio ~4.0 < 4.5 AA normal threshold
    });

    it('fails AA for normal text with dark red on black', () => {
      const result = passesAa({ r: 139, g: 0, b: 0 }, { r: 0, g: 0, b: 0 }, false);
      expect(result).toBe(false);
    });

    it('passes AA for large text with lower contrast', () => {
      const result = passesAa({ r: 200, g: 0, b: 0 }, { r: 255, g: 255, b: 255 }, true);
      expect(result).toBe(true);
    });
  });

  describe('passesAaa', () => {
    it('passes AAA for normal text with high contrast', () => {
      const result = passesAaa({ r: 255, g: 255, b: 255 }, { r: 0, g: 0, b: 0 }, false);
      expect(result).toBe(true);
    });

    it('fails AAA for normal text with lower contrast', () => {
      const result = passesAaa({ r: 200, g: 200, b: 200 }, { r: 100, g: 100, b: 100 }, false);
      expect(result).toBe(false);
    });

    it('passes AAA for large text with lower contrast', () => {
      const result = passesAaa({ r: 200, g: 0, b: 0 }, { r: 255, g: 255, b: 255 }, true);
      expect(result).toBe(true);
    });
  });

  describe('getContrastRating', () => {
    it('returns correct rating for white on black (AAA)', () => {
      const result = getContrastRating({ r: 255, g: 255, b: 255 }, { r: 0, g: 0, b: 0 });
      expect(result.ratio).toBe(21);
      expect(result.aa.normal).toBe(true);
      expect(result.aa.large).toBe(true);
      expect(result.aaa.normal).toBe(true);
      expect(result.aaa.large).toBe(true);
    });

    it('returns correct rating for red on white (AA large only)', () => {
      const result = getContrastRating({ r: 255, g: 0, b: 0 }, { r: 255, g: 255, b: 255 });
      expect(result.ratio).toBeCloseTo(4.0, 1);
      expect(result.aa.normal).toBe(false);
      expect(result.aa.large).toBe(true);  // 4.0 >= 3.0 AA large threshold
      expect(result.aaa.normal).toBe(false);
      expect(result.aaa.large).toBe(false);
    });
  });
});