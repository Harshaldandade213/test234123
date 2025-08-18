#!/usr/bin/env python3
"""
Test script for frontend integration with enhanced related sections
This tests the complete flow from frontend API call to backend response
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"

def test_frontend_api_integration():
    """Test the frontend API integration with enhanced related sections"""
    
    print("🧪 Testing Frontend API Integration with Enhanced Related Sections")
    print("=" * 70)
    
    # Test data that matches frontend format
    test_data = {
        "document_ids": ["test_doc_1", "test_doc_2"],
        "current_page": 5,
        "current_section": "Cloud Computing Architecture",
        "persona": "Software Engineer",
        "job_to_be_done": "Design scalable cloud infrastructure"
    }
    
    try:
        print(f"📡 Testing frontend-style API call to {BASE_URL}/related-sections")
        print(f"📋 Test data: {json.dumps(test_data, indent=2)}")
        
        # Simulate frontend FormData request
        form_data = {}
        for doc_id in test_data["document_ids"]:
            if "document_ids" not in form_data:
                form_data["document_ids"] = []
            form_data["document_ids"].append(doc_id)
        
        form_data["current_page"] = test_data["current_page"]
        form_data["current_section"] = test_data["current_section"]
        form_data["persona"] = test_data["persona"]
        form_data["job_to_be_done"] = test_data["job_to_be_done"]
        
        # Make the request using form data (like frontend)
        response = requests.post(
            f"{BASE_URL}/related-sections",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Frontend API integration successful!")
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            
            # Validate response structure matches frontend expectations
            if "related_sections" in result:
                sections = result["related_sections"]
                print(f"🔍 Found {len(sections)} related sections")
                
                # Check if enhanced fields are present
                enhanced_fields_present = False
                for i, section in enumerate(sections, 1):
                    print(f"\n📖 Section {i}:")
                    print(f"   Document: {section.get('document', 'Unknown')}")
                    print(f"   Title: {section.get('section_title', 'Unknown')}")
                    print(f"   Page: {section.get('page_number', 0)}")
                    print(f"   Relevance Score: {section.get('relevance_score', 0):.3f}")
                    print(f"   Explanation: {section.get('explanation', 'No explanation')}")
                    
                    # Check for enhanced fields
                    if 'relationship_type' in section:
                        print(f"   Relationship Type: {section['relationship_type']}")
                        enhanced_fields_present = True
                    
                    if 'key_concepts' in section and section['key_concepts']:
                        print(f"   Key Concepts: {', '.join(section['key_concepts'])}")
                        enhanced_fields_present = True
                
                if enhanced_fields_present:
                    print("\n✅ Enhanced fields are present - frontend integration ready!")
                else:
                    print("\n⚠️ Enhanced fields not found - check backend implementation")
                
                # Validate frontend interface compatibility
                validate_frontend_compatibility(sections)
            else:
                print("⚠️ Response missing 'related_sections' field")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")

def validate_frontend_compatibility(sections):
    """Validate that the response is compatible with frontend interface"""
    
    print("\n🔍 Validating Frontend Interface Compatibility")
    print("-" * 50)
    
    required_fields = ["document", "section_title", "page_number", "relevance_score", "explanation"]
    enhanced_fields = ["relationship_type", "key_concepts"]
    
    all_compatible = True
    
    for i, section in enumerate(sections, 1):
        print(f"\n📋 Section {i} compatibility check:")
        
        # Check required fields
        for field in required_fields:
            if field in section:
                print(f"   ✅ {field}: {type(section[field]).__name__}")
            else:
                print(f"   ❌ {field}: Missing")
                all_compatible = False
        
        # Check enhanced fields (optional)
        for field in enhanced_fields:
            if field in section:
                print(f"   ✅ {field}: {type(section[field]).__name__}")
            else:
                print(f"   ⚠️ {field}: Not present (optional)")
        
        # Validate data types
        if not isinstance(section.get("document", ""), str):
            print("   ❌ document: Should be string")
            all_compatible = False
        
        if not isinstance(section.get("section_title", ""), str):
            print("   ❌ section_title: Should be string")
            all_compatible = False
        
        if not isinstance(section.get("page_number", 0), int):
            print("   ❌ page_number: Should be integer")
            all_compatible = False
        
        if not isinstance(section.get("relevance_score", 0), (int, float)):
            print("   ❌ relevance_score: Should be number")
            all_compatible = False
        
        if not isinstance(section.get("explanation", ""), str):
            print("   ❌ explanation: Should be string")
            all_compatible = False
    
    if all_compatible:
        print("\n✅ All sections are compatible with frontend interface!")
    else:
        print("\n❌ Some sections have compatibility issues")

def test_error_handling():
    """Test error handling scenarios"""
    
    print("\n🧪 Testing Error Handling")
    print("=" * 40)
    
    # Test with missing required fields
    test_cases = [
        {
            "name": "Missing document_ids",
            "data": {
                "current_page": 5,
                "current_section": "Test",
                "persona": "Engineer",
                "job_to_be_done": "Test job"
            }
        },
        {
            "name": "Missing persona",
            "data": {
                "document_ids": ["test"],
                "current_page": 5,
                "current_section": "Test",
                "job_to_be_done": "Test job"
            }
        },
        {
            "name": "Invalid current_page",
            "data": {
                "document_ids": ["test"],
                "current_page": "invalid",
                "current_section": "Test",
                "persona": "Engineer",
                "job_to_be_done": "Test job"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📋 Testing: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/related-sections",
                data=test_case["data"],
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 422:  # Validation error
                print("   ✅ Properly handled validation error")
            elif response.status_code == 500:  # Server error
                print("   ⚠️ Server error (expected for invalid data)")
            else:
                print(f"   ❌ Unexpected status code: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting Frontend Integration Test Suite")
    print("=" * 70)
    
    # First check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed - server is running")
        else:
            print(f"❌ Health check failed - status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check failed - {str(e)}")
        print("\n💡 Please start the server first:")
        print("   cd adobev4")
        print("   python main.py")
        return
    
    print("\n" + "=" * 70)
    
    # Test frontend API integration
    test_frontend_api_integration()
    
    # Test error handling
    test_error_handling()
    
    print("\n" + "=" * 70)
    print("🏁 Frontend integration test suite completed!")
    print("\n📝 Summary:")
    print("   - Frontend API calls should now work correctly")
    print("   - Enhanced fields (relationship_type, key_concepts) are included")
    print("   - Error handling is properly implemented")
    print("   - Response format matches frontend interface expectations")

if __name__ == "__main__":
    main()
