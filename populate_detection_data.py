#!/usr/bin/env python3
"""
Create sample detection data for testing export functionality
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mongodb_config import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_detections():
    """Create sample detection data for testing"""
    
    # Initialize database connection
    db_manager.init_connection()
    
    # Sample URLs and results
    sample_data = [
        {
            'content': 'https://paypal-security-update.net/verify-account',
            'result': {'result': 'phishing', 'category': 'phishing', 'confidence': 0.95},
            'user_id': 'user_1749125333_6273'
        },
        {
            'content': 'https://amazon-prize-winner.com/claim-reward',
            'result': {'result': 'phishing', 'category': 'phishing', 'confidence': 0.89},
            'user_id': 'super_admin_001'
        },
        {
            'content': 'https://microsoft-office365-verify.info/login',
            'result': {'result': 'phishing', 'category': 'suspicious', 'confidence': 0.78},
            'user_id': 'user_1749125333_6273'
        },
        {
            'content': 'https://google.com',
            'result': {'result': 'safe', 'category': 'safe', 'confidence': 0.02},
            'user_id': 'super_admin_001'
        },
        {
            'content': 'https://github.com',
            'result': {'result': 'safe', 'category': 'safe', 'confidence': 0.01},
            'user_id': 'user_1749125333_6273'
        },
        {
            'content': 'https://bank-urgent-verification.net/secure-login',
            'result': {'result': 'dangerous', 'category': 'dangerous', 'confidence': 0.97},
            'user_id': 'super_admin_001'
        },
        {
            'content': 'https://facebook.com',
            'result': {'result': 'safe', 'category': 'safe', 'confidence': 0.03},
            'user_id': 'user_1749125333_6273'
        },
        {
            'content': 'https://crypto-investment-guaranteed.biz/signup',
            'result': {'result': 'phishing', 'category': 'phishing', 'confidence': 0.92},
            'user_id': 'super_admin_001'
        }
    ]
    
    created_count = 0
    base_time = datetime.utcnow()
    
    for i, data in enumerate(sample_data):
        try:
            # Create detection record with timestamp
            detection_record = {
                'id': f'detection_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}_{i}',
                'user_id': data['user_id'],
                'content': data['content'],
                'result': data['result'],
                'timestamp': (base_time - timedelta(hours=random.randint(1, 48))).isoformat(),
                'scan_type': 'url',
                'ip_address': f'192.168.1.{random.randint(10, 250)}',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Insert into database
            result = db_manager.insert_one('detections', detection_record)
            
            if result:
                created_count += 1
                logger.info(f"✓ Created detection record: {data['content'][:50]}...")
            else:
                logger.error(f"✗ Failed to create detection record for: {data['content']}")
                
        except Exception as e:
            logger.error(f"Error creating detection record: {e}")
    
    logger.info(f"\nCreated {created_count} sample detection records for testing export functionality")
    return created_count

if __name__ == "__main__":
    create_sample_detections()