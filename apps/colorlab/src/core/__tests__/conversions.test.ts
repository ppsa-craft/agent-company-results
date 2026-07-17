import { describe, it, expect } from 'vitest';
import { hexToHsl, hslToHex, hslToRgb, rgbToHex, rgbToHsl, hexToRgb } from '../conversions.js';

describe('conversions.ts', () => {
  describe('hexToHsl', () => {
    it('converts hex to HSL correctly', () => {
      const result = hexToHsl('#ff0000');
      expect(result).toEqual({ h: 0, s: 100, l: 50 });
    });

    it('converts blue to HSL correctly', () => {
      const result = hexToHsl('#0000ff');
      expect(result).toEqual({ h: 240, s: 100, l: 50 });
    });

    it('converts green to HSL correctly', () => {
      const result = hexToHsl('#00ff00');
      expect(result).toEqual({ h: 120, s: 100, l: 50 });
    });

    it('handles black correctly', () => {
      const result = hexToHsl('#000000');
      expect(result).toEqual({ h: 0, s: 0, l: 0 });
    });

    it('handles white correctly', () => {
      const result = hexToHsl('#ffffff');
      expect(result).toEqual({ h: 0, s: 0, l: 100 });
    });
  });

  describe('hslToHex', () => {
    it('converts HSL to hex correctly', () => {
      const result = hslToHex({ h: 0, s: 100, l: 50 });
      expect(result).toBe('#ff0000');
    });

    it('converts HSL to hex with different values', () => {
      const result = hslToHex({ h: 120, s: 100, l: 50 });
      expect(result).toBe('#00ff00');
    });

    it('converts HSL to hex with zero saturation (grayscale)', () => {
      const result = hslToHex({ h: 0, s: 0, l: 50 });
      expect(result).toBe('#808080');
    });

    it('converts HSL to hex with lower saturation', () => {
      const result = hslToHex({ h: 240, s: 50, l: 60 });
      expect(result).toBe('#6666cc');
    });
  });

  describe('hslToRgb', () => {
    it('converts HSL to RGB correctly', () => {
      const result = hslToRgb({ h: 0, s: 100, l: 50 });
      expect(result).toEqual({ r: 255, g: 0, b: 0 });
    });

    it('converts HSL to RGB for green', () => {
      const result = hslToRgb({ h: 120, s: 100, l: 50 });
      expect(result).toEqual({ r: 0, g: 255, b: 0 });
    });
  });

  describe('rgbToHex', () => {
    it('converts RGB to hex correctly', () => {
      const result = rgbToHex({ r: 255, g: 0, b: 0 });
      expect(result).toBe('#ff0000');
    });

    it('converts RGB to hex for different colors', () => {
      const result = rgbToHex({ r: 0, g: 0, b: 255 });
      expect(result).toBe('#0000ff');
    });

    it('converts RGB to hex for black', () => {
      const result = rgbToHex({ r: 0, g: 0, b: 0 });
      expect(result).toBe('#000000');
    });
  });

  describe('rgbToHsl', () => {
    it('converts RGB to HSL correctly', () => {
      const result = rgbToHsl({ r: 255, g: 0, b: 0 });
      expect(result).toEqual({ h: 0, s: 100, l: 50 });
    });

    it('converts RGB to HSL for different colors', () => {
      const result = rgbToHsl({ r: 0, g: 255, b: 0 });
      expect(result).toEqual({ h: 120, s: 100, l: 50 });
    });

    it('converts pastel RGB to HSL (l > 0.5)', () => {
      const result = rgbToHsl({ r: 200, g: 200, b: 255 });
      expect(result).toEqual({ h: 240, s: 100, l: 89 });
    });

    it('converts RGB with red max and g < b', () => {
      const result = rgbToHsl({ r: 255, g: 100, b: 200 });
      expect(result.h).toBe(321);
    });
  });

  describe('hslToHex with l >= 0.5', () => {
    it('converts light HSL to hex correctly', () => {
      const result = hslToHex({ h: 180, s: 50, l: 70 });
      expect(result).toBe('#8cd9d9');
    });
  });

  describe('hexToRgb', () => {
    it('converts hex to RGB correctly', () => {
      const result = hexToRgb('#ff0000');
      expect(result).toEqual({ r: 255, g: 0, b: 0 });
    });

    it('converts hex to RGB for blue', () => {
      const result = hexToRgb('#0000ff');
      expect(result).toEqual({ r: 0, g: 0, b: 255 });
    });

    it('converts hex to RGB for white', () => {
      const result = hexToRgb('#ffffff');
      expect(result).toEqual({ r: 255, g: 255, b: 255 });
    });
  });
});