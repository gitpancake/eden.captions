#!/usr/bin/env python3
"""
Debug script to test Captions API endpoints and understand the correct format.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("CAPTIONS_API_KEY")
BASE_URL = "https://api.captions.ai"

def test_api_endpoint(endpoint, method="GET", data=None, headers=None):
    """Test an API endpoint and print the response."""
    url = f"{BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    
    print(f"\n🔍 Testing {method} {url}")
    print(f"Headers: {headers}")
    if data:
        print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code < 400:
            try:
                print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"Response Text: {response.text}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

def main():
    """Test various API endpoints."""
    print("🎬 Captions API Debug Tool")
    print("=" * 50)
    
    if not API_KEY:
        print("❌ No API key found. Please set CAPTIONS_API_KEY environment variable.")
        return
    
    print(f"✅ Using API key: {API_KEY[:10]}...")
    
    # Test 1: API key in query parameter
    print("\n1️⃣ Testing with API key in query parameter...")
    url_with_key = f"{BASE_URL}/api/ads/submit?api_key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"url": "https://www.apple.com/iphone-15/"}
    
    try:
        response = requests.post(url_with_key, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")
    
    # Test 2: API key in X-API-Key header
    print("\n2️⃣ Testing with X-API-Key header...")
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    test_api_endpoint("/api/ads/submit", "POST", {"url": "https://www.apple.com/iphone-15/"}, headers)
    
    # Test 3: API key in Authorization header without Bearer
    print("\n3️⃣ Testing with Authorization header (no Bearer)...")
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    test_api_endpoint("/api/ads/submit", "POST", {"url": "https://www.apple.com/iphone-15/"}, headers)
    
    # Test 4: API key in X-Auth-Token header
    print("\n4️⃣ Testing with X-Auth-Token header...")
    headers = {
        "X-Auth-Token": API_KEY,
        "Content-Type": "application/json"
    }
    test_api_endpoint("/api/ads/submit", "POST", {"url": "https://www.apple.com/iphone-15/"}, headers)
    
    # Test 5: No Content-Type header
    print("\n5️⃣ Testing without Content-Type header...")
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    test_api_endpoint("/api/ads/submit", "POST", {"url": "https://www.apple.com/iphone-15/"}, headers)
    
    # Test 6: Different content type
    print("\n6️⃣ Testing with application/x-www-form-urlencoded...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "url=https://www.apple.com/iphone-15/"
    try:
        response = requests.post(f"{BASE_URL}/api/ads/submit", headers=headers, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    main() 