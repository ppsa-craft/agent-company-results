// JSON Formatter - Core Orchestration Module
// Event-driven architecture coordinating all JSON formatting components

const { EventEmitter } = require('events');

class JSONFormatterCore extends EventEmitter {
    constructor(options = {}) {
        super();
        this.options = {
            indentLevel: options.indentLevel || 2,
            enableValidation: options.enableValidation !== false,
            enableHighlighting: options.enableHighlighting !== false,
            enableSecurity: options.enableSecurity !== false,
            ...options
        };
        
        this.components = {};
        this.initializeComponents();
        this.setupEventHandling();
    }
    
    // Initialize all core components
    initializeComponents() {
        const validator = require('./validator');
        const printer = require('./printer');
        const minifier = require('./minifier');
        const highlighter = require('./highlighter');
        const clipboard = require('./clipboard');
        
        this.components = {
            validator,
            printer,
            minifier,
            highlighter,
            clipboard
        };
        
        this.emit('components:initialized', this.components);
    }
    
    // Setup event-driven architecture
    setupEventHandling() {
        // Process input events
        this.on('process:input', (data) => this.handleInputProcessing(data));
        this.on('process:format', (data) => this.handleFormatProcessing(data));
        this.on('process:validate', (data) => this.handleValidationProcessing(data));
        this.on('process:copy', (data) => this.handleCopyProcessing(data));
        
        // Error handling events
        this.on('error', (error) => this.handleError(error));
        this.on('warning', (warning) => this.handleWarning(warning));
        
        // Progress tracking events
        this.on('progress', (progress) => this.handleProgress(progress));
    }
    
    // Handle input processing pipeline
    handleInputProcessing(data) {
        const { input, format, onProgress } = data;
        
        if (this.options.enableValidation) {
            this.emit('validation:start', { input });
            
            try {
                const validationResult = this.components.validator.validateJSON(input);
                this.emit('validation:complete', validationResult);
                
                if (!validationResult.valid) {
                    this.emit('error', {
                        type: 'validation_error',
                        message: 'Invalid JSON input',
                        errors: validationResult.errors,
                        input: input
                    });
                    
                    if (this.options.enableHighlighting) {
                        this.emit('highlight:errors', validationResult);
                    }
                }
                
                if (validationResult.valid) {
                    if (format === 'pretty') {
                        this.emit('format:pretty', { input, options: data.options });
                    } else if (format === 'minify') {
                        this.emit('format:minify', { input, options: data.options });
                    } else {
                        this.emit('format:default', { input, options: data.options });
                    }
                }
            } catch (error) {
                this.emit('error', {
                    type: 'processing_error',
                    message: error.message,
                    input: input
                });
            }
        } else {
            // Skip validation and process directly
            if (format === 'pretty') {
                this.emit('format:pretty', { input, options: data.options });
            } else if (format === 'minify') {
                this.emit('format:minify', { input, options: data.options });
            }
        }
    }
    
    // Handle formatting processing
    handleFormatProcessing(data) {
        const { input, options = {} } = data;
        
        try {
            if (options.format === 'pretty') {
                const indent = options.indentLevel || this.options.indentLevel;
                const formatted = this.components.printer.printJSON(input, indent);
                this.emit('format:complete', {
                    type: 'pretty',
                    result: formatted,
                    input: input,
                    options: options
                });
            } else if (options.format === 'minify') {
                const minified = this.components.minifier.minifyJSON(input);
                this.emit('format:complete', {
                    type: 'minify',
                    result: minified,
                    input: input,
                    options: options
                });
            }
        } catch (error) {
            this.emit('error', {
                type: 'format_error',
                message: error.message,
                input: input,
                options: options
            });
        }
    }
    
    // Handle validation processing
    handleValidationProcessing(data) {
        const { input, options = {} } = data;
        
        try {
            const validationResult = this.components.validator.validateJSON(input);
            this.emit('validation:complete', validationResult);
            
            if (!validationResult.valid && this.options.enableHighlighting) {
                const highlightResult = this.components.highlighter.highlightErrors(input, validationResult);
                this.emit('highlight:errors', highlightResult);
            }
        } catch (error) {
            this.emit('error', {
                type: 'validation_processing_error',
                message: error.message,
                input: input
            });
        }
    }
    
    // Handle copy processing
    handleCopyProcessing(data) {
        const { text, options = {} } = data;
        
        try {
            this.components.clipboard.copyToClipboard(text, {
                showFeedback: options.showFeedback !== false,
                feedbackElement: options.feedbackElement,
                fallbackMethod: options.fallbackMethod || 'textarea'
            }).then(result => {
                this.emit('copy:complete', {
                    success: true,
                    result: result,
                    text: text,
                    options: options
                });
            }).catch(error => {
                this.emit('error', {
                    type: 'copy_error',
                    message: error.message,
                    text: text
                });
            });
        } catch (error) {
            this.emit('error', {
                type: 'copy_processing_error',
                message: error.message,
                text: text
            });
        }
    }
    
    // Handle errors
    handleError(error) {
        console.error('JSON Formatter Core Error:', error);
        this.emit('ui:error', error);
    }
    
    // Handle warnings
    handleWarning(warning) {
        console.warn('JSON Formatter Core Warning:', warning);
        this.emit('ui:warning', warning);
    }
    
    // Handle progress updates
    handleProgress(progress) {
        this.emit('ui:progress', progress);
    }
    
    // Public API methods
    format(input, formatOptions = {}) {
        return new Promise((resolve, reject) => {
            const processId = Date.now();
            
            const processData = {
                input: input,
                format: formatOptions.format || 'default',
                options: formatOptions,
                onProgress: (progress) => {
                    this.emit('progress', {
                        processId,
                        type: 'format',
                        ...progress
                    });
                }
            };
            
            const timeout = setTimeout(() => {
                reject(new Error('Processing timeout'));
            }, 30000); // 30 second timeout
            
            const handler = (result) => {
                clearTimeout(timeout);
                this.off('format:complete', handler);
                this.off('error', errorHandler);
                resolve(result);
            };
            
            const errorHandler = (error) => {
                clearTimeout(timeout);
                this.off('format:complete', handler);
                this.off('error', errorHandler);
                reject(error);
            };
            
            this.on('format:complete', handler);
            this.on('error', errorHandler);
            
            this.emit('process:format', processData);
        });
    }
    
    validate(input) {
        return new Promise((resolve, reject) => {
            const processId = Date.now();
            
            const processData = {
                input: input
            };
            
            const timeout = setTimeout(() => {
                reject(new Error('Validation timeout'));
            }, 10000); // 10 second timeout
            
            const handler = (result) => {
                clearTimeout(timeout);
                this.off('validation:complete', handler);
                this.off('error', errorHandler);
                resolve(result);
            };
            
            const errorHandler = (error) => {
                clearTimeout(timeout);
                this.off('validation:complete', handler);
                this.off('error', errorHandler);
                reject(error);
            };
            
            this.on('validation:complete', handler);
            this.on('error', errorHandler);
            
            this.emit('process:validate', processData);
        });
    }
    
    copy(text, options = {}) {
        return new Promise((resolve, reject) => {
            const processId = Date.now();
            
            const processData = {
                text: text,
                options: options
            };
            
            const timeout = setTimeout(() => {
                reject(new Error('Copy operation timeout'));
            }, 10000); // 10 second timeout
            
            const handler = (result) => {
                clearTimeout(timeout);
                this.off('copy:complete', handler);
                this.off('error', errorHandler);
                resolve(result);
            };
            
            const errorHandler = (error) => {
                clearTimeout(timeout);
                this.off('copy:complete', handler);
                this.off('error', errorHandler);
                reject(error);
            };
            
            this.on('copy:complete', handler);
            this.on('error', errorHandler);
            
            this.emit('process:copy', processData);
        });
    }
    
    // Get component status
    getStatus() {
        return {
            components: Object.keys(this.components),
            options: this.options,
            eventCount: this.eventNames().length
        };
    }
}

module.exports = {
    JSONFormatterCore
};