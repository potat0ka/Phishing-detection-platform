#!/usr/bin/env python3
"""
Create Test User for Local Development
=====================================

This script creates a test user account for local development when MongoDB is not available.
It creates the user data in a local file for testing authentication.

Usage:
    python create_test_user.py

Author: Bigendra Shrestha
"""

import os
import json
import bcrypt
from datetime import datetime

def create_test_user():
    """Create a test user for local development"""
    print("🔧 Creating Test User for Local Development")
    print("=" * 50)
    
    # Test user data
    username = "testuser"
    email = "test@example.com"
    password = "password123"
    
    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt)
    
    # Create user data
    user_data = {
        "_id": 1,
        "username": username,
        "email": email,
        "password_hash": password_hash.decode('utf-8'),
        "role": "user",
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save user data to local file
    with open('data/test_users.json', 'w') as f:
        json.dump([user_data], f, indent=2)
    
    print("✅ Test user created successfully!")
    print(f"📧 Email: {email}")
    print(f"🔐 Password: {password}")
    print(f"👤 Username: {username}")
    print(f"🎭 Role: user")
    
    print("\n📁 User data saved to: data/test_users.json")
    print("\n🚀 You can now log in with these credentials:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    
    return True

if __name__ == "__main__":
    create_test_user()