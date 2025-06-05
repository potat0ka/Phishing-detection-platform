#!/usr/bin/env python3
"""
Create Admin Session for Testing
Creates proper authentication session for admin dashboard access
"""

import sys
import os
from datetime import datetime
import uuid
import requests

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mongodb_config import db_manager
from encryption_utils import encrypt_sensitive_data

def create_admin_session():
    """Create admin session for testing dashboard"""
    print("Creating admin session...")
    
    # Initialize database
    db_manager.init_connection()
    
    # Check if admin user exists
    admin_user = db_manager.find_one('users', {'username': 'demo_admin'})
    
    if not admin_user:
        print("Admin user not found, creating...")
        # Create admin user
        admin_data = {
            'id': f'user_{uuid.uuid4().hex[:8]}',
            'username': 'demo_admin',
            'email': 'admin@phishingdetector.com',
            'role': 'admin',
            'active': True,
            'created_at': datetime.utcnow().isoformat(),
            'scan_count': 15
        }
        
        # Encrypt sensitive data
        try:
            encrypted_admin = encrypt_sensitive_data('user', admin_data)
            db_manager.insert_one('users', encrypted_admin)
        except:
            db_manager.insert_one('users', admin_data)
        
        print("Admin user created successfully")
    else:
        print("Admin user already exists")
    
    # Create session via HTTP request
    session = requests.Session()
    
    # First get the login page to establish session
    response = session.get('http://localhost:5000/auth/login')
    print(f"Login page status: {response.status_code}")
    
    # Attempt login
    login_data = {
        'username': 'demo_admin',
        'password': 'admin123'
    }
    
    response = session.post('http://localhost:5000/auth/login', data=login_data)
    print(f"Login attempt status: {response.status_code}")
    
    # Save cookies for testing
    with open('admin_session_cookies.txt', 'w') as f:
        for cookie in session.cookies:
            f.write(f"{cookie.name}={cookie.value}; ")
    
    print("Admin session created and saved to admin_session_cookies.txt")
    
    # Test admin dashboard access
    response = session.get('http://localhost:5000/admin/dashboard')
    print(f"Admin dashboard access status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Admin dashboard accessible")
        
        # Check for key elements
        content = response.text
        if 'Admin Panel' in content:
            print("✓ Admin panel header found")
        if 'User Management' in content:
            print("✓ User management section found")
        if 'Scan Logs' in content:
            print("✓ Scan logs section found")
        if 'Safety Tips' in content:
            print("✓ Safety tips section found")
        if 'Analytics' in content:
            print("✓ Analytics section found")
            
    return session

if __name__ == "__main__":
    create_admin_session()