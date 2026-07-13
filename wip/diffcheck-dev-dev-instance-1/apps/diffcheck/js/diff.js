/**
 * Compare two texts line by line and return a list of changes.
 * @param {string} oldText - The original text
 * @param {string} newText - The new text
 * @returns {Array<{type: 'add'|'delete'|'change', line: string, oldLine?: string, oldLineNum: number|null, newLineNum: number|null}>}
 */
export function diffLines(oldText, newText) {
  const oldLines = oldText === '' ? [] : oldText.split('\n');
  const newLines = newText === '' ? [] : newText.split('\n');
  
  // LCS dynamic programming
  const m = oldLines.length;
  const n = newLines.length;
  const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
  
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (oldLines[i - 1] === newLines[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  
  // Backtrack to find changes
  const result = [];
  let i = m, j = n;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && oldLines[i - 1] === newLines[j - 1]) {
      // lines match, no change
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      // addition
      result.unshift({
        type: 'add',
        line: newLines[j - 1],
        oldLineNum: null,
        newLineNum: j
      });
      j--;
    } else if (i > 0 && (j === 0 || dp[i][j - 1] < dp[i - 1][j])) {
      // deletion
      result.unshift({
        type: 'delete',
        line: oldLines[i - 1],
        oldLineNum: i,
        newLineNum: null
      });
      i--;
    }
  }
  
  // Merge consecutive delete+add into change when they correspond
  const merged = [];
  for (let idx = 0; idx < result.length; idx++) {
    const current = result[idx];
    const next = result[idx + 1];
    if (current.type === 'delete' && next && next.type === 'add') {
      const sim = similarity(current.line, next.line);
      if (sim > 0.5) {
        merged.push({
          type: 'change',
          line: next.line,
          oldLine: current.line,
          oldLineNum: current.oldLineNum,
          newLineNum: next.newLineNum
        });
        idx++; // skip next
        continue;
      }
    } else if (current.type === 'add' && next && next.type === 'delete') {
      const sim = similarity(current.line, next.line);
      if (sim > 0.5) {
        merged.push({
          type: 'change',
          line: current.line,
          oldLine: next.line,
          oldLineNum: next.oldLineNum,
          newLineNum: current.newLineNum
        });
        idx++; // skip next
        continue;
      }
    }
    merged.push(current);
  }
  return merged;
}

/**
 * Compute similarity between two strings (0 to 1)
 */
function similarity(a, b) {
  if (a === b) return 1;
  if (a.length === 0 || b.length === 0) return 0;
  
  // Levenshtein distance
  const matrix = Array(a.length + 1).fill(null).map(() => Array(b.length + 1).fill(0));
  for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j++) matrix[0][j] = j;
  
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  
  const distance = matrix[a.length][b.length];
  const maxLen = Math.max(a.length, b.length);
  return 1 - distance / maxLen;
}
