
"""
Safety Tips Model
================

This model handles safety tips management in MongoDB.
It manages cybersecurity tips organized by categories with full CRUD operations.

Author: AI Assistant
"""

from datetime import datetime
from .database import db
import logging
import os
import json

logger = logging.getLogger(__name__)

class SafetyTipsModel:
    """
    Safety Tips Model for MongoDB operations
    
    This class handles:
    - Managing safety tips by category (url, email, general)
    - CRUD operations for tips
    - Admin management functionality
    """
    
    CATEGORIES = ['url', 'email', 'general']
    
    @staticmethod
    def get_all_tips():
        """Get all safety tips from MongoDB or file storage"""
        try:
            if db and db.connected:
                tips = db.find_documents('safety_tips', {})
                if tips:
                    return tips
            
            # Fallback to file storage
            tips = SafetyTipsModel._load_from_file()
            if not tips:
                # Initialize with default tips if empty
                SafetyTipsModel.initialize_default_tips()
                tips = SafetyTipsModel._load_from_file()
            
            return tips
        except Exception as e:
            logger.error(f"Error getting safety tips: {e}")
            return SafetyTipsModel.get_default_tips()
    
    @staticmethod
    def get_tips_by_category(category):
        """Get safety tips filtered by category"""
        try:
            if db and db.connected:
                tips = db.find_documents('safety_tips', {'category': category})
                return tips
            else:
                # Fallback to file storage
                all_tips = SafetyTipsModel._load_from_file()
                if not all_tips:
                    # If no tips in file, initialize with defaults
                    SafetyTipsModel.initialize_default_tips()
                    all_tips = SafetyTipsModel._load_from_file()
                return [tip for tip in all_tips if tip.get('category') == category]
        except Exception as e:
            logger.error(f"Error getting tips by category: {e}")
            # Return default tips for the category if error occurs
            default_tips = SafetyTipsModel.get_default_tips()
            return [tip for tip in default_tips if tip.get('category') == category]
    
    @staticmethod
    def add_tip(title, content, category, created_by):
        """Add new safety tip"""
        try:
            if category not in SafetyTipsModel.CATEGORIES:
                return None
            
            tip_data = {
                'title': title,
                'content': content,
                'category': category,
                'created_by': created_by,
                'created_at': datetime.utcnow(),
                'is_active': True
            }
            
            if db and db.connected:
                return db.insert_document('safety_tips', tip_data)
            else:
                # Fallback to file storage
                return SafetyTipsModel._save_to_file(tip_data)
        except Exception as e:
            logger.error(f"Error adding tip: {e}")
            return None
    
    @staticmethod
    def update_tip(tip_id, title, content, category):
        """Update existing safety tip"""
        try:
            if category not in SafetyTipsModel.CATEGORIES:
                return False
            
            if db and db.connected:
                result = db.update_document(
                    'safety_tips',
                    {'_id': tip_id},
                    {
                        '$set': {
                            'title': title,
                            'content': content,
                            'category': category,
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                return result > 0
            else:
                # Fallback to file storage
                return SafetyTipsModel._update_in_file(tip_id, title, content, category)
        except Exception as e:
            logger.error(f"Error updating tip: {e}")
            return False
    
    @staticmethod
    def delete_tip(tip_id):
        """Delete safety tip"""
        try:
            if db and db.connected:
                result = db.delete_document('safety_tips', {'_id': tip_id})
                return result > 0
            else:
                # Fallback to file storage
                return SafetyTipsModel._delete_from_file(tip_id)
        except Exception as e:
            logger.error(f"Error deleting tip: {e}")
            return False
    
    @staticmethod
    def get_tip_by_id(tip_id):
        """Get single tip by ID"""
        try:
            if db and db.connected:
                tips = db.find_documents('safety_tips', {'_id': tip_id})
                return tips[0] if tips else None
            else:
                # Fallback to file storage
                all_tips = SafetyTipsModel.get_all_tips()
                for tip in all_tips:
                    if str(tip.get('_id')) == str(tip_id):
                        return tip
                return None
        except Exception as e:
            logger.error(f"Error getting tip by ID: {e}")
            return None
    
    @staticmethod
    def _save_to_file(tip_data):
        """Save tip to file storage as fallback"""
        try:
            tips_file = 'data/safety_tips.json'
            os.makedirs(os.path.dirname(tips_file), exist_ok=True)
            
            # Load existing tips
            tips = []
            if os.path.exists(tips_file):
                with open(tips_file, 'r') as f:
                    tips = json.load(f)
            
            # Add new tip with simple ID
            tip_data['_id'] = len(tips) + 1
            tip_data['created_at'] = tip_data['created_at'].isoformat()
            tips.append(tip_data)
            
            # Save back to file
            with open(tips_file, 'w') as f:
                json.dump(tips, f, indent=2, default=str)
            
            return tip_data['_id']
        except Exception as e:
            logger.error(f"Error saving tip to file: {e}")
            return None
    
    @staticmethod
    def _update_in_file(tip_id, title, content, category):
        """Update tip in file storage"""
        try:
            tips_file = 'data/safety_tips.json'
            if not os.path.exists(tips_file):
                return False
            
            with open(tips_file, 'r') as f:
                tips = json.load(f)
            
            # Find and update tip
            for i, tip in enumerate(tips):
                if str(tip.get('_id')) == str(tip_id):
                    tips[i].update({
                        'title': title,
                        'content': content,
                        'category': category,
                        'updated_at': datetime.utcnow().isoformat()
                    })
                    break
            else:
                return False
            
            # Save back to file
            with open(tips_file, 'w') as f:
                json.dump(tips, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Error updating tip in file: {e}")
            return False
    
    @staticmethod
    def _delete_from_file(tip_id):
        """Delete tip from file storage"""
        try:
            tips_file = 'data/safety_tips.json'
            if not os.path.exists(tips_file):
                return False
            
            with open(tips_file, 'r') as f:
                tips = json.load(f)
            
            # Find and remove tip
            original_count = len(tips)
            tips = [tip for tip in tips if str(tip.get('_id')) != str(tip_id)]
            
            if len(tips) == original_count:
                return False
            
            # Save back to file
            with open(tips_file, 'w') as f:
                json.dump(tips, f, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"Error deleting tip from file: {e}")
            return False
    
    @staticmethod
    def _load_from_file():
        """Load tips from file storage"""
        try:
            tips_file = 'data/safety_tips.json'
            if os.path.exists(tips_file):
                with open(tips_file, 'r') as f:
                    tips = json.load(f)
                    # Convert string dates back to datetime objects
                    for tip in tips:
                        if isinstance(tip.get('created_at'), str):
                            try:
                                tip['created_at'] = datetime.fromisoformat(tip['created_at'].replace('Z', '+00:00'))
                            except:
                                tip['created_at'] = datetime.utcnow()
                        if isinstance(tip.get('updated_at'), str):
                            try:
                                tip['updated_at'] = datetime.fromisoformat(tip['updated_at'].replace('Z', '+00:00'))
                            except:
                                pass
                    return tips
            return []
        except Exception as e:
            logger.error(f"Error loading tips from file: {e}")
            return []

    @staticmethod
    def initialize_default_tips():
        """Initialize database with default safety tips"""
        try:
            if db and db.connected:
                # Check if tips already exist
                existing_tips = db.find_documents('safety_tips', {})
                if not existing_tips:
                    default_tips = SafetyTipsModel.get_default_tips()
                    for tip in default_tips:
                        db.insert_document('safety_tips', tip)
            else:
                # File storage fallback
                tips_file = 'data/safety_tips.json'
                if not os.path.exists(tips_file) or not SafetyTipsModel._load_from_file():
                    # Initialize with default tips
                    os.makedirs(os.path.dirname(tips_file), exist_ok=True)
                    default_tips = SafetyTipsModel.get_default_tips()
                    # Convert datetime objects to strings for JSON serialization
                    for tip in default_tips:
                        if 'created_at' in tip:
                            tip['created_at'] = tip['created_at'].isoformat()
                    
                    with open(tips_file, 'w') as f:
                        json.dump(default_tips, f, indent=2, default=str)
                    
                    logger.info(f"Initialized {len(default_tips)} default safety tips in file storage")
        except Exception as e:
            logger.error(f"Error initializing default tips: {e}")
    
    @staticmethod
    def get_featured_tip():
        """Get a featured tip for homepage display"""
        try:
            tips = SafetyTipsModel.get_all_tips()
            if tips:
                # Return the first tip as featured
                return tips[0]
            return SafetyTipsModel.get_default_tips()[0]
        except Exception as e:
            logger.error(f"Error getting featured tip: {e}")
            return SafetyTipsModel.get_default_tips()[0]
    
    @staticmethod
    def get_default_tips():
        """Get default safety tips for initialization"""
        return [
            # URL Safety Tips
            {
                '_id': 'url_tip_1',
                'title': 'Check for HTTPS and Valid Certificates',
                'content': 'Always look for "https://" and the lock icon before entering personal information. Click the lock to verify the certificate belongs to the real company.',
                'category': 'url',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'url_tip_2',
                'title': 'Spot Fake URLs and Domain Tricks',
                'content': 'Scammers use similar-looking domains like "arnazon.com" instead of "amazon.com". Always double-check the main domain name.',
                'category': 'url',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'url_tip_3',
                'title': 'Avoid Suspicious URL Shorteners',
                'content': 'Be cautious with shortened URLs (bit.ly, tinyurl) from unknown sources, as they hide the real destination.',
                'category': 'url',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            
            # Email Safety Tips
            {
                '_id': 'email_tip_1',
                'title': 'Recognize Phishing Email Warning Signs',
                'content': 'Watch for urgent language, generic greetings, poor grammar, mismatched sender addresses, and unexpected attachments.',
                'category': 'email',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'email_tip_2',
                'title': 'Verify Email Senders Before Clicking',
                'content': 'Before clicking any email link, hover over it to see the real destination. Check if the sender email matches the company domain.',
                'category': 'email',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'email_tip_3',
                'title': 'Handle Suspicious Attachments Safely',
                'content': 'Never open unexpected attachments, especially .exe, .zip, or .doc files from unknown senders. Use antivirus software to scan attachments.',
                'category': 'email',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            
            # General Safety Tips
            {
                '_id': 'general_tip_1',
                'title': 'Use Strong, Unique Passwords',
                'content': 'Create passwords with at least 12 characters using uppercase, lowercase, numbers, and symbols. Use a different password for each account.',
                'category': 'general',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'general_tip_2',
                'title': 'Enable Two-Factor Authentication',
                'content': 'Turn on 2FA for all important accounts using authenticator apps or SMS codes. This adds an extra layer of security.',
                'category': 'general',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            },
            {
                '_id': 'general_tip_3',
                'title': 'Keep Software Updated',
                'content': 'Enable automatic updates for your operating system, web browser, and antivirus software. Updates often fix security vulnerabilities.',
                'category': 'general',
                'created_by': 'system',
                'created_at': datetime.utcnow(),
                'is_active': True
            }
        ]
