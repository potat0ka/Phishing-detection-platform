"""
AI Phishing Detection Platform - Main Application File
====================================================

This is the main Flask application file that sets up:
1. Flask web application
2. Simple JSON-based database system (perfect for learning!)
3. Application configuration
4. Database initialization

Perfect for beginners learning backend development!
"""

import os
import logging
import json
from flask import Flask
from datetime import datetime
from pathlib import Path

# Configure logging to see what's happening (great for debugging!)
logging.basicConfig(
    level=logging.INFO,  # Changed to INFO for cleaner output
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create the main Flask application
app = Flask(__name__)

# Set a secret key for session management (keeps user login secure)
# In production, always use a random secret key from environment variables
app.secret_key = os.environ.get("SESSION_SECRET", "phishing-detector-secret-key-2024")

# Configure file uploads for AI content detection
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'txt', 'doc', 'docx', 'pdf'}

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename, file_type):
    """Check if uploaded file has allowed extension"""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'image':
        return extension in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'document':
        return extension in ALLOWED_DOCUMENT_EXTENSIONS
    
    return False

# ============================================================================
# SIMPLE JSON DATABASE SYSTEM (Perfect for Learning!)
# ============================================================================
# Instead of complex databases like PostgreSQL or MongoDB, we use simple JSON files
# This makes it easy to understand and see exactly what data is stored

# Create a directory to store our database files
DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist

# Define our "database tables" as JSON files
USERS_FILE = DATABASE_DIR / "users.json"          # Stores user accounts
DETECTIONS_FILE = DATABASE_DIR / "detections.json"  # Stores phishing detection results
TIPS_FILE = DATABASE_DIR / "tips.json"            # Stores security tips

def init_database_files():
    """
    Initialize JSON database files with empty arrays
    This function creates empty JSON files if they don't exist
    """
    for file_path in [USERS_FILE, DETECTIONS_FILE, TIPS_FILE]:
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump([], f)  # Start with empty list
            logging.info(f"Created database file: {file_path}")

def load_json_data(file_path):
    """
    Load data from a JSON file
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        List of data from the file, or empty list if file doesn't exist
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is corrupted, return empty list
        return []

def save_json_data(file_path, data):
    """
    Save data to a JSON file
    
    Args:
        file_path: Path to the JSON file
        data: Data to save (usually a list of dictionaries)
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)  # indent=2 makes it readable

# Initialize our database files when the app starts
init_database_files()

# Import all our web routes (this must come after database setup)
import routes

# Initialize default security tips when the app starts
with app.app_context():
    from routes import initialize_tips
    initialize_tips()

# This allows the app to be run directly with: python app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
