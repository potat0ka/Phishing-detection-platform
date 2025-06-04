"""
Professional AI Phishing Detection Platform
==========================================

Flask application with MongoDB backend and comprehensive user data encryption.
"""

import os
import logging
from pathlib import Path
from flask import Flask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configuration
from config.settings import APP_CONFIG

# Create Flask application
app = Flask(__name__)
app.config.from_object(APP_CONFIG)

# Ensure upload directory exists
upload_dir = Path(APP_CONFIG.UPLOAD_FOLDER)
upload_dir.mkdir(exist_ok=True)

# Initialize database connection
try:
    from database.connection import connect_to_database, health_check
    connect_to_database()
    if health_check():
        logger.info("Database connection established successfully")
    else:
        logger.warning("Database health check failed")
except Exception as e:
    logger.error(f"Database initialization error: {e}")

# File upload validation
def allowed_file(filename: str, file_type: str) -> bool:
    """Check if uploaded file has allowed extension"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in APP_CONFIG.ALLOWED_EXTENSIONS.get(file_type, set())

# Import routes after app initialization
from routes import *

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=APP_CONFIG.DEBUG
    )