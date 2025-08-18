#!/usr/bin/env python3
"""
Integration test script for the FastAPI backend endpoints.
This script tests all endpoints that the frontend expects to be available.
"""

import requests
import json
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TEST_FILES_DIR = "documents"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_upload_pdfs():
    """Test PDF upload endpoint"""
    print("Testing PDF upload...")
    try:
        # Check if test files exist
        test_files = []
        if os.path.exists(TEST_FILES_DIR):
            for file in os.listdir(TEST_FILES_DIR):
                if file.endswith(('.pdf', '.docx', '.txt')):
                    test_files.append(os.path.join(TEST_FILES_DIR, file))
        
        if not test_files:
            print("⚠️  No test files found, skipping upload test")
            return True
        
        # Test with first file
        with open(test_files[0], 'rb') as f:
            files = {'files': (os.path.basename(test_files[0]), f, 'application/pdf')}
            data = {'persona': 'Test Persona', 'job_to_be_done': 'Test Job'}
            response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
        
        if response.status_code == 200:
            print("✅ PDF upload passed")
            return True
        else:
            print(f"❌ PDF upload failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PDF upload error: {e}")
        return False

def test_get_documents():
    """Test get documents endpoint"""
    print("Testing get documents...")
    try:
        response = requests.get(f"{BASE_URL}/documents")
        if response.status_code == 200:
            print("✅ Get documents passed")
            return True
        else:
            print(f"❌ Get documents failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get documents error: {e}")
        return False

def test_analyze_documents():
    """Test document analysis endpoint"""
    print("Testing analyze documents...")
    try:
        data = {
            "document_ids": ["test-doc-1"],
            "persona": "Test Persona",
            "job_to_be_done": "Test Job"
        }
        response = requests.post(f"{BASE_URL}/analyze-documents", json=data)
        if response.status_code == 200:
            print("✅ Analyze documents passed")
            return True
        else:
            print(f"❌ Analyze documents failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analyze documents error: {e}")
        return False

def test_related_sections():
    """Test related sections endpoint"""
    print("Testing related sections...")
    try:
        data = {
            "document_ids": ["test-doc-1"],
            "current_page": 1,
            "current_section": "Test Section",
            "persona": "Test Persona",
            "job_to_be_done": "Test Job"
        }
        response = requests.post(f"{BASE_URL}/related-sections", data=data)
        if response.status_code == 200:
            print("✅ Related sections passed")
            return True
        else:
            print(f"❌ Related sections failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Related sections error: {e}")
        return False

def test_insights():
    """Test insights endpoint"""
    print("Testing insights...")
    try:
        data = {
            "text": "This is a test text for insights generation.",
            "persona": "Test Persona",
            "job_to_be_done": "Test Job",
            "document_context": "Test context"
        }
        response = requests.post(f"{BASE_URL}/insights", json=data)
        if response.status_code == 200:
            print("✅ Insights passed")
            return True
        else:
            print(f"❌ Insights failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Insights error: {e}")
        return False

def test_comprehensive_insights():
    """Test comprehensive insights endpoint"""
    print("Testing comprehensive insights...")
    try:
        data = {
            "text": "This is a test text for comprehensive insights generation.",
            "persona": "Test Persona",
            "job_to_be_done": "Test Job",
            "document_context": "Test context"
        }
        response = requests.post(f"{BASE_URL}/comprehensive-insights", json=data)
        if response.status_code == 200:
            print("✅ Comprehensive insights passed")
            return True
        else:
            print(f"❌ Comprehensive insights failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Comprehensive insights error: {e}")
        return False

def test_podcast():
    """Test podcast generation endpoint"""
    print("Testing podcast generation...")
    try:
        data = {
            "text": "This is a test text for podcast generation.",
            "related_sections": ["Section 1", "Section 2"],
            "insights": ["Insight 1", "Insight 2"]
        }
        response = requests.post(f"{BASE_URL}/podcast", data=data)
        if response.status_code == 200:
            print("✅ Podcast generation passed")
            return True
        else:
            print(f"❌ Podcast generation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Podcast generation error: {e}")
        return False

def test_simplify():
    """Test text simplification endpoint"""
    print("Testing text simplification...")
    try:
        data = {
            "text": "This is a complex text that needs to be simplified for better understanding."
        }
        response = requests.post(f"{BASE_URL}/simplify", json=data)
        if response.status_code == 200:
            print("✅ Text simplification passed")
            return True
        else:
            print(f"❌ Text simplification failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text simplification error: {e}")
        return False

def test_define_term():
    """Test term definition endpoint"""
    print("Testing term definition...")
    try:
        data = {
            "term": "API",
            "context": "Application Programming Interface in software development"
        }
        response = requests.post(f"{BASE_URL}/define-term", json=data)
        if response.status_code == 200:
            print("✅ Term definition passed")
            return True
        else:
            print(f"❌ Term definition failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Term definition error: {e}")
        return False

def test_reading_progress():
    """Test reading progress tracking endpoint"""
    print("Testing reading progress...")
    try:
        data = {
            "doc_id": "test-doc-1",
            "current_page": 5,
            "total_pages": 20,
            "time_spent": 300
        }
        response = requests.post(f"{BASE_URL}/reading-progress", data=data)
        if response.status_code == 200:
            print("✅ Reading progress passed")
            return True
        else:
            print(f"❌ Reading progress failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Reading progress error: {e}")
        return False

def test_library_endpoints():
    """Test library endpoints"""
    print("Testing library endpoints...")
    try:
        # Test personas
        response = requests.get(f"{BASE_URL}/library/personas")
        if response.status_code == 200:
            print("✅ Library personas passed")
        else:
            print(f"❌ Library personas failed: {response.status_code}")
            return False
        
        # Test jobs
        response = requests.get(f"{BASE_URL}/library/jobs")
        if response.status_code == 200:
            print("✅ Library jobs passed")
        else:
            print(f"❌ Library jobs failed: {response.status_code}")
            return False
        
        # Test documents
        response = requests.get(f"{BASE_URL}/library/documents")
        if response.status_code == 200:
            print("✅ Library documents passed")
        else:
            print(f"❌ Library documents failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Library endpoints error: {e}")
        return False

def test_cross_connections():
    """Test cross connections endpoint"""
    print("Testing cross connections...")
    try:
        response = requests.get(f"{BASE_URL}/cross-connections/test-doc-1")
        if response.status_code == 200:
            print("✅ Cross connections passed")
            return True
        else:
            print(f"❌ Cross connections failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cross connections error: {e}")
        return False

def test_strategic_insights():
    """Test strategic insights endpoint"""
    print("Testing strategic insights...")
    try:
        data = {
            "text": "This is a test text for strategic insights generation.",
            "persona": "Test Persona",
            "job_to_be_done": "Test Job",
            "document_context": "Test context"
        }
        response = requests.post(f"{BASE_URL}/strategic-insights", json=data)
        if response.status_code == 200:
            print("✅ Strategic insights passed")
            return True
        else:
            print(f"❌ Strategic insights failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Strategic insights error: {e}")
        return False

def test_contextual_analysis():
    """Test contextual analysis endpoint"""
    print("Testing contextual analysis...")
    try:
        data = {
            "doc_id": "test-doc-1",
            "page_number": 1,
            "section_text": "This is a test section for contextual analysis."
        }
        response = requests.post(f"{BASE_URL}/contextual-analysis", data=data)
        if response.status_code == 200:
            print("✅ Contextual analysis passed")
            return True
        else:
            print(f"❌ Contextual analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Contextual analysis error: {e}")
        return False

def test_multi_document_insights():
    """Test multi-document insights endpoint"""
    print("Testing multi-document insights...")
    try:
        data = {
            "document_ids": ["test-doc-1", "test-doc-2"],
            "persona": "Test Persona",
            "job_to_be_done": "Test Job"
        }
        response = requests.post(f"{BASE_URL}/multi-document-insights", json=data)
        if response.status_code == 200:
            print("✅ Multi-document insights passed")
            return True
        else:
            print(f"❌ Multi-document insights failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Multi-document insights error: {e}")
        return False

def test_highlights():
    """Test highlights endpoints"""
    print("Testing highlights...")
    try:
        # Test add highlight
        data = {
            "text": "Test highlight text",
            "color": "yellow",
            "page": 1,
            "documentName": "test-document.pdf"
        }
        response = requests.post(f"{BASE_URL}/highlights", json=data)
        if response.status_code == 200:
            print("✅ Add highlight passed")
        else:
            print(f"❌ Add highlight failed: {response.status_code}")
            return False
        
        # Test get highlights
        response = requests.get(f"{BASE_URL}/highlights/test-document.pdf")
        if response.status_code == 200:
            print("✅ Get highlights passed")
        else:
            print(f"❌ Get highlights failed: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Highlights error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting FastAPI Backend Integration Tests")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_upload_pdfs,
        test_get_documents,
        test_analyze_documents,
        test_related_sections,
        test_insights,
        test_comprehensive_insights,
        test_podcast,
        test_simplify,
        test_define_term,
        test_reading_progress,
        test_library_endpoints,
        test_cross_connections,
        test_strategic_insights,
        test_contextual_analysis,
        test_multi_document_insights,
        test_highlights
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend integration is complete.")
    else:
        print("⚠️  Some tests failed. Please check the backend implementation.")
    
    return passed == total

if __name__ == "__main__":
    main()
