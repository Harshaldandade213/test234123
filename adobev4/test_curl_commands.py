#!/usr/bin/env python3
"""
Test script for podcast endpoints with proper URL encoding
"""
import requests
import urllib.parse
import time

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
                
                # Save the file
                filename = f"generated_podcast_{int(time.time())}.mp3"
                with open(filename, 'wb') as f:
                    f.write(download_response.content)
                print(f"✅ Saved as: {filename}")
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
        # Make the request with proper URL encoding
        encoded_query = urllib.parse.quote(query)
        url = f"{BASE_URL}/podcast/download?query={encoded_query}"
        
        print(f"Requesting: {url}")
        
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Success!")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Content-Length: {response.headers.get('content-length')}")
            
            # Extract filename from content-disposition header
            content_disposition = response.headers.get('content-disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[-1].strip('"')
                print(f"Filename: {filename}")
            
            # Save the file
            filename = f"download_podcast_{int(time.time())}.mp3"
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

def print_curl_commands():
    """Print properly encoded curl commands"""
    print("\n🔧 Properly Encoded cURL Commands")
    print("=" * 50)
    
    # Test queries
    queries = [
        "What are the benefits of artificial intelligence in healthcare?",
        "What are the latest discoveries on Mars?",
        "How does machine learning work?"
    ]
    
    for query in queries:
        encoded_query = urllib.parse.quote(query)
        print(f"\nQuery: {query}")
        print(f"Encoded: {encoded_query}")
        print(f"Generate command:")
        print(f'curl -X POST -F "query={query}" http://127.0.0.1:8000/podcast/generate')
        print(f"Download command:")
        print(f'curl -o "podcast_{int(time.time())}.mp3" "http://127.0.0.1:8000/podcast/download?query={encoded_query}"')
        print("-" * 40)

if __name__ == "__main__":
    print("🎙️ Podcast API Testing with Proper URL Encoding")
    print("=" * 60)
    
    # Print curl commands first
    print_curl_commands()
    
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

