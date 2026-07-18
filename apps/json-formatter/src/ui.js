// JSON Formatter - UI Integration Module
// Handles user interface integration, event handling, and component management

const { EventEmitter } = require('events');

class JSONFormatterUI extends EventEmitter {
    constructor(options = {}) {
        super();
        this.options = {
            theme: options.theme || 'light',
            defaultIndent: options.defaultIndent || 2,
            enableCopyFeedback: options.enableCopyFeedback !== false,
            enableErrorHighlighting: options.enableErrorHighlighting !== false,
            enableRealTimeValidation: options.enableRealTimeValidation !== false,
            ...options
        };
        
        this.components = {};
        this.state = {
            input: '',
            isValid: false,
            isProcessing: false,
            currentIndent: this.options.defaultIndent,
            lastResult: null,
            errorCount: 0,
            copied: false
        };
        
        this.initializeUIComponents();
        this.setupEventListeners();
    }
    
    // Initialize UI components
    initializeUIComponents() {
        this.components = {
            inputArea: null,
            outputArea: null,
            validator: null,
            printer: null,
            minifier: null,
            highlighter: null,
            clipboard: null,
            copyButton: null,
            formatButtons: null,
            indentSlider: null,
            statusIndicator: null,
            errorDisplay: null
        };
        
        this.emit('ui:components:initialized', this.components);
    }
    
    // Setup event listeners for UI interactions
    setupEventListeners() {
        // Input event listeners
        this.on('input:change', (data) => this.handleInputChange(data));
        this.on('input:focus', () => this.handleInputFocus());
        this.on('input:blur', () => this.handleInputBlur());
        
        // Button click event listeners
        this.on('button:click:copy', () => this.handleCopyClick());
        this.on('button:click:format:pretty', () => this.handleFormatPrettyClick());
        this.on('button:click:format:minify', () => this.handleFormatMinifyClick());
        
        // Control event listeners
        this.on('control:indent:change', (data) => this.handleIndentChange(data));
        this.on('control:validation:toggle', (data) => this.handleValidationToggle(data));
        
        // Error and warning event listeners
        this.on('error:display', (data) => this.handleErrorDisplay(data));
        this.on('warning:display', (data) => this.handleWarningDisplay(data));
    }
    
    // Handle input changes with real-time validation
    handleInputChange(data) {
        const { input } = data;
        this.state.input = input;
        
        if (this.options.enableRealTimeValidation) {
            this.validateAndUpdateUI(input);
        } else {
            this.setValidity(false);
            this.clearOutput();
        }
    }
    
    // Handle input focus
    handleInputFocus() {
        this.clearErrorDisplay();
        this.emit('ui:input:focus');
    }
    
    // Handle input blur
    handleInputBlur() {
        this.emit('ui:input:blur');
    }
    
    // Handle copy button click
    handleCopyClick() {
        if (!this.state.isValid || !this.state.lastResult) {
            this.showError('No valid JSON to copy');
            return;
        }
        
        this.setCopying(true);
        
        try {
            this.components.clipboard.copyToClipboard(this.state.lastResult, {
                showFeedback: this.options.enableCopyFeedback,
                feedbackElement: this.components.copyButton,
                fallbackMethod: 'textarea'
            }).then(result => {
                this.setCopying(false);
                this.setCopied(true);
                this.emit('ui:copy:success', { result, text: this.state.lastResult });
                
                setTimeout(() => {
                    this.setCopied(false);
                }, 2000);
            }).catch(error => {
                this.setCopying(false);
                this.showError('Failed to copy to clipboard');
                this.emit('ui:copy:error', error);
            });
        } catch (error) {
            this.setCopying(false);
            this.showError('Copy operation failed');
        }
    }
    
    // Handle pretty format button click
    handleFormatPrettyClick() {
        this.processJSON(this.state.input, 'pretty', {
            indentLevel: this.state.currentIndent
        });
    }
    
    // Handle minify format button click
    handleFormatMinifyClick() {
        this.processJSON(this.state.input, 'minify');
    }
    
    // Handle indent control change
    handleIndentChange(data) {
        const { indentLevel } = data;
        this.state.currentIndent = indentLevel;
        
        if (this.state.input && this.state.isValid) {
            this.processJSON(this.state.input, 'pretty', {
                indentLevel: indentLevel
            });
        }
    }
    
    // Handle validation toggle
    handleValidationToggle(data) {
        const { enabled } = data;
        this.options.enableRealTimeValidation = enabled;
        
        if (this.options.enableRealTimeValidation) {
            this.validateAndUpdateUI(this.state.input);
        } else {
            this.clearOutput();
        }
    }
    
    // Handle error display
    handleErrorDisplay(data) {
        const { message, type, position } = data;
        this.showError(message, type, position);
    }
    
    // Handle warning display
    handleWarningDisplay(data) {
        const { message, type } = data;
        this.showWarning(message, type);
    }
    
    // Core processing function
    processJSON(input, format, options = {}) {
        if (!input.trim()) {
            this.clearOutput();
            return;
        }
        
        this.setProcessing(true);
        this.emit('ui:processing:start', { input, format, options });
        
        const formatter = require('./core');
        const core = new formatter.JSONFormatterCore({
            indentLevel: this.options.defaultIndent,
            enableValidation: this.options.enableRealTimeValidation,
            enableHighlighting: this.options.enableErrorHighlighting,
            enableSecurity: true
        });
        
        core.format(input, formatOptions = {
            format: format,
            indentLevel: options.indentLevel || this.state.currentIndent
        }).then(result => {
            this.setProcessing(false);
            this.state.isValid = true;
            this.state.lastResult = result.result;
            
            this.updateOutput(result.result);
            this.emit('ui:processing:complete', result);
        }).catch(error => {
            this.setProcessing(false);
            this.state.isValid = false;
            this.emit('ui:processing:error', error);
        });
    }
    
    // Real-time validation
    validateAndUpdateUI(input) {
        const formatter = require('./core');
        const core = new formatter.JSONFormatterCore({
            enableValidation: true,
            enableHighlighting: this.options.enableErrorHighlighting
        });
        
        core.validate(input).then(result => {
            this.state.isValid = result.valid;
            this.state.errorCount = result.errors ? result.errors.length : 0;
            
            if (result.valid) {
                this.updateOutput(this.state.input);
                this.clearErrorDisplay();
            } else {
                this.showError(`Invalid JSON: ${this.state.errorCount} error(s) found`, 'validation', {
                    errors: result.errors
                });
            }
        }).catch(error => {
            this.state.isValid = false;
            this.showError(`Validation error: ${error.message}`, 'validation_error');
        });
    }
    
    // UI update functions
    updateOutput(formattedText) {
        if (this.components.outputArea) {
            this.components.outputArea.value = formattedText;
            this.emit('ui:output:updated', { text: formattedText });
        }
    }
    
    clearOutput() {
        if (this.components.outputArea) {
            this.components.outputArea.value = '';
            this.emit('ui:output:cleared');
        }
    }
    
    setValidity(isValid) {
        this.state.isValid = isValid;
        this.updateStatusIndicator();
        this.emit('ui:validity:changed', { isValid });
    }
    
    setProcessing(isProcessing) {
        this.state.isProcessing = isProcessing;
        this.updateStatusIndicator();
        this.emit('ui:processing:changed', { isProcessing });
    }
    
    setCopied(isCopied) {
        this.state.copied = isCopied;
        this.updateCopyButton();
        this.emit('ui:copied:changed', { isCopied });
    }
    
    showError(message, type = 'error', position = null) {
        this.clearErrorDisplay();
        if (this.components.errorDisplay) {
            this.components.errorDisplay.textContent = message;
            this.components.errorDisplay.className = `error-display error-${type}`;
            this.components.errorDisplay.style.display = 'block';
            
            if (position) {
                this.scrollToError(position);
            }
        }
        this.emit('error:displayed', { message, type, position });
    }
    
    showWarning(message, type = 'warning') {
        if (this.components.errorDisplay) {
            this.components.errorDisplay.textContent = message;
            this.components.errorDisplay.className = `error-display warning-${type}`;
            this.components.errorDisplay.style.display = 'block';
        }
        this.emit('warning:displayed', { message, type });
    }
    
    clearErrorDisplay() {
        if (this.components.errorDisplay) {
            this.components.errorDisplay.style.display = 'none';
            this.components.errorDisplay.textContent = '';
        }
    }
    
    updateStatusIndicator() {
        if (this.components.statusIndicator) {
            const status = this.getStatus();
            this.components.statusIndicator.className = `status-indicator ${status.statusClass}`;
            this.components.statusIndicator.title = status.statusText;
        }
    }
    
    updateCopyButton() {
        if (this.components.copyButton) {
            if (this.state.copied) {
                this.components.copyButton.textContent = '✓ Copied';
                this.components.copyButton.classList.add('copied');
            } else {
                this.components.copyButton.textContent = 'Copy';
                this.components.copyButton.classList.remove('copied');
            }
        }
    }
    
    scrollToError(position) {
        // Implementation for scrolling to error position
        console.log('Scrolling to error at position:', position);
    }
    
    getStatus() {
        if (this.state.isProcessing) {
            return {
                status: 'processing',
                statusClass: 'status-processing',
                statusText: 'Processing JSON...'
            };
        }
        
        if (this.state.errorCount > 0) {
            return {
                status: 'error',
                statusClass: 'status-error',
                statusText: `${this.state.errorCount} error(s) found`
            };
        }
        
        if (this.state.isValid) {
            return {
                status: 'valid',
                statusClass: 'status-valid',
                statusText: 'Valid JSON'
            };
        }
        
        return {
            status: 'invalid',
            statusClass: 'status-invalid',
            statusText: 'Invalid JSON'
        };
    }
    
    // Public API methods
    setInputComponent(element) {
        this.components.inputArea = element;
        this.setupInputEventListeners();
    }
    
    setOutputComponent(element) {
        this.components.outputArea = element;
    }
    
    setCopyButton(element) {
        this.components.copyButton = element;
        this.setupCopyButtonEventListeners();
    }
    
    setFormatButtons(elements) {
        this.components.formatButtons = elements;
        this.setupFormatButtonEventListeners();
    }
    
    setIndentSlider(element) {
        this.components.indentSlider = element;
        this.setupIndentSliderEventListeners();
    }
    
    setStatusIndicator(element) {
        this.components.statusIndicator = element;
        this.updateStatusIndicator();
    }
    
    setErrorDisplay(element) {
        this.components.errorDisplay = element;
        this.clearErrorDisplay();
    }
    
    setupInputEventListeners() {
        if (this.components.inputArea) {
            this.components.inputArea.addEventListener('input', (e) => {
                this.emit('input:change', { input: e.target.value });
            });
            
            this.components.inputArea.addEventListener('focus', () => {
                this.emit('input:focus');
            });
            
            this.components.inputArea.addEventListener('blur', () => {
                this.emit('input:blur');
            });
        }
    }
    
    setupCopyButtonEventListeners() {
        if (this.components.copyButton) {
            this.components.copyButton.addEventListener('click', () => {
                this.emit('button:click:copy');
            });
        }
    }
    
    setupFormatButtonEventListeners() {
        if (this.components.formatButtons) {
            Array.from(this.components.formatButtons).forEach(button => {
                button.addEventListener('click', (e) => {
                    const format = button.dataset.format;
                    if (format === 'pretty') {
                        this.emit('button:click:format:pretty');
                    } else if (format === 'minify') {
                        this.emit('button:click:format:minify');
                    }
                });
            });
        }
    }
    
    setupIndentSliderEventListeners() {
        if (this.components.indentSlider) {
            this.components.indentSlider.addEventListener('input', (e) => {
                this.emit('control:indent:change', {
                    indentLevel: parseInt(e.target.value)
                });
            });
        }
    }
    
    setupValidationToggleEventListeners() {
        // Validation toggle setup (assuming there's a checkbox or similar)
        console.log('Validation toggle event listeners setup');
    }
    
    // Export/Import functionality
    exportConfig() {
        return {
            theme: this.options.theme,
            defaultIndent: this.options.defaultIndent,
            input: this.state.input,
            lastResult: this.state.lastResult,
            timestamp: Date.now()
        };
    }
    
    importConfig(config) {
        this.options = { ...this.options, ...config };
        this.state.input = config.input || '';
        this.state.lastResult = config.lastResult || null;
        
        if (this.components.inputArea && config.input !== undefined) {
            this.components.inputArea.value = config.input;
        }
        
        if (this.state.input && config.input !== undefined) {
            this.validateAndUpdateUI(this.state.input);
        }
    }
    
    // Theme management
    setTheme(theme) {
        this.options.theme = theme;
        this.emit('ui:theme:changed', { theme });
    }
    
    getTheme() {
        return this.options.theme;
    }
    
    // Clear all data
    clear() {
        this.state.input = '';
        this.state.lastResult = null;
        this.state.isValid = false;
        this.state.errorCount = 0;
        
        this.clearOutput();
        this.clearErrorDisplay();
        
        if (this.components.inputArea) {
            this.components.inputArea.value = '';
        }
        
        this.emit('ui:cleared');
    }
    
    // Get current state
    getState() {
        return { ...this.state };
    }
    
    // Get current options
    getOptions() {
        return { ...this.options };
    }
}

module.exports = {
    JSONFormatterUI
};