from functools import wraps
from flask import session, redirect, url_for, flash

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session and session['user_id'] is not None

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def format_confidence(confidence):
    """Format confidence score as percentage"""
    return f"{confidence * 100:.1f}%"

def get_risk_color(classification):
    """Get Bootstrap color class for risk level"""
    colors = {
        'safe': 'success',
        'suspicious': 'warning', 
        'phishing': 'danger',
        'error': 'secondary'
    }
    return colors.get(classification, 'secondary')

def get_risk_icon(classification):
    """Get Font Awesome icon for risk level"""
    icons = {
        'safe': 'fa-shield-alt',
        'suspicious': 'fa-exclamation-triangle',
        'phishing': 'fa-times-circle',
        'error': 'fa-question-circle'
    }
    return icons.get(classification, 'fa-question-circle')

def truncate_text(text, max_length=100):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
