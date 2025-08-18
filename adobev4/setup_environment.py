#!/usr/bin/env python3
"""
Environment setup script for adobev4
Helps install dependencies and guide through API key setup
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Dependencies")
    print("=" * 40)
    
    # Core dependencies
    dependencies = [
        "fastapi",
        "uvicorn",
        "python-multipart",
        "python-dotenv",
        "requests",
        "pydantic"
    ]
    
    # AI/ML dependencies
    ai_dependencies = [
        "google-generativeai",
        "sentence-transformers",
        "scikit-learn",
        "faiss-cpu"
    ]
    
    # Document processing
    doc_dependencies = [
        "PyPDF2",
        "python-docx",
        "python-pptx"
    ]
    
    all_deps = dependencies + ai_dependencies + doc_dependencies
    
    for dep in all_deps:
        if not run_command(f"pip install {dep}", f"Installing {dep}"):
            print(f"⚠️  Failed to install {dep}, but continuing...")
    
    return True

def check_api_key():
    """Check if Google API key is configured"""
    print("\n🔑 Checking API Key Configuration")
    print("=" * 40)
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
        return True
    else:
        print("❌ GOOGLE_API_KEY not set")
        print("\n📖 To get an API key:")
        print("   1. Visit: https://makersuite.google.com/app/apikey")
        print("   2. Sign in with your Google account")
        print("   3. Click 'Create API Key'")
        print("   4. Copy the key (starts with 'AIza...')")
        print("\n🔧 To set the environment variable:")
        print("   Windows (PowerShell): $env:GOOGLE_API_KEY='your_key_here'")
        print("   Windows (CMD): set GOOGLE_API_KEY=your_key_here")
        print("   Linux/Mac: export GOOGLE_API_KEY='your_key_here'")
        print("\n📄 See GOOGLE_API_SETUP.md for detailed instructions")
        return False

def create_env_file():
    """Create .env file template"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"\n📝 Creating {env_file} template...")
        with open(env_file, 'w') as f:
            f.write("# Environment Variables\n")
            f.write("# Replace 'your_api_key_here' with your actual Google API key\n")
            f.write("GOOGLE_API_KEY=your_api_key_here\n")
        print(f"✅ Created {env_file} template")
        print("📝 Edit this file and add your actual API key")
    else:
        print(f"✅ {env_file} already exists")

def main():
    """Main setup function"""
    print("🚀 adobev4 Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Some dependencies failed to install")
    
    # Create .env file
    create_env_file()
    
    # Check API key
    api_key_configured = check_api_key()
    
    print("\n" + "=" * 50)
    if api_key_configured:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Test API key: python test_api_key.py")
        print("   2. Start backend: python main.py")
        print("   3. Run tests: python run_all_tests.py")
    else:
        print("⚠️  Setup completed, but API key needs to be configured")
        print("\n📋 Next steps:")
        print("   1. Get Google API key (see instructions above)")
        print("   2. Set environment variable or edit .env file")
        print("   3. Test API key: python test_api_key.py")
        print("   4. Start backend: python main.py")
    
    print("\n📚 Documentation:")
    print("   - GOOGLE_API_SETUP.md - Detailed API key setup")
    print("   - TESTING_GUIDE.md - How to run tests")
    print("   - ENHANCED_RELATED_SECTIONS.md - Feature documentation")
    
    return True

if __name__ == "__main__":
    main()
