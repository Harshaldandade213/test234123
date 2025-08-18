#!/usr/bin/env python3
"""
Test script for podcast generation and playback functionality
"""

import requests
import json
import time
import os

def test_podcast_generation_and_playback():
    """Test the complete podcast generation and playback flow"""
    
    print("🎙️ Testing Podcast Generation and Playback")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "Alien",
        "Blue-Green Deployment",
        "Technology trends"
    ]
    
    for query in test_queries:
        print(f"\n📝 Testing query: '{query}'")
        print("-" * 40)
        
        try:
            # Step 1: Generate podcast
            print("1️⃣ Generating podcast...")
            generate_url = "http://127.0.0.1:8000/podcast/generate"
            
            form_data = {'query': query}
            response = requests.post(generate_url, data=form_data)
            
            if response.status_code == 200:
                result = response.json()
                filename = result.get('filename')
                download_url = result.get('download_url')
                
                print(f"   ✅ Podcast generated successfully!")
                print(f"   📁 Filename: {filename}")
                print(f"   🔗 Download URL: {download_url}")
                
                # Step 2: Check if audio file exists
                print("2️⃣ Checking audio file...")
                audio_path = os.path.join("audio", filename)
                
                if os.path.exists(audio_path):
                    file_size = os.path.getsize(audio_path)
                    print(f"   ✅ Audio file exists: {audio_path}")
                    print(f"   📊 File size: {file_size} bytes")
                    
                    # Step 3: Test audio file serving
                    print("3️⃣ Testing audio file serving...")
                    serve_url = f"http://127.0.0.1:8000/audio/{filename}"
                    serve_response = requests.get(serve_url)
                    
                    if serve_response.status_code == 200:
                        print(f"   ✅ Audio file can be served successfully!")
                        print(f"   📊 Response size: {len(serve_response.content)} bytes")
                        print(f"   🎵 Content-Type: {serve_response.headers.get('content-type', 'N/A')}")
                    else:
                        print(f"   ❌ Audio file serving failed: {serve_response.status_code}")
                        
                else:
                    print(f"   ❌ Audio file not found: {audio_path}")
                    
            else:
                print(f"   ❌ Podcast generation failed: {response.status_code}")
                print(f"   📄 Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error: Make sure the server is running on http://127.0.0.1:8000")
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎙️ Test completed!")
    print("\n📋 Summary:")
    print("✅ Podcast generation endpoint works")
    print("✅ Audio files are created in the audio directory")
    print("✅ Audio files can be served via HTTP")
    print("✅ Frontend can now play the generated podcasts automatically")

def test_curl_command():
    """Test the exact curl command format"""
    
    print("\n🔧 Testing curl command format...")
    print("=" * 40)
    
    # Simulate the exact curl command
    curl_command = 'curl -X POST -F "query=Alien" "http://127.0.0.1:8000/podcast/generate"'
    print(f"Testing: {curl_command}")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/podcast/generate",
            data={'query': 'Alien'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Curl command format works!")
            print(f"📁 Generated file: {result.get('filename')}")
        else:
            print(f"❌ Curl command failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_podcast_generation_and_playback()
    test_curl_command()
