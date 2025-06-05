/**
 * Enhanced Password Toggle Functionality
 * Provides secure password visibility toggle with visual effects
 */

document.addEventListener('DOMContentLoaded', function() {
    initPasswordToggle();
});

function initPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const targetSelector = this.getAttribute('data-target');
            const target = document.querySelector(targetSelector);
            const icon = this.querySelector('.password-toggle-icon, i');
            
            if (!target || !icon) {
                console.error('Password toggle: Target input or icon not found');
                return;
            }
            
            // Add visual feedback
            this.classList.add('toggle-active');
            
            if (target.type === 'password') {
                // Show password
                target.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
                this.setAttribute('title', 'Hide Password');
                
                // Visual feedback
                target.style.backgroundColor = 'rgba(13, 110, 253, 0.1)';
                target.style.transition = 'background-color 0.3s ease';
                
                // Auto-hide after 30 seconds for security
                setTimeout(() => {
                    if (target.type === 'text') {
                        target.type = 'password';
                        icon.classList.remove('bi-eye-slash');
                        icon.classList.add('bi-eye');
                        this.setAttribute('title', 'Show Password');
                        target.style.backgroundColor = '';
                    }
                }, 30000);
            } else {
                // Hide password
                target.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
                this.setAttribute('title', 'Show Password');
                target.style.backgroundColor = '';
            }
            
            // Remove active state after animation
            setTimeout(() => {
                this.classList.remove('toggle-active');
            }, 200);
        });
        
        // Add hover effects
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Make function globally available for dynamic content
window.initPasswordToggle = initPasswordToggle;