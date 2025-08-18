#!/usr/bin/env python3
"""
Simple test script to test the podcast endpoint
"""

import requests

def test_podcast_endpoint():
    """Test the podcast generation endpoint"""
    
    print("🧪 Testing podcast endpoint...")
    
    try:
        # Test the endpoint
        response = requests.post(
            "http://127.0.0.1:8000/podcast/generate",
            data={"query": "Test query"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Filename: {result.get('filename')}")
        else:
            print(f"❌ Failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_podcast_endpoint()
