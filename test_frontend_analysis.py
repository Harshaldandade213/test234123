#!/usr/bin/env python3
"""
Test script to verify frontend can display analysis results
"""

import requests
import json

def test_analyze_query():
    """Test the analyze-query endpoint"""
    print("🧪 Testing analyze-query endpoint...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyze-query",
            data={"query": "What are microservices?"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API call successful!")
            print(f"Query: {data.get('query', 'N/A')}")
            print(f"Analysis items: {len(data.get('analysis', []))}")
            print(f"Summary: {data.get('summary', 'N/A')}")
            
            # Show first analysis item
            if data.get('analysis'):
                first_item = data['analysis'][0]
                print(f"\nFirst analysis item:")
                print(f"  Source: {first_item.get('source', 'N/A')}")
                print(f"  Category: {first_item.get('category', 'N/A')}")
                print(f"  Justification: {first_item.get('justification', 'N/A')}")
            
            return True
        else:
            print(f"❌ API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_integrated_api():
    """Test the integrated API service"""
    print("\n🧪 Testing integrated API service...")
    
    try:
        # Test the HARSHALADOBE backend's analyze-documents endpoint
        response = requests.post(
            "http://127.0.0.1:8001/analyze-documents",
            json={
                "document_ids": [],
                "persona": "Software Developer",
                "job_to_be_done": "Understanding microservices architecture",
                "query": "What are microservices?"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Integrated API call successful!")
            print(f"Query: {data.get('query', 'N/A')}")
            print(f"Analysis items: {len(data.get('analysis', []))}")
            return True
        else:
            print(f"❌ Integrated API call failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing integrated API: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Frontend Analysis Integration")
    print("=" * 50)
    
    # Test direct adobev4 API
    test1_success = test_analyze_query()
    
    # Test integrated API
    test2_success = test_integrated_api()
    
    print("\n" + "=" * 50)
    if test1_success and test2_success:
        print("🎉 All tests passed! Frontend should now be able to display analysis results.")
    else:
        print("⚠️ Some tests failed. Check the backend services.")
