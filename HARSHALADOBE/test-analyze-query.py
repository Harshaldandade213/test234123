#!/usr/bin/env python3
"""
Test script for the analyze-query endpoint integration
"""

import requests
import json

def test_analyze_query():
    """Test the analyze-query endpoint"""
    
    # Test the exact curl command from the user
    url = "http://127.0.0.1:8000/analyze-query"
    query = "What are the challenges of Mars colonization?"
    
    print(f"Testing analyze-query endpoint...")
    print(f"URL: {url}")
    print(f"Query: {query}")
    print("-" * 50)
    
    try:
        # Create form data
        data = {'query': query}
        
        # Make the POST request
        response = requests.post(url, data=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Response received:")
            print(json.dumps(result, indent=2))
            
            # Check if the response has the expected structure
            if 'query' in result and 'analysis' in result:
                print(f"\n✅ Response structure is correct!")
                print(f"Query: {result['query']}")
                print(f"Number of analysis items: {len(result.get('analysis', []))}")
                if 'summary' in result:
                    print(f"Summary: {result['summary'][:100]}...")
            else:
                print("⚠️  Response structure may be different than expected")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the adobev4 backend is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_frontend_integration():
    """Test the frontend integration by calling the HARSHALADOBE backend"""
    
    url = "http://127.0.0.1:8001/health"
    
    print(f"\nTesting HARSHALADOBE backend health...")
    print(f"URL: {url}")
    print("-" * 50)
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ HARSHALADOBE backend is running!")
        else:
            print(f"❌ HARSHALADOBE backend error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the HARSHALADOBE backend is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing analyze-query endpoint integration")
    print("=" * 60)
    
    # Test adobev4 backend
    test_analyze_query()
    
    # Test HARSHALADOBE backend
    test_frontend_integration()
    
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print("1. If adobev4 test passed: The /analyze-query endpoint is working")
    print("2. If HARSHALADOBE test passed: The frontend can communicate with backends")
    print("3. You can now use the Custom Query Analysis feature in the frontend!")
    print("\n🎯 Next Steps:")
    print("- Start both backends: adobev4 (port 8000) and HARSHALADOBE (port 8001)")
    print("- Start the frontend: npm run dev in HARSHALADOBE directory")
    print("- Use the 'Custom Query Analysis' section in the Insights panel")

