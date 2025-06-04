"""
MongoDB Models for Phishing Detection Platform
Simple MongoDB operations using PyMongo
"""

from app import get_db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import json

class User:
    """User model for MongoDB"""
    
    @staticmethod
    def create_user(username, email, password):
        """Create a new user"""
        db = get_db()
        
        # Check if user already exists
        if db.users.find_one({"$or": [{"username": username}, {"email": email}]}):
            return None
        
        user_data = {
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password),
            "created_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        db = get_db()
        return db.users.find_one({"username": username})
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = get_db()
        return db.users.find_one({"email": email})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        db = get_db()
        try:
            return db.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None
    
    @staticmethod
    def check_password(user, password):
        """Check if password matches user's password hash"""
        if user and "password_hash" in user:
            return check_password_hash(user["password_hash"], password)
        return False
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password"""
        user = User.find_by_username(username)
        if user and User.check_password(user, password):
            return user
        return None

class Detection:
    """Detection model for MongoDB"""
    
    @staticmethod
    def create_detection(user_id, input_type, input_content, result, confidence_score, reasons=None, ai_analysis=None):
        """Create a new detection record"""
        db = get_db()
        
        detection_data = {
            "user_id": user_id,
            "input_type": input_type,
            "input_content": input_content,
            "result": result,
            "confidence_score": confidence_score,
            "reasons": reasons or [],
            "ai_analysis": ai_analysis or {},
            "created_at": datetime.utcnow()
        }
        
        result = db.detections.insert_one(detection_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id, limit=10):
        """Find detections by user ID"""
        db = get_db()
        return list(db.detections.find({"user_id": user_id})
                   .sort("created_at", -1)
                   .limit(limit))
    
    @staticmethod
    def count_by_user(user_id):
        """Count detections by user"""
        db = get_db()
        return db.detections.count_documents({"user_id": user_id})
    
    @staticmethod
    def get_user_stats(user_id):
        """Get detection statistics for a user"""
        db = get_db()
        
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$result",
                "count": {"$sum": 1}
            }}
        ]
        
        results = list(db.detections.aggregate(pipeline))
        stats = {"safe": 0, "phishing": 0, "suspicious": 0}
        
        for result in results:
            if result["_id"] in stats:
                stats[result["_id"]] = result["count"]
        
        stats["total"] = sum(stats.values())
        return stats

class PhishingTip:
    """Phishing Tip model for MongoDB"""
    
    @staticmethod
    def create_tip(title, content, category, priority=1):
        """Create a new phishing tip"""
        db = get_db()
        
        tip_data = {
            "title": title,
            "content": content,
            "category": category,
            "priority": priority,
            "created_at": datetime.utcnow()
        }
        
        result = db.phishing_tips.insert_one(tip_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_category(category):
        """Find tips by category"""
        db = get_db()
        return list(db.phishing_tips.find({"category": category})
                   .sort("priority", 1))
    
    @staticmethod
    def find_all():
        """Find all tips"""
        db = get_db()
        return list(db.phishing_tips.find().sort("priority", 1))
    
    @staticmethod
    def clear_all():
        """Clear all tips (for updating)"""
        db = get_db()
        return db.phishing_tips.delete_many({})
    
    @staticmethod
    def bulk_insert(tips_list):
        """Insert multiple tips at once"""
        db = get_db()
        if tips_list:
            return db.phishing_tips.insert_many(tips_list)
        return None
    
    @staticmethod
    def find_by_title(title):
        """Find tip by title"""
        db = get_db()
        return db.phishing_tips.find_one({"title": title})
    
    @staticmethod
    def update_tip(title, content, category, priority):
        """Update existing tip"""
        db = get_db()
        return db.phishing_tips.update_one(
            {"title": title},
            {"$set": {
                "content": content,
                "category": category,
                "priority": priority,
                "updated_at": datetime.utcnow()
            }}
        )

# Utility functions for easy database operations
def get_all_users():
    """Get all users"""
    db = get_db()
    return list(db.users.find({}, {"password_hash": 0}))  # Exclude password hash

def get_recent_detections(limit=20):
    """Get recent detections across all users"""
    db = get_db()
    return list(db.detections.find()
               .sort("created_at", -1)
               .limit(limit))

def get_database_stats():
    """Get overall database statistics"""
    db = get_db()
    return {
        "total_users": db.users.count_documents({}),
        "total_detections": db.detections.count_documents({}),
        "total_tips": db.phishing_tips.count_documents({})
    }

def clean_database():
    """Clean up database for testing (use with caution)"""
    db = get_db()
    db.users.delete_many({})
    db.detections.delete_many({})
    db.phishing_tips.delete_many({})
    return "Database cleaned"