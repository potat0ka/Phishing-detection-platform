"""
Application Configuration
========================

Professional configuration management for the phishing detection platform.
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    
    # Database Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DB_NAME', 'phishing_detector')
    
    # Security Configuration
    USER_ENCRYPTION_SECRET = os.getenv('USER_ENCRYPTION_SECRET')
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 86400))  # 24 hours
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {
        'image': {'jpg', 'jpeg', 'png', 'gif', 'webp'},
        'video': {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'},
        'audio': {'mp3', 'wav', 'ogg', 'aac', 'm4a'},
        'document': {'txt', 'pdf', 'doc', 'docx'}
    }
    
    # AI Configuration
    AI_MODEL_CONFIDENCE_THRESHOLD = 0.85
    AI_POSSIBLE_THRESHOLD = 0.65
    
    # Privacy Configuration
    DEFAULT_DATA_RETENTION_DAYS = 365
    ENCRYPTION_ALGORITHM = 'AES-256'
    KEY_DERIVATION_ITERATIONS = 100000


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_NAME = 'phishing_detector_test'


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(env, DevelopmentConfig)()


# Application settings
APP_CONFIG = get_config()