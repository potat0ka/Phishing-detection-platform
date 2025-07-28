"""
Scan History Model for User Scan Storage and Retrieval
====================================================

This model handles storing and retrieving scan history for individual users,
including both authenticated and anonymous scans. It provides comprehensive
scan data management with proper MongoDB document structure.

Author: AI Phishing Detection Platform
"""

import logging
from datetime import datetime
from flask import session
from models.database import DatabaseManager

logger = logging.getLogger(__name__)

# Initialize database manager
db = None

def initialize_scan_history_model(database_manager):
    """Initialize the scan history model with database manager"""
    global db
    db = database_manager
    logger.info("Scan History Model initialized")

class ScanHistoryModel:
    """
    Model for managing user scan history and analytics
    
    This class provides methods to store scan results, retrieve user-specific
    scan history, and generate scan analytics for dashboard display.
    """
    
    @staticmethod
    def save_scan_result(content, content_type, result, user_id=None):
        """
        Save scan result to MongoDB with complete document structure
        
        Args:
            content (str): The content that was analyzed (URL, email, message)
            content_type (str): Type of content ('url', 'email', 'message')
            result (dict): Complete ML analysis result from detector
            user_id (str, optional): User ID if user is authenticated
            
        Returns:
            str: Document ID if saved successfully, None otherwise
        """
        try:
            # Get current user from session if not provided
            if user_id is None:
                user_id = session.get('user_id')
            
            # Create comprehensive scan document
            scan_document = {
                # User tracking
                'user_id': user_id,  # None for anonymous users
                'session_id': session.get('session_id') or 'anonymous',
                'is_authenticated': user_id is not None,
                
                # Content information
                'content': content[:500],  # Limit content length for storage
                'content_type': content_type,
                'content_length': len(content),
                
                # Analysis results
                'threat_level': result.get('threat_level'),
                'confidence_score': result.get('confidence_score', 0.0),
                'risk_score': result.get('risk_score', 0.0),
                'analysis_components': result.get('analysis_components', []),
                'warnings': result.get('warnings', []),
                'explanation': result.get('explanation', ''),
                
                # Additional metadata
                'urls_found': result.get('urls_found', 0),
                'analysis_timestamp': datetime.utcnow(),
                'created_at': datetime.utcnow(),
                
                # Technical details
                'ml_model_used': result.get('content_type') == content_type,
                'analysis_duration': None,  # Could be added if timing is tracked
                'user_agent': None  # Could add request headers if needed
            }
            
            # Save to MongoDB scan_logs collection
            if db and db.connected:
                document_id = db.insert_document('scan_logs', scan_document)
                
                # Log success with user context
                user_context = f"user {user_id}" if user_id else "anonymous user"
                logger.info(f"Scan result saved for {user_context}: {content_type} analysis with {result.get('threat_level')} threat level")
                
                # Update user-specific statistics if authenticated
                if user_id:
                    ScanHistoryModel._update_user_scan_stats(user_id, result.get('threat_level'))
                
                return str(document_id)
            else:
                logger.warning("Cannot save scan result - database not connected")
                return None
                
        except Exception as e:
            logger.error(f"Error saving scan result: {str(e)}")
            return None
    
    @staticmethod
    def get_user_scan_history(user_id, limit=20, offset=0):
        """
        Retrieve scan history for a specific user
        
        Args:
            user_id (str): User ID to get scans for
            limit (int): Maximum number of scans to return
            offset (int): Number of scans to skip (for pagination)
            
        Returns:
            list: List of user's scan documents, newest first
        """
        try:
            if not user_id:
                logger.warning("Cannot get scan history - no user ID provided")
                return []
            
            if db and db.connected:
                # Query user-specific scans, sorted by newest first
                user_scans = db.find_documents(
                    'scan_logs',
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
        """
        Get scan statistics for a specific user
        
        Args:
            user_id (str): User ID to get stats for
            
        Returns:
            dict: User scan statistics including counts and last scan time
        """
        try:
            if not user_id:
                return {
                    'scans_performed': 0,
                    'threats_detected': 0,
                    'last_scan': None,
                    'account_created': None
                }
            
            if db and db.connected:
                # Get all user scans for analysis
                user_scans = db.find_documents(
                    'scan_logs',
                    query={'user_id': user_id},
                    sort=[('created_at', -1)]
                )
                
                # Calculate statistics
                total_scans = len(user_scans)
                threats_detected = len([
                    scan for scan in user_scans 
                    if scan.get('threat_level') in ['high', 'medium']
                ])
                
                # Get last scan timestamp
                last_scan = user_scans[0].get('created_at') if user_scans else None
                
                # Try to get account creation from user document
                user_doc = db.find_documents('users', query={'_id': user_id}, limit=1)
                account_created = None
                if user_doc:
                    account_created = user_doc[0].get('created_at')
                
                stats = {
                    'scans_performed': total_scans,
                    'threats_detected': threats_detected,
                    'last_scan': last_scan,
                    'account_created': account_created,
                    'scan_types': ScanHistoryModel._get_scan_type_breakdown(user_scans),
                    'threat_breakdown': ScanHistoryModel._get_threat_level_breakdown(user_scans)
                }
                
                logger.info(f"Generated stats for user {user_id}: {total_scans} scans, {threats_detected} threats")
                return stats
            else:
                logger.warning("Cannot get user stats - database not connected")
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
    def get_recent_scans_all_users(limit=10):
        """
        Get recent scans from all users for analytics dashboard
        
        Args:
            limit (int): Maximum number of scans to return
            
        Returns:
            list: Recent scans from all users, anonymized
        """
        try:
            if db and db.connected:
                recent_scans = db.find_documents(
                    'scan_logs',
                    sort=[('created_at', -1)],
                    limit=limit
                )
                
                # Anonymize user data for public analytics
                for scan in recent_scans:
                    if 'user_id' in scan:
                        scan['user_id'] = 'user_***' if scan['user_id'] else 'anonymous'
                
                return recent_scans
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting recent scans: {str(e)}")
            return []
    
    @staticmethod
    def _update_user_scan_stats(user_id, threat_level):
        """
        Update user-specific scan statistics (internal method)
        
        Args:
            user_id (str): User ID to update stats for
            threat_level (str): Threat level of the completed scan
        """
        try:
            if db and db.connected:
                # Update or create user stats document
                update_doc = {
                    '$inc': {'total_scans': 1},
                    '$set': {'last_scan_time': datetime.utcnow()}
                }
                
                # Increment threat counter if threat detected
                if threat_level in ['high', 'medium']:
                    update_doc['$inc']['threats_detected'] = 1
                
                # Upsert user stats (create if doesn't exist)
                db.update_document(
                    'user_stats',
                    {'user_id': user_id},
                    update_doc,
                    upsert=True
                )
                
        except Exception as e:
            logger.error(f"Error updating user scan stats: {str(e)}")
    
    @staticmethod
    def _get_scan_type_breakdown(user_scans):
        """Get breakdown of scan types for user analytics"""
        breakdown = {'url': 0, 'email': 0, 'message': 0}
        for scan in user_scans:
            scan_type = scan.get('content_type', 'unknown')
            if scan_type in breakdown:
                breakdown[scan_type] += 1
        return breakdown
    
    @staticmethod
    def _get_threat_level_breakdown(user_scans):
        """Get breakdown of threat levels for user analytics"""
        breakdown = {'low': 0, 'medium': 0, 'high': 0}
        for scan in user_scans:
            threat_level = scan.get('threat_level', 'unknown')
            if threat_level in breakdown:
                breakdown[threat_level] += 1
        return breakdown
    
    @staticmethod
    def delete_user_scan_history(user_id):
        """
        Delete all scan history for a user (for privacy/GDPR compliance)
        
        Args:
            user_id (str): User ID to delete scan history for
            
        Returns:
            int: Number of documents deleted
        """
        try:
            if not user_id:
                return 0
            
            if db and db.connected:
                # Delete all scans for the user
                result = db.delete_documents('scan_logs', {'user_id': user_id})
                deleted_count = result.deleted_count if result else 0
                
                # Also delete user stats
                db.delete_documents('user_stats', {'user_id': user_id})
                
                logger.info(f"Deleted {deleted_count} scan records for user {user_id}")
                return deleted_count
            else:
                logger.warning("Cannot delete scan history - database not connected")
                return 0
                
        except Exception as e:
            logger.error(f"Error deleting user scan history: {str(e)}")
            return 0
    
    @staticmethod
    def get_anonymous_scan_count():
        """Get count of anonymous (non-authenticated) scans"""
        try:
            if db and db.connected:
                anonymous_scans = db.find_documents(
                    'scan_logs',
                    query={'user_id': None}
                )
                return len(anonymous_scans)
            return 0
        except Exception as e:
            logger.error(f"Error getting anonymous scan count: {str(e)}")
            return 0