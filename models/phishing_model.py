"""
Phishing Data Model
==================

This model handles all phishing-related data operations in MongoDB.
It manages phishing URLs, detection results, and threat intelligence.

Author: Bigendra Shrestha
"""

import logging
from datetime import datetime
from services.mongo_service import mongo_service

logger = logging.getLogger(__name__)

class PhishingModel:
    """
    Phishing Data Model for MongoDB operations
    
    This class handles:
    - Storing detected phishing URLs
    - Managing threat categories and status
    - Providing fallback data when database is unavailable
    """
    
    @staticmethod
    def get_all_phishing_data():
        """Get all phishing data from database or fallback"""
        if mongo_service.is_connected():
            return mongo_service.find_documents('phishing_data')
        else:
            # Fallback data when MongoDB is not available
            return PhishingModel.get_fallback_data()
    
    @staticmethod
    def add_phishing_url(url, category, status, description, confidence_score=0.8):
        """Add new phishing URL to database"""
        phishing_data = {
            'url': url,
            'category': category,
            'status': status,
            'description': description,
            'confidence_score': confidence_score,
            'detected_at': datetime.utcnow()
        }
        
        if mongo_service.is_connected():
            return mongo_service.insert_document('phishing_data', phishing_data)
        return None
    
    @staticmethod
    def update_phishing_status(url, new_status):
        """Update the status of a phishing URL"""
        if mongo_service.is_connected():
            return mongo_service.update_document(
                'phishing_data',
                {'url': url},
                {'$set': {'status': new_status}}
            )
        return 0
    
    @staticmethod
    def update_phishing_url(data_id, url, category, status, description, confidence_score):
        """Update complete phishing URL entry"""
        try:
            if mongo_service.is_connected():
                # Update in MongoDB
                result = mongo_service.update_document(
                    'phishing_data',
                    {'_id': data_id},
                    {'$set': {
                        'url': url,
                        'category': category,
                        'status': status,
                        'description': description,
                        'confidence_score': confidence_score,
                        'updated_at': datetime.utcnow()
                    }}
                )
                return result > 0
            else:
                # File-based fallback - for demo purposes
                # In production, this would update a JSON file
                logger.info(f"Updated phishing data {data_id} (fallback mode)")
                return True
        except Exception as e:
            logger.error(f"Error updating phishing URL: {e}")
            return False
    
    @staticmethod
    def delete_phishing_url(url):
        """Delete a phishing URL from database"""
        if mongo_service.is_connected():
            return mongo_service.delete_documentss('phishing_data', {'url': url})
        return 0
    
    @staticmethod
    def get_recent_threats(limit=5):
        """Get recent phishing threats"""
        if mongo_service.is_connected():
            return mongo_service.find_documents('phishing_data', limit=limit)
        else:
            fallback_data = PhishingModel.get_fallback_data()
            return fallback_data[:limit]
    
    @staticmethod
    def get_fallback_data():
        """Fallback phishing data when database is unavailable"""
        return [
            {
                '_id': 'fallback_1',
                'url': 'https://suspicious-bank-login.fake.com',
                'category': 'phishing',
                'status': 'active',
                'description': 'Fake banking website attempting to steal login credentials',
                'confidence_score': 0.95,
                'detected_at': datetime.utcnow(),
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'fallback_2', 
                'url': 'https://paypal-security-update.malicious.net',
                'category': 'phishing',
                'status': 'active',
                'description': 'Fraudulent PayPal security notification website',
                'confidence_score': 0.89,
                'detected_at': datetime.utcnow(),
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'fallback_3',
                'url': 'https://amazon-prize-winner.scam.org',
                'category': 'suspicious',
                'status': 'monitored',
                'description': 'Fake Amazon prize notification attempting to collect personal data',
                'confidence_score': 0.82,
                'detected_at': datetime.utcnow(),
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'fallback_4',
                'url': 'https://microsoft-account-suspended.phish.com',
                'category': 'phishing',
                'status': 'active',
                'description': 'Fake Microsoft account suspension notification',
                'confidence_score': 0.91,
                'detected_at': datetime.utcnow(),
                'created_at': datetime.utcnow()
            },
            {
                '_id': 'fallback_5',
                'url': 'https://covid-relief-fund.malware.net',
                'category': 'malware',
                'status': 'blocked',
                'description': 'Malicious COVID relief fund website distributing malware',
                'confidence_score': 0.97,
                'detected_at': datetime.utcnow(),
                'created_at': datetime.utcnow()
            }
        ]