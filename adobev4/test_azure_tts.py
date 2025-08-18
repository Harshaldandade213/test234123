#!/usr/bin/env python3
"""
Test script for Azure TTS functionality
"""
import os
import sys

# Add the current directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Azure TTS function from app.py
from app import generate_podcast_audio_azure

def test_azure_tts():
    print("🧪 Testing Azure TTS Integration")
    print("=" * 50)
    
    # Test script with dialogue
    test_script = """Alex: Welcome to our podcast about artificial intelligence in healthcare.
Dr. Sharma: Thank you for having me, Alex. AI is revolutionizing how we approach patient care.
Alex: That's fascinating! Can you tell us about some specific applications?
Dr. Sharma: Absolutely! AI is being used for early disease detection, personalized treatment plans, and even robotic surgery assistance."""
    
    print("📝 Test Script:")
    print(test_script)
    print("\n" + "=" * 50)
    
    # Test Azure TTS
    success, audio_files = generate_podcast_audio_azure(test_script, "test_podcast.mp3")
    
    if success:
        print(f"\n✅ Azure TTS test successful!")
        print(f"📁 Generated {len(audio_files)} audio file(s):")
        for i, audio_file in enumerate(audio_files, 1):
            print(f"   {i}. {audio_file}")
        
        # Check if files exist
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                file_size = os.path.getsize(audio_file)
                print(f"   ✅ {audio_file} exists ({file_size} bytes)")
            else:
                print(f"   ❌ {audio_file} not found")
        
        return True
    else:
        print(f"\n❌ Azure TTS test failed!")
        return False

if __name__ == "__main__":
    success = test_azure_tts()
    if success:
        print("\n🎉 Azure TTS integration is working correctly!")
    else:
        print("\n❌ Azure TTS integration needs attention.")
        sys.exit(1)

