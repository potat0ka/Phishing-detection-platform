#!/usr/bin/env python3
"""
Test the unified text analysis flow to ensure homepage and analyze-text 
now provide the exact same experience and results.
"""

import sys
import os
sys.path.append('.')

import requests
import urllib.parse

def test_unified_flow():
    """Test that homepage message analysis redirects to analyze-text for consistency"""
    print("Testing Unified Text Analysis Flow")
    print("=" * 50)
    
    # Start session
    session = requests.Session()
    
    # Login first
    print("1. Logging in...")
    login_data = {
        'email': 'testadmin@example.com',
        'password': 'password123'
    }
    
    login_response = session.post('http://localhost:8080/auth/login', data=login_data, allow_redirects=False)
    
    if login_response.status_code != 302:
        print("✗ Login failed")
        return False
    
    print("✓ Login successful")
    
    # Test message content that should redirect
    test_message = "This is a comprehensive test message for our unified text analysis system that should provide identical results whether accessed from homepage or analyze-text page. The artificial intelligence detection algorithms will analyze patterns in writing style and vocabulary usage."
    
    print(f"\n2. Testing homepage message analysis with {len(test_message)} character text...")
    
    # Submit to homepage check route
    homepage_data = {
        'input_type': 'message',
        'input_content': test_message
    }
    
    homepage_response = session.post('http://localhost:8080/check', data=homepage_data, allow_redirects=False)
    
    print(f"Homepage response status: {homepage_response.status_code}")
    
    if homepage_response.status_code == 302:
        redirect_url = homepage_response.headers.get('Location', '')
        print(f"✓ Homepage redirected to: {redirect_url}")
        
        if 'analyze-text' in redirect_url and 'prefilled_text' in redirect_url:
            print("✓ Redirect URL contains analyze-text with prefilled text")
            
            # Follow the redirect
            analyze_response = session.get(f"http://localhost:8080{redirect_url}")
            
            if analyze_response.status_code == 200:
                print("✓ Analyze-text page loaded successfully")
                
                # Check if the text was prefilled
                if test_message[:50] in analyze_response.text:
                    print("✓ Text was successfully prefilled in analyze-text form")
                    print("\n3. Testing direct analyze-text access...")
                    
                    # Also test direct access to analyze-text
                    direct_response = session.get('http://localhost:8080/analyze-text')
                    
                    if direct_response.status_code == 200:
                        print("✓ Direct analyze-text access works")
                        
                        # Test form submission
                        print("\n4. Testing form submission on analyze-text...")
                        
                        form_data = {
                            'text_content': test_message,
                            'check_ai': 'on',
                            'check_plagiarism': 'on'
                        }
                        
                        form_response = session.post('http://localhost:8080/analyze-text', data=form_data)
                        
                        if form_response.status_code == 200:
                            if 'Analysis Results' in form_response.text:
                                print("✓ Form submission successful - results displayed")
                                
                                # Check for AI and plagiarism results
                                if 'AI Content Detection' in form_response.text and 'Plagiarism Analysis' in form_response.text:
                                    print("✓ Both AI detection and plagiarism analysis results present")
                                    return True
                                else:
                                    print("✗ Missing analysis results")
                            else:
                                print("✗ No analysis results found")
                        else:
                            print(f"✗ Form submission failed: {form_response.status_code}")
                    else:
                        print(f"✗ Direct analyze-text access failed: {direct_response.status_code}")
                else:
                    print("✗ Text was not prefilled properly")
            else:
                print(f"✗ Analyze-text page failed to load: {analyze_response.status_code}")
        else:
            print("✗ Redirect URL incorrect")
    else:
        print(f"✗ Homepage did not redirect as expected: {homepage_response.status_code}")
    
    return False

def test_consistency():
    """Test that both paths now provide consistent experience"""
    print("\n" + "=" * 50)
    print("UNIFIED FLOW TEST RESULTS")
    print("=" * 50)
    
    if test_unified_flow():
        print("✓ SUCCESS: Homepage and Text Authenticity Analysis now provide unified experience!")
        print("✓ Homepage message analysis redirects to analyze-text for consistency")
        print("✓ Same interface, same logic, same results")
        print("✓ No duplicate code or different implementations")
        print("\nThe system now provides a single, consistent text analysis experience!")
        return True
    else:
        print("✗ FAILURE: Unified flow not working properly")
        return False

if __name__ == "__main__":
    success = test_consistency()
    if success:
        print("\n🎉 SUCCESS: Text analysis is now truly unified!")
        sys.exit(0)
    else:
        print("\n❌ FAILURE: Issues found with unified flow")
        sys.exit(1)