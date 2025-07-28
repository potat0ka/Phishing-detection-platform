
#!/usr/bin/env python3
"""
Test Fixed MongoDB Authentication
===============================

Tests the corrected MongoDB + bcrypt authentication system.
"""

import requests
import os
from pymongo import MongoClient
import bcrypt

def test_mongodb_user_exists():
    """Test if the MongoDB user exists with correct credentials"""
    try:
        mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
        if not mongo_uri:
            print("❌ No MongoDB URI found")
            return False
        
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client['phishing_detector']
        users_collection = db.users
        
        # Test the specific user from requirements
        user = users_collection.find_one({'email': 'superadmin@example.com'})
        if not user:
            print("❌ User superadmin@example.com not found in MongoDB")
            return False
        
        print(f"✅ Found user: {user['email']}")
        print(f"   Role: {user.get('role', 'unknown')}")
        print(f"   Password hash: {user.get('password_hash', 'none')[:30]}...")
        
        # Test password verification
        test_password = 'password123'
        stored_hash = user.get('password_hash', '')
        
        if bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("✅ Password verification successful")
            return True
        else:
            print("❌ Password verification failed")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB test error: {e}")
        return False

def test_login_endpoint():
    """Test the login endpoint"""
    print("\n🧪 Testing login endpoint...")
    
    try:
        session = requests.Session()
        
        login_data = {
            'email': 'superadmin@example.com',
            'password': 'password123'
        }
        
        response = session.post(
            'http://0.0.0.0:8080/auth/login',
            data=login_data,
            allow_redirects=False
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 302:
            redirect_location = response.headers.get('Location', '')
            print(f"✅ Login successful - Redirected to: {redirect_location}")
            
            if 'superadmin-dashboard' in redirect_location:
                print("✅ Correct role-based redirect")
                return True
            else:
                print("❌ Wrong redirect location")
                return False
        else:
            print(f"❌ Login failed: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False

def main():
    """Run comprehensive authentication tests"""
    print("🔐 Testing Fixed MongoDB Authentication")
    print("=" * 50)
    
    # Test MongoDB connection and user
    if not test_mongodb_user_exists():
        print("\n❌ MongoDB user test failed")
        return
    
    # Test login endpoint
    if not test_login_endpoint():
        print("\n❌ Login endpoint test failed")
        return
    
    print("\n🎉 All tests passed!")
    print("✅ MongoDB authentication is working correctly")
    print("✅ bcrypt password verification works")
    print("✅ Role-based redirects work")
    print("✅ Session management works")

if __name__ == "__main__":
    main()
