#!/usr/bin/env python3
"""
Comprehensive server startup script for HARSHALADOBE Backend
This script ensures all dependencies are available and starts the server properly.
"""

import os
import sys
import subprocess
import time
import requests
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'google.generativeai',
        'python-dotenv',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-dotenv':
                __import__('dotenv')
            else:
                __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies available")
    return True

def check_environment():
    """Check environment configuration."""
    print("\n🔍 Checking environment...")
    
    # Load environment variables
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:10]}...")
    else:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    return True

def test_gemini_api():
    """Test Gemini API connection."""
    print("\n🧪 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Say 'API working' in one word.")
        if response.text:
            print(f"✅ Gemini API working: {response.text}")
            return True
        else:
            print("❌ No response from API")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def start_server():
    """Start the FastAPI server."""
    print("\n🚀 Starting server...")
    
    try:
        # Start the server using subprocess
        process = subprocess.Popen([
            sys.executable, 'start.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            response = requests.get('http://localhost:8000/docs', timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully!")
                print("📖 API docs available at: http://localhost:8000/docs")
                print("🎙️ Podcast endpoint: http://localhost:8000/podcast/generate")
                return process
            else:
                print(f"⚠️ Server responded with status: {response.status_code}")
                return process
        except requests.exceptions.RequestException:
            print("⚠️ Server may still be starting up...")
            return process
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_podcast_endpoint():
    """Test the podcast generation endpoint."""
    print("\n🎙️ Testing podcast endpoint...")
    
    try:
        response = requests.post(
            'http://localhost:8000/podcast/generate',
            data={'query': 'test query'},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Podcast endpoint working!")
            print(f"   Status: {result.get('status', 'N/A')}")
            print(f"   Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Podcast endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Podcast endpoint test failed: {e}")
        return False

def main():
    """Main startup function."""
    print("🚀 HARSHALADOBE Backend Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        return
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please check your .env file.")
        return
    
    # Test Gemini API
    if not test_gemini_api():
        print("\n❌ Gemini API test failed. Please check your API key.")
        return
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("\n❌ Failed to start server.")
        return
    
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Open your browser to http://localhost:3000 (frontend)")
    print("2. Test the podcast generation feature")
    print("3. Check API docs at http://localhost:8000/docs")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        if server_process:
            server_process.terminate()

if __name__ == "__main__":
    main()
