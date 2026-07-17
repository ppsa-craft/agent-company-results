import { describe, it, expect, vi } from 'vitest';
import { generateText } from '../src/generator.js';

describe('generateText', () => {
  describe('lorem corpus', () => {
    it('generates specified number of paragraphs', () => {
      const result = generateText({ count: 3, corpus: 'lorem' });
      expect(result).toHaveLength(3);
    });

    it('generates single paragraph when count is 1', () => {
      const result = generateText({ count: 1, corpus: 'lorem' });
      expect(result).toHaveLength(1);
    });

    it('returns lorem ipsum text', () => {
      const result = generateText({ count: 1, corpus: 'lorem' });
      expect(result[0]).toContain('Lorem ipsum dolor sit amet');
    });

    it('throws error for invalid count', () => {
      expect(() => generateText({ count: 0, corpus: 'lorem' })).toThrow('Count must be a positive number');
      expect(() => generateText({ count: -1, corpus: 'lorem' })).toThrow('Count must be a positive number');
      expect(() => generateText({ count: 'abc', corpus: 'lorem' })).toThrow('Count must be a positive number');
    });
  });

  describe('corporate corpus', () => {
    it('generates specified number of paragraphs', () => {
      const result = generateText({ count: 2, corpus: 'corporate' });
      expect(result).toHaveLength(2);
    });

    it('returns corporate text', () => {
      const result = generateText({ count: 1, corpus: 'corporate' });
      expect(result[0]).toContain('streamline our workflow');
    });
  });

  describe('hipster corpus', () => {
    it('generates specified number of paragraphs', () => {
      const result = generateText({ count: 2, corpus: 'hipster' });
      expect(result).toHaveLength(2);
    });

    it('returns hipster text', () => {
      const result = generateText({ count: 1, corpus: 'hipster' });
      expect(result[0]).toContain('Pour-over flexitarian');
    });
  });

  describe('startup corpus', () => {
    it('generates specified number of paragraphs', () => {
      const result = generateText({ count: 2, corpus: 'startup' });
      expect(result).toHaveLength(2);
    });

    it('returns startup text', () => {
      const result = generateText({ count: 1, corpus: 'startup' });
      expect(result[0]).toContain('MVP disruption');
    });
  });

  describe('legal corpus', () => {
    it('generates specified number of paragraphs', () => {
      const result = generateText({ count: 2, corpus: 'legal' });
      expect(result).toHaveLength(2);
    });

    it('returns legal text', () => {
      const result = generateText({ count: 1, corpus: 'legal' });
      expect(result[0]).toContain('Agreement parties hereto');
    });
  });

  describe('unknown corpus', () => {
    it('throws error for unknown corpus', () => {
      expect(() => generateText({ count: 1, corpus: 'unknown' })).toThrow('Unknown corpus: unknown');
    });
  });
});