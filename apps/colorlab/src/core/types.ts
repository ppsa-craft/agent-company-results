export type HSL = {
  h: number; // 0–360
  s: number; // 0–100
  l: number; // 0–100
};

export type RGB = {
  r: number; // 0–255
  g: number; // 0–255
  b: number; // 0–255
};

export type HEX = `#${string}`;

export type ContrastResult = {
  ratio: number;
  aa: { normal: boolean; large: boolean };
  aaa: { normal: boolean; large: boolean };
};

export type PaletteType = 'monochromatic' | 'analogous' | 'complementary';

export type PaletteAlgorithm = 'monochromatic' | 'analogous' | 'complementary' | 'triadic' | 'tetradic' | 'split-complementary';

export type PaletteOptions = {
  count?: number;
  angle?: number;
};

export type Palette = {
  type: PaletteAlgorithm;
  base: HSL;
  colors: HSL[];
  contrast: {
    white: ContrastResult;
    black: ContrastResult;
  }[];
};