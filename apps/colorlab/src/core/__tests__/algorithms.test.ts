import { describe, it, expect } from 'vitest';
import { generateMonochromatic, generateAnalogous, generateComplementary, generateTriadic, generateTetradic, generateSplitComplementary } from '../algorithms.js';

describe('algorithms.ts', () => {
  describe('generateMonochromatic', () => {
    it('generates monochromatic palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateMonochromatic(base, 5);
      expect(result).toHaveLength(5);
      expect(result[0]).toEqual({ h: 0, s: 100, l: 0 });
      expect(result[4]).toEqual({ h: 0, s: 100, l: 100 });
    });

    it('generates monochromatic palette with count=1', () => {
      const base = { h: 200, s: 80, l: 50 };
      const result = generateMonochromatic(base, 1);
      expect(result).toHaveLength(1);
      expect(result[0]).toEqual({ h: 200, s: 80, l: 0 });
    });

    it('generates monochromatic palette with different base', () => {
      const base = { h: 120, s: 50, l: 30 };
      const result = generateMonochromatic(base, 3);
      expect(result).toHaveLength(3);
      expect(result[0]).toEqual({ h: 120, s: 50, l: 0 });
      expect(result[2]).toEqual({ h: 120, s: 50, l: 100 });
    });
  });

  describe('generateAnalogous', () => {
    it('generates analogous palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateAnalogous(base, 5, 30);
      expect(result).toHaveLength(5);
      expect(result[0].h).toBe(345);
      expect(result[2].h).toBe(0);
    });

    it('generates analogous palette with different angle', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateAnalogous(base, 3, 60);
      expect(result).toHaveLength(3);
      expect(result[0].h).toBe(330);
    });

    it('generates analogous palette with count=1', () => {
      const base = { h: 90, s: 70, l: 40 };
      const result = generateAnalogous(base, 1, 30);
      expect(result).toHaveLength(1);
      expect(result[0].h).toBe(75);
    });

    it('generates analogous palette with 3 colors', () => {
      const base = { h: 120, s: 50, l: 50 };
      const result = generateAnalogous(base, 3, 30);
      expect(result).toHaveLength(3);
      expect(result[0].h).toBe(105);
      expect(result[1].h).toBe(120);
      expect(result[2].h).toBe(135);
    });
  });

  describe('generateComplementary', () => {
    it('generates complementary palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateComplementary(base);
      expect(result).toHaveLength(2);
      expect(result[0]).toEqual({ h: 0, s: 100, l: 50 });
      expect(result[1]).toEqual({ h: 180, s: 100, l: 50 });
    });

    it('generates complementary of different hue', () => {
      const base = { h: 120, s: 50, l: 60 };
      const result = generateComplementary(base);
      expect(result).toHaveLength(2);
      expect(result[0]).toEqual({ h: 120, s: 50, l: 60 });
      expect(result[1]).toEqual({ h: 300, s: 50, l: 60 });
    });
  });

  describe('generateTriadic', () => {
    it('generates triadic palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateTriadic(base);
      expect(result).toHaveLength(3);
      expect(result[0]).toEqual({ h: 0, s: 100, l: 50 });
      expect(result[1].h).toBe(120);
      expect(result[2].h).toBe(240);
    });

    it('generates triadic of different hue', () => {
      const base = { h: 90, s: 70, l: 40 };
      const result = generateTriadic(base);
      expect(result).toHaveLength(3);
      expect(result[0]).toEqual({ h: 90, s: 70, l: 40 });
      expect(result[1].h).toBe(210);
      expect(result[2].h).toBe(330);
    });
  });

  describe('generateTetradic', () => {
    it('generates tetradic palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateTetradic(base);
      expect(result).toHaveLength(4);
      expect(result[0]).toEqual({ h: 0, s: 100, l: 50 });
      expect(result[1].h).toBe(90);
      expect(result[2].h).toBe(180);
      expect(result[3].h).toBe(270);
    });

    it('generates tetradic of different hue', () => {
      const base = { h: 45, s: 60, l: 70 };
      const result = generateTetradic(base);
      expect(result).toHaveLength(4);
      expect(result[0]).toEqual({ h: 45, s: 60, l: 70 });
      expect(result[1].h).toBe(135);
      expect(result[2].h).toBe(225);
      expect(result[3].h).toBe(315);
    });
  });

  describe('generateSplitComplementary', () => {
    it('generates split complementary palette correctly', () => {
      const base = { h: 0, s: 100, l: 50 };
      const result = generateSplitComplementary(base);
      expect(result).toHaveLength(3);
      expect(result[0]).toEqual({ h: 0, s: 100, l: 50 });
      expect(result[1].h).toBe(150);
      expect(result[2].h).toBe(210);
    });

    it('generates split complementary of different hue', () => {
      const base = { h: 90, s: 80, l: 60 };
      const result = generateSplitComplementary(base);
      expect(result).toHaveLength(3);
      expect(result[0]).toEqual({ h: 90, s: 80, l: 60 });
      expect(result[1].h).toBe(240);
      expect(result[2].h).toBe(300);
    });
  });
});