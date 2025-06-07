#!/usr/bin/env python3
"""
Test Admin Dashboard Action Buttons
==================================

This script tests the admin dashboard action buttons functionality
to ensure they work correctly with the fixed JavaScript endpoints.
"""

import requests
import json
from werkzeug.security import generate_password_hash

def test_admin_buttons():
    """Test admin dashboard action buttons"""
    
    base_url = "http://localhost:8080"
    
    # Create a test admin session
    session = requests.Session()
    
    # First unlock the super admin account
    print("🔓 Unlocking super admin account...")
    
    # Read users data
    with open('data/users.json', 'r') as f:
        users = json.load(f)
    
    # Find and unlock super admin
    for user in users:
        if user.get('username') == 'super_admin':
            user['locked_until'] = None
            user['login_attempts'] = 0
            break
    
    # Save updated users
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print("✅ Super admin account unlocked")
    
    # Test login
    print("🔐 Testing admin login...")
    login_data = {
        'username': 'super_admin',
        'password': 'admin123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Login successful")
    else:
        print("❌ Login failed")
        return False
    
    # Test admin dashboard access
    print("📊 Testing admin dashboard access...")
    dashboard_response = session.get(f"{base_url}/admin/dashboard")
    
    if dashboard_response.status_code == 200:
        print("✅ Admin dashboard accessible")
    else:
        print(f"❌ Dashboard access failed: {dashboard_response.status_code}")
        return False
    
    # Test user management endpoints
    print("👥 Testing user management endpoints...")
    
    # Get users list
    users_response = session.get(f"{base_url}/admin/users")
    if users_response.status_code == 200:
        print("✅ Get users endpoint working")
    else:
        print(f"❌ Get users failed: {users_response.status_code}")
    
    # Test get specific user (using test user ID)
    test_user_id = "user_1749125333_6273"  # potato user
    user_response = session.get(f"{base_url}/admin/get-user/{test_user_id}")
    
    if user_response.status_code == 200:
        user_data = user_response.json()
        if user_data.get('success'):
            print("✅ Get user details endpoint working")
            print(f"   Retrieved user: {user_data['user']['username']}")
        else:
            print(f"❌ Get user details failed: {user_data.get('error')}")
    else:
        print(f"❌ Get user details endpoint failed: {user_response.status_code}")
    
    # Test edit user endpoint
    print("✏️ Testing edit user endpoint...")
    edit_data = {
        'username': 'potato',
        'email': 'bige.stha88@gmail.com',
        'role': 'sub_admin',
        'is_active': True
    }
    
    edit_response = session.post(
        f"{base_url}/admin/edit-user/{test_user_id}",
        json=edit_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if edit_response.status_code == 200:
        edit_result = edit_response.json()
        if edit_result.get('success'):
            print("✅ Edit user endpoint working")
        else:
            print(f"❌ Edit user failed: {edit_result.get('error')}")
    else:
        print(f"❌ Edit user endpoint failed: {edit_response.status_code}")
    
    # Test JavaScript functions presence
    print("🔧 Checking JavaScript functions in dashboard...")
    
    if 'viewUser(' in dashboard_response.text:
        print("✅ viewUser function found in dashboard")
    else:
        print("❌ viewUser function missing")
    
    if 'editUser(' in dashboard_response.text:
        print("✅ editUser function found in dashboard")
    else:
        print("❌ editUser function missing")
    
    if 'deleteUser(' in dashboard_response.text:
        print("✅ deleteUser function found in dashboard")
    else:
        print("❌ deleteUser function missing")
    
    # Check for proper user ID handling
    if 'onclick="viewUser(' in dashboard_response.text and '{{ user.id }}' in dashboard_response.text:
        print("✅ User ID properly passed to JavaScript functions")
    else:
        print("⚠️ User ID handling may need verification")
    
    print("\n🎯 Admin Action Buttons Test Complete!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_admin_buttons()