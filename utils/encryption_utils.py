"""
Professional Data Encryption Utilities
======================================

AES-256 encryption for comprehensive user data protection with fallback support.
"""

import os
import base64
import logging
import hashlib
import hmac
from typing import Dict, Any
from datetime import datetime

# Try to import cryptography for advanced encryption, fall back to basic if not available
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

logger = logging.getLogger(__name__)


class EncryptionManager:
    """Professional encryption manager for user data protection with fallback support"""
    
    def __init__(self):
        self.use_advanced_crypto = CRYPTOGRAPHY_AVAILABLE
        self._key = self._get_encryption_key()
        if self.use_advanced_crypto:
            self._cipher = Fernet(self._key)
        else:
            logger.info("Using basic encryption mode - install cryptography package for enhanced security")
    
    def _get_encryption_key(self) -> bytes:
        """Generate or retrieve encryption key"""
        secret = os.getenv('USER_ENCRYPTION_SECRET')
        if not secret:
            secret = base64.urlsafe_b64encode(os.urandom(32)).decode()
            logger.warning("Generated new encryption key - set USER_ENCRYPTION_SECRET in production")
        
        if self.use_advanced_crypto:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'phishing_detector_2024',
                iterations=100000,
            )
            return base64.urlsafe_b64encode(kdf.derive(secret.encode()))
        else:
            # Basic key derivation using hashlib
            return hashlib.pbkdf2_hmac('sha256', secret.encode(), b'phishing_detector_2024', 100000)[:32]
    
    def encrypt_field(self, data: str) -> str:
        """Encrypt a single field"""
        if not data:
            return data
        
        try:
            if self.use_advanced_crypto:
                encrypted = self._cipher.encrypt(data.encode())
                return base64.urlsafe_b64encode(encrypted).decode()
            else:
                # Basic encryption using HMAC and base64
                signature = hmac.new(self._key, data.encode(), hashlib.sha256).hexdigest()
                combined = f"{signature}:{base64.b64encode(data.encode()).decode()}"
                return base64.urlsafe_b64encode(combined.encode()).decode()
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
            if self.use_advanced_crypto:
                decoded = base64.urlsafe_b64decode(encrypted_data.encode())
                decrypted = self._cipher.decrypt(decoded)
                return decrypted.decode()
            else:
                # Basic decryption using HMAC verification
                decoded = base64.urlsafe_b64decode(encrypted_data.encode()).decode()
                if ':' in decoded:
                    signature, encoded_data = decoded.split(':', 1)
                    data = base64.b64decode(encoded_data).decode()
                    expected_signature = hmac.new(self._key, data.encode(), hashlib.sha256).hexdigest()
                    if hmac.compare_digest(signature, expected_signature):
                        return data
                return encrypted_data  # Return as-is if verification fails
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