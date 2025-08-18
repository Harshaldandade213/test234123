#!/usr/bin/env python3
"""
Test script for podcast generation from query
"""

import requests
import json

def test_podcast_generate():
    """Test the /podcast/generate endpoint"""
    
    # Test with the exact curl command format
    url = "http://127.0.0.1:8000/podcast/generate"
    
    # Test data
    test_queries = [
        "Alien",
        "Space exploration",
        "Technology trends",
        "Artificial intelligence"
    ]
    
    print("🎙️ Testing Podcast Generation Endpoint")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Testing query: '{query}'")
        
        try:
            # Create form data (equivalent to curl -F)
            form_data = {
                'query': query
            }
            
            # Make the request
            response = requests.post(url, data=form_data)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success!")
                print(f"   📁 Filename: {result.get('filename', 'N/A')}")
                print(f"   🔗 Download URL: {result.get('download_url', 'N/A')}")
                print(f"   💬 Message: {result.get('message', 'N/A')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   📄 Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error: Make sure the server is running on http://127.0.0.1:8000")
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎙️ Test completed!")

if __name__ == "__main__":
    test_podcast_generate()
