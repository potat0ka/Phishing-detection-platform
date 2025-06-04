"""
Professional MongoDB Models with Encryption
==========================================

Clean, production-ready models with MongoDB backend and comprehensive data encryption.
"""

import json
import uuid
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, USERS_FILE, DETECTIONS_FILE, TIPS_FILE, load_json_data, save_json_data
from encryption_utils import encrypt_sensitive_data, decrypt_sensitive_data

logger = logging.getLogger(__name__)


class User:
    """Professional User model with MongoDB and encryption support"""
    
    @staticmethod
    def create_user(username, email, password):
        """Create new user with encrypted data storage"""
        try:
            if db is not None:
                # MongoDB implementation
                existing_user = db.users.find_one({
                    '$or': [
                        {'username': username},
                        {'email': email}
                    ]
                })
                if existing_user:
                    return None
                
                user_data = {
                    'username': username,
                    'email': email,
                    'password_hash': generate_password_hash(password),
                    'created_at': datetime.utcnow(),
                    'privacy_level': 'high',
                    'data_retention_days': 365,
                    'last_login': None
                }
                
                # Encrypt sensitive data
                encrypted_data = encrypt_sensitive_data('user', user_data)
                
                result = db.users.insert_one(encrypted_data)
                logger.info(f"Created encrypted user in MongoDB: {result.inserted_id}")
                return str(result.inserted_id)
            else:
                # JSON fallback implementation
                users = load_json_data(USERS_FILE)
                
                # Check if user exists (decrypt to compare)
                for encrypted_user in users:
                    user = decrypt_sensitive_data('user', encrypted_user)
                    if user.get('username') == username or user.get('email') == email:
                        return None
                
                user_data = {
                    'id': str(uuid.uuid4()),
                    'username': username,
                    'email': email,
                    'password_hash': generate_password_hash(password),
                    'created_at': datetime.now().isoformat(),
                    'privacy_level': 'high',
                    'data_retention_days': 365,
                    'last_login': None
                }
                
                # Encrypt sensitive data
                encrypted_data = encrypt_sensitive_data('user', user_data)
                
                users.append(encrypted_data)
                save_json_data(USERS_FILE, users)
                
                logger.info(f"Created encrypted user in JSON: {user_data['id']}")
                return user_data['id']
                
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def find_by_username(username):
        """Find user by username with data decryption"""
        try:
            if db is not None:
                # MongoDB implementation - search through encrypted data
                for user_doc in db.users.find():
                    decrypted = decrypt_sensitive_data('user', user_doc)
                    if decrypted.get('username') == username:
                        decrypted['_id'] = str(user_doc['_id'])
                        return decrypted
                return None
            else:
                # JSON implementation
                users = load_json_data(USERS_FILE)
                for encrypted_user in users:
                    user = decrypt_sensitive_data('user', encrypted_user)
                    if user.get('username') == username:
                        return user
                return None
                
        except Exception as e:
            logger.error(f"Error finding user by username: {e}")
            return None
    
    @staticmethod
    def find_by_email(email):
        """Find user by email with data decryption"""
        try:
            if db is not None:
                # MongoDB implementation
                for user_doc in db.users.find():
                    decrypted = decrypt_sensitive_data('user', user_doc)
                    if decrypted.get('email') == email:
                        decrypted['_id'] = str(user_doc['_id'])
                        return decrypted
                return None
            else:
                # JSON implementation
                users = load_json_data(USERS_FILE)
                for encrypted_user in users:
                    user = decrypt_sensitive_data('user', encrypted_user)
                    if user.get('email') == email:
                        return user
                return None
                
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        try:
            if db is not None:
                from bson.objectid import ObjectId
                user_doc = db.users.find_one({'_id': ObjectId(user_id)})
                if user_doc:
                    decrypted = decrypt_sensitive_data('user', user_doc)
                    decrypted['_id'] = str(user_doc['_id'])
                    return decrypted
                return None
            else:
                users = load_json_data(USERS_FILE)
                for encrypted_user in users:
                    user = decrypt_sensitive_data('user', encrypted_user)
                    if user.get('id') == user_id:
                        return user
                return None
                
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with encrypted data"""
        user = User.find_by_username(username)
        if user and check_password_hash(user.get('password_hash', ''), password):
            return user
        return None


class Detection:
    """Professional Detection model with MongoDB and encryption support"""
    
    @staticmethod
    def create_detection(user_id, input_type, input_content, result, confidence_score, 
                        reasons=None, ai_analysis=None, user_ip=None, user_agent=None):
        """Create detection with encrypted activity data"""
        try:
            detection_data = {
                'user_id': user_id,
                'input_type': input_type,
                'input_content': input_content,
                'result': result,
                'confidence_score': confidence_score,
                'reasons': reasons or [],
                'ai_analysis': ai_analysis or {},
                'user_ip': user_ip,
                'user_agent': user_agent,
                'created_at': datetime.now().isoformat(),
                'privacy_protected': True
            }
            
            if db is not None:
                # MongoDB implementation
                detection_data['created_at'] = datetime.utcnow()
                encrypted_data = encrypt_sensitive_data('activity', detection_data)
                
                result = db.detections.insert_one(encrypted_data)
                logger.info(f"Created encrypted detection in MongoDB: {result.inserted_id}")
                return str(result.inserted_id)
            else:
                # JSON implementation
                detection_data['id'] = str(uuid.uuid4())
                encrypted_data = encrypt_sensitive_data('activity', detection_data)
                
                detections = load_json_data(DETECTIONS_FILE)
                detections.append(encrypted_data)
                save_json_data(DETECTIONS_FILE, detections)
                
                logger.info(f"Created encrypted detection in JSON: {detection_data['id']}")
                return detection_data['id']
                
        except Exception as e:
            logger.error(f"Error creating detection: {e}")
            return None
    
    @staticmethod
    def find_by_user(user_id, limit=10):
        """Find detections by user with decryption"""
        try:
            user_detections = []
            
            if db is not None:
                # MongoDB implementation
                cursor = db.detections.find({'user_id': user_id}).sort('created_at', -1).limit(limit)
                for doc in cursor:
                    decrypted = decrypt_sensitive_data('activity', doc)
                    decrypted['id'] = str(doc['_id'])
                    user_detections.append(decrypted)
            else:
                # JSON implementation
                detections = load_json_data(DETECTIONS_FILE)
                for encrypted_detection in detections:
                    detection = decrypt_sensitive_data('activity', encrypted_detection)
                    if detection.get('user_id') == user_id:
                        user_detections.append(detection)
                
                user_detections.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                user_detections = user_detections[:limit]
            
            return user_detections
            
        except Exception as e:
            logger.error(f"Error finding detections by user: {e}")
            return []
    
    @staticmethod
    def count_by_user(user_id):
        """Count detections by user"""
        try:
            if db is not None:
                return db.detections.count_documents({'user_id': user_id})
            else:
                detections = load_json_data(DETECTIONS_FILE)
                count = 0
                for encrypted_detection in detections:
                    detection = decrypt_sensitive_data('activity', encrypted_detection)
                    if detection.get('user_id') == user_id:
                        count += 1
                return count
        except Exception as e:
            logger.error(f"Error counting detections: {e}")
            return 0
    
    @staticmethod
    def get_user_stats(user_id):
        """Get detection statistics for user"""
        try:
            user_detections = Detection.find_by_user(user_id, limit=1000)
            stats = {'safe': 0, 'phishing': 0, 'suspicious': 0}
            
            for detection in user_detections:
                result = detection.get('result', '')
                if result in stats:
                    stats[result] += 1
            
            stats['total'] = sum(stats.values())
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {'safe': 0, 'phishing': 0, 'suspicious': 0, 'total': 0}
    
    @staticmethod
    def delete_detection(detection_id, user_id):
        """Delete detection by ID if belongs to user"""
        try:
            if db is not None:
                from bson.objectid import ObjectId
                result = db.detections.delete_one({
                    '_id': ObjectId(detection_id),
                    'user_id': user_id
                })
                return result.deleted_count > 0
            else:
                detections = load_json_data(DETECTIONS_FILE)
                original_length = len(detections)
                
                # Filter out the detection while checking ownership
                filtered_detections = []
                for encrypted_detection in detections:
                    detection = decrypt_sensitive_data('activity', encrypted_detection)
                    if not (detection.get('id') == detection_id and detection.get('user_id') == user_id):
                        filtered_detections.append(encrypted_detection)
                
                if len(filtered_detections) < original_length:
                    save_json_data(DETECTIONS_FILE, filtered_detections)
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Error deleting detection: {e}")
            return False


class PhishingTip:
    """Professional PhishingTip model with MongoDB support"""
    
    @staticmethod
    def get_all_tips():
        """Get all security tips"""
        try:
            if db is not None:
                return list(db.security_tips.find())
            else:
                return load_json_data(TIPS_FILE)
        except Exception as e:
            logger.error(f"Error getting tips: {e}")
            return []
    
    @staticmethod
    def bulk_insert(tips):
        """Insert multiple tips"""
        try:
            if db is not None:
                # Clear existing tips and insert new ones
                db.security_tips.delete_many({})
                if tips:
                    db.security_tips.insert_many(tips)
                return len(tips)
            else:
                save_json_data(TIPS_FILE, tips)
                return len(tips)
        except Exception as e:
            logger.error(f"Error bulk inserting tips: {e}")
            return 0


# Database utility functions
def get_all_users():
    """Get all users (excluding password hashes)"""
    try:
        users = []
        if db is not None:
            for user_doc in db.users.find():
                decrypted = decrypt_sensitive_data('user', user_doc)
                decrypted.pop('password_hash', None)
                users.append(decrypted)
        else:
            encrypted_users = load_json_data(USERS_FILE)
            for encrypted_user in encrypted_users:
                user = decrypt_sensitive_data('user', encrypted_user)
                user.pop('password_hash', None)
                users.append(user)
        return users
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return []


def get_recent_detections(limit=20):
    """Get recent detections across all users"""
    try:
        detections = []
        if db is not None:
            cursor = db.detections.find().sort('created_at', -1).limit(limit)
            for doc in cursor:
                decrypted = decrypt_sensitive_data('activity', doc)
                detections.append(decrypted)
        else:
            encrypted_detections = load_json_data(DETECTIONS_FILE)
            for encrypted_detection in encrypted_detections:
                detection = decrypt_sensitive_data('activity', encrypted_detection)
                detections.append(detection)
            
            detections.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            detections = detections[:limit]
        
        return detections
    except Exception as e:
        logger.error(f"Error getting recent detections: {e}")
        return []


def get_database_stats():
    """Get overall database statistics"""
    try:
        if db is not None:
            return {
                'total_users': db.users.count_documents({}),
                'total_detections': db.detections.count_documents({}),
                'total_tips': db.security_tips.count_documents({})
            }
        else:
            users = load_json_data(USERS_FILE)
            detections = load_json_data(DETECTIONS_FILE)
            tips = load_json_data(TIPS_FILE)
            
            return {
                'total_users': len(users),
                'total_detections': len(detections),
                'total_tips': len(tips)
            }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {'total_users': 0, 'total_detections': 0, 'total_tips': 0}