"""
Formatting Utilities
===================

This module contains functions for formatting data for display.
It helps present information in a user-friendly way.

Author: Bigendra Shrestha
"""

def format_confidence_score(score):
    """
    Format confidence score for display
    
    Args:
        score (float): Confidence score (0.0 to 1.0)
        
    Returns:
        str: Formatted percentage string
    """
    if score is None:
        return "0%"
    
    try:
        percentage = float(score) * 100
        return f"{percentage:.1f}%"
    except (ValueError, TypeError):
        return "0%"

def format_threat_level(threat_level):
    """
    Format threat level with appropriate styling
    
    Args:
        threat_level (str): Threat level (safe, low, medium, high)
        
    Returns:
        dict: Formatted threat level with CSS class and display text
    """
    threat_mappings = {
        'safe': {'class': 'success', 'text': 'Safe', 'icon': 'check-circle'},
        'low': {'class': 'info', 'text': 'Low Risk', 'icon': 'info-circle'},
        'medium': {'class': 'warning', 'text': 'Medium Risk', 'icon': 'exclamation-triangle'},
        'high': {'class': 'danger', 'text': 'High Risk', 'icon': 'times-circle'},
        'unknown': {'class': 'secondary', 'text': 'Unknown', 'icon': 'question-circle'}
    }
    
    return threat_mappings.get(threat_level, threat_mappings['unknown'])

def format_datetime(dt):
    """
    Format datetime for display
    
    Args:
        dt (datetime): DateTime object
        
    Returns:
        str: Formatted date string
    """
    if dt is None:
        return "Unknown"
    
    try:
        return dt.strftime("%Y-%m-%d %H:%M")
    except (ValueError, AttributeError):
        return "Invalid Date"

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes is None or size_bytes < 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"

def truncate_text(text, max_length=100):
    """
    Truncate text to specified length
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

def format_url_display(url, max_length=50):
    """
    Format URL for safe display
    
    Args:
        url (str): URL to format
        max_length (int): Maximum display length
        
    Returns:
        str: Formatted URL for display
    """
    if not url:
        return ""
    
    # Remove protocol for cleaner display
    display_url = url.replace('https://', '').replace('http://', '')
    
    return truncate_text(display_url, max_length)