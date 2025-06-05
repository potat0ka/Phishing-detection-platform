/**
 * AI Phishing Detection Platform - Main Application Entry Point
 * Professional modular architecture with clean separation of concerns
 * 
 * This file orchestrates all modules and provides the main application logic.
 * Entry-level developers can easily understand the flow and add new features.
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
 * This is the main entry point that sets up all modules
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Phishing Detector initialized');
    
    // Initialize all managers in proper order
    initializeApplication();
});

/**
 * Main application initialization function
 * Sets up all modules and connects them together
 */
async function initializeApplication() {
    try {
        // Initialize core managers
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
    const content = formData.get('content');
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
    
    const threatLevel = result.threat_level || 'unknown';
    const confidence = result.confidence || 0;
    const explanation = result.explanation || 'No explanation available';
    
    // Determine result styling based on threat level
    const alertClass = {
        'safe': 'alert-success',
        'low': 'alert-info',
        'medium': 'alert-warning',
        'high': 'alert-danger',
        'critical': 'alert-danger'
    }[threatLevel] || 'alert-secondary';
    
    const resultHTML = `
        <div class="alert ${alertClass} mb-4">
            <div class="d-flex align-items-center mb-3">
                <div class="threat-icon me-3">
                    ${getThreatIcon(threatLevel)}
                </div>
                <div>
                    <h5 class="mb-1">Analysis Complete</h5>
                    <p class="mb-0">Threat Level: <strong>${threatLevel.toUpperCase()}</strong></p>
                </div>
            </div>
            
            <div class="confidence-bar mb-3">
                <label class="form-label small">Confidence Score</label>
                <div class="progress">
                    <div class="progress-bar" style="width: ${confidence}%" data-width="${confidence}%">
                        ${confidence}%
                    </div>
                </div>
            </div>
            
            <div class="explanation">
                <h6>Analysis Details:</h6>
                <p>${explanation}</p>
            </div>
            
            ${result.recommendations ? `
                <div class="recommendations mt-3">
                    <h6>Recommendations:</h6>
                    <ul class="list-unstyled">
                        ${result.recommendations.map(rec => `<li><i class="bi bi-check-circle text-primary me-2"></i>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
    
    resultContainer.innerHTML = resultHTML;
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Animate the progress bar
    setTimeout(() => {
        const progressBar = resultContainer.querySelector('.progress-bar');
        if (progressBar && window.PhishingDetectorApp.managers.animations) {
            window.PhishingDetectorApp.managers.animations.animateProgressBar(progressBar);
        }
    }, 100);
}

/**
 * Get appropriate icon for threat level
 */
function getThreatIcon(threatLevel) {
    const icons = {
        'safe': '<i class="bi bi-shield-check text-success" style="font-size: 2rem;"></i>',
        'low': '<i class="bi bi-info-circle text-info" style="font-size: 2rem;"></i>',
        'medium': '<i class="bi bi-exclamation-triangle text-warning" style="font-size: 2rem;"></i>',
        'high': '<i class="bi bi-exclamation-triangle-fill text-danger" style="font-size: 2rem;"></i>',
        'critical': '<i class="bi bi-shield-x text-danger" style="font-size: 2rem;"></i>'
    };
    
    return icons[threatLevel] || '<i class="bi bi-question-circle text-secondary" style="font-size: 2rem;"></i>';
}

/**
 * Initialize content type switcher
 */
function initializeContentTypeSwitcher() {
    const contentTypeRadios = document.querySelectorAll('input[name="input_type"]');
    const contentInput = document.querySelector('#content');
    const exampleButtons = document.querySelectorAll('.example-btn');
    
    if (!contentInput || contentTypeRadios.length === 0) return;
    
    contentTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            updateContentPlaceholder(contentInput, radio.value);
            updateExampleButtons(exampleButtons, radio.value);
        });
    });
    
    // Initialize with default type
    const defaultType = document.querySelector('input[name="input_type"]:checked');
    if (defaultType) {
        updateContentPlaceholder(contentInput, defaultType.value);
        updateExampleButtons(exampleButtons, defaultType.value);
    }
}

/**
 * Update content input placeholder based on selected type
 */
function updateContentPlaceholder(input, type) {
    const placeholders = {
        'url': 'Enter URL to analyze (e.g., https://suspicious-site.com)',
        'email': 'Paste email content or headers here',
        'message': 'Enter message or text content to analyze for phishing'
    };
    
    input.placeholder = placeholders[type] || 'Enter content to analyze';
    input.focus();
}

/**
 * Update example buttons based on content type
 */
function updateExampleButtons(buttons, type) {
    const examples = {
        'url': [
            'https://secure-bank-login.suspicious-domain.com',
            'http://paypal-verification.fake-site.net',
            'https://microsoft-support.phishing-example.org'
        ],
        'email': [
            'Your account has been suspended. Click here to verify: [suspicious link]',
            'Congratulations! You\'ve won $1000. Claim now: [phishing link]',
            'Security alert: Unusual activity detected. Verify immediately: [malicious link]'
        ],
        'message': [
            'URGENT: Your bank account will be closed. Call this number immediately.',
            'You have a package waiting. Click to track: [suspicious link]',
            'IRS Notice: You owe taxes. Pay immediately to avoid penalties.'
        ]
    };
    
    buttons.forEach((button, index) => {
        if (examples[type] && examples[type][index]) {
            button.textContent = examples[type][index];
            button.style.display = 'block';
            button.onclick = () => {
                document.querySelector('#content').value = examples[type][index];
            };
        } else {
            button.style.display = 'none';
        }
    });
}

/**
 * Initialize demo features
 */
function initializeDemoFeatures() {
    // Example content buttons
    document.querySelectorAll('.example-btn').forEach(button => {
        button.addEventListener('click', () => {
            const content = button.textContent;
            const contentInput = document.querySelector('#content');
            if (contentInput) {
                contentInput.value = content;
                contentInput.focus();
            }
        });
    });
}

/**
 * Initialize dashboard features
 */
function initializeDashboard() {
    // Bulk delete functionality
    initializeBulkDelete();
    
    // Detection history filtering
    initializeHistoryFiltering();
    
    // Statistics updates
    updateDashboardStatistics();
}

/**
 * Initialize bulk delete functionality
 */
function initializeBulkDelete() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const deleteSelectedBtn = document.getElementById('deleteSelected');
    const detectionCheckboxes = document.querySelectorAll('.detection-checkbox');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', (e) => {
            detectionCheckboxes.forEach(checkbox => {
                checkbox.checked = e.target.checked;
            });
            updateDeleteButtonState();
        });
    }
    
    detectionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateDeleteButtonState);
    });
    
    if (deleteSelectedBtn) {
        deleteSelectedBtn.addEventListener('click', handleBulkDelete);
    }
}

/**
 * Update delete button state based on selections
 */
function updateDeleteButtonState() {
    const deleteBtn = document.getElementById('deleteSelected');
    const checkedBoxes = document.querySelectorAll('.detection-checkbox:checked');
    
    if (deleteBtn) {
        deleteBtn.disabled = checkedBoxes.length === 0;
        deleteBtn.textContent = `Delete Selected (${checkedBoxes.length})`;
    }
}

/**
 * Handle bulk delete operation
 */
async function handleBulkDelete() {
    const checkedBoxes = document.querySelectorAll('.detection-checkbox:checked');
    const detectionIds = Array.from(checkedBoxes).map(cb => cb.value);
    
    if (detectionIds.length === 0) return;
    
    if (!confirm(`Are you sure you want to delete ${detectionIds.length} detection(s)?`)) {
        return;
    }
    
    window.uiManager.showGlobalLoading('Deleting selected detections...');
    
    try {
        const deletePromises = detectionIds.map(id => 
            fetch(`/delete-detection/${id}`, {
                method: 'DELETE',
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
        );
        
        await Promise.all(deletePromises);
        
        window.uiManager.showSuccess('Selected detections deleted successfully');
        
        // Remove deleted rows from DOM
        checkedBoxes.forEach(checkbox => {
            const row = checkbox.closest('tr');
            if (row) row.remove();
        });
        
        updateDashboardStatistics();
        
    } catch (error) {
        console.error('Bulk delete error:', error);
        window.uiManager.showError('Failed to delete some detections');
    } finally {
        window.uiManager.hideGlobalLoading();
    }
}

/**
 * Initialize history filtering
 */
function initializeHistoryFiltering() {
    const filterInputs = document.querySelectorAll('.history-filter');
    filterInputs.forEach(input => {
        input.addEventListener('input', filterDetectionHistory);
    });
}

/**
 * Filter detection history based on user input
 */
function filterDetectionHistory() {
    const searchTerm = document.getElementById('searchHistory')?.value.toLowerCase() || '';
    const threatFilter = document.getElementById('threatFilter')?.value || 'all';
    const rows = document.querySelectorAll('.detection-row');
    
    rows.forEach(row => {
        const content = row.querySelector('.detection-content')?.textContent.toLowerCase() || '';
        const threat = row.querySelector('.threat-badge')?.textContent.toLowerCase() || '';
        
        const matchesSearch = content.includes(searchTerm);
        const matchesThreat = threatFilter === 'all' || threat.includes(threatFilter);
        
        row.style.display = (matchesSearch && matchesThreat) ? '' : 'none';
    });
}

/**
 * Update dashboard statistics
 */
function updateDashboardStatistics() {
    const totalDetections = document.querySelectorAll('.detection-row:not([style*="display: none"])').length;
    const highThreatCount = document.querySelectorAll('.threat-badge.bg-danger').length;
    
    const statsElements = {
        totalDetections: document.getElementById('totalDetections'),
        highThreats: document.getElementById('highThreats')
    };
    
    if (statsElements.totalDetections) {
        statsElements.totalDetections.textContent = totalDetections;
    }
    
    if (statsElements.highThreats) {
        statsElements.highThreats.textContent = highThreatCount;
    }
}

/**
 * Initialize security tips page
 */
function initializeSecurityTips() {
    // Category filtering
    initializeTipCategories();
    
    // Search functionality
    initializeTipSearch();
    
    // Interactive features
    initializeInteractiveTips();
}

/**
 * Initialize tip categories
 */
function initializeTipCategories() {
    const categoryButtons = document.querySelectorAll('.category-btn');
    categoryButtons.forEach(button => {
        button.addEventListener('click', () => {
            const category = button.dataset.category;
            filterTipsByCategory(category);
            
            // Update active state
            categoryButtons.forEach(b => b.classList.remove('active'));
            button.classList.add('active');
        });
    });
}

/**
 * Filter tips by category
 */
function filterTipsByCategory(category) {
    const tipCards = document.querySelectorAll('.tip-card');
    tipCards.forEach(card => {
        const cardCategory = card.dataset.category;
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * Initialize tip search
 */
function initializeTipSearch() {
    const searchInput = document.getElementById('tipSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            const tipCards = document.querySelectorAll('.tip-card');
            
            tipCards.forEach(card => {
                const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
                const content = card.querySelector('.card-text')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

/**
 * Initialize interactive tips
 */
function initializeInteractiveTips() {
    // Expandable tip content
    document.querySelectorAll('.tip-expand').forEach(button => {
        button.addEventListener('click', () => {
            const content = button.parentElement.querySelector('.tip-full-content');
            if (content) {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
                button.textContent = content.style.display === 'none' ? 'Read More' : 'Read Less';
            }
        });
    });
}

/**
 * Initialize AI content check page
 */
function initializeAIContentCheck() {
    const fileInput = document.getElementById('file');
    const dropZone = document.getElementById('dropZone');
    
    if (fileInput && dropZone) {
        setupFileDropZone(fileInput, dropZone);
    }
}

/**
 * Set up file drop zone functionality
 */
function setupFileDropZone(fileInput, dropZone) {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });
    
    // Handle file input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

/**
 * Prevent default drag behaviors
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Handle file selection and preview
 */
function handleFileSelection(file) {
    const previewContainer = document.getElementById('filePreview');
    if (!previewContainer) return;
    
    const fileInfo = `
        <div class="file-info-card">
            <div class="d-flex align-items-center">
                <i class="bi bi-file-earmark-text text-primary me-3" style="font-size: 2rem;"></i>
                <div>
                    <h6 class="mb-1">${file.name}</h6>
                    <small class="text-muted">${formatFileSize(file.size)} • ${file.type || 'Unknown type'}</small>
                </div>
            </div>
        </div>
    `;
    
    previewContainer.innerHTML = fileInfo;
    previewContainer.style.display = 'block';
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Set up global error handling
 */
function setupGlobalErrorHandling() {
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        
        // Track error with analytics
        if (window.PhishingDetectorApp.managers.analytics) {
            window.PhishingDetectorApp.managers.analytics.trackError('Global Error', event.error);
        }
    });
    
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        
        // Track error with analytics
        if (window.PhishingDetectorApp.managers.analytics) {
            window.PhishingDetectorApp.managers.analytics.trackError('Promise Rejection', event.reason);
        }
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