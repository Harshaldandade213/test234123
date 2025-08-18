#!/usr/bin/env python3
"""
Debug script to test the analyze_and_categorize function
"""

import sys
import os

# Add the current directory to the path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import analyze_and_categorize, perform_search

def test_search():
    """Test the search function"""
    print("Testing search function...")
    results = perform_search("microservices", k=5)
    print(f"Search results: {len(results) if results else 0}")
    if results:
        print(f"First result: {results[0]}")
    return results

def test_analyze():
    """Test the analyze function"""
    print("\nTesting analyze_and_categorize function...")
    try:
        result = analyze_and_categorize("What are microservices?")
        if result:
            print("✅ Analysis successful!")
            print(f"Query: {result.get('query', 'N/A')}")
            print(f"Analysis items: {len(result.get('analysis', []))}")
            return result
        else:
            print("❌ Analysis returned None")
            return None
    except Exception as e:
        print(f"❌ Analysis failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🔍 Debugging analyze_and_categorize function")
    print("=" * 50)
    
    # Test search first
    search_results = test_search()
    
    # Test analyze
    analyze_result = test_analyze()
    
    print("\n" + "=" * 50)
    if analyze_result:
        print("✅ All tests passed!")
    else:
        print("❌ Analysis test failed!")

