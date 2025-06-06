#!/usr/bin/env python3
"""
Local Environment Setup and Login Fix Utility
Fixes common issues when running the platform locally
"""

import os
import json
import secrets
from pathlib import Path

def create_env_file():
    """Create .env file with required environment variables"""
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env file already exists")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'SESSION_SECRET' in content:
                print("✅ SESSION_SECRET already configured")
                return True
    
    # Generate secure session secret
    session_secret = secrets.token_hex(32)
    
    env_content = f"""# AI Phishing Detection Platform - Environment Variables
# This file contains sensitive configuration for local development

# Session Management (Required for login/logout)
SESSION_SECRET={session_secret}

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration (Optional - uses JSON fallback by default)
# DATABASE_URL=mongodb://localhost:27017/phishing_detector

# Security Settings
USER_ENCRYPTION_SECRET={secrets.token_hex(32)}

# Application Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with secure session configuration")
    return True

def verify_data_directory():
    """Ensure data directory exists with proper structure"""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Check if users.json exists
    users_file = data_dir / 'users.json'
    if not users_file.exists():
        print("⚠️  Users database not found, creating default accounts...")
        create_default_users()
    else:
        print("✅ Users database found")
    
    # Create other required data files
    required_files = [
        'security_tips.json',
        'detections.json',
        'scan_logs.json'
    ]
    
    for filename in required_files:
        file_path = data_dir / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump([], f)
            print(f"✅ Created {filename}")

def create_default_users():
    """Create default user accounts for local testing"""
    from werkzeug.security import generate_password_hash
    
    default_users = [
        {
            "id": "super_admin_001",
            "_id": "users_1_local",
            "username": "super_admin",
            "email": "admin@localhost.com",
            "password_hash": generate_password_hash("SuperAdmin123!"),
            "role": "super_admin",
            "active": True,
            "is_active": True,
            "created_at": "2025-06-06T00:00:00Z",
            "last_login": None,
            "login_attempts": 0,
            "locked_until": None
        },
        {
            "id": "user_001_local",
            "_id": "users_2_local",
            "username": "potato",
            "email": "user@localhost.com",
            "password_hash": generate_password_hash("potato123"),
            "role": "user",
            "active": True,
            "is_active": True,
            "created_at": "2025-06-06T00:00:00Z",
            "last_login": None,
            "login_attempts": 0,
            "locked_until": None
        }
    ]
    
    users_file = Path('data/users.json')
    with open(users_file, 'w') as f:
        json.dump(default_users, f, indent=2)
    
    print("✅ Created default user accounts")
    print("   Super Admin: super_admin / SuperAdmin123!")
    print("   Regular User: potato / potato123")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_modules = [
        'flask',
        'werkzeug',
        'pymongo',
        'cryptography',
        'numpy'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements-local.txt")
        return False
    else:
        print("✅ All dependencies installed")
        return True

def fix_local_environment():
    """Complete local environment setup"""
    print("🔧 Local Environment Setup for AI Phishing Detection Platform")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Create environment file
    create_env_file()
    
    # Setup data directory
    verify_data_directory()
    
    # Create required directories
    required_dirs = ['uploads', 'static/uploads', 'instance', 'logs']
    for dir_name in required_dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    print("\n✅ Local environment setup complete!")
    print("\n🚀 To start the application:")
    print("1. python main.py")
    print("2. Open browser: http://localhost:8080")
    print("3. Login with: super_admin / SuperAdmin123!")
    
    return True

if __name__ == "__main__":
    fix_local_environment()