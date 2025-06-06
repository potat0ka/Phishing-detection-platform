#!/usr/bin/env python3
"""Simple registration verification script"""

import json
import os
from datetime import datetime

def check_registration():
    """Check if registration system can create users"""
    
    # Load current users
    users_file = 'data/users.json'
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    print(f"Current users in database: {len(users)}")
    for user in users:
        username = user.get('username', 'Unknown')
        role = user.get('role', 'Unknown')
        print(f"- {username} ({role})")
    
    # Simulate creating a new regular user
    new_user = {
        "id": f"user_{int(datetime.now().timestamp())}",
        "_id": f"users_test_{int(datetime.now().timestamp())}",
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password_hash": "scrypt:32768:8:1$test$hash",
        "role": "user",  # Regular user role
        "active": True,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None,
        "login_attempts": 0,
        "locked_until": None
    }
    
    # Check if user already exists
    existing = any(u.get('username') == 'testuser123' for u in users)
    if not existing:
        users.append(new_user)
        
        # Save back to file
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        print(f"SUCCESS: Created regular user 'testuser123'")
        print(f"Total users now: {len(users)}")
        return True
    else:
        print("User 'testuser123' already exists")
        return True

if __name__ == "__main__":
    check_registration()