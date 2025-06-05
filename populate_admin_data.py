#!/usr/bin/env python3
"""
Populate Admin Dashboard with Sample Data
Creates realistic detection records and safety tips for demonstration
"""

import sys
import os
from datetime import datetime, timedelta
import uuid

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mongodb_config import db_manager

def populate_detection_data():
    """Create sample detection records"""
    print("Creating sample detection records...")
    
    # Sample detection data with realistic phishing examples
    sample_detections = [
        {
            'id': f'detection_{uuid.uuid4().hex[:8]}',
            'user_id': 'user_demo_admin',
            'input_type': 'url',
            'input_content': 'https://secure-bank-login.suspicious-domain.com/verify-account',
            'result': 'dangerous',
            'confidence_score': 0.95,
            'created_at': (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            'threat_indicators': ['Suspicious domain', 'Typosquatting attempt', 'SSL certificate mismatch'],
            'recommendations': ['Do not click this link', 'Report to authorities', 'Verify with official bank website']
        },
        {
            'id': f'detection_{uuid.uuid4().hex[:8]}',
            'user_id': 'user_demo_user',
            'input_type': 'email',
            'input_content': 'Urgent: Your account will be suspended. Click here to verify your information immediately.',
            'result': 'suspicious',
            'confidence_score': 0.78,
            'created_at': (datetime.utcnow() - timedelta(hours=5)).isoformat(),
            'threat_indicators': ['Urgency tactics', 'Generic greeting', 'Suspicious call-to-action'],
            'recommendations': ['Verify sender identity', 'Contact organization directly', 'Do not provide personal information']
        },
        {
            'id': f'detection_{uuid.uuid4().hex[:8]}',
            'user_id': 'user_demo_admin',
            'input_type': 'url',
            'input_content': 'https://www.google.com',
            'result': 'safe',
            'confidence_score': 0.99,
            'created_at': (datetime.utcnow() - timedelta(hours=8)).isoformat(),
            'threat_indicators': [],
            'recommendations': ['Website appears safe to visit']
        },
        {
            'id': f'detection_{uuid.uuid4().hex[:8]}',
            'user_id': 'user_demo_user',
            'input_type': 'message',
            'input_content': 'Congratulations! You have won $1,000,000. Send your bank details to claim your prize.',
            'result': 'dangerous',
            'confidence_score': 0.92,
            'created_at': (datetime.utcnow() - timedelta(days=1)).isoformat(),
            'threat_indicators': ['Prize scam', 'Request for financial information', 'Too good to be true'],
            'recommendations': ['Delete message immediately', 'Never provide financial details', 'Report as spam']
        },
        {
            'id': f'detection_{uuid.uuid4().hex[:8]}',
            'user_id': 'user_demo_admin',
            'input_type': 'email',
            'input_content': 'Hello, this is a legitimate business email from our marketing team.',
            'result': 'safe',
            'confidence_score': 0.85,
            'created_at': (datetime.utcnow() - timedelta(days=2)).isoformat(),
            'threat_indicators': [],
            'recommendations': ['Email appears legitimate']
        }
    ]
    
    # Insert detection records
    for detection in sample_detections:
        existing = db_manager.find_one('detections', {'id': detection['id']})
        if not existing:
            db_manager.insert_one('detections', detection)
            print(f"Created detection: {detection['result']} - {detection['input_type']}")

def populate_safety_tips():
    """Create comprehensive safety tips"""
    print("Creating safety tips...")
    
    safety_tips = [
        # Email Tips
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Verify Sender Identity',
            'content': 'Always verify the sender\'s email address and look for spelling mistakes or suspicious domains.',
            'category': 'email',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Check for Urgency Tactics',
            'content': 'Be suspicious of emails that create a sense of urgency or pressure you to act immediately.',
            'category': 'email',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Verify Links Before Clicking',
            'content': 'Hover over links to see the actual destination URL before clicking on them.',
            'category': 'email',
            'priority': 2,
            'created_at': datetime.utcnow().isoformat()
        },
        
        # URL Tips
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Check SSL Certificates',
            'content': 'Look for the padlock icon and "https://" in the address bar for secure connections.',
            'category': 'url',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Beware of URL Shorteners',
            'content': 'Be cautious with shortened URLs that hide the actual destination website.',
            'category': 'url',
            'priority': 2,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Check Domain Spelling',
            'content': 'Look for misspelled domain names that mimic legitimate websites (typosquatting).',
            'category': 'url',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        },
        
        # General Tips
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Enable Two-Factor Authentication',
            'content': 'Use 2FA on all important accounts to add an extra layer of security.',
            'category': 'general',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Keep Software Updated',
            'content': 'Regularly update your browser, operating system, and security software.',
            'category': 'general',
            'priority': 2,
            'created_at': datetime.utcnow().isoformat()
        },
        {
            'id': f'tip_{uuid.uuid4().hex[:8]}',
            'title': 'Use Strong Passwords',
            'content': 'Create unique, complex passwords and use a password manager to store them securely.',
            'category': 'general',
            'priority': 1,
            'created_at': datetime.utcnow().isoformat()
        }
    ]
    
    # Insert safety tips
    for tip in safety_tips:
        existing = db_manager.find_one('security_tips', {'id': tip['id']})
        if not existing:
            db_manager.insert_one('security_tips', tip)
            print(f"Created tip: {tip['category']} - {tip['title']}")

def main():
    """Main function to populate admin dashboard data"""
    print("Populating Admin Dashboard with sample data...")
    
    # Initialize database
    db_manager.init_connection()
    
    # Create sample data
    populate_detection_data()
    populate_safety_tips()
    
    print("\nAdmin Dashboard data populated successfully!")
    print("You can now see:")
    print("- User management with scan statistics")
    print("- Recent phishing scan logs")
    print("- Safety tips organized by category")
    print("- Live analytics and system statistics")

if __name__ == "__main__":
    main()