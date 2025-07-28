"""
Validation Utilities
===================

This module contains validation functions for user input.
It helps ensure data integrity and security throughout the application.

Author: Bigendra Shrestha
"""

import re
from urllib.parse import urlparse

def validate_url(url):
    """
    Validate URL format and structure
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if URL is valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False
    
    # Remove whitespace
    url = url.strip()
    
    # Check minimum length
    if len(url) < 10:
        return False
    
    # Check maximum length (prevent DoS)
    if len(url) > 2048:
        return False
    
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False
        
        # Scheme must be http or https
        if parsed.scheme.lower() not in ['http', 'https']:
            return False
        
        # Basic domain validation
        domain = parsed.netloc.lower()
        
        # Check for basic domain structure
        if '.' not in domain:
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            'file://',
            'javascript:',
            'data:'
        ]
        
        for pattern in suspicious_patterns:
            if pattern in url.lower():
                return False
        
        return True
        
    except Exception:
        return False

def validate_email(email):
    """
    Validate email address format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    # Check length
    if len(email) < 5 or len(email) > 254:
        return False
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False
    
    # Check for common invalid patterns
    invalid_patterns = [
        '..@',
        '.@',
        '@.',
        '@@'
    ]
    
    for pattern in invalid_patterns:
        if pattern in email:
            return False
    
    return True

def validate_password(password):
    """
    Validate password strength
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if password meets requirements, False otherwise
    """
    if not password or not isinstance(password, str):
        return False
    
    # Minimum length requirement
    if len(password) < 8:
        return False
    
    # Maximum length (prevent DoS)
    if len(password) > 128:
        return False
    
    # Must contain at least one letter
    if not re.search(r'[a-zA-Z]', password):
        return False
    
    # Must contain at least one number
    if not re.search(r'\d', password):
        return False
    
    # Optional: Uncomment for stricter requirements
    # Must contain at least one special character
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return False
    
    return True

def validate_username(username):
    """
    Validate username format
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if username is valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    username = username.strip()
    
    # Length requirements
    if len(username) < 3 or len(username) > 50:
        return False
    
    # Alphanumeric and underscore only
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    
    # Cannot start with number
    if username[0].isdigit():
        return False
    
    return True

def sanitize_input(text, max_length=1000):
    """
    Sanitize user input to prevent XSS and injection attacks
    
    Args:
        text (str): Text to sanitize
        max_length (int): Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text