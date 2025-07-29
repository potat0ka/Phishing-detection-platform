"""
User Model - Clean MongoDB User Management
========================================

This model handles user authentication and management using the centralized MongoDB service.
It manages user accounts, sessions, and role-based access control.

Author: Bigendra Shrestha
"""

import logging
import bcrypt
from datetime import datetime
from services.mongo_service import mongo_service

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

class UserModel:
    """User Model for MongoDB operations"""
    
    @staticmethod
    def create_user(username, email, password, role='user'):
        """Create a new user account with bcrypt hashing"""
        try:
            password_hash = hash_password(password)
            
            user_data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'role': role,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'last_login': None,
                'login_attempts': 0
            }
            
            if mongo_service.is_connected():
                result = mongo_service.insert_document('users', user_data)
                if result:
                    logger.info(f"User created successfully: {username}")
                    return result
                else:
                    logger.error(f"Failed to create user in database: {username}")
                    return None
            else:
                logger.error("MongoDB connection not available")
                return None
                
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def find_user_by_email(email):
        """Find user by email address"""
        try:
            if mongo_service.is_connected():
                return mongo_service.find_document('users', {'email': email})
            return None
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    @staticmethod
    def find_user_by_username(username):
        """Find user by username"""
        try:
            if mongo_service.is_connected():
                return mongo_service.find_document('users', {'username': username})
            return None
        except Exception as e:
            logger.error(f"Error finding user by username: {e}")
            return None
    
    @staticmethod
    def find_user_by_id(user_id):
        """Find user by ID"""
        try:
            if mongo_service.is_connected():
                from bson import ObjectId
                if isinstance(user_id, str):
                    user_id = ObjectId(user_id)
                return mongo_service.find_document('users', {'_id': user_id})
            return None
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user with email and password"""
        try:
            user = UserModel.find_user_by_email(email)
            if user and verify_password(password, user['password_hash']):
                # Update last login
                UserModel.update_last_login(user['_id'])
                return user
            return None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return None
    
    @staticmethod
    def update_last_login(user_id):
        """Update user's last login timestamp"""
        try:
            if mongo_service.is_connected():
                from bson import ObjectId
                if isinstance(user_id, str):
                    user_id = ObjectId(user_id)
                mongo_service.update_document(
                    'users', 
                    {'_id': user_id}, 
                    {'last_login': datetime.utcnow()}
                )
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
    
    @staticmethod
    def get_all_users():
        """Get all users for admin management"""
        try:
            if mongo_service.is_connected():
                return mongo_service.find_documents('users', {}, sort=[('created_at', -1)])
            return []
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    @staticmethod
    def update_user_role(user_id, new_role):
        """Update user role for admin operations"""
        try:
            if mongo_service.is_connected():
                from bson import ObjectId
                if isinstance(user_id, str):
                    user_id = ObjectId(user_id)
                result = mongo_service.update_document(
                    'users',
                    {'_id': user_id},
                    {'role': new_role}
                )
                return result > 0
            return False
        except Exception as e:
            logger.error(f"Error updating user role: {e}")
            return False
    
    @staticmethod
    def get_user_count():
        """Get total number of users"""
        try:
            if mongo_service.is_connected():
                return mongo_service.count_documents('users', {})
            return 0
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
    
    @staticmethod
    def get_admin_count():
        """Get total number of admin users"""
        try:
            if mongo_service.is_connected():
                return mongo_service.count_documents('users', {'role': 'admin'})
            return 0
        except Exception as e:
            logger.error(f"Error getting admin count: {e}")
            return 0
    
    @staticmethod
    def get_superadmin_count():
        """Get total number of superadmin users"""
        try:
            if mongo_service.is_connected():
                return mongo_service.count_documents('users', {'role': 'superadmin'})
            return 0
        except Exception as e:
            logger.error(f"Error getting superadmin count: {e}")
            return 0
    
    @staticmethod
    def get_users_by_role(role):
        """Get all users with specified role"""
        try:
            if mongo_service.is_connected():
                return mongo_service.find_documents('users', {'role': role})
            return []
        except Exception as e:
            logger.error(f"Error getting users by role: {e}")
            return []
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate a user account"""
        try:
            if mongo_service.is_connected():
                from bson import ObjectId
                if isinstance(user_id, str):
                    user_id = ObjectId(user_id)
                result = mongo_service.update_document(
                    'users',
                    {'_id': user_id},
                    {'is_active': False, 'deactivated_at': datetime.utcnow()}
                )
                return result > 0
            return False
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            return False