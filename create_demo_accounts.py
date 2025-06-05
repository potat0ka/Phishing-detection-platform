#!/usr/bin/env python3
"""
Demo Account Creator for AI Phishing Detection Platform
Creates demo admin and user accounts for testing purposes
"""

import sys
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mongodb_config import db_manager
from encryption_utils import encrypt_sensitive_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_demo_accounts():
    """Create demo admin and user accounts"""
    
    # Initialize database connection
    db_manager.init_connection()
    
    # Demo accounts data
    demo_accounts = [
        {
            'username': 'demo_admin',
            'email': 'admin@demo.com',
            'password': 'admin123',
            'role': 'admin',
            'display_name': 'Demo Administrator'
        },
        {
            'username': 'demo_user',
            'email': 'user@demo.com', 
            'password': 'user123',
            'role': 'user',
            'display_name': 'Demo User'
        }
    ]
    
    logger.info("Creating demo accounts...")
    print("Starting demo account creation...")
    
    for account in demo_accounts:
        try:
            # Check if user already exists by searching all users
            existing_users = db_manager.find_many('users', {})
            user_exists = False
            
            for existing_user in existing_users:
                # Check both encrypted and non-encrypted usernames
                if (existing_user.get('username') == account['username'] or
                    existing_user.get('email') == account['email']):
                    user_exists = True
                    break
            
            if user_exists:
                logger.info(f"User {account['username']} already exists, skipping...")
                continue
            
            # Create user data
            user_data = {
                'username': account['username'],
                'email': account['email'],
                'password_hash': generate_password_hash(account['password']),
                'role': account['role'],
                'display_name': account['display_name'],
                'created_at': datetime.utcnow().isoformat(),
                'last_login': None,
                'is_active': True,
                'login_attempts': 0,
                'locked_until': None,
                'email_verified': True,
                'profile_completed': True
            }
            
            # Don't encrypt demo accounts for easier testing
            # Insert user into database
            user_id = db_manager.insert_one('users', user_data)
            
            if user_id:
                logger.info(f"✓ Created {account['role']} account: {account['username']}")
                logger.info(f"  Email: {account['email']}")
                logger.info(f"  Password: {account['password']}")
                print(f"SUCCESS: Created {account['username']} with password {account['password']}")
            else:
                logger.error(f"✗ Failed to create account: {account['username']}")
                print(f"FAILED: Could not create {account['username']}")
                
        except Exception as e:
            logger.error(f"Error creating account {account['username']}: {e}")
            print(f"ERROR: {e}")
    
    logger.info("\nDemo accounts creation completed!")
    logger.info("\n" + "="*50)
    logger.info("DEMO LOGIN CREDENTIALS:")
    logger.info("="*50)
    logger.info("Admin Account:")
    logger.info("  Username: demo_admin")
    logger.info("  Password: admin123")
    logger.info("")
    logger.info("User Account:")
    logger.info("  Username: demo_user") 
    logger.info("  Password: user123")
    logger.info("="*50)

if __name__ == "__main__":
    create_demo_accounts()