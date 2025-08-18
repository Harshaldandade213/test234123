#!/usr/bin/env python3
"""
Simple TTS test script to demonstrate AWS Polly functionality.
"""

import boto3
import os

# AWS Configuration
AWS_REGION = "us-east-1"

def test_tts_voices():
    """Test different AWS Polly voices."""
    print("🎵 AWS Polly TTS Test")
    print("=" * 50)
    
    try:
        # Initialize AWS Polly client
        polly_client = boto3.client('polly', region_name=AWS_REGION)
        
        # Test voices
        test_voices = [
            ("Matthew", "en-US", "Hello! I'm Matthew, your male podcast host."),
            ("Joanna", "en-US", "Hi there! I'm Joanna, your female podcast expert."),
            ("Matthew", "en-US", "Space exploration offers incredible benefits for humanity."),
            ("Joanna", "en-US", "The technological advancements from space missions help solve Earth's problems.")
        ]
        
        for i, (voice_id, language_code, text) in enumerate(test_voices):
            print(f"\n🎤 Testing {voice_id} ({language_code}):")
            print(f"   Text: '{text}'")
            
            # Generate speech
            response = polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                Engine='neural'  # Use neural engine for better quality
            )
            
            # Save audio file
            filename = f"test_voice_{voice_id.lower()}_{i:02d}.mp3"
            with open(filename, 'wb') as f:
                f.write(response['AudioStream'].read())
            
            print(f"   ✅ Generated: {filename}")
        
        print(f"\n🎉 TTS Test Complete!")
        print("📁 Check the generated MP3 files to hear the voices.")
        print("🎵 You can play these files with any media player.")
        
    except Exception as e:
        print(f"❌ Error during TTS test: {e}")
        print("Please ensure you have AWS credentials configured.")
        print("Run: aws configure")

if __name__ == "__main__":
    test_tts_voices()
