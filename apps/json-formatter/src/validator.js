// JSON Formatter - Core Validator Module
// Validates JSON input with detailed error reporting

function validateJSON(jsonString) {
    const errors = [];
    let parsed;
    
    try {
      // Attempt to parse the JSON string
      parsed = JSON.parse(jsonString);
      return { valid: true, parsed, errors: [] };
    } catch (error) {
      // Capture validation errors with detailed information
      errors.push({
        type: 'syntax',
        message: error.message,
        line: getLineNumber(jsonString, error.position),
        column: getColumnNumber(jsonString, error.position),
        position: error.position,
        expected: getExpectedToken(jsonString, error.position),
        suggestion: getErrorSuggestion(error.message)
      });
    }
    
    return { valid: false, parsed: null, errors };
}

// Extract line number from position within JSON string
function getLineNumber(jsonString, position) {
  let line = 1;
  let col = 0;
  
  for (let i = 0; i < position && i < jsonString.length; i++) {
    if (jsonString[i] === '\n') {
      line++;
      col = 0;
    } else {
      col++;
    }
  }
  
  return { line, column: col };
}

// Get column number from position within JSON string
function getColumnNumber(jsonString, position) {
  let col = 0;
  
  for (let i = 0; i < position && i < jsonString.length; i++) {
    if (jsonString[i] === '\n') {
      col = 0;
    } else {
      col++;
    }
  }
  
  return col;
}

// Determine expected token based on error position
function getExpectedToken(jsonString, position) {
  if (position >= jsonString.length) {
    return 'end of input';
  }
  
  const char = jsonString[position];
  const prevChar = position > 0 ? jsonString[position - 1] : '';
  
  switch (char) {
    case '"':
      return 'string value';
    case ':':
      return 'colon separator';
    case ',':
      return 'comma separator';
    case ']':
      return 'closing bracket';
    case '}':
      return 'closing brace';
    case '{':
      return 'object opening brace';
    case '[':
      return 'array opening bracket';
    case 't':
      if (prevChar === 'f') return 'false or false literal';
      return 'true literal';
    case 'f':
      return 'false literal';
    case 'n':
      return 'null literal';
    case 't':
      return 'true literal';
    default:
      if (char >= '0' && char <= '9') {
        return 'numeric value';
      }
      return 'valid character';
  }
}

// Provide helpful error suggestions based on error message
function getErrorSuggestion(errorMessage) {
  const lowerMsg = errorMessage.toLowerCase();
  
  if (lowerMsg.includes('expecting') && lowerMsg.includes('string')) {
    return 'Check if your string values are properly quoted';
  }
  if (lowerMsg.includes('expecting') && lowerMsg.includes('number')) {
    return 'Check if your numbers are valid (no trailing dots)';
  }
  if (lowerMsg.includes('expecting') && lowerMsg.includes('}')) {
    return 'Check for missing closing brace or extra comma';
  }
  if (lowerMsg.includes('expecting') && lowerMsg.includes(']')) {
    return 'Check for missing closing bracket or extra comma';
  }
  if (lowerMsg.includes('unterminated string')) {
    return 'Ensure string values are properly closed with quotes';
  }
  if (lowerMsg.includes('invalid escape')) {
    return 'Use \\n, \\t, \\r, \\uXXXX for escape sequences';
  }
  if (lowerMsg.includes('trailing comma')) {
    return 'Remove trailing comma before closing brace or bracket';
  }
  
  return 'Check JSON syntax at marked location';
}

// Validate JSON with streaming for large files
function validateLargeJSON(jsonString, onProgress) {
  const CHUNK_SIZE = 65536; // 64KB chunks
  let position = 0;
  let chunksProcessed = 0;
  const totalChunks = Math.ceil(jsonString.length / CHUNK_SIZE);
  
  // For now, use standard validation but with progress reporting
  if (onProgress) {
    onProgress(0, totalChunks);
  }
  
  const result = validateJSON(jsonString);
  
  if (onProgress && totalChunks > 0) {
    for (let i = 1; i <= totalChunks; i++) {
      onProgress(i, totalChunks);
    }
  }
  
  return result;
}

module.exports = {
  validateJSON,
  validateLargeJSON,
  getLineNumber,
  getColumnNumber,
  getExpectedToken,
  getErrorSuggestion
};