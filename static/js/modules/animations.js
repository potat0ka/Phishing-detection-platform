/**
 * Animation Module - Handles all CSS animations and scroll effects
 * Professional modular architecture for better maintainability
 */

class AnimationManager {
    constructor() {
        this.observers = new Map();
        this.init();
    }

    /**
     * Initialize all animation systems
     */
    init() {
        this.setupScrollAnimations();
        this.initializeHeroAnimations();
        this.initializeProgressAnimations();
    }

    /**
     * Set up intersection observer for scroll-triggered animations
     */
    setupScrollAnimations() {
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    // Handle special animation types
                    if (entry.target.classList.contains('stat-number')) {
                        this.animateCounter(entry.target);
                    }
                    
                    if (entry.target.classList.contains('progress-bar')) {
                        this.animateProgressBar(entry.target);
                    }
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe elements for scroll animations
        document.querySelectorAll('.feature-card, .tip-card, .stat-item, .card').forEach(el => {
            animationObserver.observe(el);
        });

        this.observers.set('scroll', animationObserver);
    }

    /**
     * Initialize hero section staggered animations
     */
    initializeHeroAnimations() {
        const hero = document.querySelector('.hero-section');
        if (!hero) return;

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

        // Shield icon hover effects
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
     * Animate counter numbers with smooth counting effect
     */
    animateCounter(element) {
        const target = element.textContent;
        const isPercentage = target.includes('%');
        const numericValue = parseFloat(target.replace(/[^\d.]/g, ''));
        
        if (isNaN(numericValue)) return;

        let current = 0;
        const increment = numericValue / 60; // 60 frames for 1 second animation
        const suffix = isPercentage ? '%' : '';

        const timer = setInterval(() => {
            current += increment;
            if (current >= numericValue) {
                current = numericValue;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, 16); // ~60fps
    }

    /**
     * Animate progress bars with smooth fill effect
     */
    animateProgressBar(element) {
        const width = element.getAttribute('data-width') || '0%';
        element.style.width = '0%';
        
        setTimeout(() => {
            element.style.transition = 'width 1.5s ease-out';
            element.style.width = width;
        }, 100);
    }

    /**
     * Initialize progress bar animations for all progress elements
     */
    initializeProgressAnimations() {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.animateProgressBar(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });
            
            observer.observe(bar);
        });
    }

    /**
     * Add smooth hover effects to interactive elements
     */
    addHoverEffects(selector, hoverClass = 'hover-lift') {
        document.querySelectorAll(selector).forEach(element => {
            element.addEventListener('mouseenter', () => {
                element.classList.add(hoverClass);
            });
            
            element.addEventListener('mouseleave', () => {
                element.classList.remove(hoverClass);
            });
        });
    }

    /**
     * Cleanup observers when needed
     */
    cleanup() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
    }
}

// Export for use in main application
window.AnimationManager = AnimationManager;