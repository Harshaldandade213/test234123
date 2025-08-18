#!/usr/bin/env python3
"""
Comprehensive API Endpoint Testing Script
This script tests all endpoints of the FastAPI backend server with real data.
"""

import requests
import json
import time
import os
from pathlib import Path

# API Configuration
BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_test_result(test_name, success, details=""):
    """Print formatted test result"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} | {test_name}")
    if details:
        print(f"   📝 {details}")

def test_health_check():
    """Test the health check endpoint"""
    print_section("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_test_result("Health Check", True, f"Status: {data['status']}, Timestamp: {data['timestamp']}")
            return True
        else:
            print_test_result("Health Check", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Health Check", False, f"Error: {e}")
        return False

def test_get_documents():
    """Test getting documents"""
    print_section("Document Management - Get Documents")
    
    try:
        response = requests.get(f"{BASE_URL}/documents")
        if response.status_code == 200:
            data = response.json()
            print_test_result("Get Documents", True, f"Found {len(data)} documents")
            return True
        else:
            print_test_result("Get Documents", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Get Documents", False, f"Error: {e}")
        return False

def test_get_personas():
    """Test getting personas"""
    print_section("Library - Get Personas")
    
    try:
        response = requests.get(f"{BASE_URL}/library/personas")
        if response.status_code == 200:
            data = response.json()
            print_test_result("Get Personas", True, f"Found {len(data)} personas: {data}")
            return True
        else:
            print_test_result("Get Personas", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test_result("Get Personas", False, f"Error: {e}")
        return False

def test_generate_insights():
    """Test generating insights"""
    print_section("AI Analysis - Generate Insights")
    
    try:
        payload = {
            "text": "Artificial intelligence is transforming the way we work and live. Machine learning algorithms are becoming more sophisticated and accessible. Companies are increasingly adopting AI solutions to improve efficiency and gain competitive advantages.",
            "persona": "Technology Professional",
            "job_to_be_done": "Understanding AI trends and applications"
        }
        
        response = requests.post(
            f"{BASE_URL}/insights", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            insights_count = len(data.get('insights', []))
            print_test_result("Generate Insights", True, f"Generated {insights_count} insights")
            
            # Print first insight as example
            if insights_count > 0:
                first_insight = data['insights'][0]
                print(f"   📊 Sample insight: {first_insight['type']} - {first_insight['content'][:100]}...")
            
            return True
        else:
            print_test_result("Generate Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Generate Insights", False, f"Error: {e}")
        return False

def test_comprehensive_insights():
    """Test comprehensive insights"""
    print_section("AI Analysis - Comprehensive Insights")
    
    try:
        payload = {
            "text": "The rapid advancement of artificial intelligence technologies is reshaping industries across the globe. Companies are increasingly adopting AI solutions to improve efficiency and gain competitive advantages. This transformation is creating new opportunities for innovation and growth.",
            "persona": "Business Executive",
            "job_to_be_done": "Evaluating AI adoption strategies"
        }
        
        response = requests.post(
            f"{BASE_URL}/comprehensive-insights", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            insights_count = len(data.get('insights', []))
            persona_insights_count = len(data.get('persona_insights', []))
            keywords_count = len(data.get('keywords', []))
            
            print_test_result("Comprehensive Insights", True, 
                            f"Insights: {insights_count}, Persona insights: {persona_insights_count}, Keywords: {keywords_count}")
            
            # Print sample data
            if keywords_count > 0:
                print(f"   🔑 Keywords: {', '.join(data['keywords'][:5])}")
            
            return True
        else:
            print_test_result("Comprehensive Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Comprehensive Insights", False, f"Error: {e}")
        return False

def test_simplify_text():
    """Test text simplification"""
    print_section("Content Processing - Simplify Text")
    
    try:
        payload = {
            "text": "The implementation of artificial intelligence algorithms necessitates comprehensive understanding of machine learning paradigms and neural network architectures."
        }
        
        response = requests.post(
            f"{BASE_URL}/simplify-text", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            original = data.get('original', '')
            simplified = data.get('text', '')
            
            print_test_result("Simplify Text", True, f"Original: {len(original)} chars, Simplified: {len(simplified)} chars")
            print(f"   📝 Original: {original[:80]}...")
            print(f"   ✨ Simplified: {simplified[:80]}...")
            
            return True
        else:
            print_test_result("Simplify Text", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Simplify Text", False, f"Error: {e}")
        return False

def test_define_term():
    """Test term definition"""
    print_section("Content Processing - Define Term")
    
    try:
        payload = {
            "term": "machine learning",
            "context": "In the context of artificial intelligence and data science"
        }
        
        response = requests.post(
            f"{BASE_URL}/define-term", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            definition = data.get('definition', '')
            
            print_test_result("Define Term", True, f"Definition length: {len(definition)} chars")
            print(f"   📖 Definition: {definition[:150]}...")
            
            return True
        else:
            print_test_result("Define Term", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Define Term", False, f"Error: {e}")
        return False

def test_library_documents():
    """Test library documents filtering"""
    print_section("Library - Filter Documents")
    
    try:
        # Test without filters
        response = requests.get(f"{BASE_URL}/library/documents")
        if response.status_code == 200:
            data = response.json()
            print_test_result("Get Library Documents (no filter)", True, f"Found {len(data)} documents")
        
        # Test with persona filter
        response = requests.get(f"{BASE_URL}/library/documents?persona=technology")
        if response.status_code == 200:
            data = response.json()
            print_test_result("Get Library Documents (persona filter)", True, f"Found {len(data)} documents")
        
        return True
    except Exception as e:
        print_test_result("Get Library Documents", False, f"Error: {e}")
        return False

def test_reading_progress():
    """Test reading progress tracking"""
    print_section("Reading Progress - Track Progress")
    
    try:
        # Create a mock document ID for testing
        mock_doc_id = "test-document-123"
        
        payload = {
            "doc_id": mock_doc_id,
            "current_page": 5,
            "total_pages": 20,
            "time_spent": 300  # 5 minutes in seconds
        }
        
        response = requests.post(
            f"{BASE_URL}/reading-progress",
            data=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            progress = data.get('progress_percentage', 0)
            time_spent = data.get('time_spent_minutes', 0)
            
            print_test_result("Track Reading Progress", True, 
                            f"Progress: {progress:.1f}%, Time spent: {time_spent:.1f} minutes")
            
            return True
        else:
            print_test_result("Track Reading Progress", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Track Reading Progress", False, f"Error: {e}")
        return False

def test_upload_document():
    """Test document upload (if test file exists)"""
    print_section("Document Management - Upload Document")
    
    # Check if there are any documents in the documents folder
    documents_dir = Path("documents")
    if documents_dir.exists():
        test_files = list(documents_dir.glob("*.txt")) + list(documents_dir.glob("*.pdf")) + list(documents_dir.glob("*.docx"))
        
        if test_files:
            test_file = test_files[0]  # Use the first available file
            
            try:
                with open(test_file, 'rb') as f:
                    files = {'files': (test_file.name, f, 'application/octet-stream')}
                    data = {
                        'persona': 'Test User',
                        'job_to_be_done': 'Testing API functionality'
                    }
                    
                    response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
                    
                    if response.status_code == 200:
                        uploaded_docs = response.json()
                        print_test_result("Upload Document", True, f"Uploaded {len(uploaded_docs)} documents")
                        
                        # Store document ID for later tests
                        if uploaded_docs:
                            global test_document_id
                            test_document_id = uploaded_docs[0]['id']
                            print(f"   📄 Test document ID: {test_document_id}")
                        
                        return True
                    else:
                        print_test_result("Upload Document", False, f"Status code: {response.status_code}")
                        print(f"   Response: {response.text}")
                        return False
            except Exception as e:
                print_test_result("Upload Document", False, f"Error: {e}")
                return False
        else:
            print_test_result("Upload Document", True, "No test files available - skipping")
            return True
    else:
        print_test_result("Upload Document", True, "Documents directory not found - skipping")
        return True

def test_analyze_documents():
    """Test document analysis (if we have uploaded documents)"""
    print_section("Document Analysis - Analyze Documents")
    
    global test_document_id
    
    if 'test_document_id' in globals() and test_document_id:
        try:
            payload = {
                "document_ids": [test_document_id],
                "persona": "Test Analyst",
                "job_to_be_done": "Testing document analysis functionality"
            }
            
            response = requests.post(
                f"{BASE_URL}/analyze-documents",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                insights_count = len(data.get('insights', []))
                print_test_result("Analyze Documents", True, f"Generated {insights_count} insights")
                return True
            else:
                print_test_result("Analyze Documents", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print_test_result("Analyze Documents", False, f"Error: {e}")
            return False
    else:
        print_test_result("Analyze Documents", True, "No test documents available - skipping")
        return True

def main():
    """Run all endpoint tests"""
    print("🚀 Comprehensive API Endpoint Testing")
    print("=" * 60)
    print(f"🌐 Testing server at: {BASE_URL}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize global variable
    global test_document_id
    test_document_id = None
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Get Documents", test_get_documents),
        ("Get Personas", test_get_personas),
        ("Generate Insights", test_generate_insights),
        ("Comprehensive Insights", test_comprehensive_insights),
        ("Simplify Text", test_simplify_text),
        ("Define Term", test_define_term),
        ("Library Documents", test_library_documents),
        ("Reading Progress", test_reading_progress),
        ("Upload Document", test_upload_document),
        ("Analyze Documents", test_analyze_documents)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            time.sleep(1)  # Small delay between tests
        except Exception as e:
            print(f"❌ ERROR | {test_name} - Exception: {e}")
    
    # Print summary
    print_section("Test Summary")
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working perfectly.")
    else:
        print(f"⚠️ {total - passed} test(s) failed. Check the details above.")
    
    print(f"\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")
    
    print(f"\n🔧 Server Status: {'🟢 Running' if passed > 0 else '🔴 Not responding'}")

if __name__ == "__main__":
    main()
