#!/usr/bin/env python3
"""
Test script to verify audio combining fix works with fallback methods
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

def test_ffmpeg_availability():
    """Test if ffmpeg is available"""
    print("🔍 Testing ffmpeg availability...")
    
    # Try system ffmpeg first
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ ffmpeg is available in PATH")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    
    # Try local ffmpeg installation
    try:
        result = subprocess.run(['./ffmpeg/ffmpeg.exe', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ Local ffmpeg installation is available")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        pass
    
    print("   ❌ ffmpeg is not available")
    return False

def test_pydub_availability():
    """Test if pydub is available"""
    print("🔍 Testing pydub availability...")
    
    try:
        from pydub import AudioSegment
        print("   ✅ pydub is available")
        return True
    except ImportError:
        print("   ❌ pydub is not installed")
        return False

def create_test_audio_files():
    """Create test audio files for combining"""
    print("🎵 Creating test audio files...")
    
    test_files = []
    
    try:
        # Create a temporary directory
        temp_dir = Path("test_audio")
        temp_dir.mkdir(exist_ok=True)
        
        # Create simple test audio files using ffmpeg (if available)
        if test_ffmpeg_availability():
            for i in range(3):
                filename = temp_dir / f"test_audio_{i}.wav"
                # Generate a simple sine wave using local ffmpeg
                cmd = [
                    './ffmpeg/ffmpeg.exe', '-f', 'lavfi', '-i', 
                    f'sine=frequency=440:duration=2', 
                    '-y', str(filename)
                ]
                subprocess.run(cmd, capture_output=True, check=True)
                test_files.append(str(filename))
                print(f"   Created: {filename}")
        else:
            # Create dummy files if ffmpeg is not available
            for i in range(3):
                filename = temp_dir / f"test_audio_{i}.wav"
                # Create a minimal WAV file header
                with open(filename, 'wb') as f:
                    # WAV file header (44 bytes)
                    f.write(b'RIFF')
                    f.write((36).to_bytes(4, 'little'))  # File size
                    f.write(b'WAVE')
                    f.write(b'fmt ')
                    f.write((16).to_bytes(4, 'little'))  # Chunk size
                    f.write((1).to_bytes(2, 'little'))   # Audio format (PCM)
                    f.write((1).to_bytes(2, 'little'))   # Channels
                    f.write((44100).to_bytes(4, 'little'))  # Sample rate
                    f.write((88200).to_bytes(4, 'little'))  # Byte rate
                    f.write((2).to_bytes(2, 'little'))   # Block align
                    f.write((16).to_bytes(2, 'little'))  # Bits per sample
                    f.write(b'data')
                    f.write((0).to_bytes(4, 'little'))   # Data size
                
                test_files.append(str(filename))
                print(f"   Created dummy: {filename}")
        
        return test_files
        
    except Exception as e:
        print(f"   ❌ Failed to create test files: {e}")
        return []

def test_audio_combining():
    """Test the audio combining functionality"""
    print("\n🧪 Testing audio combining functionality...")
    
    # Create test files
    test_files = create_test_audio_files()
    if not test_files:
        print("❌ Could not create test files")
        return False
    
    try:
        # Import the combine function
        sys.path.append('.')
        from app import combine_audio_files
        
        # Test combining
        output_file = "test_combined.mp3"
        success = combine_audio_files(test_files, output_file)
        
        if success and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"   ✅ Audio combining successful!")
            print(f"   📁 Output file: {output_file}")
            print(f"   📊 File size: {file_size} bytes")
            
            # Clean up
            os.remove(output_file)
            return True
        else:
            print("   ❌ Audio combining failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False
    finally:
        # Clean up test files
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
        
        # Clean up test directory
        test_dir = Path("test_audio")
        if test_dir.exists():
            shutil.rmtree(test_dir)

def main():
    """Main test function"""
    print("🎵 Audio Combining Fix Test")
    print("=" * 40)
    
    # Test availability
    ffmpeg_available = test_ffmpeg_availability()
    pydub_available = test_pydub_availability()
    
    print(f"\n📋 Availability Summary:")
    print(f"   ffmpeg: {'✅ Available' if ffmpeg_available else '❌ Not available'}")
    print(f"   pydub: {'✅ Available' if pydub_available else '❌ Not available'}")
    
    if not ffmpeg_available and not pydub_available:
        print("\n❌ Neither ffmpeg nor pydub is available!")
        print("Please install at least one of them:")
        print("   - ffmpeg: Run 'python install_ffmpeg_windows.py'")
        print("   - pydub: Run 'pip install pydub'")
        return
    
    # Test combining
    success = test_audio_combining()
    
    if success:
        print("\n🎉 Audio combining fix is working!")
        print("The system will now automatically combine audio files.")
    else:
        print("\n❌ Audio combining test failed.")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
