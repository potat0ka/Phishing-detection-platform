/**
 * AI Phishing Detection Platform - Modular Application Entry Point
 * Professional architecture with clean separation of concerns
 * 
 * This file replaces the previous 1083-line monolithic main.js with a
 * modular system that loads components dynamically for better maintainability.
 */

// Application configuration
const APP_CONFIG = {
    version: '2.0.0',
    modules: [
        '/static/js/modules/animations.js',
        '/static/js/modules/forms.js',
        '/static/js/modules/auth.js',
        '/static/js/modules/ui.js',
        '/static/js/app.js'
    ],
    fallbackEnabled: true
};

// Module loading system
class ModuleLoader {
    constructor() {
        this.loadedModules = 0;
        this.totalModules = APP_CONFIG.modules.length;
        this.startTime = Date.now();
    }

    async loadModules() {
        console.log('AI Phishing Detector - Loading modular components...');
        
        for (const modulePath of APP_CONFIG.modules) {
            let retryCount = 0;
            const maxRetries = 3;
            
            while (retryCount < maxRetries) {
                try {
                    await this.loadModule(modulePath);
                    break; // Success, exit retry loop
                } catch (error) {
                    retryCount++;
                    console.warn(`Failed to load module: ${modulePath} (attempt ${retryCount}/${maxRetries})`, error);
                    
                    if (retryCount >= maxRetries) {
                        console.error(`Module load failed after ${maxRetries} attempts: ${modulePath}`);
                        if (!APP_CONFIG.fallbackEnabled) {
                            throw error;
                        }
                        // Continue with next module if fallback is enabled
                        break;
                    }
                    
                    // Wait before retry (exponential backoff)
                    const delay = Math.pow(2, retryCount - 1) * 1000; // 1s, 2s, 4s
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        this.onAllModulesLoaded();
    }

    loadModule(scriptPath) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = scriptPath;
            script.type = 'text/javascript';
            
            // Add cache busting parameter to prevent caching issues
            const cacheBuster = Date.now();
            script.src = scriptPath + '?v=' + cacheBuster;
            
            script.onload = () => {
                this.loadedModules++;
                console.log(`Module loaded: ${scriptPath.split('/').pop()} (${this.loadedModules}/${this.totalModules})`);
                resolve();
            };
            
            script.onerror = (error) => {
                console.error(`Failed to load module: ${scriptPath}`, error);
                // Try loading without cache buster as fallback
                const fallbackScript = document.createElement('script');
                fallbackScript.src = scriptPath;
                fallbackScript.type = 'text/javascript';
                
                fallbackScript.onload = () => {
                    this.loadedModules++;
                    console.log(`Module loaded (fallback): ${scriptPath.split('/').pop()} (${this.loadedModules}/${this.totalModules})`);
                    resolve();
                };
                
                fallbackScript.onerror = () => {
                    reject(new Error(`Module load failed: ${scriptPath}`));
                };
                
                document.head.appendChild(fallbackScript);
            };
            
            document.head.appendChild(script);
        });
    }

    onAllModulesLoaded() {
        const loadTime = Date.now() - this.startTime;
        console.log(`All modules loaded successfully in ${loadTime}ms - Application ready`);
        
        // Dispatch custom event for application ready
        document.dispatchEvent(new CustomEvent('appReady', {
            detail: { loadTime, version: APP_CONFIG.version }
        }));
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const loader = new ModuleLoader();
    loader.loadModules().catch(error => {
        console.error('Critical error loading application modules:', error);
        
        // Show fallback error message to user
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger';
        errorDiv.innerHTML = `
            <h4>Application Loading Error</h4>
            <p>Some components failed to load. Please refresh the page and try again.</p>
            <p><small>Error: ${error.message}</small></p>
        `;
        
        const container = document.querySelector('.container') || document.body;
        container.insertAdjacentElement('afterbegin', errorDiv);
    });
});

// Global utilities for backward compatibility
window.showGlobalLoading = function(text) {
    console.log('Loading:', text);
    // Will be overridden by UI module when loaded
};

window.hideGlobalLoading = function() {
    console.log('Loading complete');
    // Will be overridden by UI module when loaded
};

// Export for debugging
window.APP_CONFIG = APP_CONFIG;