#!/usr/bin/env python3
"""
Test script to verify the generate_podcast function returns correct format
"""

import sys
import os

# Add current directory to path
sys.path.append('.')

def test_function_format():
    """Test that generate_podcast function returns correct format"""
    
    print("🔍 Testing generate_podcast function format...")
    
    try:
        from app import generate_podcast
        
        # Test with a simple query that will fail due to API quota
        query = "Test query"
        
        print(f"Testing with query: '{query}'")
        result = generate_podcast(query, "test_output.mp3")
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if isinstance(result, tuple) and len(result) == 2:
            success, audio_files = result
            print(f"✅ Function returns correct tuple format")
            print(f"   Success: {success}")
            print(f"   Audio files: {audio_files}")
        else:
            print(f"❌ Function returns incorrect format: {type(result)}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_function_format()
