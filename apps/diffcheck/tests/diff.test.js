import { describe, it, expect } from 'vitest';
import { diffLines } from '../js/diff.js';

describe('diffLines', () => {
  it('returns empty array for identical texts', () => {
    const result = diffLines('hello', 'hello');
    expect(result).toEqual([]);
  });

  it('detects added lines', () => {
    const result = diffLines('', 'new line');
    expect(result).toEqual([
      { type: 'add', line: 'new line', oldLineNum: null, newLineNum: 1 }
    ]);
  });

  it('detects deleted lines', () => {
    const result = diffLines('deleted', '');
    expect(result).toEqual([
      { type: 'delete', line: 'deleted', oldLineNum: 1, newLineNum: null }
    ]);
  });

  it('detects changed lines', () => {
    const result = diffLines('old', 'new');
    expect(result).toEqual([
      { type: 'delete', line: 'old', oldLineNum: 1, newLineNum: null },
      { type: 'add', line: 'new', oldLineNum: null, newLineNum: 1 }
    ]);
  });

  it('detects similar lines as change', () => {
    const result = diffLines('hello world', 'hello world!');
    expect(result).toEqual([
      {
        type: 'change',
        line: 'hello world!',
        oldLine: 'hello world',
        oldLineNum: 1,
        newLineNum: 1
      }
    ]);
  });
});
