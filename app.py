import os
import logging
import json
from flask import Flask
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "phishing-detector-secret-key-2024")

# Simple JSON-based database for learning
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
            logging.info(f"Created database file: {file_path}")

def load_json_data(file_path):
    """Load data from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json_data(file_path, data):
    """Save data to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, default=str)

# Initialize database files
init_database_files()

# Import routes
import routes

# Initialize default security tips data
with app.app_context():
    from routes import initialize_tips
    initialize_tips()
