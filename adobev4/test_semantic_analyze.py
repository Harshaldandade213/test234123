#!/usr/bin/env python3
"""
Test script to verify the semantic search-based analyze-query endpoint
"""

import requests
import json

def test_analyze_query():
    """Test the analyze-query endpoint with semantic search"""
    print("🧪 Testing analyze-query endpoint with semantic search...")
    
    try:
        # Test with form data
        form_data = {"query": "What are microservices?"}
        response = requests.post(
            "http://127.0.0.1:8000/analyze-query",
            data=form_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print(f"Query: {data.get('query', 'N/A')}")
            print(f"Analysis items: {len(data.get('analysis', []))}")
            print(f"Summary: {data.get('summary', 'N/A')}")
            
            # Show first analysis item
            if data.get('analysis'):
                print("\nFirst analysis item:")
                print(json.dumps(data['analysis'][0], indent=2))
                
                # Check if it has the expected fields
                expected_fields = ['passage_number', 'source', 'passage_preview', 'category', 'justification', 'quote']
                missing_fields = [field for field in expected_fields if field not in data['analysis'][0]]
                if missing_fields:
                    print(f"⚠️ Missing fields: {missing_fields}")
                else:
                    print("✅ All expected fields present")
        else:
            print(f"❌ API call failed with status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Error calling API: {e}")

if __name__ == "__main__":
    test_analyze_query()
