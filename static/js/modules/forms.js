/**
 * Form Management Module - Handles form validation and submission
 * Professional validation with real-time feedback
 */

class FormManager {
    constructor() {
        this.validators = new Map();
        this.init();
    }

    /**
     * Initialize form management systems
     */
    init() {
        this.setupFormValidation();
        this.setupRealTimeValidation();
        this.setupFileUploadHandling();
        this.setupFormSubmissionHandlers();
    }

    /**
     * Set up comprehensive form validation
     */
    setupFormValidation() {
        // URL validation patterns
        this.validators.set('url', {
            pattern: /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/,
            message: 'Please enter a valid URL (e.g., example.com or https://example.com)'
        });

        // Email validation patterns
        this.validators.set('email', {
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: 'Please enter a valid email address'
        });

        // Apply validation to all forms
        document.querySelectorAll('form').forEach(form => {
            this.attachFormValidation(form);
        });
    }

    /**
     * Attach validation to specific form
     */
    attachFormValidation(form) {
        const inputs = form.querySelectorAll('input[data-validate], textarea[data-validate]');
        
        inputs.forEach(input => {
            const validationType = input.getAttribute('data-validate');
            
            // Real-time validation on input
            input.addEventListener('input', () => {
                this.validateField(input, validationType);
            });

            // Validation on blur
            input.addEventListener('blur', () => {
                this.validateField(input, validationType);
            });
        });

        // Form submission validation
        form.addEventListener('submit', (e) => {
            if (!this.validateForm(form)) {
                e.preventDefault();
                return false;
            }
        });
    }

    /**
     * Validate individual field
     */
    validateField(field, type) {
        const value = field.value.trim();
        const validator = this.validators.get(type);
        
        if (!validator) return true;

        const isValid = validator.pattern.test(value) || value === '';
        
        // Update field styling
        field.classList.toggle('is-invalid', !isValid && value !== '');
        field.classList.toggle('is-valid', isValid && value !== '');

        // Show/hide error message
        this.updateFieldMessage(field, isValid ? '' : validator.message);
        
        return isValid;
    }

    /**
     * Update field validation message
     */
    updateFieldMessage(field, message) {
        let messageEl = field.parentNode.querySelector('.invalid-feedback');
        
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.className = 'invalid-feedback';
            field.parentNode.appendChild(messageEl);
        }
        
        messageEl.textContent = message;
    }

    /**
     * Validate entire form
     */
    validateForm(form) {
        const inputs = form.querySelectorAll('input[data-validate], textarea[data-validate]');
        let isValid = true;

        inputs.forEach(input => {
            const validationType = input.getAttribute('data-validate');
            if (!this.validateField(input, validationType)) {
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Set up real-time validation feedback
     */
    setupRealTimeValidation() {
        // Content type switcher validation
        const contentTypeRadios = document.querySelectorAll('input[name="input_type"]');
        const contentInput = document.querySelector('#content');

        if (contentInput && contentTypeRadios.length > 0) {
            contentTypeRadios.forEach(radio => {
                radio.addEventListener('change', () => {
                    const selectedType = radio.value;
                    contentInput.setAttribute('data-validate', selectedType);
                    this.updateInputPlaceholder(contentInput, selectedType);
                });
            });
        }
    }

    /**
     * Update input placeholder based on content type
     */
    updateInputPlaceholder(input, type) {
        const placeholders = {
            'url': 'Enter URL (e.g., https://example.com)',
            'email': 'Enter email content or forward the email',
            'message': 'Enter message or text content to analyze'
        };

        input.placeholder = placeholders[type] || 'Enter content to analyze';
    }

    /**
     * Set up file upload handling with progress
     */
    setupFileUploadHandling() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.handleFileUpload(e.target);
            });
        });
    }

    /**
     * Handle file upload with validation and preview
     */
    handleFileUpload(input) {
        const file = input.files[0];
        if (!file) return;

        // File size validation (500MB max)
        const maxSize = 500 * 1024 * 1024; // 500MB
        if (file.size > maxSize) {
            this.showFileError(input, 'File size must be less than 500MB');
            input.value = '';
            return;
        }

        // File type validation
        const allowedTypes = {
            'image': ['image/jpeg', 'image/png', 'image/gif'],
            'video': ['video/mp4', 'video/avi', 'video/mov'],
            'audio': ['audio/mp3', 'audio/wav', 'audio/mpeg'],
            'document': ['text/plain', 'application/pdf']
        };

        const isValidType = Object.values(allowedTypes).some(types => 
            types.includes(file.type)
        );

        if (!isValidType) {
            this.showFileError(input, 'Please select a valid file type');
            input.value = '';
            return;
        }

        // Show file preview
        this.showFilePreview(input, file);
    }

    /**
     * Show file error message
     */
    showFileError(input, message) {
        this.updateFieldMessage(input, message);
        input.classList.add('is-invalid');
    }

    /**
     * Show file preview
     */
    showFilePreview(input, file) {
        const previewContainer = input.parentNode.querySelector('.file-preview') || 
                               this.createFilePreviewContainer(input);

        const fileInfo = `
            <div class="file-info">
                <i class="bi bi-file-earmark"></i>
                <span class="file-name">${file.name}</span>
                <span class="file-size">(${this.formatFileSize(file.size)})</span>
                <button type="button" class="btn btn-sm btn-outline-danger" onclick="this.closest('.file-preview').remove(); document.querySelector('#${input.id}').value = '';">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        `;

        previewContainer.innerHTML = fileInfo;
        input.classList.add('is-valid');
    }

    /**
     * Create file preview container
     */
    createFilePreviewContainer(input) {
        const container = document.createElement('div');
        container.className = 'file-preview mt-2';
        input.parentNode.appendChild(container);
        return container;
    }

    /**
     * Format file size for display
     */
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Set up form submission handlers with loading states
     */
    setupFormSubmissionHandlers() {
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmission(form);
            });
        });
    }

    /**
     * Handle form submission with loading state
     */
    handleFormSubmission(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            // Show loading state
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="bi bi-arrow-clockwise spin"></i> Analyzing...';
            submitBtn.disabled = true;

            // Reset button after form processing (fallback)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 10000);
        }
    }
}

// Export for use in main application
window.FormManager = FormManager;