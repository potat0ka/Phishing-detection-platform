#!/usr/bin/env python3
"""
Test Role-Based Dashboard Integration
Verifies admin users see integrated admin features while regular users see standard dashboard
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

def ensure_demo_users():
    """Ensure demo admin and user accounts exist with proper roles"""
    print("Ensuring demo accounts exist...")
    
    # Initialize database
    db_manager.init_connection()
    
    # Check for admin user
    admin_user = None
    all_users = db_manager.find_many('users')
    
    for user_data in all_users:
        # Check non-encrypted data first
        if user_data.get('username') == 'demo_admin':
            admin_user = user_data
            break
        # Check encrypted data
        try:
            from encryption_utils import decrypt_sensitive_data
            decrypted = decrypt_sensitive_data('user', user_data)
            if decrypted.get('username') == 'demo_admin':
                admin_user = user_data
                break
        except:
            continue
    
    if not admin_user:
        print("Creating demo admin user...")
        admin_data = {
            'id': f'user_admin_{uuid.uuid4().hex[:8]}',
            'username': 'demo_admin',
            'email': 'admin@phishingdetector.com',
            'password_hash': 'pbkdf2:sha256:260000$abc123$def456',  # admin123
            'role': 'admin',
            'active': True,
            'created_at': datetime.utcnow().isoformat(),
            'scan_count': 25
        }
        db_manager.insert_one('users', admin_data)
        print("Demo admin created")
    else:
        print("Demo admin exists")
    
    # Check for regular user
    user_user = None
    for user_data in all_users:
        # Check non-encrypted data first
        if user_data.get('username') == 'demo_user':
            user_user = user_data
            break
        # Check encrypted data
        try:
            decrypted = decrypt_sensitive_data('user', user_data)
            if decrypted.get('username') == 'demo_user':
                user_user = user_data
                break
        except:
            continue
    
    if not user_user:
        print("Creating demo regular user...")
        user_data = {
            'id': f'user_regular_{uuid.uuid4().hex[:8]}',
            'username': 'demo_user',
            'email': 'user@phishingdetector.com',
            'password_hash': 'pbkdf2:sha256:260000$abc123$def456',  # user123
            'role': 'user',
            'active': True,
            'created_at': datetime.utcnow().isoformat(),
            'scan_count': 8
        }
        db_manager.insert_one('users', user_data)
        print("Demo user created")
    else:
        print("Demo user exists")

def test_admin_dashboard():
    """Test admin dashboard access with role-based features"""
    print("\nTesting admin dashboard functionality...")
    
    session = requests.Session()
    
    # Login as admin
    login_data = {'username': 'demo_admin', 'password': 'admin123'}
    response = session.post('http://localhost:5000/auth/login', data=login_data)
    print(f"Admin login status: {response.status_code}")
    
    # Access dashboard
    response = session.get('http://localhost:5000/dashboard')
    print(f"Admin dashboard access: {response.status_code}")
    
    if response.status_code == 200:
        content = response.text
        admin_features = [
            'Admin Panel',
            'User Management', 
            'Scan Logs',
            'Safety Tips',
            'Analytics',
            'Total Users',
            'Total Scans'
        ]
        
        found_features = []
        for feature in admin_features:
            if feature in content:
                found_features.append(feature)
        
        print(f"Admin features found: {len(found_features)}/{len(admin_features)}")
        for feature in found_features:
            print(f"  ✓ {feature}")
        
        return len(found_features) >= 5  # At least 5 admin features should be present
    
    return False

def test_user_dashboard():
    """Test regular user dashboard access with standard features"""
    print("\nTesting user dashboard functionality...")
    
    session = requests.Session()
    
    # Login as user
    login_data = {'username': 'demo_user', 'password': 'user123'}
    response = session.post('http://localhost:5000/auth/login', data=login_data)
    print(f"User login status: {response.status_code}")
    
    # Access dashboard
    response = session.get('http://localhost:5000/dashboard')
    print(f"User dashboard access: {response.status_code}")
    
    if response.status_code == 200:
        content = response.text
        
        # User should NOT see admin features
        admin_features = ['User Management', 'Reported Content', 'Safety Tips Management']
        admin_features_found = sum(1 for feature in admin_features if feature in content)
        
        # User should see standard features
        user_features = ['Welcome back', 'Total Checks', 'Phishing Detected', 'Recent Activity']
        user_features_found = sum(1 for feature in user_features if feature in content)
        
        print(f"Admin features found (should be 0): {admin_features_found}")
        print(f"User features found: {user_features_found}/{len(user_features)}")
        
        return admin_features_found == 0 and user_features_found >= 2
    
    return False

def main():
    """Main test function"""
    print("Testing Role-Based Dashboard Integration")
    print("=" * 50)
    
    ensure_demo_users()
    
    admin_test = test_admin_dashboard()
    user_test = test_user_dashboard()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Admin Dashboard: {'✓ PASS' if admin_test else '✗ FAIL'}")
    print(f"User Dashboard:  {'✓ PASS' if user_test else '✗ FAIL'}")
    
    if admin_test and user_test:
        print("\n🎉 Role-based dashboard integration successful!")
        print("- Admins see integrated admin features")
        print("- Users see standard dashboard only")
        print("- No separate admin panel navigation needed")
    else:
        print("\n⚠️  Some tests failed - check implementation")

if __name__ == "__main__":
    main()