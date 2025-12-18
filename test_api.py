#!/usr/bin/env python3
"""
Test script for Document Verification API
Usage: python test_api.py <base_url>
Example: python test_api.py https://your-app.vercel.app
"""

import sys
import requests
import json

def test_health_check(base_url):
    """Test the health check endpoint"""
    print("\n🔍 Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_home_page(base_url):
    """Test the home page loads"""
    print("\n🔍 Testing Home Page...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200 and "DOCUMENT VERIFICATION" in response.text:
            print("✅ Home page loads correctly")
            return True
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False

def test_aadhar_page(base_url):
    """Test the Aadhar page loads"""
    print("\n🔍 Testing Aadhar Page...")
    try:
        response = requests.get(f"{base_url}/aadhar")
        if response.status_code == 200 and "AADHAR" in response.text.upper():
            print("✅ Aadhar page loads correctly")
            return True
        else:
            print(f"❌ Aadhar page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Aadhar page error: {e}")
        return False

def test_pan_page(base_url):
    """Test the PAN page loads"""
    print("\n🔍 Testing PAN Page...")
    try:
        response = requests.get(f"{base_url}/pan")
        if response.status_code == 200 and "PAN" in response.text.upper():
            print("✅ PAN page loads correctly")
            return True
        else:
            print(f"❌ PAN page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PAN page error: {e}")
        return False

def test_aadhar_number_validation(base_url):
    """Test Aadhar number validation"""
    print("\n🔍 Testing Aadhar Number Validation...")
    try:
        # Test valid Aadhar number
        valid_number = "234567891234"
        response = requests.post(
            f"{base_url}/aadharVerification",
            data={"number": valid_number}
        )
        if response.status_code == 200:
            print(f"✅ Aadhar number validation endpoint works")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ Aadhar validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Aadhar validation error: {e}")
        return False

def test_pan_number_validation(base_url):
    """Test PAN number validation"""
    print("\n🔍 Testing PAN Number Validation...")
    try:
        # Test valid PAN number
        valid_pan = "ABCDE1234F"
        response = requests.post(
            f"{base_url}/panVerification",
            data={"number": valid_pan}
        )
        if response.status_code == 200:
            print(f"✅ PAN number validation endpoint works")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ PAN validation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PAN validation error: {e}")
        return False

def test_static_files(base_url):
    """Test if static files are accessible"""
    print("\n🔍 Testing Static Files...")
    static_files = [
        "/static/css/aadhar.css",
        "/static/js/aadhar.js",
    ]
    
    all_passed = True
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}")
            if response.status_code == 200:
                print(f"✅ {file_path} is accessible")
            else:
                print(f"⚠️  {file_path} returned {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ Error accessing {file_path}: {e}")
            all_passed = False
    
    return all_passed

def run_all_tests(base_url):
    """Run all tests and provide summary"""
    print("=" * 60)
    print(f"🚀 Testing Document Verification API")
    print(f"📍 Base URL: {base_url}")
    print("=" * 60)
    
    results = {
        "Health Check": test_health_check(base_url),
        "Home Page": test_home_page(base_url),
        "Aadhar Page": test_aadhar_page(base_url),
        "PAN Page": test_pan_page(base_url),
        "Aadhar Number Validation": test_aadhar_number_validation(base_url),
        "PAN Number Validation": test_pan_number_validation(base_url),
        "Static Files": test_static_files(base_url),
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\n📝 Notes:")
    print("- Image upload tests require actual image files")
    print("- OCR functionality requires Google Cloud Vision API credentials")
    print("- Resize and reduce size endpoints need to be tested manually with images")
    
    return passed == total

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_api.py <base_url>")
        print("Example: python test_api.py https://your-app.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    success = run_all_tests(base_url)
    sys.exit(0 if success else 1)
