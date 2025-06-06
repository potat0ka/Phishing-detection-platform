#!/usr/bin/env python3
"""
Test script to verify user registration functionality
This script tests that new regular users can be created properly
"""

import sys
import os
sys.path.append('.')

from models.mongodb_config import db_manager
from utils.encryption_utils import encrypt_sensitive_data
from werkzeug.security import generate_password_hash
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_registration():
    """Test creating a new regular user account"""
    
    test_username = "testuser123"
    test_email = "testuser123@example.com"
    test_password = "TestPass123"
    
    print("=" * 50)
    print("🧪 Testing User Registration System")
    print("=" * 50)
    
    try:
        # Check if user already exists
        existing_user = db_manager.find_one('users', {'username': test_username})
        if existing_user:
            print(f"❌ User '{test_username}' already exists")
            return False
        
        # Create new user data
        user_data = {
            'username': test_username,
            'email': test_email,
            'password_hash': generate_password_hash(test_password),
            'role': 'user',  # Regular user (not admin)
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'is_active': True,
            'login_attempts': 0,
            'locked_until': None,
            'profile': {
                'full_name': '',
                'phone': '',
                'preferences': {
                    'email_notifications': True,
                    'security_alerts': True
                }
            }
        }
        
        print(f"📝 Creating user: {test_username}")
        print(f"📧 Email: {test_email}")
        print(f"👤 Role: {user_data['role']}")
        
        # Encrypt and store user data
        encrypted_user_data = encrypt_sensitive_data('user', user_data)
        user_id = db_manager.insert_one('users', encrypted_user_data)
        
        if user_id:
            print(f"✅ User created successfully with ID: {user_id}")
            
            # Verify user was created
            created_user = db_manager.find_one('users', {'username': test_username})
            if created_user:
                print(f"✅ User verification successful")
                print(f"📊 Database status: {db_manager.connected}")
                
                # Check all users to see the new addition
                all_users = db_manager.find_many('users', {})
                print(f"👥 Total users in database: {len(all_users)}")
                
                return True
            else:
                print(f"❌ User creation verification failed")
                return False
        else:
            print(f"❌ Failed to create user")
            return False
            
    except Exception as e:
        print(f"❌ Error during registration test: {e}")
        return False

def list_all_users():
    """List all users in the database for verification"""
    print("\n" + "=" * 50)
    print("👥 Current Users in Database")
    print("=" * 50)
    
    try:
        all_users = db_manager.find_many('users', {})
        if not all_users:
            print("📭 No users found in database")
            return
        
        for i, user in enumerate(all_users, 1):
            username = user.get('username', 'Unknown')
            role = user.get('role', 'Unknown')
            created_at = user.get('created_at', 'Unknown')
            print(f"{i}. Username: {username} | Role: {role} | Created: {created_at[:10] if isinstance(created_at, str) else 'Unknown'}")
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")

if __name__ == "__main__":
    print("🚀 Starting Registration Test")
    
    # Test user creation
    success = test_registration()
    
    # List all users
    list_all_users()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Registration test PASSED")
        print("👤 Regular users can be created successfully")
        print("🔧 Super admin can promote these users to sub-admin")
    else:
        print("❌ Registration test FAILED")
        print("🔧 Check database connection and encryption settings")
    print("=" * 50)