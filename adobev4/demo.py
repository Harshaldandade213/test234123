#!/usr/bin/env python3
"""
Demo script for podcast generation functionality.
This script demonstrates how to use the podcast generation feature.
"""

import os
import sys

# Add the current directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import generate_podcast

def main():
    print("🎙️ PODCAST GENERATION DEMO")
    print("=" * 50)
    
    # Sample query for testing
    test_query = "Is colonizing Mars a good idea?"
    
    print(f"Query: {test_query}")
    print("\nThis will:")
    print("1. Analyze your documents for relevant information")
    print("2. Generate a podcast script with two speakers")
    print("3. Convert the script to audio using AWS Polly TTS")
    print("\nNote: You need AWS credentials configured for TTS.")
    print("Run: aws configure or set environment variables")
    
    # Ask user if they want to proceed
    response = input("\nDo you want to proceed? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\nStarting podcast generation...")
        success = generate_podcast(test_query, "demo_podcast.mp3")
        
        if success:
            print("\n🎉 Demo completed successfully!")
            print("Check 'demo_podcast.mp3' for the generated audio.")
        else:
            print("\n❌ Demo failed. Check the error messages above.")
    else:
        print("Demo cancelled.")

if __name__ == "__main__":
    main()
