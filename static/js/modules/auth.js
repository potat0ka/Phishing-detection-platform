/**
 * Authentication Module - Handles user authentication and session management
 * Professional security implementation with encrypted sessions
 */

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.sessionTimeout = 30 * 60 * 1000; // 30 minutes
        this.init();
    }

    /**
     * Initialize authentication system
     */
    init() {
        this.setupAuthForms();
        this.setupSessionManagement();
        this.setupUserInterface();
        this.checkAuthState();
    }

    /**
     * Set up authentication forms with validation
     */
    setupAuthForms() {
        // Login form handler
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin(loginForm);
            });
        }

        // Registration form handler
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegistration(registerForm);
            });
        }

        // Logout handlers
        document.querySelectorAll('.logout-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleLogout();
            });
        });
    }

    /**
     * Handle user login
     */
    async handleLogin(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Show loading state
        this.setLoadingState(submitBtn, 'Logging in...');

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json();

            if (result.success) {
                this.onLoginSuccess(result.user);
                window.location.href = result.redirect || '/dashboard';
            } else {
                this.showAuthError(form, result.message || 'Login failed');
            }
        } catch (error) {
            this.showAuthError(form, 'Connection error. Please try again.');
        } finally {
            this.resetLoadingState(submitBtn, 'Sign In');
        }
    }

    /**
     * Handle user registration
     */
    async handleRegistration(form) {
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Validate password confirmation
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        if (password !== confirmPassword) {
            this.showAuthError(form, 'Passwords do not match');
            return;
        }

        // Show loading state
        this.setLoadingState(submitBtn, 'Creating account...');

        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const result = await response.json();

            if (result.success) {
                this.showAuthSuccess(form, 'Account created successfully! You can now log in.');
                // Redirect to login or dashboard
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                this.showAuthError(form, result.message || 'Registration failed');
            }
        } catch (error) {
            this.showAuthError(form, 'Connection error. Please try again.');
        } finally {
            this.resetLoadingState(submitBtn, 'Create Account');
        }
    }

    /**
     * Handle user logout
     */
    async handleLogout() {
        try {
            const response = await fetch('/auth/logout', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                this.onLogoutSuccess();
                window.location.href = '/';
            }
        } catch (error) {
            console.error('Logout error:', error);
            // Force logout on client side
            this.onLogoutSuccess();
            window.location.href = '/';
        }
    }

    /**
     * Set loading state for submit buttons
     */
    setLoadingState(button, text) {
        button.disabled = true;
        button.innerHTML = `<i class="bi bi-arrow-clockwise spin"></i> ${text}`;
    }

    /**
     * Reset loading state for submit buttons
     */
    resetLoadingState(button, text) {
        button.disabled = false;
        button.innerHTML = text;
    }

    /**
     * Show authentication error message
     */
    showAuthError(form, message) {
        let errorDiv = form.querySelector('.auth-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-danger auth-error';
            form.insertBefore(errorDiv, form.firstChild);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    /**
     * Show authentication success message
     */
    showAuthSuccess(form, message) {
        let successDiv = form.querySelector('.auth-success');
        if (!successDiv) {
            successDiv = document.createElement('div');
            successDiv.className = 'alert alert-success auth-success';
            form.insertBefore(successDiv, form.firstChild);
        }
        successDiv.textContent = message;
        successDiv.style.display = 'block';
    }

    /**
     * Handle successful login
     */
    onLoginSuccess(user) {
        this.currentUser = user;
        this.updateUserInterface();
        this.startSessionTimer();
    }

    /**
     * Handle successful logout
     */
    onLogoutSuccess() {
        this.currentUser = null;
        this.clearSessionTimer();
        this.updateUserInterface();
    }

    /**
     * Set up session management
     */
    setupSessionManagement() {
        // Check session periodically
        setInterval(() => {
            this.checkSessionValidity();
        }, 5 * 60 * 1000); // Check every 5 minutes

        // Extend session on user activity
        ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
            document.addEventListener(event, () => {
                this.extendSession();
            });
        });
    }

    /**
     * Start session timeout timer
     */
    startSessionTimer() {
        this.clearSessionTimer();
        this.sessionTimer = setTimeout(() => {
            this.handleSessionTimeout();
        }, this.sessionTimeout);
    }

    /**
     * Clear session timeout timer
     */
    clearSessionTimer() {
        if (this.sessionTimer) {
            clearTimeout(this.sessionTimer);
            this.sessionTimer = null;
        }
    }

    /**
     * Extend session on user activity
     */
    extendSession() {
        if (this.currentUser) {
            this.startSessionTimer();
        }
    }

    /**
     * Handle session timeout
     */
    handleSessionTimeout() {
        alert('Your session has expired. Please log in again.');
        this.handleLogout();
    }

    /**
     * Check session validity with server
     */
    async checkSessionValidity() {
        if (!this.currentUser) return;

        try {
            const response = await fetch('/auth/check-session', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                this.handleLogout();
            }
        } catch (error) {
            console.error('Session check error:', error);
        }
    }

    /**
     * Check current authentication state
     */
    checkAuthState() {
        // Check if user data is available in page
        const userDataElement = document.getElementById('user-data');
        if (userDataElement) {
            try {
                this.currentUser = JSON.parse(userDataElement.textContent);
                this.updateUserInterface();
                this.startSessionTimer();
            } catch (error) {
                console.error('Error parsing user data:', error);
            }
        }
    }

    /**
     * Set up user interface elements
     */
    setupUserInterface() {
        // Toggle password visibility
        document.querySelectorAll('.toggle-password').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const input = document.querySelector(btn.getAttribute('data-target'));
                const icon = btn.querySelector('i');
                
                if (input.type === 'password') {
                    input.type = 'text';
                    icon.className = 'bi bi-eye-slash';
                } else {
                    input.type = 'password';
                    icon.className = 'bi bi-eye';
                }
            });
        });
    }

    /**
     * Update user interface based on auth state
     */
    updateUserInterface() {
        const userMenus = document.querySelectorAll('.user-menu');
        const guestMenus = document.querySelectorAll('.guest-menu');
        const userNameElements = document.querySelectorAll('.user-name');

        if (this.currentUser) {
            // Show user menus, hide guest menus
            userMenus.forEach(menu => menu.style.display = 'block');
            guestMenus.forEach(menu => menu.style.display = 'none');
            
            // Update user name displays
            userNameElements.forEach(element => {
                element.textContent = this.currentUser.username || this.currentUser.email;
            });
        } else {
            // Show guest menus, hide user menus
            userMenus.forEach(menu => menu.style.display = 'none');
            guestMenus.forEach(menu => menu.style.display = 'block');
        }
    }

    /**
     * Get current user
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        return this.currentUser !== null;
    }
}

// Export for use in main application
window.AuthManager = AuthManager;