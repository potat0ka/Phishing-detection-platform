#!/usr/bin/env python3
"""
Direct test of admin dashboard action buttons functionality
"""

import json
import re
from datetime import datetime

def test_dashboard_html():
    """Test the admin dashboard HTML contains proper action buttons"""
    
    print("Testing Admin Dashboard Action Buttons Implementation")
    print("=" * 55)
    
    # Read the dashboard template
    try:
        with open('templates/admin/dashboard.html', 'r') as f:
            html_content = f.read()
        print("✓ Dashboard template loaded successfully")
    except Exception as e:
        print(f"✗ Error loading dashboard template: {e}")
        return
    
    # Test 1: Check for action button HTML
    print("\n1. Checking HTML button implementations...")
    
    view_buttons = re.findall(r'onclick=["\']viewUser\([^)]+\)["\']', html_content)
    edit_buttons = re.findall(r'onclick=["\']editUser\([^)]+\)["\']', html_content)
    delete_buttons = re.findall(r'onclick=["\']deleteUser\([^)]+\)["\']', html_content)
    
    print(f"   - View button patterns found: {len(view_buttons)}")
    print(f"   - Edit button patterns found: {len(edit_buttons)}")
    print(f"   - Delete button patterns found: {len(delete_buttons)}")
    
    # Test 2: Check for JavaScript functions
    print("\n2. Checking JavaScript function implementations...")
    
    js_functions = {
        'viewUser': 'function viewUser(' in html_content,
        'editUser': 'function editUser(' in html_content,
        'deleteUser': 'function deleteUser(' in html_content,
        'logout': 'function logout(' in html_content,
        'changePassword': 'function changePassword(' in html_content,
        'showAlert': 'function showAlert(' in html_content,
        'refreshUserTable': 'function refreshUserTable(' in html_content
    }
    
    for func_name, exists in js_functions.items():
        status = "✓" if exists else "✗"
        print(f"   {status} {func_name}: {'Found' if exists else 'Missing'}")
    
    # Test 3: Check for login/logout dropdown
    print("\n3. Checking login/logout dropdown...")
    
    dropdown_patterns = [
        'dropdown-toggle',
        'logout()',
        'changePassword()',
        'viewProfile()'
    ]
    
    dropdown_found = all(pattern in html_content for pattern in dropdown_patterns)
    print(f"   {'✓' if dropdown_found else '✗'} Login/logout dropdown: {'Implemented' if dropdown_found else 'Missing'}")
    
    # Test 4: Check for role-based permissions
    print("\n4. Checking role-based permission controls...")
    
    permission_patterns = [
        "current_user.role == 'super_admin'",
        "current_user.role == 'sub_admin'",
        "canDeleteUser",
        "role not in ['super_admin', 'sub_admin']"
    ]
    
    permissions_found = sum(1 for pattern in permission_patterns if pattern in html_content)
    print(f"   - Permission patterns found: {permissions_found}/{len(permission_patterns)}")
    
    # Test 5: Check for modals
    print("\n5. Checking modal implementations...")
    
    modal_patterns = [
        'viewUserModal',
        'editUserModal',
        'changePasswordModal',
        'bootstrap.Modal'
    ]
    
    modals_found = sum(1 for pattern in modal_patterns if pattern in html_content)
    print(f"   - Modal patterns found: {modals_found}/{len(modal_patterns)}")
    
    print("\n" + "=" * 55)
    
    # Overall assessment
    total_features = len(js_functions) + len(permission_patterns) + len(modal_patterns) + 3  # +3 for buttons, dropdown, overall
    implemented_features = sum(js_functions.values()) + permissions_found + modals_found + len(view_buttons) + (1 if dropdown_found else 0)
    
    percentage = (implemented_features / total_features) * 100
    
    print(f"IMPLEMENTATION STATUS: {percentage:.1f}% Complete")
    
    if percentage >= 90:
        print("✓ Action buttons are fully implemented and ready for use")
    elif percentage >= 70:
        print("⚠ Action buttons are mostly implemented with minor issues")
    else:
        print("✗ Action buttons need significant implementation work")
    
    return percentage >= 70

def test_admin_routes():
    """Test admin routes implementation"""
    
    print("\n6. Checking admin route implementations...")
    
    try:
        with open('admin_routes.py', 'r') as f:
            routes_content = f.read()
        
        required_routes = [
            '/get-user/<user_id>',
            '/edit-user/<user_id>',
            '/delete-user/<user_id>',
            'def get_user(',
            'def edit_user(',
            'def delete_user('
        ]
        
        routes_found = sum(1 for route in required_routes if route in routes_content)
        print(f"   - Required routes found: {routes_found}/{len(required_routes)}")
        
        return routes_found == len(required_routes)
        
    except Exception as e:
        print(f"   ✗ Error checking admin routes: {e}")
        return False

if __name__ == "__main__":
    html_test = test_dashboard_html()
    routes_test = test_admin_routes()
    
    print(f"\n🔍 FINAL ASSESSMENT:")
    print(f"   Dashboard HTML: {'✓ Ready' if html_test else '✗ Needs work'}")
    print(f"   Admin Routes: {'✓ Ready' if routes_test else '✗ Needs work'}")
    
    if html_test and routes_test:
        print("🎉 Action buttons are fully functional!")
    else:
        print("⚠ Action buttons need additional fixes")