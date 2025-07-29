"""
AI Phishing Detection Platform - Main Flask Application
======================================================

This is the main Flask application file that initializes and configures the app.
It sets up MongoDB connection, registers route blueprints, and starts the server.

Folder Structure:
- app.py: Main application (this file)
- config.py: Configuration settings
- routes/: All route handlers (landing, admin, API)
- models/: MongoDB models and database logic
- utils/: Helper functions (validation, formatting, etc.)
- templates/: HTML templates
- static/: CSS, JS, images

Author: Bigendra Shrestha
Project: AI Phishing Detection Platform with MongoDB
"""

import os
import logging
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import config

# Configure logging for better debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Initialize MongoDB connection
# PyMongo connects to MongoDB using the MONGO_URI from config
mongo = PyMongo(app)

# Make mongo available to other modules (type: ignore for Flask extension)
app.mongo = mongo  # type: ignore

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # type: ignore
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Flask-Login User class
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, email, role='user'):
        self.id = str(user_id)
        self.username = username
        self.email = email
        self.role = role

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login sessions with fallback support"""
    try:
        from models.user_model import UserModel
        user_data = UserModel.find_user_by_id(int(user_id))
        if user_data:
            return User(
                user_id=user_data['_id'],
                username=user_data['username'],
                email=user_data['email'],
                role=user_data.get('role', 'user')
            )
    except Exception as e:
        logger.error(f"Error loading user {user_id}: {e}")
        # Fallback: Create a temporary user for local development
        if user_id:
            return User(
                user_id=user_id,
                username='local_user',
                email='user@local.dev',
                role='user'
            )
    return None

# Initialize MongoDB service
from services.mongo_service import mongo_service

# Initialize scan history model
try:
    from models.scan_history_model import initialize_scan_history_model
    initialize_scan_history_model()
    logger.info("Scan history model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize scan history model: {e}")

# Import and register route blueprints
# Blueprints organize routes into separate modules
try:
    from routes import main_bp, auth_bp, admin_bp, rbac_bp
    from routes.dashboard_routes import dashboard_bp
    from utils.rbac_decorators import init_template_globals
    
    # Initialize RBAC template globals
    init_template_globals(app)
    
    # Register blueprints with URL prefixes
    app.register_blueprint(main_bp)           # Main routes: /, /check, /tips
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes: /auth/login, /auth/register
    app.register_blueprint(admin_bp, url_prefix='/admin') # Admin routes: /admin/dashboard
    app.register_blueprint(dashboard_bp)      # User dashboard: /dashboard
    app.register_blueprint(rbac_bp)           # RBAC routes: /rbac/*
    
    logger.info("All route blueprints registered successfully")
except ImportError as e:
    logger.error(f"Failed to import route blueprints: {e}")

# Global error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors with custom template"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with fallback"""
    logger.error(f"Internal server error: {error}")
    return render_template('errors/500.html'), 500

# Context processor to make common data available to templates
@app.context_processor
def inject_app_info():
    """Make app info available to all templates"""
    return {
        'app_name': app.config['APP_NAME'],
        'version': app.config['VERSION'],
        'author': app.config['AUTHOR']
    }

if __name__ == '__main__':
    # App startup message for beginners
    logger.info("=" * 60)
    logger.info("AI Phishing Detection Platform Starting")
    logger.info("=" * 60)
    logger.info(f"Author: {app.config['AUTHOR']}")
    logger.info("Project: Cybersecurity & AI Platform")
    logger.info("=" * 60)
    logger.info("Web server starting...")
    logger.info("Access URL: http://localhost:8080")
    logger.info("Press Ctrl+C to stop the server")
    logger.info("=" * 60)
    
    # Start Flask development server  
    app.run(host='0.0.0.0', port=8080, debug=True)