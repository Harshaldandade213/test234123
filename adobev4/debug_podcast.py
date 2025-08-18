#!/usr/bin/env python3
"""
Debug script to test podcast generation step by step
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

def test_podcast_generation():
    """Test podcast generation step by step"""
    
    print("🔍 Debugging podcast generation...")
    
    try:
        from app import generate_podcast, analyze_and_categorize, generate_podcast_script
        
        # Test query
        query = "Test query"
        
        print(f"1️⃣ Testing analysis for query: '{query}'")
        analysis_result = analyze_and_categorize(query)
        if analysis_result:
            print("   ✅ Analysis successful")
        else:
            print("   ❌ Analysis failed")
            return
        
        print(f"2️⃣ Testing script generation")
        script_text = generate_podcast_script(query, analysis_result)
        if script_text:
            print("   ✅ Script generation successful")
            print(f"   📝 Script length: {len(script_text)} characters")
        else:
            print("   ❌ Script generation failed")
            return
        
        print(f"3️⃣ Testing full podcast generation")
        success, audio_files = generate_podcast(query, "debug_podcast.mp3")
        
        print(f"   Success: {success}")
        print(f"   Audio files: {audio_files}")
        
        if success and audio_files:
            print("   ✅ Podcast generation successful!")
        else:
            print("   ❌ Podcast generation failed")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_podcast_generation()
