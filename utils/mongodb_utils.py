
import os
import bcrypt
from pymongo import MongoClient
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def get_mongodb_connection():
    """Get MongoDB connection with proper configuration"""
    try:
        mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
        if not mongo_uri:
            logger.warning("No MongoDB URI found in environment variables")
            return None, None

        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
            tlsAllowInvalidCertificates=True,
            retryWrites=True
        )
        
        # Test connection
        client.admin.command('ping')
        db = client['phishing_detector']
        logger.info("MongoDB connection successful")
        
        return client, db.users
    except Exception as e:
        logger.warning(f"MongoDB connection failed: {e}")
        return None, None

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against bcrypt hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def setup_test_users():
    """Setup test users with proper bcrypt passwords"""
    client, users_collection = get_mongodb_connection()
    if not users_collection:
        return False
    
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
    
    for user_data in test_users:
        # Hash password
        password_hash = hash_password(user_data['password'])
        
        user_doc = {
            'username': user_data['username'],
            'email': user_data['email'],
            'password_hash': password_hash,
            'role': user_data['role'],
            'is_active': True,
            'created_at': datetime.utcnow(),
            'last_login': None
        }
        
        # Update or insert user
        users_collection.update_one(
            {'email': user_data['email']},
            {'$set': user_doc},
            upsert=True
        )
        print(f"✅ Setup user: {user_data['email']} ({user_data['role']})")
    
    return True

if __name__ == "__main__":
    setup_test_users()
