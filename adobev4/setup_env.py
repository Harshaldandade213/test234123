#!/usr/bin/env python3
"""
Environment setup script for Adobe+ Document Analysis & Podcast Generation API
"""

import os
import sys

def create_env_file():
    """Create .env file with required environment variables"""
    
    env_content = """# Adobe+ Document Analysis & Podcast Generation API Environment Variables

# Gemini API Configuration
GEMINI_API_KEY=AIzaSyB3RHGywLeBmdN485INVuoZNgRtV-1LbrI

# Azure Speech Services (for TTS)
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_REGION=your_azure_region_here

# AWS Configuration (alternative TTS)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=your_aws_region_here

# TTS Provider (azure, aws, or local)
TTS_PROVIDER=azure

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Development Settings
DEVELOPMENT_MODE=True
VERBOSE_LOGGING=True
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 Please update the Azure Speech Services and AWS credentials as needed.")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'python-multipart',
        'requests',
        'google-generativeai',
        'sentence-transformers',
        'faiss-cpu',
        'numpy',
        'scikit-learn',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("📦 Install them with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("\n✅ All required packages are installed!")
        return True

def check_directories():
    """Check and create required directories"""
    
    required_dirs = [
        'documents',
        'index', 
        'audio',
        'uploads'
    ]
    
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Created directory: {dir_name}")
        else:
            print(f"✅ Directory exists: {dir_name}")

def main():
    """Main setup function"""
    
    print("🚀 Adobe+ Document Analysis & Podcast Generation API Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Create .env file
    print("\n📝 Setting up environment variables...")
    if not create_env_file():
        return False
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n⚠️ Some dependencies are missing. Please install them before proceeding.")
        return False
    
    # Check directories
    print("\n📁 Checking directories...")
    check_directories()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update Azure Speech Services credentials in .env file")
    print("2. Run: python run_server.py")
    print("3. Access the API at: http://localhost:8000")
    print("4. View documentation at: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
