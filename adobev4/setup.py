#!/usr/bin/env python3
"""
Setup script for the Semantic Search Document System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["documents", "index"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}/")

def main():
    print("🚀 Setting up Semantic Search Document System...")
    print()
    
    # Create directories
    create_directories()
    print()
    
    # Install requirements
    if install_requirements():
        print()
        print("🎉 Setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Add your PDF, DOCX, or TXT files to the 'documents/' folder")
        print("2. Run: python app.py add")
        print("3. Search your documents: python app.py search \"your query\"")
        print()
        print("For more information, see README.md")
    else:
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
