#!/usr/bin/env python3
"""
Script to help install ffmpeg on Windows for audio combining functionality
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path

def check_ffmpeg_installed():
    """Check if ffmpeg is already installed and accessible"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ ffmpeg is already installed and accessible!")
            print(f"Version: {result.stdout.split('ffmpeg version')[1].split()[0]}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        pass
    
    print("❌ ffmpeg is not installed or not in PATH")
    return False

def download_ffmpeg():
    """Download ffmpeg for Windows"""
    print("\n📥 Downloading ffmpeg for Windows...")
    
    # FFmpeg download URL (latest release)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    try:
        # Create temp directory
        temp_dir = Path("temp_ffmpeg")
        temp_dir.mkdir(exist_ok=True)
        
        zip_path = temp_dir / "ffmpeg.zip"
        
        print(f"   Downloading from: {ffmpeg_url}")
        print("   This may take a few minutes...")
        
        # Download the file
        urllib.request.urlretrieve(ffmpeg_url, zip_path)
        
        print("   ✅ Download completed!")
        return zip_path
        
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
        return None

def extract_ffmpeg(zip_path):
    """Extract ffmpeg from zip file"""
    print("\n📦 Extracting ffmpeg...")
    
    try:
        temp_dir = Path("temp_ffmpeg")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        print("   ✅ Extraction completed!")
        
        # Find the extracted directory
        extracted_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
        if extracted_dirs:
            return extracted_dirs[0]
        else:
            print("   ❌ Could not find extracted directory")
            return None
            
    except Exception as e:
        print(f"   ❌ Extraction failed: {e}")
        return None

def install_ffmpeg(extracted_dir):
    """Install ffmpeg to a permanent location"""
    print("\n🔧 Installing ffmpeg...")
    
    try:
        # Create installation directory
        install_dir = Path("ffmpeg")
        install_dir.mkdir(exist_ok=True)
        
        # Find ffmpeg.exe in the extracted directory
        ffmpeg_exe = None
        for root, dirs, files in os.walk(extracted_dir):
            if "ffmpeg.exe" in files:
                ffmpeg_exe = Path(root) / "ffmpeg.exe"
                break
        
        if not ffmpeg_exe:
            print("   ❌ Could not find ffmpeg.exe in extracted files")
            return False
        
        # Copy ffmpeg.exe to installation directory
        target_path = install_dir / "ffmpeg.exe"
        shutil.copy2(ffmpeg_exe, target_path)
        
        print(f"   ✅ ffmpeg installed to: {target_path.absolute()}")
        
        # Add to PATH for current session
        current_path = os.environ.get('PATH', '')
        if str(install_dir.absolute()) not in current_path:
            os.environ['PATH'] = f"{install_dir.absolute()};{current_path}"
            print("   ✅ Added to PATH for current session")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Installation failed: {e}")
        return False

def cleanup_temp_files():
    """Clean up temporary files"""
    print("\n🧹 Cleaning up temporary files...")
    
    try:
        temp_dir = Path("temp_ffmpeg")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("   ✅ Temporary files cleaned up")
    except Exception as e:
        print(f"   ⚠️ Could not clean up temporary files: {e}")

def test_ffmpeg_installation():
    """Test if ffmpeg installation works"""
    print("\n🧪 Testing ffmpeg installation...")
    
    try:
        # Try to run ffmpeg
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ ffmpeg is working correctly!")
            return True
        else:
            print("   ❌ ffmpeg is not working correctly")
            return False
            
    except Exception as e:
        print(f"   ❌ ffmpeg test failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🎬 FFmpeg Installation for Windows")
    print("=" * 50)
    
    # Check if already installed
    if check_ffmpeg_installed():
        return
    
    print("\n📋 FFmpeg is required for audio combining functionality.")
    print("This script will download and install ffmpeg for you.")
    
    # Ask for confirmation
    response = input("\nDo you want to install ffmpeg? (y/n): ").lower().strip()
    if response != 'y':
        print("Installation cancelled.")
        return
    
    try:
        # Download ffmpeg
        zip_path = download_ffmpeg()
        if not zip_path:
            print("❌ Download failed. Please install ffmpeg manually.")
            return
        
        # Extract ffmpeg
        extracted_dir = extract_ffmpeg(zip_path)
        if not extracted_dir:
            print("❌ Extraction failed. Please install ffmpeg manually.")
            return
        
        # Install ffmpeg
        if not install_ffmpeg(extracted_dir):
            print("❌ Installation failed. Please install ffmpeg manually.")
            return
        
        # Test installation
        if not test_ffmpeg_installation():
            print("❌ Installation test failed. Please install ffmpeg manually.")
            return
        
        # Cleanup
        cleanup_temp_files()
        
        print("\n🎉 FFmpeg installation completed successfully!")
        print("You can now use the audio combining functionality.")
        
    except KeyboardInterrupt:
        print("\n⚠️ Installation interrupted by user.")
        cleanup_temp_files()
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        cleanup_temp_files()

if __name__ == "__main__":
    main()
