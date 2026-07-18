// JSON Formatter - Pretty-Printing Engine
// Formats JSON with configurable indentation levels (2-8 spaces)

function printJSON(jsonString, indent = 2) {
    let parsed;
    
    try {
        parsed = JSON.parse(jsonString);
    } catch (error) {
        throw new Error(`Invalid JSON input: ${error.message}`);
    }
    
    const indentStr = ' '.repeat(indent);
    return formatJSON(parsed, 0, indentStr);
}

// Recursively format JSON with proper indentation
function formatJSON(value, indentLevel, indentStr) {
    if (value === null) {
        return 'null';
    }
    
    if (typeof value === 'string') {
        return escapeString(value);
    }
    
    if (typeof value === 'number') {
        return String(value);
    }
    
    if (typeof value === 'boolean') {
        return String(value);
    }
    
    if (Array.isArray(value)) {
        return formatArray(value, indentLevel, indentStr);
    }
    
    if (typeof value === 'object') {
        return formatObject(value, indentLevel, indentStr);
    }
    
    throw new Error(`Unsupported value type: ${typeof value}`);
}

// Format array elements
function formatArray(arr, indentLevel, indentStr) {
    if (arr.length === 0) {
        return '[]';
    }
    
    const indentNext = indentLevel + 1;
    const elements = arr.map(item => {
        const itemIndent = ' '.repeat(indentNext * indentStr.length);
        const itemFormatted = formatJSON(item, indentNext, indentStr);
        return '\n' + itemIndent + itemFormatted;
    });
    
    const closingIndent = ' '.repeat(indentLevel * indentStr.length);
    return '[
' + elements.join(',') + 
    '\n' + closingIndent + ']';
}

// Format object key-value pairs
function formatObject(obj, indentLevel, indentStr) {
    const entries = Object.entries(obj);
    
    if (entries.length === 0) {
        return '{}';
    }
    
    const indentNext = indentLevel + 1;
    const pairs = entries.map(([key, value]) => {
        const keyFormatted = escapeString(key);
        const itemIndent = ' '.repeat(indentNext * indentStr.length);
        const valueFormatted = formatJSON(value, indentNext, indentStr);
        return '\n' + itemIndent + keyFormatted + ': ' + valueFormatted;
    });
    
    const closingIndent = ' '.repeat(indentLevel * indentStr.length);
    return '{
' + pairs.join(',') + 
    '\n' + closingIndent + '}';
}

// Escape special characters in JSON strings
function escapeString(str) {
    return '"' + str
        .replace(/\\/g, '\\\\')
        .replace(/\/g, '\\/')
        .replace(/\b/g, '\\b')
        .replace(/\f/g, '\\f')
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '\\r')
        .replace(/\t/g, '\\t')
        .replace(/[\x00-\x1f\x7f]/g, (c) => {
            return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
        })
        .replace(/[\uffff]/g, (c) => {
            return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
        })
        .replace(/["&'<>]/g, (c) => {
            return '\\u' + ('0000' + c.charCodeAt(0).toString(16)).slice(-4);
        }) + '"';
}

// Validate indentation level
function validateIndentLevel(indent) {
    if (typeof indent !== 'number' || indent < 2 || indent > 8) {
        throw new Error('Indentation level must be a number between 2 and 8');
    }
    return indent;
}

// Preserve comments (if present) while formatting
function formatWithComments(jsonString, indent = 2) {
    const lines = jsonString.split('\n');
    const indentStr = ' '.repeat(indent);
    let result = '';
    let indentLevel = 0;
    let inString = false;
    let escapeNext = false;
    let currentIndent = '';
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        
        // Handle multi-line strings
        if (inString) {
            if (escapeNext) {
                escapeNext = false;
            } else if (line.includes('\\"')) {
                escapeNext = true;
            }
        }
        
        const trimmedLine = line.trim();
        
        if (!inString && trimmedLine.startsWith('//')) {
            result += '\n' + currentIndent + trimmedLine;
            continue;
        }
        
        // Build result with proper indentation
        for (let j = 0; j < line.length; j++) {
            const char = line[j];
            
            if (!inString) {
                if (char === '{' || char === '[') {
                    result += char;
                    indentLevel++;
                    currentIndent = indentStr.repeat(indentLevel);
                } else if (char === '}' || char === ']') {
                    indentLevel = Math.max(0, indentLevel - 1);
                    currentIndent = indentStr.repeat(indentLevel);
                    result += char;
                } else if (char === ',') {
                    result += char + ' ';
                } else if (char === '"') {
                    inString = true;
                    result += char;
                } else {
                    result += char;
                }
            } else {
                if (escapeNext) {
                    escapeNext = false;
                    result += char;
                } else if (char === '\\') {
                    escapeNext = true;
                    result += char;
                } else if (char === '"') {
                    inString = false;
                    result += char;
                } else {
                    result += char;
                }
            }
        }
    }
    
    return result.trim() + '\n';
}

module.exports = {
  printJSON,
  formatJSON,
  formatArray,
  formatObject,
  escapeString,
  validateIndentLevel,
  formatWithComments
};