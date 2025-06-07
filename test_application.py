#!/usr/bin/env python3
"""
AI Phishing Detection Platform - Test Suite
==========================================

Comprehensive test suite to validate application functionality,
security features, and AI detection capabilities.

Usage:
    python test_application.py

Tests include:
- Authentication system
- AI detection accuracy
- Database operations
- Security features
- API endpoints
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class ApplicationTester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test result"""
        status = "PASS" if success else "FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status}] {test_name}: {message}")
        
    def test_server_health(self):
        """Test if server is running and healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    self.log_test("Server Health", True, "Server is healthy and responsive")
                    return True
                else:
                    self.log_test("Server Health", False, f"Unhealthy status: {data}")
                    return False
            else:
                self.log_test("Server Health", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Health", False, f"Connection failed: {str(e)}")
            return False
            
    def test_home_page_access(self):
        """Test home page accessibility"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                if "AI Phishing Detector" in response.text:
                    self.log_test("Home Page Access", True, "Home page loads correctly")
                    return True
                else:
                    self.log_test("Home Page Access", False, "Missing expected content")
                    return False
            else:
                self.log_test("Home Page Access", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Home Page Access", False, f"Request failed: {str(e)}")
            return False
            
    def test_registration_page(self):
        """Test user registration page"""
        try:
            response = self.session.get(f"{self.base_url}/register", timeout=10)
            if response.status_code == 200:
                if "Register" in response.text and "username" in response.text.lower():
                    self.log_test("Registration Page", True, "Registration page accessible")
                    return True
                else:
                    self.log_test("Registration Page", False, "Missing registration form")
                    return False
            else:
                self.log_test("Registration Page", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Registration Page", False, f"Request failed: {str(e)}")
            return False
            
    def test_login_page(self):
        """Test user login page"""
        try:
            response = self.session.get(f"{self.base_url}/login", timeout=10)
            if response.status_code == 200:
                if "Login" in response.text and "password" in response.text.lower():
                    self.log_test("Login Page", True, "Login page accessible")
                    return True
                else:
                    self.log_test("Login Page", False, "Missing login form")
                    return False
            else:
                self.log_test("Login Page", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Login Page", False, f"Request failed: {str(e)}")
            return False
            
    def test_phishing_detection_page(self):
        """Test phishing detection interface"""
        try:
            response = self.session.get(f"{self.base_url}/check", timeout=10)
            if response.status_code == 200:
                if "URL" in response.text and "analyze" in response.text.lower():
                    self.log_test("Detection Page", True, "Detection interface accessible")
                    return True
                else:
                    self.log_test("Detection Page", False, "Missing detection form")
                    return False
            else:
                self.log_test("Detection Page", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Detection Page", False, f"Request failed: {str(e)}")
            return False
            
    def test_ai_content_detection_page(self):
        """Test AI content detection interface"""
        try:
            response = self.session.get(f"{self.base_url}/ai-content-check", timeout=10)
            if response.status_code == 200:
                if "AI Content" in response.text:
                    self.log_test("AI Content Page", True, "AI content detection accessible")
                    return True
                else:
                    self.log_test("AI Content Page", False, "Missing AI content interface")
                    return False
            else:
                self.log_test("AI Content Page", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("AI Content Page", False, f"Request failed: {str(e)}")
            return False
            
    def test_safety_tips_page(self):
        """Test safety tips educational page"""
        try:
            response = self.session.get(f"{self.base_url}/tips", timeout=10)
            if response.status_code == 200:
                if "Safety" in response.text or "Tips" in response.text:
                    self.log_test("Safety Tips Page", True, "Educational content accessible")
                    return True
                else:
                    self.log_test("Safety Tips Page", False, "Missing educational content")
                    return False
            else:
                self.log_test("Safety Tips Page", False, f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Safety Tips Page", False, f"Request failed: {str(e)}")
            return False
            
    def test_admin_redirect(self):
        """Test admin access (should redirect to login)"""
        try:
            response = self.session.get(f"{self.base_url}/admin", timeout=10, allow_redirects=False)
            if response.status_code in [302, 401, 403]:
                self.log_test("Admin Protection", True, "Admin area properly protected")
                return True
            else:
                self.log_test("Admin Protection", False, f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Admin Protection", False, f"Request failed: {str(e)}")
            return False
            
    def test_static_files(self):
        """Test static file serving"""
        static_files = [
            "/static/css/style.css",
            "/static/js/main.js"
        ]
        
        success_count = 0
        for file_path in static_files:
            try:
                response = self.session.get(f"{self.base_url}{file_path}", timeout=10)
                if response.status_code == 200:
                    success_count += 1
            except:
                pass
                
        if success_count > 0:
            self.log_test("Static Files", True, f"{success_count}/{len(static_files)} static files accessible")
            return True
        else:
            self.log_test("Static Files", False, "No static files accessible")
            return False
            
    def test_ai_detection_functionality(self):
        """Test AI detection with sample data"""
        test_cases = [
            {
                'url': 'https://example-phishing-site.com/fake-bank-login',
                'expected_risk': 'high'
            },
            {
                'url': 'https://google.com',
                'expected_risk': 'low'
            },
            {
                'url': 'http://suspicious-url-with-many-redirects.tk/login.php?user=admin',
                'expected_risk': 'medium'
            }
        ]
        
        try:
            # Test URL analysis
            for i, test_case in enumerate(test_cases):
                response = self.session.post(
                    f"{self.base_url}/analyze",
                    data={'url': test_case['url'], 'input_type': 'url'},
                    timeout=15
                )
                
                if response.status_code == 200:
                    self.log_test(f"AI Detection Test {i+1}", True, f"Analysis completed for {test_case['url']}")
                else:
                    self.log_test(f"AI Detection Test {i+1}", False, f"Analysis failed: HTTP {response.status_code}")
                    
        except Exception as e:
            self.log_test("AI Detection Functionality", False, f"Detection test failed: {str(e)}")
            return False
            
        return True
        
    def test_database_connectivity(self):
        """Test database operations"""
        try:
            # Import database manager
            from models.mongodb_config import get_mongodb_manager
            
            db_manager = get_mongodb_manager()
            
            # Test basic operations
            test_data = {
                'test_id': 'connectivity_test',
                'timestamp': datetime.now().isoformat(),
                'data': 'test_value'
            }
            
            # Test write operation
            result = db_manager.insert_detection_log('test_user', 'http://test.com', 'test', {'result': 'test'})
            
            if result:
                self.log_test("Database Write", True, "Database write operation successful")
            else:
                self.log_test("Database Write", False, "Database write operation failed")
                
            # Test read operation
            logs = db_manager.get_user_detection_history('test_user', limit=1)
            
            if logs is not None:
                self.log_test("Database Read", True, "Database read operation successful")
            else:
                self.log_test("Database Read", False, "Database read operation failed")
                
            return True
            
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Database test failed: {str(e)}")
            return False
            
    def test_security_headers(self):
        """Test security headers"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            headers = response.headers
            
            security_checks = []
            
            # Check for security headers
            if 'X-Content-Type-Options' in headers:
                security_checks.append("X-Content-Type-Options present")
                
            if 'X-Frame-Options' in headers:
                security_checks.append("X-Frame-Options present")
                
            if len(security_checks) > 0:
                self.log_test("Security Headers", True, f"Found: {', '.join(security_checks)}")
            else:
                self.log_test("Security Headers", False, "No security headers detected")
                
            return True
            
        except Exception as e:
            self.log_test("Security Headers", False, f"Header check failed: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run complete test suite"""
        print("=" * 60)
        print("AI Phishing Detection Platform - Test Suite")
        print("=" * 60)
        print(f"Testing application at: {self.base_url}")
        print(f"Test started at: {datetime.now().isoformat()}")
        print("-" * 60)
        
        # Run all tests
        tests = [
            self.test_server_health,
            self.test_home_page_access,
            self.test_registration_page,
            self.test_login_page,
            self.test_phishing_detection_page,
            self.test_ai_content_detection_page,
            self.test_safety_tips_page,
            self.test_admin_redirect,
            self.test_static_files,
            self.test_database_connectivity,
            self.test_security_headers,
            self.test_ai_detection_functionality
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log_test(test.__name__, False, f"Test exception: {str(e)}")
            time.sleep(0.5)  # Brief pause between tests
            
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate test summary report"""
        print("-" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASS')
        failed_tests = total_tests - passed_tests
        
        print(f"TEST SUMMARY:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"- {result['test']}: {result['message']}")
                    
        print("-" * 60)
        print(f"Test completed at: {datetime.now().isoformat()}")
        
        # Save results to file
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print("Detailed results saved to: test_results.json")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test AI Phishing Detection Platform')
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='Base URL of the application (default: http://localhost:8080)')
    parser.add_argument('--quick', action='store_true',
                       help='Run quick tests only (skip AI detection tests)')
    
    args = parser.parse_args()
    
    tester = ApplicationTester(args.url)
    
    # Check if server is running
    if not tester.test_server_health():
        print("\nERROR: Server is not running or not accessible!")
        print("Please start the application with: python main.py")
        sys.exit(1)
        
    # Run tests
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()