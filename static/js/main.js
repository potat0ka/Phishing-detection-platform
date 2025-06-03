/**
 * AI Phishing Detector - Main JavaScript File
 * Handles interactive features, animations, and user experience enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Phishing Detector initialized');
    
    // Initialize all components
    initializeAnimations();
    initializeFormValidations();
    initializeTooltips();
    initializeLoadingStates();
    initializeThemeSupport();
    initializeMobileOptimizations();
    initializeAnalyticsTracking();
});

/**
 * Initialize CSS animations and scroll-triggered effects
 */
function initializeAnimations() {
    // Intersection Observer for scroll animations
    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Special handling for statistics counters
                if (entry.target.classList.contains('stat-number')) {
                    animateCounter(entry.target);
                }
                
                // Special handling for progress bars
                if (entry.target.classList.contains('progress-bar')) {
                    animateProgressBar(entry.target);
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .tip-card, .stat-item, .card').forEach(el => {
        animationObserver.observe(el);
    });

    // Initialize hero animations
    initializeHeroAnimations();
}

/**
 * Initialize hero section animations
 */
function initializeHeroAnimations() {
    const hero = document.querySelector('.hero-section');
    if (!hero) return;

    // Stagger animation for hero elements
    const heroElements = hero.querySelectorAll('.fade-in > *');
    heroElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 200);
    });

    // Pulse animation for security shield
    const shield = document.querySelector('.shield-icon');
    if (shield) {
        shield.addEventListener('mouseenter', () => {
            shield.style.animation = 'float 1s ease-in-out, glow 2s ease-in-out';
        });
        
        shield.addEventListener('mouseleave', () => {
            shield.style.animation = 'float 3s ease-in-out infinite';
        });
    }
}

/**
 * Animate counter numbers
 */
function animateCounter(element) {
    const target = element.textContent;
    const isPercentage = target.includes('%');
    const numericValue = parseFloat(target.replace(/[^\d.]/g, ''));
    
    if (isNaN(numericValue)) return;
    
    let current = 0;
    const increment = numericValue / 50; // 50 steps
    const duration = 2000; // 2 seconds
    const stepTime = duration / 50;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= numericValue) {
            current = numericValue;
            clearInterval(timer);
        }
        
        let displayValue = Math.round(current * 10) / 10;
        if (isPercentage) {
            element.textContent = displayValue + '%';
        } else if (target.includes('B')) {
            element.textContent = displayValue + 'B';
        } else if (target.includes('M')) {
            element.textContent = '$' + displayValue + 'M';
        } else if (target.includes('s')) {
            element.textContent = '< ' + Math.round(displayValue) + 's';
        } else {
            element.textContent = displayValue;
        }
    }, stepTime);
}

/**
 * Animate progress bars
 */
function animateProgressBar(progressBar) {
    const width = progressBar.style.width;
    progressBar.style.width = '0%';
    progressBar.style.transition = 'width 2s ease-in-out';
    
    setTimeout(() => {
        progressBar.style.width = width;
    }, 100);
}

/**
 * Initialize form validations and interactions
 */
function initializeFormValidations() {
    // Real-time form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmission);
        
        // Add real-time validation to inputs
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', debounce(validateField, 300));
        });
    });

    // Password strength indicator
    const passwordField = document.querySelector('input[name="password"]');
    if (passwordField) {
        initializePasswordStrength(passwordField);
    }

    // Email validation
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('input', validateEmail);
    });

    // Content type switcher for detection form
    initializeContentTypeSwitcher();
}

/**
 * Handle form submission with loading states
 */
function handleFormSubmission(event) {
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    if (!submitButton) return;
    
    // Show loading state
    showLoadingState(submitButton);
    
    // Validate form before submission
    const isValid = validateForm(form);
    if (!isValid) {
        hideLoadingState(submitButton);
        event.preventDefault();
        return false;
    }
    
    // Add form data validation for detection form
    if (form.action.includes('/check')) {
        const contentField = form.querySelector('[name="input_content"]');
        if (contentField && !validateContent(contentField.value, form.querySelector('[name="input_type"]:checked')?.value)) {
            hideLoadingState(submitButton);
            event.preventDefault();
            showAlert('Please provide valid content for analysis.', 'warning');
            return false;
        }
    }
}

/**
 * Show loading state on button
 */
function showLoadingState(button) {
    const originalText = button.querySelector('.btn-text')?.textContent || button.textContent;
    button.dataset.originalText = originalText;
    
    const spinner = button.querySelector('.spinner-border');
    if (spinner) {
        spinner.classList.remove('d-none');
    } else {
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Processing...
        `;
    }
    
    button.disabled = true;
}

/**
 * Hide loading state on button
 */
function hideLoadingState(button) {
    const originalText = button.dataset.originalText;
    if (originalText) {
        button.innerHTML = originalText;
    }
    
    const spinner = button.querySelector('.spinner-border');
    if (spinner) {
        spinner.classList.add('d-none');
    }
    
    button.disabled = false;
}

/**
 * Validate individual form field
 */
function validateField(event) {
    const field = event.target;
    const value = field.value.trim();
    
    // Clear previous validation
    clearFieldValidation(field);
    
    let isValid = true;
    let message = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required.';
    }
    
    // Specific field validations
    switch (field.type) {
        case 'email':
            if (value && !isValidEmail(value)) {
                isValid = false;
                message = 'Please enter a valid email address.';
            }
            break;
            
        case 'password':
            if (value && value.length < 6) {
                isValid = false;
                message = 'Password must be at least 6 characters long.';
            }
            break;
            
        case 'text':
            if (field.name === 'username' && value && value.length < 3) {
                isValid = false;
                message = 'Username must be at least 3 characters long.';
            }
            break;
    }
    
    // Show validation result
    if (!isValid) {
        showFieldError(field, message);
    } else if (value) {
        showFieldSuccess(field);
    }
    
    return isValid;
}

/**
 * Show field validation error
 */
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.appendChild(feedback);
    }
    feedback.textContent = message;
}

/**
 * Show field validation success
 */
function showFieldSuccess(field) {
    field.classList.add('is-valid');
    field.classList.remove('is-invalid');
    
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

/**
 * Clear field validation
 */
function clearFieldValidation(field) {
    field.classList.remove('is-valid', 'is-invalid');
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.remove();
    }
}

/**
 * Initialize password strength indicator
 */
function initializePasswordStrength(passwordField) {
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength mt-2';
    strengthIndicator.innerHTML = `
        <div class="progress" style="height: 4px;">
            <div class="progress-bar" role="progressbar" style="width: 0%"></div>
        </div>
        <small class="text-muted mt-1 d-block">Password strength: <span class="strength-text">None</span></small>
    `;
    passwordField.parentNode.appendChild(strengthIndicator);
    
    passwordField.addEventListener('input', function() {
        const strength = calculatePasswordStrength(this.value);
        updatePasswordStrength(strengthIndicator, strength);
    });
}

/**
 * Calculate password strength
 */
function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = [];
    
    if (password.length >= 8) score += 25;
    else feedback.push('8+ characters');
    
    if (/[a-z]/.test(password)) score += 25;
    else feedback.push('lowercase letter');
    
    if (/[A-Z]/.test(password)) score += 25;
    else feedback.push('uppercase letter');
    
    if (/[0-9]/.test(password)) score += 25;
    else feedback.push('number');
    
    if (/[^a-zA-Z0-9]/.test(password)) score += 25;
    else feedback.push('special character');
    
    let level = 'Weak';
    let className = 'bg-danger';
    
    if (score >= 75) {
        level = 'Strong';
        className = 'bg-success';
    } else if (score >= 50) {
        level = 'Medium';
        className = 'bg-warning';
    } else if (score >= 25) {
        level = 'Fair';
        className = 'bg-info';
    }
    
    return { score, level, className, feedback };
}

/**
 * Update password strength display
 */
function updatePasswordStrength(container, strength) {
    const progressBar = container.querySelector('.progress-bar');
    const strengthText = container.querySelector('.strength-text');
    
    progressBar.style.width = strength.score + '%';
    progressBar.className = `progress-bar ${strength.className}`;
    strengthText.textContent = strength.level;
    
    if (strength.feedback.length > 0) {
        strengthText.textContent += ` (needs: ${strength.feedback.join(', ')})`;
    }
}

/**
 * Initialize content type switcher for detection form
 */
function initializeContentTypeSwitcher() {
    const typeRadios = document.querySelectorAll('input[name="input_type"]');
    const contentTextarea = document.querySelector('#input_content');
    
    if (!typeRadios.length || !contentTextarea) return;
    
    const placeholders = {
        'url': 'Paste the website URL here (e.g., https://example.com/suspicious-link)',
        'email': 'Paste the email content here, including subject line and body text...',
        'message': 'Paste the message or text content here that you want to analyze...'
    };
    
    typeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            contentTextarea.placeholder = placeholders[this.value];
            contentTextarea.focus();
            
            // Update help text based on type
            updateDetectionHelp(this.value);
        });
    });
}

/**
 * Update detection help based on content type
 */
function updateDetectionHelp(type) {
    const helpTexts = {
        'url': 'The AI will analyze the URL structure, domain reputation, and suspicious patterns.',
        'email': 'The AI will examine the sender, content patterns, language, and embedded links.',
        'message': 'The AI will analyze text patterns, sentiment, and potential manipulation tactics.'
    };
    
    const helpElement = document.querySelector('.form-text');
    if (helpElement) {
        helpElement.innerHTML = `<i class="fas fa-info-circle me-1"></i>${helpTexts[type]}`;
    }
}

/**
 * Initialize tooltips and popovers
 */
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add custom tooltips for security features
    addSecurityTooltips();
}

/**
 * Add custom security tooltips
 */
function addSecurityTooltips() {
    const securityElements = document.querySelectorAll('.fas.fa-shield-alt, .fas.fa-lock, .fas.fa-user-secret');
    securityElements.forEach(element => {
        if (!element.hasAttribute('title')) {
            element.setAttribute('title', 'Security feature enabled');
            element.setAttribute('data-bs-toggle', 'tooltip');
            new bootstrap.Tooltip(element);
        }
    });
}

/**
 * Initialize loading states and progress indicators
 */
function initializeLoadingStates() {
    // Global loading overlay
    window.showGlobalLoading = function(message = 'Processing...') {
        let overlay = document.getElementById('globalLoadingOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'globalLoadingOverlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="text-center text-white">
                    <div class="loading-spinner mb-3"></div>
                    <h5 class="loading-message">${message}</h5>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        overlay.style.display = 'flex';
    };
    
    window.hideGlobalLoading = function() {
        const overlay = document.getElementById('globalLoadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    };
    
    // Auto-hide loading on page load
    window.addEventListener('load', function() {
        hideGlobalLoading();
    });
}

/**
 * Initialize theme support and dark mode enhancements
 */
function initializeThemeSupport() {
    // Detect system theme preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Listen for theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        updateThemeElements(e.matches);
    });
    
    // Update theme-specific elements
    updateThemeElements(prefersDark);
}

/**
 * Update theme-specific elements
 */
function updateThemeElements(isDark) {
    const charts = document.querySelectorAll('canvas');
    charts.forEach(chart => {
        // Update chart colors if Chart.js is available
        if (typeof Chart !== 'undefined' && chart.chart) {
            chart.chart.options.plugins.legend.labels.color = isDark ? '#ffffff' : '#000000';
            chart.chart.update();
        }
    });
}

/**
 * Initialize mobile optimizations
 */
function initializeMobileOptimizations() {
    // Touch-friendly interactions
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // Improve touch targets
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
    }
    
    // Responsive table handling
    const tables = document.querySelectorAll('.table-responsive table');
    tables.forEach(table => {
        if (window.innerWidth < 768) {
            makeTableMobileFriendly(table);
        }
    });
    
    // Mobile-specific animations
    if (window.innerWidth < 768) {
        // Reduce animation complexity on mobile
        document.documentElement.style.setProperty('--animation-duration', '0.3s');
    }
    
    // Handle orientation changes
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            // Recalculate layouts after orientation change
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });
}

/**
 * Make table mobile-friendly
 */
function makeTableMobileFriendly(table) {
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
            if (headers[index]) {
                cell.setAttribute('data-label', headers[index]);
            }
        });
    });
    
    table.classList.add('mobile-table');
}

/**
 * Initialize analytics and usage tracking
 */
function initializeAnalyticsTracking() {
    // Track user interactions (privacy-respecting)
    const trackEvent = function(category, action, label = '') {
        // In a real implementation, you would send this to your analytics service
        console.log(`Analytics: ${category} - ${action} - ${label}`);
    };
    
    // Track button clicks
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn')) {
            const btnText = e.target.textContent.trim();
            trackEvent('Button', 'Click', btnText);
        }
    });
    
    // Track form submissions
    document.addEventListener('submit', function(e) {
        const form = e.target;
        const formAction = form.action.split('/').pop();
        trackEvent('Form', 'Submit', formAction);
    });
    
    // Track page views
    trackEvent('Page', 'View', window.location.pathname);
}

/**
 * Utility Functions
 */

// Debounce function for performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Content validation for detection
function validateContent(content, type) {
    if (!content || content.trim().length < 5) return false;
    
    switch (type) {
        case 'url':
            try {
                new URL(content);
                return true;
            } catch {
                return /^https?:\/\//.test(content) || /^www\./.test(content);
            }
        case 'email':
        case 'message':
            return content.trim().length >= 10;
        default:
            return true;
    }
}

// Form validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        const fieldValid = validateField({ target: input });
        if (!fieldValid) isValid = false;
    });
    
    return isValid;
}

// Email validation for real-time feedback
function validateEmail(event) {
    const field = event.target;
    const email = field.value.trim();
    
    if (email && !isValidEmail(email)) {
        showFieldError(field, 'Please enter a valid email address');
    } else if (email) {
        showFieldSuccess(field);
    } else {
        clearFieldValidation(field);
    }
}

// Show alert messages
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container') || document.body;
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Smooth scroll to element
function smoothScrollTo(element, offset = 80) {
    const elementPosition = element.offsetTop - offset;
    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });
}

// Copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showAlert('Copied to clipboard!', 'success');
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Export functions for global use
window.PhishingDetector = {
    showAlert,
    smoothScrollTo,
    copyToClipboard,
    formatFileSize,
    showGlobalLoading,
    hideGlobalLoading,
    validateContent,
    isValidEmail
};

// CSS for mobile tables and additional enhancements
const additionalStyles = `
<style>
.mobile-table td {
    display: block;
    text-align: right;
    border: none;
    padding: 0.5rem 1rem;
}

.mobile-table td:before {
    content: attr(data-label) ': ';
    float: left;
    font-weight: bold;
    color: var(--bs-primary);
}

.touch-device .btn:hover {
    transform: none;
}

.password-strength .progress {
    transition: all 0.3s ease;
}

@media (max-width: 767px) {
    .mobile-table thead {
        display: none;
    }
    
    .mobile-table tr {
        display: block;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        overflow: hidden;
    }
}

.animate-in {
    animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
`;

// Inject additional styles
document.head.insertAdjacentHTML('beforeend', additionalStyles);

console.log('AI Phishing Detector JavaScript loaded successfully');
