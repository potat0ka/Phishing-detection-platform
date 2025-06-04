"""
Simple JSON-based Models for Phishing Detection Platform
Perfect for learning backend development without complex database setup
"""

import json
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import USERS_FILE, DETECTIONS_FILE, TIPS_FILE, load_json_data, save_json_data

class User:
    """Simple User model using JSON storage"""
    
    @staticmethod
    def create_user(username, email, password):
        """Create a new user"""
        users = load_json_data(USERS_FILE)
        
        # Check if user already exists
        for user in users:
            if user.get('username') == username or user.get('email') == email:
                return None
        
        user_data = {
            'id': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.now().isoformat()
        }
        
        users.append(user_data)
        save_json_data(USERS_FILE, users)
        return user_data['id']
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        users = load_json_data(USERS_FILE)
        for user in users:
            if user.get('username') == username:
                return user
        return None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        users = load_json_data(USERS_FILE)
        for user in users:
            if user.get('email') == email:
                return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        users = load_json_data(USERS_FILE)
        for user in users:
            if user.get('id') == user_id:
                return user
        return None
    
    @staticmethod
    def check_password(user, password):
        """Check if password matches user's password hash"""
        if user and 'password_hash' in user:
            return check_password_hash(user['password_hash'], password)
        return False
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password"""
        user = User.find_by_username(username)
        if user and User.check_password(user, password):
            return user
        return None

class Detection:
    """Simple Detection model using JSON storage"""
    
    @staticmethod
    def create_detection(user_id, input_type, input_content, result, confidence_score, reasons=None, ai_analysis=None):
        """Create a new detection record"""
        detections = load_json_data(DETECTIONS_FILE)
        
        detection_data = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'input_type': input_type,
            'input_content': input_content,
            'result': result,
            'confidence_score': confidence_score,
            'reasons': reasons or [],
            'ai_analysis': ai_analysis or {},
            'created_at': datetime.now().isoformat()
        }
        
        detections.append(detection_data)
        save_json_data(DETECTIONS_FILE, detections)
        return detection_data['id']
    
    @staticmethod
    def find_by_user(user_id, limit=10):
        """Find detections by user ID"""
        detections = load_json_data(DETECTIONS_FILE)
        user_detections = [d for d in detections if d.get('user_id') == user_id]
        
        # Sort by created_at (newest first) and limit results
        user_detections.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return user_detections[:limit]
    
    @staticmethod
    def count_by_user(user_id):
        """Count detections by user"""
        detections = load_json_data(DETECTIONS_FILE)
        return len([d for d in detections if d.get('user_id') == user_id])
    
    @staticmethod
    def get_user_stats(user_id):
        """Get detection statistics for a user"""
        detections = load_json_data(DETECTIONS_FILE)
        user_detections = [d for d in detections if d.get('user_id') == user_id]
        
        stats = {"safe": 0, "phishing": 0, "suspicious": 0}
        
        for detection in user_detections:
            result = detection.get('result', '')
            if result in stats:
                stats[result] += 1
        
        stats["total"] = sum(stats.values())
        return stats

class PhishingTip:
    """Simple Phishing Tip model using JSON storage"""
    
    @staticmethod
    def create_tip(title, content, category, priority=1):
        """Create a new phishing tip"""
        tips = load_json_data(TIPS_FILE)
        
        tip_data = {
            'id': str(uuid.uuid4()),
            'title': title,
            'content': content,
            'category': category,
            'priority': priority,
            'created_at': datetime.now().isoformat()
        }
        
        tips.append(tip_data)
        save_json_data(TIPS_FILE, tips)
        return tip_data['id']
    
    @staticmethod
    def find_by_category(category):
        """Find tips by category"""
        tips = load_json_data(TIPS_FILE)
        category_tips = [t for t in tips if t.get('category') == category]
        
        # Sort by priority
        category_tips.sort(key=lambda x: x.get('priority', 999))
        return category_tips
    
    @staticmethod
    def find_all():
        """Find all tips"""
        tips = load_json_data(TIPS_FILE)
        tips.sort(key=lambda x: x.get('priority', 999))
        return tips
    
    @staticmethod
    def clear_all():
        """Clear all tips (for updating)"""
        save_json_data(TIPS_FILE, [])
        return True
    
    @staticmethod
    def bulk_insert(tips_list):
        """Insert multiple tips at once"""
        if tips_list:
            save_json_data(TIPS_FILE, tips_list)
            return len(tips_list)
        return 0
    
    @staticmethod
    def find_by_title(title):
        """Find tip by title"""
        tips = load_json_data(TIPS_FILE)
        for tip in tips:
            if tip.get('title') == title:
                return tip
        return None
    
    @staticmethod
    def update_tip(title, content, category, priority):
        """Update existing tip"""
        tips = load_json_data(TIPS_FILE)
        
        for tip in tips:
            if tip.get('title') == title:
                tip.update({
                    'content': content,
                    'category': category,
                    'priority': priority,
                    'updated_at': datetime.now().isoformat()
                })
                save_json_data(TIPS_FILE, tips)
                return True
        return False

# Utility functions for easy database operations
def get_all_users():
    """Get all users (excluding password hashes)"""
    users = load_json_data(USERS_FILE)
    return [{k: v for k, v in user.items() if k != 'password_hash'} for user in users]

def get_recent_detections(limit=20):
    """Get recent detections across all users"""
    detections = load_json_data(DETECTIONS_FILE)
    detections.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return detections[:limit]

def get_database_stats():
    """Get overall database statistics"""
    users = load_json_data(USERS_FILE)
    detections = load_json_data(DETECTIONS_FILE)
    tips = load_json_data(TIPS_FILE)
    
    return {
        'total_users': len(users),
        'total_detections': len(detections),
        'total_tips': len(tips)
    }

def clean_database():
    """Clean up database for testing (use with caution)"""
    save_json_data(USERS_FILE, [])
    save_json_data(DETECTIONS_FILE, [])
    save_json_data(TIPS_FILE, [])
    return "Database cleaned"