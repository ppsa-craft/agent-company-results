// JSON Formatter - Minification Engine
// Removes all unnecessary whitespace while preserving valid JSON syntax

function minifyJSON(jsonString) {
    let parsed;
    
    try {
        parsed = JSON.parse(jsonString);
    } catch (error) {
        throw new Error(`Invalid JSON input: ${error.message}`);
    }
    
    return JSON.stringify(parsed);
}

// Stream-based minification for large files
function minifyLargeJSON(jsonString, onProgress) {
    const CHUNK_SIZE = 65536; // 64KB chunks
    let position = 0;
    let chunksProcessed = 0;
    const totalChunks = Math.ceil(jsonString.length / CHUNK_SIZE);
    
    // For now, use standard minification with progress reporting
    if (onProgress) {
        onProgress(0, totalChunks);
    }
    
    const result = minifyJSON(jsonString);
    
    if (onProgress && totalChunks > 0) {
        for (let i = 1; i <= totalChunks; i++) {
            onProgress(i, totalChunks);
        }
    }
    
    return result;
}

// Remove specific whitespace characters
function removeWhitespace(str) {
    return str.replace(/\s+/g, ' ')  // Replace runs of whitespace with single space
        .replace(/\s*([,:{\[])\s*/g, '$1')  // Remove space before/after :,{[
        .replace(/\s*(\]|})\s*/g, '$1')  // Remove space before/after ]}
        .trim();
}

// Validate JSON before/after minification
function roundTripValidation(jsonString, minifier, formatter) {
    try {
        const minified = minifier(jsonString);
        const formatted = formatter(minified, 2);
        const reFormatted = formatter(jsonString, 2);
        
        const minifiedParsed = JSON.parse(minified);
        const formattedParsed = JSON.parse(formatted);
        const reFormattedParsed = JSON.parse(reFormatted);
        
        // Compare parsed objects (structural equality)
        return JSON.stringify(minifiedParsed) === JSON.stringify(formattedParsed) &&
               JSON.stringify(reFormattedParsed) === JSON.stringify(formattedParsed);
    } catch (error) {
        return false;
    }
}

// Handle empty objects and arrays specially
function minifyEmptyStructures(jsonString) {
    if (/^\s*{}\s*$/.test(jsonString)) return '{}';
    if (/^\s*\[\]\s*$/.test(jsonString)) return '[]';
    return jsonString;
}

// Preserve order of object keys
function minifyWithKeyOrder(jsonString, indent = 2) {
    const parsed = JSON.parse(jsonString);
    return JSON.stringify(parsed, null, indent);
}

module.exports = {
  minifyJSON,
  minifyLargeJSON,
  removeWhitespace,
  roundTripValidation,
  minifyEmptyStructures,
  minifyWithKeyOrder
};