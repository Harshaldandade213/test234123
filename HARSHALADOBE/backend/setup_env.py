#!/usr/bin/env python3
"""
Environment Setup Script for HARSHALADOBE Backend
This script helps you set up the required environment variables.
"""

import os
import sys

def create_env_file():
    """Create a .env file with the required environment variables."""
    
    env_content = """# Gemini API Configuration
GEMINI_API_KEY=AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c

# Azure Speech Services (optional - for TTS)
# AZURE_SPEECH_KEY=your_azure_speech_key_here
# AZURE_SPEECH_REGION=your_azure_region_here

# Other optional configurations
# DATABASE_URL=your_database_url_here
# LOG_LEVEL=INFO
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    try:
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created .env file at: {env_file_path}")
        print("📝 Environment variables configured:")
        print("   - GEMINI_API_KEY: AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_environment():
    """Check if environment variables are properly set."""
    print("🔍 Checking environment configuration...")
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"✅ GEMINI_API_KEY is set: {gemini_key[:10]}...")
    else:
        print("❌ GEMINI_API_KEY is not set")
    
    # Check if .env file exists
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file_path):
        print(f"✅ .env file exists at: {env_file_path}")
    else:
        print("❌ .env file not found")
    
    return gemini_key is not None

def main():
    """Main setup function."""
    print("🚀 HARSHALADOBE Backend Environment Setup")
    print("=" * 50)
    
    # Check current environment
    if check_environment():
        print("\n✅ Environment is already configured!")
        return
    
    print("\n📝 Setting up environment variables...")
    
    # Create .env file
    if create_env_file():
        print("\n✅ Environment setup completed!")
        print("\n📋 Next steps:")
        print("1. Restart your backend server")
        print("2. Test the podcast generation feature")
        print("3. Check the logs for any API errors")
    else:
        print("\n❌ Environment setup failed!")
        print("\n🔧 Manual setup:")
        print("1. Create a .env file in the backend directory")
        print("2. Add: GEMINI_API_KEY=AIzaSyAInqw9seke43AUqjjPA8ftJcJVggRKA6c")
        print("3. Restart your backend server")

if __name__ == "__main__":
    main()
