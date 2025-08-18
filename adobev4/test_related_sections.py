#!/usr/bin/env python3
"""
Test script for enhanced related sections functionality
This tests the integration of HARSHALADOBE's sophisticated related sections logic
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

def test_related_sections():
    """Test the enhanced related sections endpoint"""
    
    print("🧪 Testing Enhanced Related Sections Functionality")
    print("=" * 60)
    
    # Test data
    test_data = {
        "document_ids": ["test_doc_1", "test_doc_2"],
        "current_page": 5,
        "current_section": "Cloud Computing Architecture",
        "persona": "Software Engineer",
        "job_to_be_done": "Design scalable cloud infrastructure"
    }
    
    try:
        print(f"📡 Making request to {BASE_URL}/related-sections")
        print(f"📋 Test data: {json.dumps(test_data, indent=2)}")
        
        # Make the request
        response = requests.post(
            f"{BASE_URL}/related-sections",
            data=test_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Request successful!")
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            
            # Validate response structure
            if "related_sections" in result:
                sections = result["related_sections"]
                print(f"🔍 Found {len(sections)} related sections")
                
                for i, section in enumerate(sections, 1):
                    print(f"\n📖 Section {i}:")
                    print(f"   Document: {section.get('document', 'Unknown')}")
                    print(f"   Title: {section.get('section_title', 'Unknown')}")
                    print(f"   Page: {section.get('page_number', 0)}")
                    print(f"   Relevance Score: {section.get('relevance_score', 0):.3f}")
                    print(f"   Explanation: {section.get('explanation', 'No explanation')}")
                    print(f"   Relationship Type: {section.get('relationship_type', 'related')}")
                    
                    if 'key_concepts' in section:
                        print(f"   Key Concepts: {', '.join(section['key_concepts'])}")
            else:
                print("⚠️ Response missing 'related_sections' field")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed - server is running")
            return True
        else:
            print(f"❌ Health check failed - status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed - {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Enhanced Related Sections Test Suite")
    print("=" * 60)
    
    # First check if server is running
    if not test_health_check():
        print("\n💡 Please start the server first:")
        print("   cd adobev4")
        print("   python main.py")
        return
    
    print("\n" + "=" * 60)
    
    # Test related sections
    test_related_sections()
    
    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")

if __name__ == "__main__":
    main()
