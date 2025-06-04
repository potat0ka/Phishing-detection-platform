"""
Detection Model with MongoDB and Encryption
===========================================

Professional detection history management with encrypted activity data.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId
import logging

from database.connection import get_database
from utils.encryption import encrypt_sensitive_data, decrypt_sensitive_data

logger = logging.getLogger(__name__)


class Detection:
    """Detection model with encrypted activity storage in MongoDB"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self._id = data.get('_id')
    
    @property
    def id(self) -> str:
        """Get detection ID as string"""
        return str(self._id) if self._id else None
    
    @property
    def user_id(self) -> str:
        """Get user ID"""
        return self.data.get('user_id', '')
    
    @property
    def created_at(self) -> datetime:
        """Get detection timestamp"""
        return self.data.get('created_at', datetime.utcnow())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with decrypted data"""
        decrypted = decrypt_sensitive_data('activity', self.data)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'input_type': decrypted.get('input_type'),
            'input_content': decrypted.get('input_content'),
            'result': decrypted.get('result'),
            'confidence_score': decrypted.get('confidence_score'),
            'reasons': decrypted.get('reasons', []),
            'ai_analysis': decrypted.get('ai_analysis', {}),
            'created_at': self.created_at
        }
    
    @classmethod
    def create(cls, user_id: str, input_type: str, input_content: str, 
               result: str, confidence_score: float, reasons: List[str] = None,
               ai_analysis: Dict[str, Any] = None, user_ip: str = None,
               user_agent: str = None) -> Optional['Detection']:
        """Create new detection with encrypted activity data"""
        try:
            db = get_database()
            
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
                'created_at': datetime.utcnow(),
                'privacy_protected': True
            }
            
            # Encrypt sensitive activity data
            encrypted_data = encrypt_sensitive_data('activity', detection_data)
            
            # Insert into database
            result = db.detections.insert_one(encrypted_data)
            encrypted_data['_id'] = result.inserted_id
            
            logger.info(f"Created encrypted detection: {result.inserted_id}")
            return cls(encrypted_data)
            
        except Exception as e:
            logger.error(f"Error creating detection: {e}")
            return None
    
    @classmethod
    def find_by_user(cls, user_id: str, limit: int = 10) -> List['Detection']:
        """Find detections by user ID with decryption"""
        try:
            db = get_database()
            
            # Find all detections for user and decrypt
            detections = []
            cursor = db.detections.find({'user_id': user_id}).sort('created_at', -1).limit(limit)
            
            for doc in cursor:
                detections.append(cls(doc))
            
            return detections
            
        except Exception as e:
            logger.error(f"Error finding detections by user: {e}")
            return []
    
    @classmethod
    def count_by_user(cls, user_id: str) -> int:
        """Count detections by user"""
        try:
            db = get_database()
            return db.detections.count_documents({'user_id': user_id})
        except Exception as e:
            logger.error(f"Error counting detections: {e}")
            return 0
    
    @classmethod
    def get_user_stats(cls, user_id: str) -> Dict[str, int]:
        """Get detection statistics for user"""
        try:
            db = get_database()
            
            # Get all user detections and decrypt for stats
            user_detections = []
            for doc in db.detections.find({'user_id': user_id}):
                decrypted = decrypt_sensitive_data('activity', doc)
                user_detections.append(decrypted)
            
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
    
    @classmethod
    def delete_by_id(cls, detection_id: str, user_id: str) -> bool:
        """Delete detection by ID (only if belongs to user)"""
        try:
            db = get_database()
            
            result = db.detections.delete_one({
                '_id': ObjectId(detection_id),
                'user_id': user_id
            })
            
            if result.deleted_count > 0:
                logger.info(f"Deleted detection: {detection_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting detection: {e}")
            return False
    
    @classmethod
    def delete_by_user(cls, user_id: str) -> int:
        """Delete all detections for a user"""
        try:
            db = get_database()
            result = db.detections.delete_many({'user_id': user_id})
            
            logger.info(f"Deleted {result.deleted_count} detections for user: {user_id}")
            return result.deleted_count
            
        except Exception as e:
            logger.error(f"Error deleting user detections: {e}")
            return 0
    
    @staticmethod
    def get_total_count() -> int:
        """Get total number of detections"""
        try:
            db = get_database()
            return db.detections.count_documents({})
        except Exception as e:
            logger.error(f"Error getting total detection count: {e}")
            return 0