#!/usr/bin/env python3
"""
Super Admin Password Reset Utility
Resets the super admin password to the documented default value
"""

import json
import os
from werkzeug.security import generate_password_hash

def reset_super_admin_password():
    """Reset super admin password to documented default"""
    users_file = 'data/users.json'
    
    if not os.path.exists(users_file):
        print("❌ Users file not found!")
        return False
    
    try:
        # Load existing users
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        # Find super admin user
        super_admin = None
        for user in users:
            if user.get('username') == 'super_admin':
                super_admin = user
                break
        
        if not super_admin:
            print("❌ Super admin user not found!")
            return False
        
        # Generate new password hash for documented password
        new_password = "SuperAdmin123!"
        new_hash = generate_password_hash(new_password)
        
        # Update password hash
        super_admin['password_hash'] = new_hash
        super_admin['login_attempts'] = 0
        super_admin['locked_until'] = None
        
        # Save updated users
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        print("✅ Super admin password reset successfully!")
        print(f"Username: super_admin")
        print(f"Password: {new_password}")
        print("\n⚠️  Please change this password after logging in!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Super Admin Password Reset Utility")
    print("=" * 40)
    reset_super_admin_password()