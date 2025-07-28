
#!/usr/bin/env python3
"""
Setup MongoDB Users with Bcrypt Passwords
=========================================

This script creates test users in MongoDB with properly hashed passwords.
"""

import os
import bcrypt
from pymongo import MongoClient
from datetime import datetime

def setup_mongodb_users():
    """Create test users in MongoDB with bcrypt hashed passwords"""
    try:
        # Get MongoDB URI from environment
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            mongo_uri = os.getenv("MONGODB_URI")
            
        if not mongo_uri:
            print("❌ No MongoDB URI found in environment variables")
            return False
        
        print("🔗 Connecting to MongoDB...")
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            tlsAllowInvalidCertificates=True,
            retryWrites=True
        )
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")
        
        db = client['phishing_detector']
        users_collection = db.users
        
        # Create test users with bcrypt hashed passwords
        test_users = [
            {
                'username': 'testuser',
                'email': 'user@test.com',
                'password': 'password123',
                'role': 'user'
            },
            {
                'username': 'testadmin', 
                'email': 'admin@test.com',
                'password': 'password123',
                'role': 'admin'
            },
            {
                'username': 'testsuperadmin',
                'email': 'superadmin@test.com',
                'password': 'password123', 
                'role': 'superadmin'
            },
            {
                'username': 'superadmin',
                'email': 'superadmin@example.com',
                'password': 'password123',
                'role': 'superadmin'
            }
        ]
        
        # Special case for superadmin@example.com to ensure correct hash
        special_user = {
            'username': 'superadmin',
            'email': 'superadmin@example.com',
            'password_hash': '$2b$12$O34hDrO3oSmtxK3ObiLrcew3A1W.kMQbE6Z4NSIYKkb9lEZk9TD8C',
            'role': 'superadmin',
            'is_active': True,
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        
        # Insert the special user first
        existing_special = users_collection.find_one({'email': 'superadmin@example.com'})
        if existing_special:
            users_collection.update_one(
                {'email': 'superadmin@example.com'},
                {'$set': special_user}
            )
            print(f"✅ Updated special user: superadmin@example.com (superadmin)")
        else:
            users_collection.insert_one(special_user)
            print(f"✅ Created special user: superadmin@example.com (superadmin)")
        
        for user_data in test_users:
            # Check if user already exists
            existing = users_collection.find_one({'email': user_data['email']})
            
            # Hash password with bcrypt
            password_hash = bcrypt.hashpw(
                user_data['password'].encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            user_doc = {
                'username': user_data['username'],
                'email': user_data['email'],
                'password_hash': password_hash,  # Store as password_hash
                'role': user_data['role'],
                'is_active': True,
                'created_at': datetime.utcnow(),
                'last_login': None
            }
            
            if existing:
                # Update existing user with new hashed password
                users_collection.update_one(
                    {'email': user_data['email']},
                    {'$set': user_doc}
                )
                print(f"✅ Updated user: {user_data['email']} ({user_data['role']})")
            else:
                # Create new user
                users_collection.insert_one(user_doc)
                print(f"✅ Created user: {user_data['email']} ({user_data['role']})")
        
        print(f"\n🎉 Setup complete! All users have password: password123")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    setup_mongodb_users()
