"""
AI Phishing Detection Platform - Professional Flask Application
==============================================================

Modular Flask application with MongoDB backend, authentication system,
and comprehensive user data encryption using AES-256.
"""

import os
import json
import logging
from datetime import timedelta
from pathlib import Path
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask application with professional configuration
app = Flask(__name__)

# Security configuration
app.secret_key = os.environ.get("SESSION_SECRET", os.urandom(32))
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
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

# Ensure upload directory exists
upload_dir = Path(UPLOAD_FOLDER)
upload_dir.mkdir(exist_ok=True)

def allowed_file(filename, file_type):
    """Check if uploaded file has allowed extension"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS.get(file_type, set())

# Initialize MongoDB connection
try:
    from pymongo import MongoClient
    
    # MongoDB configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DB_NAME', 'phishing_detector')
    
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    
    # Test connection
    mongo_client.admin.command('ping')
    db = mongo_client[DATABASE_NAME]
    
    # Create indexes for performance
    db.users.create_index("created_at")
    db.detections.create_index([("user_id", 1), ("created_at", -1)])
    
    logger.info(f"Connected to MongoDB database: {DATABASE_NAME}")
    
except Exception as e:
    logger.warning(f"MongoDB connection failed, using JSON fallback: {e}")
    # Fallback to JSON database system
    DATABASE_DIR = Path("database")
    DATABASE_DIR.mkdir(exist_ok=True)
    
    USERS_FILE = DATABASE_DIR / "users.json"
    DETECTIONS_FILE = DATABASE_DIR / "detections.json"
    TIPS_FILE = DATABASE_DIR / "tips.json"
    
    def init_database_files():
        """Initialize JSON database files"""
        for file_path in [USERS_FILE, DETECTIONS_FILE, TIPS_FILE]:
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    json.dump([], f)
    
    def load_json_data(file_path):
        """Load data from JSON file"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON data: {e}")
        return []
    
    def save_json_data(file_path, data):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving JSON data: {e}")
    
    init_database_files()
    db = None  # Indicate JSON mode

# Import routes after app initialization
import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)