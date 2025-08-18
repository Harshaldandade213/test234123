#!/usr/bin/env python3
"""
Test script for the new podcast API endpoints
"""
import requests
import time
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_podcast_generate():
    """Test the /podcast/generate endpoint"""
    print("🧪 Testing /podcast/generate endpoint")
    print("=" * 50)
    
    # Test data
    query = "What are the benefits of artificial intelligence in healthcare?"
    
    try:
        # Make the request
        response = requests.post(
            f"{BASE_URL}/podcast/generate",
            data={"query": query}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Status: {result.get('status')}")
            print(f"Message: {result.get('message')}")
            print(f"Filename: {result.get('filename')}")
            print(f"Download URL: {result.get('download_url')}")
            
            # Test the download URL
            download_response = requests.get(f"{BASE_URL}{result.get('download_url')}")
            if download_response.status_code == 200:
                print("✅ Download URL works!")
                print(f"Audio file size: {len(download_response.content)} bytes")
            else:
                print(f"❌ Download URL failed: {download_response.status_code}")
            
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_podcast_download():
    """Test the /podcast/download endpoint"""
    print("\n🧪 Testing /podcast/download endpoint")
    print("=" * 50)
    
    # Test data
    query = "What are the latest discoveries on Mars?"
    
    try:
        # Make the request
        response = requests.get(
            f"{BASE_URL}/podcast/download",
            params={"query": query}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Content-Length: {response.headers.get('content-length')}")
            print(f"Filename: {response.headers.get('content-disposition', '').split('filename=')[-1] if 'filename=' in response.headers.get('content-disposition', '') else 'Not specified'}")
            
            # Save the file
            filename = f"test_download_podcast_{int(time.time())}.mp3"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Audio file saved as: {filename}")
            print(f"File size: {len(response.content)} bytes")
            
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test if the server is running"""
    print("🏥 Testing server health")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print(f"❌ Server responded with: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Server not reachable: {e}")
        return False

if __name__ == "__main__":
    print("🎙️ Podcast API Testing Suite")
    print("=" * 60)
    
    # Check if server is running
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first:")
        print("   cd adobev4")
        print("   python main.py")
        exit(1)
    
    # Test the endpoints
    success_count = 0
    total_tests = 2
    
    if test_podcast_generate():
        success_count += 1
    
    if test_podcast_download():
        success_count += 1
    
    # Summary
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Podcast API is working correctly.")
    else:
        print("❌ Some tests failed. Check the server logs for details.")

