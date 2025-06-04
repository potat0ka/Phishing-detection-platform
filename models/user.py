"""
User Model with MongoDB and Encryption
=====================================

Professional user management with encrypted data storage using MongoDB.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import logging

from database.connection import get_database
from utils.encryption import encrypt_sensitive_data, decrypt_sensitive_data

logger = logging.getLogger(__name__)


class User:
    """User model with encrypted data storage in MongoDB"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self._id = data.get('_id')
        
    @property
    def id(self) -> str:
        """Get user ID as string"""
        return str(self._id) if self._id else None
    
    @property
    def username(self) -> str:
        """Get decrypted username"""
        decrypted = decrypt_sensitive_data('user', self.data)
        return decrypted.get('username', '')
    
    @property
    def email(self) -> str:
        """Get decrypted email"""
        decrypted = decrypt_sensitive_data('user', self.data)
        return decrypted.get('email', '')
    
    @property
    def created_at(self) -> datetime:
        """Get account creation timestamp"""
        return self.data.get('created_at', datetime.utcnow())
    
    def check_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return check_password_hash(self.data.get('password_hash', ''), password)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with decrypted data"""
        decrypted = decrypt_sensitive_data('user', self.data)
        return {
            'id': self.id,
            'username': decrypted.get('username'),
            'email': decrypted.get('email'),
            'created_at': self.created_at,
            'privacy_level': decrypted.get('privacy_level', 'high')
        }
    
    @classmethod
    def create(cls, username: str, email: str, password: str) -> Optional['User']:
        """Create new user with encrypted data"""
        try:
            db = get_database()
            
            # Check if user already exists
            if cls.find_by_username(username) or cls.find_by_email(email):
                return None
            
            # Prepare user data
            user_data = {
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.utcnow(),
                'privacy_level': 'high',
                'data_retention_days': 365,
                'last_login': None
            }
            
            # Encrypt sensitive data
            encrypted_data = encrypt_sensitive_data('user', user_data)
            
            # Insert into database
            result = db.users.insert_one(encrypted_data)
            encrypted_data['_id'] = result.inserted_id
            
            logger.info(f"Created encrypted user account: {result.inserted_id}")
            return cls(encrypted_data)
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @classmethod
    def find_by_username(cls, username: str) -> Optional['User']:
        """Find user by username (searches encrypted data)"""
        try:
            db = get_database()
            
            # Search through all users and decrypt to compare
            for user_doc in db.users.find():
                decrypted = decrypt_sensitive_data('user', user_doc)
                if decrypted.get('username') == username:
                    return cls(user_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by username: {e}")
            return None
    
    @classmethod
    def find_by_email(cls, email: str) -> Optional['User']:
        """Find user by email (searches encrypted data)"""
        try:
            db = get_database()
            
            # Search through all users and decrypt to compare
            for user_doc in db.users.find():
                decrypted = decrypt_sensitive_data('user', user_doc)
                if decrypted.get('email') == email:
                    return cls(user_doc)
            
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    @classmethod
    def find_by_id(cls, user_id: str) -> Optional['User']:
        """Find user by ID"""
        try:
            db = get_database()
            user_doc = db.users.find_one({'_id': ObjectId(user_id)})
            
            if user_doc:
                return cls(user_doc)
            return None
            
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    def update_login_time(self) -> bool:
        """Update last login timestamp"""
        try:
            db = get_database()
            
            # Decrypt current data
            decrypted = decrypt_sensitive_data('user', self.data)
            decrypted['last_login'] = datetime.utcnow()
            
            # Re-encrypt and update
            encrypted_data = encrypt_sensitive_data('user', decrypted)
            
            result = db.users.update_one(
                {'_id': self._id},
                {'$set': encrypted_data}
            )
            
            if result.modified_count > 0:
                self.data.update(encrypted_data)
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error updating login time: {e}")
            return False
    
    def delete(self) -> bool:
        """Delete user account permanently"""
        try:
            db = get_database()
            
            # Delete user document
            result = db.users.delete_one({'_id': self._id})
            
            if result.deleted_count > 0:
                # Also delete user's detection history
                db.detections.delete_many({'user_id': str(self._id)})
                logger.info(f"Deleted user account and data: {self._id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
    
    @staticmethod
    def get_user_count() -> int:
        """Get total number of users"""
        try:
            db = get_database()
            return db.users.count_documents({})
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0