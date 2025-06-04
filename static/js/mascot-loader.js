/*
Cybersecurity Mascot Loading System
==================================
Playful loading animations with cybersecurity mascots for phishing detection
*/

class MascotLoader {
    constructor() {
        this.mascots = ['shield-knight', 'cyber-detective', 'security-robot'];
        this.currentMascot = 0;
        this.loadingMessages = [
            'Analyzing suspicious patterns...',
            'Scanning for phishing indicators...',
            'Checking threat intelligence...',
            'Evaluating domain reputation...',
            'Inspecting email headers...',
            'Running AI detection algorithms...',
            'Cross-referencing security databases...',
            'Performing deep content analysis...'
        ];
        this.funFacts = [
            '🔍 Did you know? 96% of phishing attacks arrive via email',
            '🛡️ Fun fact: The first phishing attack was recorded in 1995',
            '🤖 AI can detect phishing with 99.9% accuracy when properly trained',
            '📧 Phishing emails cost businesses $1.8 billion annually',
            '🔐 Always verify URLs before clicking - hover to see the real destination',
            '⚡ Our AI analyzes over 50 different indicators to protect you'
        ];
        this.messageIndex = 0;
        this.factIndex = 0;
        this.progressValue = 0;
        this.loadingInterval = null;
        this.messageInterval = null;
        this.progressInterval = null;
    }

    show(duration = 5000) {
        this.createLoadingOverlay();
        this.startAnimations();
        
        // Auto-hide after duration if still showing
        setTimeout(() => {
            if (document.querySelector('.loading-overlay')) {
                this.hide();
            }
        }, duration);
    }

    hide() {
        this.stopAnimations();
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    }

    createLoadingOverlay() {
        // Remove existing overlay if any
        const existing = document.querySelector('.loading-overlay');
        if (existing) {
            existing.remove();
        }

        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="mascot-container">
                ${this.getMascotHTML()}
            </div>
            
            <div class="loading-text">
                <span id="loading-message">${this.loadingMessages[0]}</span>
                <span class="dots">
                    <span style="--i:0">.</span>
                    <span style="--i:1">.</span>
                    <span style="--i:2">.</span>
                </span>
            </div>
            
            <div class="loading-subtitle">
                Our cyber guardian is protecting you
            </div>
            
            <div class="cyber-progress">
                <div class="cyber-progress-bar" id="progress-bar"></div>
            </div>
            
            <div class="fun-facts" id="fun-facts">
                ${this.funFacts[0]}
            </div>
        `;

        document.body.appendChild(overlay);
        
        // Fade in effect
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 50);
    }

    getMascotHTML() {
        const mascotType = this.mascots[this.currentMascot];
        
        switch(mascotType) {
            case 'shield-knight':
                return `
                    <div class="shield-knight">
                        <div class="helmet"></div>
                        <div class="shield"></div>
                    </div>
                `;
            
            case 'cyber-detective':
                return `
                    <div class="cyber-detective">
                        <div class="hat"></div>
                        <div class="head"></div>
                        <div class="magnifying-glass"></div>
                    </div>
                `;
            
            case 'security-robot':
                return `
                    <div class="security-robot">
                        <div class="antenna"></div>
                        <div class="head">
                            <div class="eyes"></div>
                        </div>
                        <div class="body"></div>
                    </div>
                `;
            
            default:
                return this.getMascotHTML('shield-knight');
        }
    }

    startAnimations() {
        // Rotate loading messages
        this.messageInterval = setInterval(() => {
            this.messageIndex = (this.messageIndex + 1) % this.loadingMessages.length;
            const messageEl = document.getElementById('loading-message');
            if (messageEl) {
                messageEl.textContent = this.loadingMessages[this.messageIndex];
            }
        }, 1500);

        // Update fun facts
        setInterval(() => {
            this.factIndex = (this.factIndex + 1) % this.funFacts.length;
            const factsEl = document.getElementById('fun-facts');
            if (factsEl) {
                factsEl.textContent = this.funFacts[this.factIndex];
            }
        }, 4000);

        // Animate progress bar
        this.progressInterval = setInterval(() => {
            this.progressValue += Math.random() * 15 + 5;
            if (this.progressValue > 100) this.progressValue = 100;
            
            const progressBar = document.getElementById('progress-bar');
            if (progressBar) {
                progressBar.style.width = this.progressValue + '%';
            }
        }, 200);

        // Switch mascots occasionally
        this.mascotInterval = setInterval(() => {
            this.switchMascot();
        }, 8000);
    }

    stopAnimations() {
        if (this.messageInterval) clearInterval(this.messageInterval);
        if (this.progressInterval) clearInterval(this.progressInterval);
        if (this.mascotInterval) clearInterval(this.mascotInterval);
        
        this.messageIndex = 0;
        this.factIndex = 0;
        this.progressValue = 0;
    }

    switchMascot() {
        this.currentMascot = (this.currentMascot + 1) % this.mascots.length;
        const container = document.querySelector('.mascot-container');
        if (container) {
            container.style.opacity = '0';
            setTimeout(() => {
                container.innerHTML = this.getMascotHTML();
                container.style.opacity = '1';
            }, 300);
        }
    }

    // Quick show for short operations
    quickShow(message = 'Processing...') {
        this.createQuickLoader(message);
    }

    createQuickLoader(message) {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay quick-loader';
        overlay.innerHTML = `
            <div class="mascot-container">
                <div class="security-robot">
                    <div class="antenna"></div>
                    <div class="head">
                        <div class="eyes"></div>
                    </div>
                    <div class="body"></div>
                </div>
            </div>
            <div class="loading-text">${message}</div>
        `;

        document.body.appendChild(overlay);
        
        setTimeout(() => {
            overlay.style.opacity = '1';
        }, 50);
    }
}

// Global instance
const mascotLoader = new MascotLoader();

// Integration with forms
document.addEventListener('DOMContentLoaded', function() {
    // Hook into form submissions
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            const formAction = form.action || window.location.pathname;
            
            // Show loading for phishing detection forms
            if (formAction.includes('/check') || form.id === 'detectionForm' || form.id === 'quickCheckForm') {
                e.preventDefault();
                
                // Disable submit button
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
                }
                
                // Show mascot loader
                mascotLoader.show(8000);
                
                // Submit form after short delay for UX
                setTimeout(() => {
                    form.submit();
                }, 500);
            }
        });
    });

    // Hook into AJAX requests for quick check
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        const url = args[0];
        
        if (typeof url === 'string' && url.includes('/api/quick-check')) {
            mascotLoader.quickShow('Quick scanning...');
            
            return originalFetch.apply(this, args)
                .finally(() => {
                    setTimeout(() => {
                        mascotLoader.hide();
                    }, 1000);
                });
        }
        
        return originalFetch.apply(this, args);
    };

    // Add click handlers for analyze buttons
    document.addEventListener('click', function(e) {
        if (e.target.matches('.btn[onclick*="checkContent"]') || 
            e.target.matches('button[onclick*="analyze"]') ||
            e.target.closest('.btn[onclick*="checkContent"]')) {
            
            mascotLoader.show(6000);
        }
    });
});

// Utility functions for manual control
function showMascotLoader(duration = 5000) {
    mascotLoader.show(duration);
}

function hideMascotLoader() {
    mascotLoader.hide();
}

function showQuickLoader(message = 'Processing...') {
    mascotLoader.quickShow(message);
}