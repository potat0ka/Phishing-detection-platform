"""
AI Phishing Detection Platform - Flask Application Configuration
==============================================================

This file sets up the Flask web application with all necessary configurations,
security settings, database connections, and error handling.

For beginners:
- Flask is a web framework that helps create websites with Python
- This file configures how the website behaves (security, database, file uploads)
- Think of it as the "settings" file for the entire platform
- All routes (web pages) are imported at the bottom of this file

Key components:
1. Security settings (encryption, sessions, file upload limits)
2. Database initialization (MongoDB with JSON fallback)
3. Error handling (404, 500 errors)
4. File upload configuration
5. Route imports (connecting web pages to the app)
"""

import os
import json
import logging
from datetime import timedelta
from pathlib import Path
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure professional logging system
# This helps track what happens in the application and debug issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the main Flask application instance
# This is the core of our web application
app = Flask(__name__)

# Security configuration for user sessions and data protection
# SESSION_SECRET is used to encrypt user session data
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(32))
app.config['SESSION_PERMANENT'] = True  # Keep users logged in
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)  # Auto-logout after 2 hours
app.config['SESSION_COOKIE_SECURE'] = True if os.environ.get('FLASK_ENV') == 'production' else False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Proxy fix for production deployment
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# File upload configuration
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'image': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
    'video': {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'},
    'audio': {'mp3', 'wav', 'ogg', 'aac', 'm4a'},
    'document': {'txt', 'pdf', 'doc', 'docx'}
}

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create necessary directories
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)
Path('analysis_results').mkdir(exist_ok=True)
Path('data').mkdir(exist_ok=True)

def allowed_file(filename, file_type):
    """Check if uploaded file has allowed extension"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS.get(file_type, set())

# Import MongoDB manager and authentication system
from mongodb_config import db_manager
from auth_routes import auth_bp, login_required, admin_required, get_current_user
from encryption_utils import EncryptionManager

# Initialize encryption manager
encryption_manager = EncryptionManager()

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Log database connection status
logger.info(f"Database: {'MongoDB' if db_manager.connected else 'JSON Fallback'}")

# Global template variables
@app.context_processor
def inject_global_vars():
    """Inject global variables into all templates"""
    return {
        'db_connected': db_manager.connected,
        'app_version': '2.0.0',
        'current_user': get_current_user()
    }

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(413)
def too_large(error):
    """Handle file too large errors"""
    return render_template('errors/413.html'), 413

# Application health check
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return {
        'status': 'healthy',
        'database': 'connected' if db_manager.connected else 'fallback',
        'version': '2.0.0'
    }

# Import and register routes after app initialization
import routes

# Register admin blueprint
from admin_routes import admin_bp
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    logger.info("Starting AI Phishing Detection Platform v2.0.0")
    logger.info(f"Database: {'MongoDB' if db_manager.connected else 'JSON Fallback'}")
    app.run(host='0.0.0.0', port=5000, debug=True)