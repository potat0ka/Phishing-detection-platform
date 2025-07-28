/**
 * AI Phishing Detection Platform - Main Application Entry Point
 * Clean version focused on homepage quick check functionality
 */

// Global application state
window.PhishingDetectorApp = {
    managers: {},
    config: {
        version: '2.0.0',
        apiEndpoints: {
            quickCheck: '/api/quick-check',
            aiContent: '/ai-content-check',
            login: '/auth/login',
            register: '/auth/register',
            logout: '/auth/logout'
        }
    },
    isInitialized: false
};

/**
 * Initialize the entire application
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Phishing Detector initialized');
    initializeApplication();
});

/**
 * Main application initialization function
 */
async function initializeApplication() {
    try {
        // Initialize core managers (simplified)
        window.PhishingDetectorApp.managers.ui = new UIManager();
        window.PhishingDetectorApp.managers.auth = new AuthManager();
        window.PhishingDetectorApp.managers.forms = new FormManager();
        window.PhishingDetectorApp.managers.animations = new AnimationManager();
        window.PhishingDetectorApp.managers.analytics = new AnalyticsManager();
        
        // Make managers globally accessible for easier debugging
        window.uiManager = window.PhishingDetectorApp.managers.ui;
        window.authManager = window.PhishingDetectorApp.managers.auth;
        
        // Initialize page-specific features
        initializePageFeatures();
        
        // Set up global error handling
        setupGlobalErrorHandling();
        
        // Mark application as initialized
        window.PhishingDetectorApp.isInitialized = true;
        
        console.log('Application initialized successfully');
        
    } catch (error) {
        console.error('Application initialization failed:', error);
        showInitializationError();
    }
}

/**
 * Initialize features specific to current page
 */
function initializePageFeatures() {
    const currentPage = window.location.pathname;
    
    // Home page features
    if (currentPage === '/' || currentPage === '/index.html') {
        initializeHomePage();
    }
    
    // Dashboard features
    if (currentPage === '/dashboard') {
        initializeDashboard();
    }
    
    // Security tips features
    if (currentPage === '/tips') {
        initializeSecurityTips();
    }
    
    // AI content check features
    if (currentPage === '/ai-content-check') {
        initializeAIContentCheck();
    }
}

/**
 * Initialize home page specific features
 */
function initializeHomePage() {
    // Set up quick analysis form
    const quickAnalysisForm = document.getElementById('quickAnalysisForm');
    if (quickAnalysisForm) {
        quickAnalysisForm.addEventListener('submit', handleQuickAnalysis);
    }
    
    // Initialize content type switcher
    initializeContentTypeSwitcher();
    
    // Set up demo buttons
    initializeDemoFeatures();
}

/**
 * Handle quick analysis form submission
 */
async function handleQuickAnalysis(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const content = formData.get('input_content');
    const inputType = formData.get('input_type');
    
    if (!content || !content.trim()) {
        window.uiManager.showError('Please enter content to analyze');
        return;
    }
    
    // Show loading state
    window.uiManager.showGlobalLoading('Analyzing content for threats...');
    
    try {
        const response = await fetch('/api/quick-check', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayAnalysisResult(result);
            
            // Track analytics
            if (window.PhishingDetectorApp.managers.analytics) {
                window.PhishingDetectorApp.managers.analytics.trackPhishingDetection(inputType, result);
            }
        } else {
            window.uiManager.showError(result.message || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Analysis error:', error);
        window.uiManager.showError('Connection error. Please try again.');
    } finally {
        window.uiManager.hideGlobalLoading();
    }
}

/**
 * Display analysis results in a user-friendly format
 */
function displayAnalysisResult(result) {
    const resultContainer = document.getElementById('analysisResult');
    if (!resultContainer) return;
    
    const data = result.data || result;
    const threatLevel = data.threat_level || 'unknown';
    const confidence = data.confidence_percentage || (data.confidence_score * 100) || 0;
    const explanation = data.explanation || 'No explanation available';
    
    // Determine result styling based on threat level
    const alertClass = {
        'low': 'success',
        'medium': 'warning', 
        'high': 'danger',
        'unknown': 'secondary'
    }[threatLevel] || 'secondary';
    
    const iconClass = {
        'low': 'fa-check-circle',
        'medium': 'fa-exclamation-triangle',
        'high': 'fa-skull-crossbones',
        'unknown': 'fa-question-circle'
    }[threatLevel] || 'fa-question-circle';
    
    // Create result HTML
    resultContainer.innerHTML = `
        <div class="card border-0 shadow">
            <div class="card-header bg-${alertClass} text-white">
                <h5 class="mb-0">
                    <i class="fas fa-chart-line me-2"></i>
                    AI Analysis Complete
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <div class="d-flex align-items-center mb-3">
                            <div class="threat-icon me-3">
                                <i class="fas ${iconClass} fa-2x text-${alertClass}"></i>
                            </div>
                            <div>
                                <h6 class="mb-1">Threat Level: <span class="badge bg-${alertClass}">${threatLevel.toUpperCase()}</span></h6>
                                <p class="mb-0 text-muted">Confidence: ${confidence}%</p>
                            </div>
                        </div>
                        <div class="explanation-section">
                            <h6 class="text-primary">AI Explanation:</h6>
                            <p class="text-muted">${explanation}</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="confidence-meter text-center">
                            <div class="progress mt-3" style="height: 20px;">
                                <div class="progress-bar bg-${alertClass}" role="progressbar" style="width: ${confidence}%" aria-valuenow="${confidence}" aria-valuemin="0" aria-valuemax="100">
                                    ${confidence}%
                                </div>
                            </div>
                            <p class="mt-2 small text-muted">Confidence Score</p>
                        </div>
                    </div>
                </div>
                <div class="action-buttons mt-4">
                    <button class="btn btn-outline-primary me-2" onclick="resetAnalysisForm()">
                        <i class="fas fa-redo me-1"></i>Check Another
                    </button>
                    <a href="/check" class="btn btn-outline-secondary">
                        <i class="fas fa-cog me-1"></i>Advanced Analysis
                    </a>
                </div>
            </div>
        </div>
    `;
    
    // Show result container
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Reset analysis form for new check
 */
function resetAnalysisForm() {
    const form = document.getElementById('quickAnalysisForm');
    const resultContainer = document.getElementById('analysisResult');
    
    if (form) form.reset();
    if (resultContainer) resultContainer.style.display = 'none';
    
    // Scroll back to form
    form.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Content type switching functionality
 */
function initializeContentTypeSwitcher() {
    const inputType = document.getElementById('input_type');
    const inputContent = document.getElementById('input_content');
    
    if (inputType && inputContent) {
        inputType.addEventListener('change', function() {
            const placeholders = {
                'url': 'Enter URL to analyze (e.g., https://example.com)',
                'email': 'Paste email content here',
                'message': 'Enter message or text content to analyze'
            };
            inputContent.placeholder = placeholders[this.value] || 'Enter content to analyze';
        });
    }
}

function initializeDemoFeatures() {
    console.log('Demo features initialized');
}

function initializeDashboard() {
    console.log('Dashboard features initialized');
}

function initializeSecurityTips() {
    console.log('Security tips features initialized');
}

function initializeAIContentCheck() {
    console.log('AI content check features initialized');
}

function setupGlobalErrorHandling() {
    window.addEventListener('error', function(e) {
        console.error('Global error:', e.error);
    });
}

/**
 * Show initialization error to user
 */
function showInitializationError() {
    const errorHTML = `
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Application Error</h4>
            <p>The application failed to initialize properly. Please refresh the page and try again.</p>
            <hr>
            <p class="mb-0">If the problem persists, please contact support.</p>
        </div>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertAdjacentHTML('afterbegin', errorHTML);
}

// Export main functions for external use
window.PhishingDetectorApp.displayAnalysisResult = displayAnalysisResult;
window.PhishingDetectorApp.handleQuickAnalysis = handleQuickAnalysis;