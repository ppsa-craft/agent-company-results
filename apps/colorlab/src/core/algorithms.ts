import { HSL } from './types.js';

/**
 * Generate monochromatic palette (variations of lightness)
 */
export function generateMonochromatic(base: HSL, count: number): HSL[] {
  const result: HSL[] = [];
  const step = count > 1 ? 100 / (count - 1) : 0;

  for (let i = 0; i < count; i++) {
    const l = Math.round(i * step);
    result.push({ h: base.h, s: base.s, l: Math.max(0, Math.min(100, l)) });
  }

  return result;
}

/**
 * Generate analogous palette (adjacent hues)
 */
export function generateAnalogous(base: HSL, count: number, angle = 30): HSL[] {
  const result: HSL[] = [];
  const step = count > 1 ? angle / (count - 1) : 0;
  const startAngle = base.h - angle / 2;

  for (let i = 0; i < count; i++) {
    let h = (startAngle + i * step) % 360;
    if (h < 0) h += 360;
    result.push({ h: Math.round(h), s: base.s, l: base.l });
  }

  return result;
}

/**
 * Generate complementary palette (opposite hue)
 */
export function generateComplementary(base: HSL): HSL[] {
  const h = (base.h + 180) % 360;
  return [base, { h: Math.round(h), s: base.s, l: base.l }];
}

/**
 * Generate triadic palette (three hues 120° apart)
 */
export function generateTriadic(base: HSL): HSL[] {
  const h1 = base.h;
  const h2 = (base.h + 120) % 360;
  const h3 = (base.h + 240) % 360;
  return [
    { h: h1, s: base.s, l: base.l },
    { h: Math.round(h2), s: base.s, l: base.l },
    { h: Math.round(h3), s: base.s, l: base.l }
  ];
}

/**
 * Generate tetradic palette (four hues 90° apart)
 */
export function generateTetradic(base: HSL): HSL[] {
  const h1 = base.h;
  const h2 = (base.h + 90) % 360;
  const h3 = (base.h + 180) % 360;
  const h4 = (base.h + 270) % 360;
  return [
    { h: h1, s: base.s, l: base.l },
    { h: Math.round(h2), s: base.s, l: base.l },
    { h: Math.round(h3), s: base.s, l: base.l },
    { h: Math.round(h4), s: base.s, l: base.l }
  ];
}

/**
 * Generate split complementary palette (base + two adjacent to complement)
 */
export function generateSplitComplementary(base: HSL): HSL[] {
  const complementHue = (base.h + 180) % 360;
  const h1 = (complementHue - 30 + 360) % 360;
  const h2 = (complementHue + 30) % 360;
  return [
    base,
    { h: Math.round(h1), s: base.s, l: base.l },
    { h: Math.round(h2), s: base.s, l: base.l }
  ];
}