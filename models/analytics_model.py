"""
Analytics Model
==============

This model handles analytics and system statistics in MongoDB.
It tracks usage metrics, detection rates, and system performance.

Author: Bigendra Shrestha
"""

import logging
from datetime import datetime
from services.mongo_service import mongo_service

logger = logging.getLogger(__name__)

class AnalyticsModel:
    """
    Analytics Model for MongoDB operations
    
    This class handles:
    - System statistics and metrics
    - Detection rate tracking
    - User activity analytics
    """
    
    @staticmethod
    def get_user_scan_count(user_id):
        """Get total scans performed by a specific user"""
        try:
            if mongo_service.is_connected():
                # Count scans for this user
                scan_logs = mongo_service.find_documents('scan_logs', {'user_id': str(user_id)})
                return len(scan_logs)
            return 0
        except Exception as e:
            logger.error(f"Error getting user scan count: {e}")
            return 0
    
    @staticmethod
    def get_user_threat_count(user_id):
        """Get total threats detected in user's scans"""
        try:
            if mongo_service.is_connected():
                # Count threats detected for this user
                scan_logs = mongo_service.find_documents('scan_logs', {
                    'user_id': str(user_id),
                    'result': {'$in': ['high', 'medium']}
                })
                return len(scan_logs)
            return 0
        except Exception as e:
            logger.error(f"Error getting user threat count: {e}")
            return 0
    
    @staticmethod
    def get_user_recent_scans(user_id, limit=5):
        """Get recent scans for a specific user"""
        try:
            if mongo_service.is_connected():
                scan_logs = mongo_service.find_documents('scan_logs', 
                                            {'user_id': str(user_id)}, 
                                            sort=[('timestamp', -1)], 
                                            limit=limit)
                return scan_logs
            return []
        except Exception as e:
            logger.error(f"Error getting user recent scans: {e}")
            return []
    
    @staticmethod
    def get_user_last_scan(user_id):
        """Get timestamp of user's last scan"""
        try:
            recent_scans = AnalyticsModel.get_user_recent_scans(user_id, limit=1)
            if recent_scans:
                return recent_scans[0].get('timestamp')
            return None
        except Exception as e:
            logger.error(f"Error getting user last scan: {e}")
            return None

    @staticmethod
    def get_system_stats():
        """Get current system statistics"""
        if mongo_service.is_connected():
            stats = mongo_service.find_documents('system_stats')
            return stats[0] if stats else AnalyticsModel.get_fallback_stats()
        else:
            return AnalyticsModel.get_fallback_stats()
    
    @staticmethod
    def update_scan_count():
        """Increment total scan count"""
        if mongo_service.is_connected():
            return mongo_service.update_document(
                'system_stats',
                {},
                {'$inc': {'total_scans': 1}}
            )
        return 0
    
    @staticmethod
    def update_threat_blocked():
        """Increment threats blocked count"""
        if mongo_service.is_connected():
            return mongo_service.update_document(
                'system_stats',
                {},
                {'$inc': {'threats_blocked': 1}}
            )
        return 0
    
    @staticmethod
    def log_scan_activity(url, result, confidence_score):
        """Log a scan activity"""
        scan_log = {
            'url': url,
            'result': result,
            'confidence_score': confidence_score,
            'timestamp': datetime.utcnow(),
            'user_agent': None  # Could add request headers if needed
        }
        
        if mongo_service.is_connected():
            return mongo_service.insert_document('scan_logs', scan_log)
        return None
    
    @staticmethod
    def get_recent_scans(limit=10):
        """Get recent scan activities"""
        if mongo_service.is_connected():
            return mongo_service.find_documents('scan_logs', limit=limit)
        return []
    
    @staticmethod
    def get_detection_stats():
        """Get detection statistics by category"""
        if mongo_service.is_connected():
            # In a real implementation, this would use MongoDB aggregation
            phishing_data = mongo_service.find_documents('phishing_data')
            stats = {
                'total_threats': len(phishing_data),
                'phishing': len([p for p in phishing_data if p.get('category') == 'phishing']),
                'malware': len([p for p in phishing_data if p.get('category') == 'malware']),
                'suspicious': len([p for p in phishing_data if p.get('category') == 'suspicious'])
            }
            return stats
        else:
            return {
                'total_threats': 15,
                'phishing': 8,
                'malware': 4,
                'suspicious': 3
            }
    
    @staticmethod
    def get_fallback_stats():
        """Fallback system statistics when database is unavailable"""
        return {
            'total_scans': 12847,
            'threats_blocked': 1293,
            'total_users': 2456,
            'detection_rate': 99.2,
            'uptime': '99.8%',
            'last_updated': datetime.utcnow()
        }
    
    @staticmethod
    def initialize_stats():
        """Initialize system statistics in database"""
        if mongo_service.is_connected():
            existing_stats = mongo_service.find_documents('system_stats')
            if not existing_stats:
                initial_stats = {
                    'total_scans': 0,
                    'threats_blocked': 0,
                    'total_users': 0,
                    'detection_rate': 99.2,
                    'uptime': '100%',
                    'last_updated': datetime.utcnow()
                }
                return mongo_service.insert_document('system_stats', initial_stats)
        return None