"""
Security Tips Model
==================

This model handles security tips and educational content in MongoDB.
It manages cybersecurity advice, tips, and learning materials.

Author: Bigendra Shrestha
"""

from datetime import datetime
from .database import db

class SecurityTipsModel:
    """
    Security Tips Model for MongoDB operations
    
    This class handles:
    - Managing cybersecurity tips and advice
    - Categorizing tips by difficulty and topic
    - Providing educational content for users
    """
    
    @staticmethod
    def get_all_tips():
        """Get all cybersecurity tips from MongoDB"""
        try:
            if db and db.connected:
                tips = db.find_documents('security_tips', {})
                if tips:
                    return tips
            
            # Initialize with comprehensive real cybersecurity tips if empty
            SecurityTipsModel.initialize_default_tips()
            
            # Return comprehensive tips
            return SecurityTipsModel.get_comprehensive_tips()
        except Exception as e:
            import logging
            logging.error(f"Error getting security tips: {e}")
            return SecurityTipsModel.get_comprehensive_tips()
    
    @staticmethod
    def add_security_tip(title, content, category, difficulty='beginner'):
        """Add new security tip to database"""
        tip_data = {
            'title': title,
            'content': content,
            'category': category,
            'difficulty': difficulty,
            'views': 0,
            'helpful_votes': 0
        }
        
        if db and db.connected:
            return db.insert_document('security_tips', tip_data)
        return None
    
    @staticmethod
    def get_featured_tip():
        """Get a featured security tip for homepage"""
        tips = SecurityTipsModel.get_all_tips()
        if tips:
            # Return first tip as featured (in production, could be random or most popular)
            return tips[0]
        return None
    
    @staticmethod
    def get_tips_by_category(category):
        """Get security tips filtered by category"""
        if db and db.connected:
            return db.find_documents('security_tips', {'category': category})
        else:
            fallback_tips = SecurityTipsModel.get_fallback_tips()
            return [tip for tip in fallback_tips if tip['category'] == category]
    
    @staticmethod
    def update_tip_views(tip_id):
        """Increment view count for a tip"""
        if db and db.connected:
            return db.update_document(
                'security_tips',
                {'_id': tip_id},
                {'$inc': {'views': 1}}
            )
        return 0
    
    @staticmethod 
    def initialize_default_tips():
        """Initialize database with comprehensive cybersecurity tips"""
        try:
            if db and db.connected:
                # Check if tips already exist
                existing_tips = db.find_documents('security_tips', {})
                if not existing_tips:
                    default_tips = SecurityTipsModel.get_comprehensive_tips()
                    for tip in default_tips:
                        db.insert_document('security_tips', tip)
        except Exception as e:
            import logging
            logging.error(f"Error initializing default tips: {e}")

    @staticmethod
    def get_comprehensive_tips():
        """Comprehensive real cybersecurity tips for beginners"""
        return [
            # EMAIL SAFETY TIPS
            {
                '_id': 'email_tip_1',
                'title': 'Recognize Phishing Email Warning Signs',
                'content': 'Watch for urgent language like "Act now or lose access", generic greetings like "Dear Customer", poor grammar, mismatched sender addresses, and unexpected attachments. Legitimate companies rarely ask for passwords via email.',
                'category': 'email',
                'difficulty': 'beginner',
                'views': 1245,
                'helpful_votes': 342,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'email_tip_2', 
                'title': 'Verify Email Senders Before Clicking',
                'content': 'Before clicking any email link, hover over it to see the real destination. Check if the sender email matches the company domain. When in doubt, go directly to the company website instead of clicking email links.',
                'category': 'email',
                'difficulty': 'beginner',
                'views': 987,
                'helpful_votes': 287,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'email_tip_3',
                'title': 'Handle Suspicious Attachments Safely',
                'content': 'Never open unexpected attachments, especially .exe, .zip, or .doc files from unknown senders. Use antivirus software to scan attachments. When receiving unexpected attachments from known contacts, verify by calling them first.',
                'category': 'email',
                'difficulty': 'beginner',
                'views': 756,
                'helpful_votes': 198,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'email_tip_4',
                'title': 'Report and Block Phishing Attempts',
                'content': 'Report phishing emails to your email provider and the company being impersonated. Block the sender and delete the email. Never reply to phishing emails, even to unsubscribe, as this confirms your email is active.',
                'category': 'email',
                'difficulty': 'beginner',
                'views': 654,
                'helpful_votes': 156,
                'created_at': datetime.utcnow()
            },
            
            # URL SAFETY TIPS
            {
                '_id': 'url_tip_1',
                'title': 'Check for HTTPS and Valid Certificates',
                'content': 'Always look for "https://" and the lock icon before entering personal information. Click the lock to verify the certificate belongs to the real company. Avoid sites showing certificate errors or warnings.',
                'category': 'url',
                'difficulty': 'beginner',
                'views': 1432,
                'helpful_votes': 398,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'url_tip_2',
                'title': 'Spot Fake URLs and Domain Tricks',
                'content': 'Scammers use similar-looking domains like "arnazon.com" instead of "amazon.com" or add extra words like "amazon-security.com". Always double-check the main domain name and be wary of unusual subdomains.',
                'category': 'url',
                'difficulty': 'beginner',
                'views': 1156,
                'helpful_votes': 312,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'url_tip_3',
                'title': 'Avoid Suspicious URL Shorteners',
                'content': 'Be cautious with shortened URLs (bit.ly, tinyurl) from unknown sources, as they hide the real destination. Use URL expander tools to see where they lead before clicking, or type the company URL directly.',
                'category': 'url',
                'difficulty': 'intermediate',
                'views': 843,
                'helpful_votes': 234,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'url_tip_4',
                'title': 'Bookmark Important Websites',
                'content': 'Save bookmarks for your bank, email, and frequently used sites. Use these bookmarks instead of clicking links in emails or search results. This protects you from typosquatting and phishing sites.',
                'category': 'url',
                'difficulty': 'beginner',
                'views': 721,
                'helpful_votes': 189,
                'created_at': datetime.utcnow()
            },
            
            # GENERAL SAFETY TIPS
            {
                '_id': 'general_tip_1',
                'title': 'Use Strong, Unique Passwords Everywhere',
                'content': 'Create passwords with at least 12 characters using uppercase, lowercase, numbers, and symbols. Use a different password for each account. Consider phrases like "Coffee@Morning#2024!" that are long but memorable.',
                'category': 'general',
                'difficulty': 'beginner',
                'views': 1687,
                'helpful_votes': 445,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'general_tip_2',
                'title': 'Enable Two-Factor Authentication (2FA)',
                'content': 'Turn on 2FA for all important accounts using authenticator apps like Google Authenticator or SMS codes. Even if hackers get your password, they still need your phone to access your account.',
                'category': 'general',
                'difficulty': 'intermediate',
                'views': 1298,
                'helpful_votes': 367,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'general_tip_3',
                'title': 'Keep Software and Browsers Updated',
                'content': 'Enable automatic updates for your operating system, web browser, and antivirus software. Updates often fix security holes that hackers exploit. Restart your devices when updates require it.',
                'category': 'general',
                'difficulty': 'beginner',
                'views': 1087,
                'helpful_votes': 298,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'general_tip_4',
                'title': 'Be Careful on Public Wi-Fi',
                'content': 'Avoid accessing sensitive accounts on public Wi-Fi networks. If you must, use a VPN to encrypt your connection. Never enter passwords or credit card information on unsecured public networks.',
                'category': 'general',
                'difficulty': 'intermediate',
                'views': 934,
                'helpful_votes': 256,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'general_tip_5',
                'title': 'Regularly Monitor Your Accounts',
                'content': 'Check your bank and credit card statements monthly for unauthorized charges. Set up account alerts for logins and transactions. Report suspicious activity immediately to prevent further damage.',
                'category': 'general',
                'difficulty': 'beginner',
                'views': 876,
                'helpful_votes': 234,
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'general_tip_6',
                'title': 'Think Before You Share Personal Information',
                'content': 'Be cautious about sharing personal details on social media or with strangers online. Scammers use this information for identity theft and targeted phishing attacks. Keep private information private.',
                'category': 'general',
                'difficulty': 'beginner',
                'views': 743,
                'helpful_votes': 198,
                'created_at': datetime.utcnow()
            }
        ]
    
    @staticmethod
    def add_tip(title, content, category, difficulty='beginner'):
        """Add new security tip to database"""
        try:
            tip_data = {
                'title': title,
                'content': content,
                'category': category,
                'difficulty': difficulty,
                'views': 0,
                'helpful_votes': 0,
                'created_at': datetime.utcnow()
            }
            
            if db and db.connected:
                result = db.insert_document('security_tips', tip_data)
                return result
            return None
        except Exception as e:
            import logging
            logging.error(f"Error adding tip: {e}")
            return None
    
    @staticmethod
    def update_tip(tip_id, title, content, category, difficulty):
        """Update existing security tip"""
        try:
            if db and db.connected:
                result = db.update_document(
                    'security_tips',
                    {'_id': tip_id},
                    {
                        '$set': {
                            'title': title,
                            'content': content,
                            'category': category,
                            'difficulty': difficulty
                        }
                    }
                )
                return result
            return 0
        except Exception as e:
            import logging
            logging.error(f"Error updating tip: {e}")
            return 0
    
    @staticmethod
    def delete_tip(tip_id):
        """Delete security tip from database"""
        try:
            if db and db.connected:
                result = db.delete_document('security_tips', {'_id': tip_id})
                return result
            return 0
        except Exception as e:
            import logging
            logging.error(f"Error deleting tip: {e}")
            return 0
    
    @staticmethod
    def get_tip_by_id(tip_id):
        """Get single tip by ID"""
        try:
            if db and db.connected:
                tip = db.find_document('security_tips', {'_id': tip_id})
                return tip
            return None
        except Exception as e:
            import logging
            logging.error(f"Error getting tip by ID: {e}")
            return None