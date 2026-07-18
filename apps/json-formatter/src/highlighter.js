// JSON Formatter - Error Highlighting Engine
// Detects and highlights errors in JSON input with detailed information

function highlightErrors(jsonString, validationResults) {
    if (validationResults.valid) {
        return {
            errors: [],
            highlighted: false,
            message: 'No errors found'
        };
    }
    
    const errors = validationResults.errors;
    const highlighterResults = {
        errors: errors.map(error => ({
            ...error,
            highlighted: true,
            context: getErrorContext(jsonString, error),
            suggestion: getErrorSuggestion(error.message)
        })),
        highlighted: true,
        message: `${errors.length} error(s) found`
    };
    
    return highlighterResults;
}

// Get context around error location
function getErrorContext(jsonString, error, contextLength = 5) {
    const position = error.position;
    const start = Math.max(0, position - contextLength);
    const end = Math.min(jsonString.length, position + contextLength + 1);
    
    return {
        snippet: jsonString.substring(start, end),
        snippetStart: start,
        snippetEnd: end,
        errorOffset: position - start,
        before: jsonString.substring(start, position),
        after: jsonString.substring(position + 1, end)
    };
}

// Identify error type based on error message
function identifyErrorType(errorMessage) {
    const lowerMsg = errorMessage.toLowerCase();
    
    if (lowerMsg.includes('expecting "') || lowerMsg.includes('expecting \'')) {
        return 'syntax_error';
    }
    if (lowerMsg.includes('unterminated') || lowerMsg.includes('missing quote')) {
        return 'string_error';
    }
    if (lowerMsg.includes('unexpected token') || lowerMsg.includes('unexpected end')) {
        return 'unexpected_token';
    }
    if (lowerMsg.includes('invalid') && lowerMsg.includes('escape')) {
        return 'escape_error';
    }
    if (lowerMsg.includes('trailing comma')) {
        return 'trailing_comma';
    }
    if (lowerMsg.includes('duplicate key')) {
        return 'duplicate_key';
    }
    
    return 'general_syntax_error';
}

// Calculate cursor position for error highlighting
function calculateCursorPositions(errors) {
    return errors.map(error => {
        const position = error.position || 0;
        return {
            line: error.line,
            column: error.column,
            position: position,
            range: {
                start: position,
                end: position + 1,
                length: 1
            },
            type: identifyErrorType(error.message),
            severity: getErrorSeverity(error.message)
        };
    });
}

// Get error severity level
function getErrorSeverity(errorMessage) {
    const lowerMsg = errorMessage.toLowerCase();
    
    if (lowerMsg.includes('invalid escape') || lowerMsg.includes('unexpected token')) {
        return 'warning';
    }
    if (lowerMsg.includes('missing quote') || lowerMsg.includes('expecting')) {
        return 'error';
    }
    if (lowerMsg.includes('trailing comma') || lowerMsg.includes('duplicate')) {
        return 'info';
    }
    
    return 'error';
}

// Perform incremental JSON parsing for real-time highlighting
function incrementalParsing(jsonString, onProgress) {
    let parsed;
    let position = 0;
    
    try {
        parsed = JSON.parse(jsonString);
        onProgress && onProgress({
            stage: 'complete',
            parsed,
            position: jsonString.length,
            valid: true
        });
        
        return {
            parsed,
            valid: true,
            position: jsonString.length,
            stage: 'complete'
        };
    } catch (error) {
        position = error.position || 0;
        onProgress && onProgress({
            stage: 'error',
            error: error.message,
            position: position,
            valid: false
        });
        
        return {
            parsed: null,
            valid: false,
            position: position,
            stage: 'error',
            error: error.message
        };
    }
}

// Generate visual markers for error highlighting
function generateVisualMarkers(jsonString, cursorPositions) {
    const markers = [];
    
    cursorPositions.forEach((cursor, index) => {
        if (cursor.position < jsonString.length) {
            const char = jsonString[cursor.position];
            
            markers.push({
                type: 'error-marker',
                position: cursor.position,
                char: char,
                severity: cursor.severity,
                index: index,
                htmlClass: `error-marker error-${cursor.severity}`
            });
        }
    });
    
    return markers;
}

// Batch processing for multiple error highlights
function batchHighlight(jsonStrings) {
    return jsonStrings.map((jsonString, index) => {
        const validationResults = { valid: true, errors: [] };
        try {
            JSON.parse(jsonString);
        } catch (error) {
            validationResults.valid = false;
            validationResults.errors = [{ 
                message: error.message,
                position: error.position || 0,
                line: error.line || 1,
                column: error.column || 0
            }];
        }
        
        return {
            index,
            jsonString: jsonString.substring(0, 100) + '...',
            validation: validationResults,
            highlighted: !validationResults.valid
        };
    });
}

module.exports = {
  highlightErrors,
  getErrorContext,
  identifyErrorType,
  calculateCursorPositions,
  getErrorSeverity,
  incrementalParsing,
  generateVisualMarkers,
  batchHighlight
};