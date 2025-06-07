#!/usr/bin/env python3
"""
Test script to verify admin dashboard action buttons functionality
"""

import requests
import json
from bs4 import BeautifulSoup

def test_admin_dashboard_buttons():
    """Test the admin dashboard action buttons functionality"""
    
    base_url = "http://localhost:8080"
    session = requests.Session()
    
    print("🔍 Testing Admin Dashboard Action Buttons")
    print("=" * 50)
    
    # Step 1: Login as super admin
    print("1. Logging in as super admin...")
    login_data = {
        'username': 'super_admin',
        'password': 'super123'  # Try common admin passwords
    }
    
    # Try different password combinations
    passwords = ['super123', 'admin123', 'password', 'superadmin', 'admin']
    login_success = False
    
    for password in passwords:
        login_data['password'] = password
        login_response = session.post(f"{base_url}/auth/login", data=login_data)
        
        if login_response.status_code == 200 and "Invalid username or password" not in login_response.text:
            print(f"✓ Login successful with password: {password}")
            login_success = True
            break
        else:
            print(f"✗ Login failed with password: {password}")
    
    if not login_success:
        print("❌ Could not login - testing with direct access")
        # Test endpoints directly
        test_endpoints_directly(base_url, session)
        return
    
    # Step 2: Access admin dashboard
    print("\n2. Accessing admin dashboard...")
    dashboard_response = session.get(f"{base_url}/admin/dashboard")
    
    if dashboard_response.status_code != 200:
        print(f"❌ Dashboard access failed: {dashboard_response.status_code}")
        return
    
    # Step 3: Parse HTML and check for action buttons
    print("\n3. Analyzing dashboard HTML...")
    soup = BeautifulSoup(dashboard_response.text, 'html.parser')
    
    # Check for JavaScript functions
    view_buttons = soup.find_all('button', onclick=lambda x: x and 'viewUser' in x)
    edit_buttons = soup.find_all('button', onclick=lambda x: x and 'editUser' in x)
    delete_buttons = soup.find_all('button', onclick=lambda x: x and 'deleteUser' in x)
    
    print(f"   - View buttons found: {len(view_buttons)}")
    print(f"   - Edit buttons found: {len(edit_buttons)}")
    print(f"   - Delete buttons found: {len(delete_buttons)}")
    
    # Check for JavaScript functions in script tags
    script_tags = soup.find_all('script')
    js_functions = []
    
    for script in script_tags:
        if script.string:
            if 'function viewUser' in script.string:
                js_functions.append('viewUser')
            if 'function editUser' in script.string:
                js_functions.append('editUser')
            if 'function deleteUser' in script.string:
                js_functions.append('deleteUser')
            if 'function logout' in script.string:
                js_functions.append('logout')
            if 'function changePassword' in script.string:
                js_functions.append('changePassword')
    
    print(f"\n4. JavaScript functions found: {js_functions}")
    
    # Check for login/logout dropdown
    dropdown_toggle = soup.find('button', class_='dropdown-toggle')
    if dropdown_toggle:
        print("✓ Login/logout dropdown found in header")
    else:
        print("✗ Login/logout dropdown not found")
    
    # Step 4: Test API endpoints
    print("\n5. Testing API endpoints...")
    test_endpoints_directly(base_url, session)

def test_endpoints_directly(base_url, session):
    """Test the admin API endpoints directly"""
    
    # Test get-user endpoint
    print("   Testing /admin/get-user endpoint...")
    try:
        # Try to get user data
        user_response = session.get(f"{base_url}/admin/get-user/super_admin_001")
        print(f"   - GET /admin/get-user: {user_response.status_code}")
        
        if user_response.status_code == 200:
            try:
                user_data = user_response.json()
                if user_data.get('success'):
                    print("   ✓ User data endpoint working")
                else:
                    print(f"   ✗ User data error: {user_data.get('message', 'Unknown error')}")
            except:
                print("   ✗ Invalid JSON response")
    except Exception as e:
        print(f"   ✗ Endpoint test failed: {e}")
    
    # Test edit-user endpoint
    print("   Testing /admin/edit-user endpoint...")
    try:
        edit_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'role': 'user'
        }
        edit_response = session.post(f"{base_url}/admin/edit-user/test_id", 
                                   json=edit_data,
                                   headers={'Content-Type': 'application/json'})
        print(f"   - POST /admin/edit-user: {edit_response.status_code}")
    except Exception as e:
        print(f"   ✗ Edit endpoint test failed: {e}")

if __name__ == "__main__":
    test_admin_dashboard_buttons()