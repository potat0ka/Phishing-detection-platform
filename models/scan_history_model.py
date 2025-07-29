"""
Scan History Model - Clean MongoDB Implementation
===============================================

This model handles storing and retrieving scan history for users using the centralized MongoDB service.

Author: Bigendra Shrestha
"""

import logging
from datetime import datetime
from flask import session
from services.mongo_service import mongo_service

logger = logging.getLogger(__name__)

def initialize_scan_history_model():
    """Initialize the scan history model"""
    logger.info("Scan History Model initialized")

class ScanHistoryModel:
    """Model for managing user scan history and analytics"""
    
    @staticmethod
    def save_scan_result(content, content_type, result, user_id=None):
        """Save scan result to MongoDB"""
        try:
            if user_id is None:
                user_id = session.get('user_id')
            
            scan_document = {
                'user_id': user_id,
                'session_id': session.get('session_id') or 'anonymous',
                'is_authenticated': user_id is not None,
                'content': content[:500],
                'content_type': content_type,
                'content_length': len(content),
                'threat_level': result.get('threat_level'),
                'confidence_score': result.get('confidence_score', 0.0),
                'risk_score': result.get('risk_score', 0.0),
                'analysis_components': result.get('analysis_components', []),
                'warnings': result.get('warnings', []),
                'explanation': result.get('explanation', ''),
                'urls_found': result.get('urls_found', 0),
                'analysis_timestamp': datetime.utcnow(),
                'created_at': datetime.utcnow(),
                'ml_model_used': result.get('content_type') == content_type,
                'analysis_duration': None,
                'user_agent': None
            }
            
            if mongo_service.is_connected():
                document_id = mongo_service.insert_document('scan_history', scan_document)
                user_context = f"user {user_id}" if user_id else "anonymous user"
                logger.info(f"Scan result saved for {user_context}: {content_type} analysis with {result.get('threat_level')} threat level")
                return str(document_id) if document_id else None
            else:
                logger.warning("Cannot save scan result - database not connected")
                return None
                
        except Exception as e:
            logger.error(f"Error saving scan result: {str(e)}")
            return None
    
    @staticmethod
    def get_user_scan_history(user_id, limit=20, offset=0):
        """Retrieve scan history for a specific user"""
        try:
            if not user_id:
                logger.warning("Cannot get scan history - no user ID provided")
                return []
            
            if mongo_service.is_connected():
                user_scans = mongo_service.find_documents(
                    'scan_history',
                    query={'user_id': user_id},
                    sort=[('created_at', -1)],
                    limit=limit,
                    skip=offset
                )
                logger.info(f"Retrieved {len(user_scans)} scan records for user {user_id}")
                return user_scans
            else:
                logger.warning("Cannot get scan history - database not connected")
                return []
                
        except Exception as e:
            logger.error(f"Error retrieving user scan history: {str(e)}")
            return []
    
    @staticmethod
    def get_user_scan_stats(user_id):
        """Get scan statistics for a specific user"""
        try:
            if not user_id:
                return {
                    'scans_performed': 0,
                    'threats_detected': 0,
                    'last_scan': None,
                    'account_created': None
                }
            
            if mongo_service.is_connected():
                user_scans = mongo_service.find_documents(
                    'scan_history',
                    query={'user_id': user_id},
                    sort=[('created_at', -1)]
                )
                
                scans_performed = len(user_scans)
                threats_detected = sum(1 for scan in user_scans if scan.get('threat_level') in ['HIGH', 'CRITICAL'])
                last_scan = user_scans[0].get('created_at') if user_scans else None
                
                user_doc = mongo_service.find_documents('users', query={'_id': user_id}, limit=1)
                account_created = user_doc[0].get('created_at') if user_doc else None
                
                return {
                    'scans_performed': scans_performed,
                    'threats_detected': threats_detected,
                    'last_scan': last_scan,
                    'account_created': account_created
                }
            else:
                return {
                    'scans_performed': 0,
                    'threats_detected': 0,
                    'last_scan': None,
                    'account_created': None
                }
                
        except Exception as e:
            logger.error(f"Error getting user scan stats: {str(e)}")
            return {
                'scans_performed': 0,
                'threats_detected': 0,
                'last_scan': None,
                'account_created': None
            }
    
    @staticmethod
    def get_recent_scans(limit=50):
        """Get recent scans from all users for admin dashboard"""
        try:
            if mongo_service.is_connected():
                recent_scans = mongo_service.find_documents(
                    'scan_history',
                    sort=[('created_at', -1)],
                    limit=limit
                )
                
                # Anonymize user data for privacy
                for scan in recent_scans:
                    if scan.get('user_id'):
                        scan['user_id'] = 'user_***'
                    scan['content'] = scan.get('content', '')[:100] + '...' if len(scan.get('content', '')) > 100 else scan.get('content', '')
                
                return recent_scans
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting recent scans: {str(e)}")
            return []