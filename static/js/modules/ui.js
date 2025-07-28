/**
 * UI Module - Handles user interface interactions and responsive design
 * Professional UI management with mobile optimization
 */

class UIManager {
    constructor() {
        this.isMobile = window.innerWidth < 768;
        this.tooltips = new Map();
        this.init();
    }

    /**
     * Initialize UI management systems
     */
    init() {
        this.setupResponsiveHandlers();
        this.setupTooltips();
        this.setupModals();
        this.setupThemeSupport();
        this.setupMobileOptimizations();
        this.setupLoadingStates();
    }

    /**
     * Set up responsive design handlers
     */
    setupResponsiveHandlers() {
        window.addEventListener('resize', () => {
            this.isMobile = window.innerWidth < 768;
            this.handleResize();
        });

        // Initial setup
        this.handleResize();
    }

    /**
     * Handle window resize events
     */
    handleResize() {
        // Update mobile-specific UI elements
        this.updateNavigation();
        this.updateCardLayouts();
        this.updateFormLayouts();
    }

    /**
     * Update navigation for mobile/desktop
     */
    updateNavigation() {
        const navbar = document.querySelector('.navbar');
        const navToggler = document.querySelector('.navbar-toggler');
        
        if (this.isMobile) {
            navbar?.classList.add('mobile-nav');
            navToggler?.setAttribute('aria-expanded', 'false');
        } else {
            navbar?.classList.remove('mobile-nav');
            // Close mobile menu if open
            const navCollapse = document.querySelector('.navbar-collapse');
            navCollapse?.classList.remove('show');
        }
    }

    /**
     * Update card layouts for responsive design
     */
    updateCardLayouts() {
        const cardColumns = document.querySelectorAll('.card-columns');
        cardColumns.forEach(column => {
            if (this.isMobile) {
                column.style.columnCount = '1';
            } else {
                column.style.columnCount = '';
            }
        });
    }

    /**
     * Update form layouts for mobile
     */
    updateFormLayouts() {
        const forms = document.querySelectorAll('.form-row');
        forms.forEach(form => {
            if (this.isMobile) {
                form.classList.add('mobile-form');
            } else {
                form.classList.remove('mobile-form');
            }
        });
    }

    /**
     * Set up tooltip system
     */
    setupTooltips() {
        // Initialize Bootstrap tooltips if available
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(tooltipTriggerEl => {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }

        // Custom tooltip system for better mobile support
        this.setupCustomTooltips();
    }

    /**
     * Set up custom tooltip system
     */
    setupCustomTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            const tooltipText = element.getAttribute('data-tooltip');
            
            element.addEventListener('mouseenter', (e) => {
                if (!this.isMobile) {
                    this.showTooltip(e.target, tooltipText);
                }
            });

            element.addEventListener('mouseleave', (e) => {
                this.hideTooltip(e.target);
            });

            // Touch support for mobile
            element.addEventListener('touchstart', (e) => {
                if (this.isMobile) {
                    this.toggleTooltip(e.target, tooltipText);
                }
            });
        });
    }

    /**
     * Show custom tooltip
     */
    showTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = text;
        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';

        this.tooltips.set(element, tooltip);
    }

    /**
     * Hide custom tooltip
     */
    hideTooltip(element) {
        const tooltip = this.tooltips.get(element);
        if (tooltip) {
            tooltip.remove();
            this.tooltips.delete(element);
        }
    }

    /**
     * Toggle tooltip for mobile
     */
    toggleTooltip(element, text) {
        if (this.tooltips.has(element)) {
            this.hideTooltip(element);
        } else {
            this.showTooltip(element, text);
        }
    }

    /**
     * Set up modal system
     */
    setupModals() {
        // Custom modal handlers
        document.querySelectorAll('[data-modal]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.getAttribute('data-modal');
                this.openModal(modalId);
            });
        });

        // Close modal handlers
        document.querySelectorAll('.modal-close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.closeModal(closeBtn.closest('.modal'));
            });
        });

        // Close modal on backdrop click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });
    }

    /**
     * Open modal
     */
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
            
            // Focus trap for accessibility
            this.trapFocus(modal);
        }
    }

    /**
     * Close modal
     */
    closeModal(modal) {
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    /**
     * Trap focus within modal for accessibility
     */
    trapFocus(modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }

    /**
     * Set up theme support
     */
    setupThemeSupport() {
        // Detect system theme preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        // Apply theme based on preference or saved setting
        const savedTheme = localStorage.getItem('theme');
        const theme = savedTheme || (prefersDark ? 'dark' : 'light');
        
        this.applyTheme(theme);

        // Theme toggle handlers
        document.querySelectorAll('.theme-toggle').forEach(toggle => {
            toggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        });

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /**
     * Apply theme to document
     */
    applyTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update theme toggle buttons
        document.querySelectorAll('.theme-toggle').forEach(toggle => {
            const icon = toggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon';
            }
        });
    }

    /**
     * Toggle between light and dark themes
     */
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(newTheme);
    }

    /**
     * Set up mobile-specific optimizations
     */
    setupMobileOptimizations() {
        if (this.isMobile) {
            // Add mobile-specific classes
            document.body.classList.add('mobile-device');
            
            // Optimize touch interactions
            this.setupTouchOptimizations();
            
            // Optimize form inputs for mobile
            this.optimizeMobileInputs();
        }
    }

    /**
     * Set up touch optimizations
     */
    setupTouchOptimizations() {
        // Add touch-friendly hover effects
        document.querySelectorAll('.btn, .card, .nav-link').forEach(element => {
            element.addEventListener('touchstart', () => {
                element.classList.add('touch-active');
            });
            
            element.addEventListener('touchend', () => {
                setTimeout(() => {
                    element.classList.remove('touch-active');
                }, 150);
            });
        });

        // Prevent double-tap zoom on buttons
        document.querySelectorAll('button, .btn').forEach(button => {
            button.addEventListener('touchend', (e) => {
                e.preventDefault();
                button.click();
            });
        });
    }

    /**
     * Optimize mobile input interactions
     */
    optimizeMobileInputs() {
        // Improve input focus behavior
        document.querySelectorAll('input, textarea').forEach(input => {
            input.addEventListener('focus', () => {
                // Scroll input into view with padding
                setTimeout(() => {
                    input.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }, 300);
            });
        });
    }

    /**
     * Set up loading state management
     */
    setupLoadingStates() {
        // Global loading overlay
        this.createGlobalLoadingOverlay();
        
        // Loading state for buttons
        this.setupButtonLoadingStates();
    }

    /**
     * Create global loading overlay
     */
    createGlobalLoadingOverlay() {
        if (document.getElementById('globalLoading')) return;

        const overlay = document.createElement('div');
        overlay.id = 'globalLoading';
        overlay.className = 'global-loading-overlay';
        overlay.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="loading-text mt-3">Processing your request...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    /**
     * Show global loading overlay
     */
    showGlobalLoading(text = 'Processing your request...') {
        const overlay = document.getElementById('globalLoading');
        const loadingText = overlay?.querySelector('.loading-text');
        
        if (loadingText) {
            loadingText.textContent = text;
        }
        
        if (overlay) {
            overlay.style.display = 'flex';
        }
    }

    /**
     * Hide global loading overlay
     */
    hideGlobalLoading() {
        const overlay = document.getElementById('globalLoading');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    /**
     * Set up button loading states
     */
    setupButtonLoadingStates() {
        document.querySelectorAll('[data-loading-text]').forEach(button => {
            button.addEventListener('click', () => {
                this.setButtonLoading(button);
            });
        });
    }

    /**
     * Set button to loading state
     */
    setButtonLoading(button, loadingText = null) {
        const originalText = button.innerHTML;
        const text = loadingText || button.getAttribute('data-loading-text') || 'Loading...';
        
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = `<i class="bi bi-arrow-clockwise spin"></i> ${text}`;
        button.disabled = true;
    }

    /**
     * Reset button from loading state
     */
    resetButtonLoading(button) {
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.disabled = false;
            button.removeAttribute('data-original-text');
        }
    }

    /**
     * Show success message
     */
    showSuccess(message, duration = 5000) {
        this.showAlert(message, 'success', duration);
    }

    /**
     * Show error message
     */
    showError(message, duration = 8000) {
        this.showAlert(message, 'danger', duration);
    }

    /**
     * Show info message
     */
    showInfo(message, duration = 5000) {
        this.showAlert(message, 'info', duration);
    }

    /**
     * Show alert message
     */
    showAlert(message, type = 'info', duration = 5000) {
        const alertId = 'alert-' + Date.now();
        const alert = document.createElement('div');
        alert.id = alertId;
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
        `;
        
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="document.getElementById('${alertId}').remove()"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                if (document.getElementById(alertId)) {
                    alert.remove();
                }
            }, duration);
        }
    }
}

// Make UI functions globally available
window.showGlobalLoading = function(text) {
    if (window.uiManager) {
        window.uiManager.showGlobalLoading(text);
    }
};

window.hideGlobalLoading = function() {
    if (window.uiManager) {
        window.uiManager.hideGlobalLoading();
    }
};

// Export for use in main application
window.UIManager = UIManager;