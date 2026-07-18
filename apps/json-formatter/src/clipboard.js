// JSON Formatter - Clipboard Operations
// Handles copying formatted/minified JSON to system clipboard

function copyToClipboard(text, options = {}) {
    const {
        showFeedback = true,
        feedbackElement = null,
        fallbackMethod = 'fallback'
    } = options;
    
    // Try modern clipboard API first
    if (isModernClipboardAvailable()) {
        return copyWithModernAPI(text, showFeedback, feedbackElement);
    }
    
    // Fall back to textarea method
    if (fallbackMethod === 'textarea') {
        return copyWithTextarea(text, showFeedback, feedbackElement);
    }
    
    // Last resort fallback
    return copyWithFallback(text, showFeedback, feedbackElement);
}

// Check if modern clipboard API is available
function isModernClipboardAvailable() {
    return typeof navigator !== 'undefined' && 
           typeof navigator.clipboard === 'object' && 
           typeof navigator.clipboard.writeText === 'function';
}

// Copy using modern clipboard API
function copyWithModernAPI(text, showFeedback, feedbackElement) {
    return navigator.clipboard.writeText(text).then(() => {
        return {
            success: true,
            method: 'modern-clipboard-api',
            timestamp: Date.now(),
            textLength: text.length
        };
    }).catch(error => {
        console.error('Modern clipboard API failed:', error);
        throw error;
    });
}

// Copy using textarea fallback method
function copyWithTextarea(text, showFeedback, feedbackElement) {
    // Create temporary textarea element
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'absolute';
    textarea.style.left = '-999999px';
    textarea.style.top = '-999999px';
    textarea.setAttribute('readonly', '');
    
    document.body.appendChild(textarea);
    
    try {
        // Select and copy text
        textarea.select();
        const successful = document.execCommand('copy');
        
        if (showFeedback && feedbackElement) {
            showCopyFeedback(feedbackElement, successful);
        }
        
        return {
            success: successful,
            method: 'textarea-fallback',
            timestamp: Date.now(),
            textLength: text.length
        };
    } finally {
        document.body.removeChild(textarea);
    }
}

// Basic fallback method for environments without clipboard API
function copyWithFallback(text, showFeedback, feedbackElement) {
    // Store original clipboard state if available
    const originalClipboard = typeof window !== 'undefined' && window.clipboardData ? 
        window.clipboardData.getData('Text') : null;
    
    try {
        // Attempt to set clipboard data (works in some older browsers)
        if (typeof window !== 'undefined' && window.clipboardData) {
            window.clipboardData.setData('Text', text);
        }
        
        if (showFeedback && feedbackElement) {
            showCopyFeedback(feedbackElement, true);
        }
        
        return {
            success: true,
            method: 'fallback-method',
            timestamp: Date.now(),
            textLength: text.length
        };
    } catch (error) {
        console.error('All clipboard methods failed:', error);
        throw error;
    } finally {
        // Restore original clipboard state
        if (typeof window !== 'undefined' && window.clipboardData && originalClipboard !== null) {
            window.clipboardData.setData('Text', originalClipboard);
        }
    }
}

// Show visual feedback for successful copy
function showCopyFeedback(feedbackElement, success) {
    if (!feedbackElement) return;
    
    if (success) {
        // Add success visual indicator
        feedbackElement.classList.add('copy-success');
        feedbackElement.textContent = 'Copied!';
        
        setTimeout(() => {
            feedbackElement.classList.remove('copy-success');
            feedbackElement.textContent = 'Copy';
        }, 2000);
    } else {
        // Add error visual indicator
        feedbackElement.classList.add('copy-error');
        feedbackElement.textContent = 'Failed!';
        
        setTimeout(() => {
            feedbackElement.classList.remove('copy-error');
            feedbackElement.textContent = 'Copy';
        }, 2000);
    }
}

// Copy large JSON with progress tracking
function copyLargeJSON(jsonString, onProgress, options = {}) {
    const CHUNK_SIZE = 64 * 1024; // 64KB chunks
    const totalChunks = Math.ceil(jsonString.length / CHUNK_SIZE);
    
    if (onProgress) {
        onProgress(0, totalChunks);
    }
    
    return copyToClipboard(jsonString, options).finally(() => {
        if (onProgress && totalChunks > 0) {
            for (let i = 1; i <= totalChunks; i++) {
                onProgress(i, totalChunks);
            }
        }
    });
}

// Check clipboard permissions (for modern browsers)
function checkClipboardPermission() {
    if (isModernClipboardAvailable()) {
        return navigator.permissions.query({ name: 'clipboard-write' })
            .then(permissionStatus => {
                return {
                    available: true,
                    permitted: permissionStatus.state === 'granted',
                    state: permissionStatus.state
                };
            })
            .catch(() => {
                return {
                    available: true,
                    permitted: false,
                    state: 'denied'
                };
            });
    }
    
    return Promise.resolve({
        available: false,
        permitted: false,
        state: 'unavailable'
    });
}

// Get clipboard content (for reading)
function readFromClipboard() {
    if (isModernClipboardAvailable()) {
        return navigator.clipboard.readText().then(text => {
            return {
                text,
                success: true,
                method: 'modern-read'
            };
        }).catch(error => {
            console.error('Failed to read from clipboard:', error);
            return {
                text: null,
                success: false,
                error: error.message
            };
        });
    }
    
    // Fallback for older browsers
    if (typeof window !== 'undefined' && window.clipboardData) {
        const text = window.clipboardData.getData('Text');
        return Promise.resolve({
            text,
            success: true,
            method: 'fallback-read'
        });
    }
    
    return Promise.resolve({
        text: null,
        success: false,
        error: 'Clipboard read not supported'
    });
}

module.exports = {
  copyToClipboard,
  isModernClipboardAvailable,
  copyWithModernAPI,
  copyWithTextarea,
  copyWithFallback,
  showCopyFeedback,
  copyLargeJSON,
  checkClipboardPermission,
  readFromClipboard
};