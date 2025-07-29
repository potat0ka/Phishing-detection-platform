"""
Flask Application Configuration
============================

This file contains all configuration settings for the AI Phishing Detection Platform.
It handles environment variables, database connections, and app settings.

Author: Bigendra Shrestha
Project: AI Phishing Detection Platform with MongoDB
"""

import os
from datetime import timedelta


class Config:
    """
    Main configuration class for Flask application
    
    This class manages all app settings including:
    - Database connections (MongoDB)
    - Security settings
    - Session management
    - File upload configurations
    """
    
    # Flask App Settings
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    DEBUG = True  # Change to False in production
    
    # MongoDB Configuration
    # The MONGO_URI connects to MongoDB Atlas or local MongoDB instance
    MONGO_URI = os.environ.get('MONGO_URI') or os.environ.get('MONGODB_URI', 'mongodb+srv://bigendraengineer:ztGPNnUgGp5F8Mie@cluster0.19pf3wn.mongodb.net/phishing_detection_db?retryWrites=true&w=majority')
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # Set to True with HTTPS in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    # Security Settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # AI/ML Model Settings
    ML_MODEL_CONFIDENCE_THRESHOLD = 0.7
    MAX_URL_LENGTH = 2048
    
    # Application Info
    APP_NAME = "AI Phishing Detection Platform"
    VERSION = "2.0.0"
    AUTHOR = "Bigendra Shrestha"


# Development Configuration (current active config)
class DevelopmentConfig(Config):
    """Development-specific settings"""
    DEBUG = True
    TESTING = False


# Production Configuration (for deployment)
class ProductionConfig(Config):
    """Production-specific settings"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True


# Testing Configuration
class TestingConfig(Config):
    """Testing-specific settings"""
    TESTING = True
    DEBUG = True
    MONGO_URI = 'mongodb://localhost:27017/test_phishing_db'


# Configuration selector based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Default configuration
config = DevelopmentConfig