#!/usr/bin/env python3
"""
Simple script to test Google API key configuration
"""
import os
import sys

def test_api_key():
    print("🔑 Testing Google API Key Configuration")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY environment variable not set")
        print("\n📝 To set it:")
        print("   Windows (PowerShell): $env:GOOGLE_API_KEY='your_key_here'")
        print("   Windows (CMD): set GOOGLE_API_KEY=your_key_here")
        print("   Linux/Mac: export GOOGLE_API_KEY='your_key_here'")
        print("\n📖 See GOOGLE_API_SETUP.md for detailed instructions")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Try to import and test the API
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package installed")
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("📦 Install with: pip install google-generativeai")
        return False
    
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        # Test with a simple request
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, this is a test message.")
        
        print("✅ API key is working correctly!")
        print(f"📝 Test response: {response.text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        print("\n🔧 Common solutions:")
        print("   1. Check if the API key is valid")
        print("   2. Ensure Gemini API is enabled in Google Cloud Console")
        print("   3. Check your internet connection")
        print("   4. Verify API key restrictions (if any)")
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n🎉 API key is ready! You can now:")
        print("   1. Start the backend: python main.py")
        print("   2. Run tests: python run_all_tests.py")
        print("   3. Test enhanced features")
    else:
        print("\n⚠️  Please fix the issues above before proceeding")
        sys.exit(1)
