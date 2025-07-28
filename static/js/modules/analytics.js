/**
 * Analytics Module - Handles user analytics and performance tracking
 * Privacy-focused analytics with local data processing
 */

class AnalyticsManager {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.pageStartTime = Date.now();
        this.events = [];
        this.init();
    }

    /**
     * Initialize analytics system
     */
    init() {
        this.setupPageTracking();
        this.setupUserInteractionTracking();
        this.setupPerformanceTracking();
        this.setupErrorTracking();
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Set up page view tracking
     */
    setupPageTracking() {
        // Track initial page load
        this.trackPageView();

        // Track page visibility changes
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.trackEvent('Page', 'Hidden', window.location.pathname);
            } else {
                this.trackEvent('Page', 'Visible', window.location.pathname);
            }
        });

        // Track page unload
        window.addEventListener('beforeunload', () => {
            this.trackPageExit();
        });
    }

    /**
     * Track page view
     */
    trackPageView() {
        const pageData = {
            page: window.location.pathname,
            title: document.title,
            referrer: document.referrer,
            timestamp: Date.now(),
            userAgent: navigator.userAgent,
            screenResolution: `${screen.width}x${screen.height}`,
            viewportSize: `${window.innerWidth}x${window.innerHeight}`
        };

        this.trackEvent('Page', 'View', window.location.pathname, pageData);
        console.log('Analytics: Page - View -', window.location.pathname);
    }

    /**
     * Track page exit with time spent
     */
    trackPageExit() {
        const timeSpent = Date.now() - this.pageStartTime;
        this.trackEvent('Page', 'Exit', window.location.pathname, {
            timeSpent: timeSpent,
            scrollDepth: this.getScrollDepth()
        });
    }

    /**
     * Set up user interaction tracking
     */
    setupUserInteractionTracking() {
        // Track button clicks
        document.addEventListener('click', (e) => {
            const button = e.target.closest('button, .btn, a[href]');
            if (button) {
                this.trackButtonClick(button);
            }
        });

        // Track form submissions
        document.addEventListener('submit', (e) => {
            this.trackFormSubmission(e.target);
        });

        // Track input focus (privacy-safe)
        document.addEventListener('focus', (e) => {
            if (e.target.matches('input, textarea, select')) {
                this.trackEvent('Form', 'Field Focus', e.target.type || e.target.tagName);
            }
        }, true);

        // Track file uploads
        document.addEventListener('change', (e) => {
            if (e.target.type === 'file' && e.target.files.length > 0) {
                this.trackFileUpload(e.target);
            }
        });
    }

    /**
     * Track button clicks
     */
    trackButtonClick(button) {
        const buttonText = button.textContent.trim() || button.getAttribute('aria-label') || 'Unknown';
        const buttonType = button.type || 'link';
        const buttonClass = button.className;

        this.trackEvent('Button', 'Click', buttonText, {
            type: buttonType,
            className: buttonClass,
            href: button.href || null
        });
    }

    /**
     * Track form submissions
     */
    trackFormSubmission(form) {
        const formId = form.id || 'unknown';
        const formAction = form.action || window.location.href;
        const fieldCount = form.querySelectorAll('input, textarea, select').length;

        this.trackEvent('Form', 'Submit', formId, {
            action: formAction,
            fieldCount: fieldCount,
            method: form.method || 'GET'
        });
    }

    /**
     * Track file uploads (privacy-safe)
     */
    trackFileUpload(input) {
        const file = input.files[0];
        this.trackEvent('File', 'Upload', 'File Selected', {
            fileType: file.type,
            fileSize: file.size,
            fileName: file.name.split('.').pop() // Only track extension
        });
    }

    /**
     * Set up performance tracking
     */
    setupPerformanceTracking() {
        // Track page load performance
        window.addEventListener('load', () => {
            this.trackPagePerformance();
        });

        // Track Core Web Vitals
        this.trackWebVitals();
    }

    /**
     * Track page performance metrics
     */
    trackPagePerformance() {
        if (window.performance && window.performance.timing) {
            const timing = window.performance.timing;
            const loadTime = timing.loadEventEnd - timing.navigationStart;
            const domReady = timing.domContentLoadedEventEnd - timing.navigationStart;

            this.trackEvent('Performance', 'Page Load', 'Load Time', {
                loadTime: loadTime,
                domReady: domReady,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Track Core Web Vitals (simplified)
     */
    trackWebVitals() {
        // Track Largest Contentful Paint (LCP)
        if ('PerformanceObserver' in window) {
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    this.trackEvent('Performance', 'LCP', 'Largest Contentful Paint', {
                        value: lastEntry.startTime,
                        element: lastEntry.element?.tagName || 'unknown'
                    });
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (error) {
                console.log('LCP tracking not supported');
            }
        }
    }

    /**
     * Set up error tracking
     */
    setupErrorTracking() {
        // Track JavaScript errors
        window.addEventListener('error', (e) => {
            this.trackError('JavaScript Error', e.error, {
                filename: e.filename,
                lineno: e.lineno,
                colno: e.colno
            });
        });

        // Track unhandled promise rejections
        window.addEventListener('unhandledrejection', (e) => {
            this.trackError('Unhandled Promise Rejection', e.reason);
        });
    }

    /**
     * Track errors
     */
    trackError(type, error, details = {}) {
        this.trackEvent('Error', type, error.message || error.toString(), {
            stack: error.stack || 'No stack trace',
            ...details,
            timestamp: Date.now(),
            url: window.location.href
        });
    }

    /**
     * Track custom events
     */
    trackEvent(category, action, label = '', data = {}) {
        const event = {
            sessionId: this.sessionId,
            category: category,
            action: action,
            label: label,
            data: data,
            timestamp: Date.now(),
            url: window.location.href
        };

        this.events.push(event);
        
        // Keep only last 100 events to prevent memory issues
        if (this.events.length > 100) {
            this.events.shift();
        }

        // Send to analytics endpoint (if available)
        this.sendAnalytics(event);
    }

    /**
     * Send analytics data to server
     */
    async sendAnalytics(event) {
        try {
            // Only send if analytics endpoint is available
            await fetch('/analytics/track', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(event)
            });
        } catch (error) {
            // Silently fail - analytics should not affect user experience
            console.debug('Analytics tracking failed:', error.message);
        }
    }

    /**
     * Get scroll depth percentage
     */
    getScrollDepth() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
        return documentHeight > 0 ? Math.round((scrollTop / documentHeight) * 100) : 0;
    }

    /**
     * Track phishing detection usage
     */
    trackPhishingDetection(inputType, result) {
        this.trackEvent('Phishing Detection', 'Analysis Complete', inputType, {
            confidence: result.confidence,
            classification: result.classification,
            threatLevel: result.threat_level
        });
    }

    /**
     * Track AI content detection usage
     */
    trackAIContentDetection(contentType, result) {
        this.trackEvent('AI Content Detection', 'Analysis Complete', contentType, {
            confidence: result.confidence,
            classification: result.classification,
            fileSize: result.file_size
        });
    }

    /**
     * Get analytics summary
     */
    getAnalyticsSummary() {
        const pageViews = this.events.filter(e => e.category === 'Page' && e.action === 'View').length;
        const buttonClicks = this.events.filter(e => e.category === 'Button').length;
        const formSubmissions = this.events.filter(e => e.category === 'Form' && e.action === 'Submit').length;
        const errors = this.events.filter(e => e.category === 'Error').length;

        return {
            sessionId: this.sessionId,
            pageViews: pageViews,
            buttonClicks: buttonClicks,
            formSubmissions: formSubmissions,
            errors: errors,
            sessionDuration: Date.now() - this.pageStartTime,
            totalEvents: this.events.length
        };
    }

    /**
     * Clear analytics data
     */
    clearAnalytics() {
        this.events = [];
    }
}

// Export for use in main application
window.AnalyticsManager = AnalyticsManager;