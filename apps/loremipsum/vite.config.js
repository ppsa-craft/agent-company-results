import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    lib: {
      entry: 'src/cli.js',
      formats: ['es'],
      fileName: () => 'cli.js',
    },
    outDir: 'dist',
    target: 'node20',
  },
});