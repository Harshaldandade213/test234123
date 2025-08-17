#!/usr/bin/env python3
"""
Test script to check if HARSHALADOBE backend can import app.py functions
"""

import sys
import os

# Add the adobev4 path
sys.path.append('../../adobev4')

try:
    from app import analyze_and_categorize, perform_search
    print("✅ Successfully imported app.py functions")
    
    # Test search function
    print("Testing search function...")
    results = perform_search("microservices", k=3)
    if results:
        print(f"✅ Search function works! Found {len(results)} results")
        print(f"First result source: {results[0]['source']}")
    else:
        print("❌ Search function returned no results")
    
    # Test analyze function
    print("\nTesting analyze function...")
    analysis = analyze_and_categorize("What are microservices?")
    if analysis:
        print(f"✅ Analyze function works! Found {len(analysis.get('analysis', []))} analysis items")
    else:
        print("❌ Analyze function returned None")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
