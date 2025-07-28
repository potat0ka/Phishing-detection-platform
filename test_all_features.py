
#!/usr/bin/env python3
"""
Comprehensive Feature Test
=========================

Tests all major features after authentication fixes.
"""

import requests
import json

def test_homepage():
    """Test if homepage loads"""
    try:
        response = requests.get('http://0.0.0.0:8080/')
        if response.status_code == 200:
            print("✅ Homepage loads correctly")
            return True
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Homepage error: {e}")
        return False

def test_safety_tips():
    """Test safety tips page"""
    try:
        response = requests.get('http://0.0.0.0:8080/tips')
        if response.status_code == 200:
            print("✅ Safety tips page loads correctly")
            return True
        else:
            print(f"❌ Safety tips failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Safety tips error: {e}")
        return False

def test_url_scan():
    """Test URL scanning functionality"""
    try:
        response = requests.get('http://0.0.0.0:8080/check')
        if response.status_code == 200:
            print("✅ URL scan page loads correctly")
            return True
        else:
            print(f"❌ URL scan failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ URL scan error: {e}")
        return False

def test_authenticated_dashboard():
    """Test dashboard access after login"""
    try:
        session = requests.Session()
        
        # Login first
        login_data = {
            'email': 'superadmin@example.com',
            'password': 'password123'
        }
        
        login_response = session.post(
            'http://0.0.0.0:8080/auth/login',
            data=login_data,
            allow_redirects=True
        )
        
        if 'superadmin-dashboard' in login_response.url:
            print("✅ Dashboard access after login works")
            return True
        else:
            print(f"❌ Dashboard access failed")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard test error: {e}")
        return False

def main():
    """Run all feature tests"""
    print("🧪 Comprehensive Feature Validation")
    print("=" * 40)
    
    tests = [
        ("Homepage", test_homepage),
        ("Safety Tips", test_safety_tips),
        ("URL Scanner", test_url_scan),
        ("Authenticated Dashboard", test_authenticated_dashboard)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All features working correctly!")
    else:
        print("⚠️ Some features need attention")

if __name__ == "__main__":
    main()
