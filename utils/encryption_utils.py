"""
Professional Data Encryption Utilities
======================================

AES-256 encryption for comprehensive user data protection.
"""

import os
import base64
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Professional encryption manager for user data protection"""
    
    def __init__(self):
        self._key = self._get_encryption_key()
        self._cipher = Fernet(self._key)
    
    def _get_encryption_key(self) -> bytes:
        """Generate or retrieve encryption key"""
        secret = os.getenv('USER_ENCRYPTION_SECRET')
        if not secret:
            secret = base64.urlsafe_b64encode(os.urandom(32)).decode()
            logger.warning("Generated new encryption key - set USER_ENCRYPTION_SECRET in production")
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'phishing_detector_2024',
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    
    def encrypt_field(self, data: str) -> str:
        """Encrypt a single field"""
        if not data:
            return data
        
        try:
            encrypted = self._cipher.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return data
    
    def decrypt_field(self, encrypted_data: str) -> str:
        """Decrypt a single field"""
        if not encrypted_data or not isinstance(encrypted_data, str):
            return encrypted_data
        
        # Skip decryption for non-encrypted data
        if not self._is_encrypted_format(encrypted_data):
            return encrypted_data
        
        try:
            decoded = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self._cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return encrypted_data
    
    def _is_encrypted_format(self, data: str) -> bool:
        """Check if data appears to be in encrypted format"""
        try:
            # Check if it's base64 encoded and reasonable length for encrypted data
            if len(data) < 20:  # Too short to be encrypted
                return False
            decoded = base64.urlsafe_b64decode(data.encode())
            return len(decoded) > 16  # Fernet adds at least 16 bytes overhead
        except:
            return False


# Global encryption instance
encryption_manager = EncryptionManager()


def encrypt_sensitive_data(data_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt sensitive data based on type"""
    if not isinstance(data, dict):
        return data
    
    encrypted_data = data.copy()
    
    if data_type == 'user':
        # Encrypt user personal information
        sensitive_fields = ['username', 'email']
        for field in sensitive_fields:
            if field in encrypted_data:
                encrypted_data[field] = encryption_manager.encrypt_field(encrypted_data[field])
                encrypted_data[f'{field}_encrypted'] = True
        
        encrypted_data['encryption_version'] = '2.0'
        encrypted_data['encrypted_at'] = datetime.utcnow()
    
    elif data_type == 'activity':
        # Encrypt user activity data
        sensitive_fields = ['input_content', 'user_ip', 'user_agent']
        for field in sensitive_fields:
            if field in encrypted_data:
                encrypted_data[field] = encryption_manager.encrypt_field(str(encrypted_data[field]))
                encrypted_data[f'{field}_encrypted'] = True
        
        encrypted_data['activity_encrypted'] = True
        encrypted_data['activity_encryption_timestamp'] = datetime.utcnow()
    
    elif data_type == 'file':
        # Encrypt file metadata
        sensitive_fields = ['original_filename', 'file_path', 'user_ip']
        for field in sensitive_fields:
            if field in encrypted_data:
                encrypted_data[field] = encryption_manager.encrypt_field(str(encrypted_data[field]))
                encrypted_data[f'{field}_encrypted'] = True
        
        encrypted_data['file_metadata_encrypted'] = True
    
    return encrypted_data


def decrypt_sensitive_data(data_type: str, encrypted_data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt sensitive data based on type"""
    if not isinstance(encrypted_data, dict):
        return encrypted_data
    
    # Check if data is encrypted
    if not any(key.endswith('_encrypted') for key in encrypted_data.keys()):
        return encrypted_data
    
    decrypted_data = encrypted_data.copy()
    
    if data_type == 'user':
        sensitive_fields = ['username', 'email']
        for field in sensitive_fields:
            if f'{field}_encrypted' in decrypted_data and decrypted_data.get(f'{field}_encrypted'):
                if field in decrypted_data:
                    decrypted_data[field] = encryption_manager.decrypt_field(decrypted_data[field])
                    del decrypted_data[f'{field}_encrypted']
    
    elif data_type == 'activity':
        sensitive_fields = ['input_content', 'user_ip', 'user_agent']
        for field in sensitive_fields:
            if f'{field}_encrypted' in decrypted_data and decrypted_data.get(f'{field}_encrypted'):
                if field in decrypted_data:
                    decrypted_data[field] = encryption_manager.decrypt_field(decrypted_data[field])
                    del decrypted_data[f'{field}_encrypted']
    
    elif data_type == 'file':
        sensitive_fields = ['original_filename', 'file_path', 'user_ip']
        for field in sensitive_fields:
            if f'{field}_encrypted' in decrypted_data and decrypted_data.get(f'{field}_encrypted'):
                if field in decrypted_data:
                    decrypted_data[field] = encryption_manager.decrypt_field(decrypted_data[field])
                    del decrypted_data[f'{field}_encrypted']
    
    return decrypted_data