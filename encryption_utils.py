"""
User Data Encryption System
===========================

This module provides comprehensive encryption for all user data and activity
to ensure maximum privacy and security protection.

Features:
- Field-level encryption for sensitive data
- Activity log encryption
- Secure key derivation
- Data anonymization options
"""

import os
import json
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserDataEncryption:
    """
    Comprehensive user data encryption system
    
    Encrypts sensitive user information including:
    - Personal details (email, username)
    - Activity logs and detection history
    - File uploads and analysis results
    - Session data and preferences
    """
    
    def __init__(self):
        """Initialize encryption system with secure key derivation"""
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        logger.info("User data encryption system initialized")
    
    def _get_or_create_encryption_key(self):
        """
        Get or create a secure encryption key for user data
        
        The key is derived from a master secret and stored securely
        """
        try:
            # Use environment variable or generate secure key
            master_secret = os.environ.get('USER_ENCRYPTION_SECRET')
            if not master_secret:
                # Generate a secure master secret if not provided
                master_secret = base64.urlsafe_b64encode(os.urandom(32)).decode()
                logger.warning("No USER_ENCRYPTION_SECRET found, generated new key")
            
            # Derive encryption key using PBKDF2
            salt = b'user_data_salt_2024'  # Fixed salt for consistency
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(master_secret.encode()))
            return key
            
        except Exception as e:
            logger.error(f"Error creating encryption key: {e}")
            # Fallback to a default key (not recommended for production)
            return Fernet.generate_key()
    
    def encrypt_user_field(self, data):
        """
        Encrypt sensitive user field data
        
        Args:
            data (str): The data to encrypt
            
        Returns:
            str: Encrypted data as base64 string
        """
        if not data:
            return data
            
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encrypting user field: {e}")
            return data
    
    def decrypt_user_field(self, encrypted_data):
        """
        Decrypt sensitive user field data
        
        Args:
            encrypted_data (str): Base64 encoded encrypted data
            
        Returns:
            str: Decrypted original data
        """
        if not encrypted_data:
            return encrypted_data
            
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error decrypting user field: {e}")
            return encrypted_data
    
    def encrypt_user_profile(self, user_data):
        """
        Encrypt all sensitive fields in user profile
        
        Args:
            user_data (dict): User profile data
            
        Returns:
            dict: User data with encrypted sensitive fields
        """
        encrypted_user = user_data.copy()
        
        # Fields to encrypt for privacy
        sensitive_fields = ['email', 'username', 'full_name', 'phone', 'address']
        
        for field in sensitive_fields:
            if field in encrypted_user:
                encrypted_user[field] = self.encrypt_user_field(encrypted_user[field])
                encrypted_user[f'{field}_encrypted'] = True
        
        # Add encryption metadata
        encrypted_user['encryption_version'] = '1.0'
        encrypted_user['encrypted_at'] = datetime.utcnow().isoformat()
        
        return encrypted_user
    
    def decrypt_user_profile(self, encrypted_user_data):
        """
        Decrypt user profile data for display
        
        Args:
            encrypted_user_data (dict): Encrypted user data
            
        Returns:
            dict: Decrypted user data
        """
        if not encrypted_user_data.get('encryption_version'):
            # Data is not encrypted
            return encrypted_user_data
        
        decrypted_user = encrypted_user_data.copy()
        
        # Fields that were encrypted
        sensitive_fields = ['email', 'username', 'full_name', 'phone', 'address']
        
        for field in sensitive_fields:
            if f'{field}_encrypted' in decrypted_user and decrypted_user.get(f'{field}_encrypted'):
                if field in decrypted_user:
                    decrypted_user[field] = self.decrypt_user_field(decrypted_user[field])
                    # Remove encryption flag for clean data
                    del decrypted_user[f'{field}_encrypted']
        
        return decrypted_user
    
    def encrypt_activity_log(self, activity_data):
        """
        Encrypt user activity and detection history
        
        Args:
            activity_data (dict): Activity log entry
            
        Returns:
            dict: Encrypted activity data
        """
        encrypted_activity = activity_data.copy()
        
        # Encrypt sensitive activity fields
        sensitive_activity_fields = ['input_content', 'user_ip', 'user_agent', 'file_path']
        
        for field in sensitive_activity_fields:
            if field in encrypted_activity:
                encrypted_activity[field] = self.encrypt_user_field(str(encrypted_activity[field]))
                encrypted_activity[f'{field}_encrypted'] = True
        
        # Add activity encryption metadata
        encrypted_activity['activity_encrypted'] = True
        encrypted_activity['activity_encryption_timestamp'] = datetime.utcnow().isoformat()
        
        return encrypted_activity
    
    def decrypt_activity_log(self, encrypted_activity_data):
        """
        Decrypt activity log for display
        
        Args:
            encrypted_activity_data (dict): Encrypted activity data
            
        Returns:
            dict: Decrypted activity data
        """
        if not encrypted_activity_data.get('activity_encrypted'):
            return encrypted_activity_data
        
        decrypted_activity = encrypted_activity_data.copy()
        
        # Decrypt activity fields
        sensitive_activity_fields = ['input_content', 'user_ip', 'user_agent', 'file_path']
        
        for field in sensitive_activity_fields:
            if f'{field}_encrypted' in decrypted_activity and decrypted_activity.get(f'{field}_encrypted'):
                if field in decrypted_activity:
                    decrypted_activity[field] = self.decrypt_user_field(decrypted_activity[field])
                    del decrypted_activity[f'{field}_encrypted']
        
        return decrypted_activity
    
    def anonymize_user_data(self, user_data):
        """
        Create anonymized version of user data for analytics
        
        Args:
            user_data (dict): Original user data
            
        Returns:
            dict: Anonymized user data
        """
        anonymized = {
            'user_id_hash': self.create_anonymous_id(user_data.get('id', '')),
            'account_created': user_data.get('created_at', ''),
            'activity_count': user_data.get('detection_count', 0),
            'last_activity': user_data.get('last_login', ''),
            'anonymized': True,
            'anonymization_timestamp': datetime.utcnow().isoformat()
        }
        
        return anonymized
    
    def create_anonymous_id(self, user_id):
        """
        Create anonymous but consistent identifier for analytics
        
        Args:
            user_id (str): Original user ID
            
        Returns:
            str: Anonymous identifier hash
        """
        # Create consistent hash for analytics while protecting identity
        hash_input = f"{user_id}_anonymous_salt_2024"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def secure_file_metadata(self, file_metadata):
        """
        Encrypt file upload metadata and analysis results
        
        Args:
            file_metadata (dict): File metadata and analysis results
            
        Returns:
            dict: Encrypted file metadata
        """
        encrypted_metadata = file_metadata.copy()
        
        # Encrypt sensitive file information
        file_sensitive_fields = ['original_filename', 'file_path', 'user_ip', 'analysis_details']
        
        for field in file_sensitive_fields:
            if field in encrypted_metadata:
                if isinstance(encrypted_metadata[field], dict):
                    encrypted_metadata[field] = json.dumps(encrypted_metadata[field])
                encrypted_metadata[field] = self.encrypt_user_field(str(encrypted_metadata[field]))
                encrypted_metadata[f'{field}_encrypted'] = True
        
        encrypted_metadata['file_metadata_encrypted'] = True
        return encrypted_metadata
    
    def decrypt_file_metadata(self, encrypted_metadata):
        """
        Decrypt file metadata for display
        
        Args:
            encrypted_metadata (dict): Encrypted file metadata
            
        Returns:
            dict: Decrypted file metadata
        """
        if not encrypted_metadata.get('file_metadata_encrypted'):
            return encrypted_metadata
        
        decrypted_metadata = encrypted_metadata.copy()
        
        file_sensitive_fields = ['original_filename', 'file_path', 'user_ip', 'analysis_details']
        
        for field in file_sensitive_fields:
            if f'{field}_encrypted' in decrypted_metadata and decrypted_metadata.get(f'{field}_encrypted'):
                if field in decrypted_metadata:
                    decrypted_field = self.decrypt_user_field(decrypted_metadata[field])
                    
                    # Try to parse JSON if it was a dict
                    if field == 'analysis_details':
                        try:
                            decrypted_metadata[field] = json.loads(decrypted_field)
                        except:
                            decrypted_metadata[field] = decrypted_field
                    else:
                        decrypted_metadata[field] = decrypted_field
                    
                    del decrypted_metadata[f'{field}_encrypted']
        
        return decrypted_metadata

# Global encryption instance
encryption_manager = UserDataEncryption()

def encrypt_sensitive_data(data_type, data):
    """
    Convenience function to encrypt different types of sensitive data
    
    Args:
        data_type (str): Type of data ('user', 'activity', 'file')
        data (dict): Data to encrypt
        
    Returns:
        dict: Encrypted data
    """
    if data_type == 'user':
        return encryption_manager.encrypt_user_profile(data)
    elif data_type == 'activity':
        return encryption_manager.encrypt_activity_log(data)
    elif data_type == 'file':
        return encryption_manager.secure_file_metadata(data)
    else:
        return data

def decrypt_sensitive_data(data_type, encrypted_data):
    """
    Convenience function to decrypt different types of sensitive data
    
    Args:
        data_type (str): Type of data ('user', 'activity', 'file')
        encrypted_data (dict): Encrypted data
        
    Returns:
        dict: Decrypted data
    """
    if data_type == 'user':
        return encryption_manager.decrypt_user_profile(encrypted_data)
    elif data_type == 'activity':
        return encryption_manager.decrypt_activity_log(encrypted_data)
    elif data_type == 'file':
        return encryption_manager.decrypt_file_metadata(encrypted_data)
    else:
        return encrypted_data