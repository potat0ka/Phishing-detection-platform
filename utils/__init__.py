"""
Utilities Package
================

This package contains helper functions and utilities used throughout the application.
These functions handle common tasks like validation, formatting, and data processing.

For beginners: Utilities are reusable functions that help with common tasks
across different parts of the application.
"""

from .validation import validate_url, validate_email, validate_password
from .formatting import format_confidence_score, format_threat_level

# Make utilities available when importing from utils package
__all__ = [
    'validate_url',
    'validate_email', 
    'validate_password',
    'format_confidence_score',
    'format_threat_level'
]
