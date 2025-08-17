#!/usr/bin/env python3
"""
Comprehensive Test Script for Integrated Document Analysis System
Tests both adobev4 and HARSHALADOBE backends
"""

import requests
import json
import time
import os
from typing import Dict, Any

# Configuration
ADOBEV4_URL = "http://localhost:8000"
HARSHALADOBE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:8081"

class IntegratedSystemTester:
    def __init__(self):
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
        
    def test_backend_health(self):
        """Test if both backends are running"""
        print("\n🔍 Testing Backend Health...")
        
        # Test adobev4 backend
        try:
            response = self.session.get(f"{ADOBEV4_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("adobev4 Backend Health", True)
            else:
                self.log_test("adobev4 Backend Health", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("adobev4 Backend Health", False, str(e))
            
        # Test HARSHALADOBE backend
        try:
            response = self.session.get(f"{HARSHALADOBE_URL}/health", timeout=5)
            if response.status_code == 200:
                self.log_test("HARSHALADOBE Backend Health", True)
            else:
                self.log_test("HARSHALADOBE Backend Health", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("HARSHALADOBE Backend Health", False, str(e))
            
    def test_frontend_health(self):
        """Test if frontend is running"""
        print("\n🌐 Testing Frontend Health...")
        try:
            response = self.session.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Health", True)
            else:
                self.log_test("Frontend Health", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Frontend Health", False, str(e))
            
    def test_document_upload(self):
        """Test document upload functionality"""
        print("\n📄 Testing Document Upload...")
        
        # Create a test PDF file
        test_pdf_path = "test_document.pdf"
        try:
            # Create a simple test PDF
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(test_pdf_path)
            c.drawString(100, 750, "Test Document for Integration Testing")
            c.drawString(100, 700, "This is a test document to validate the integrated system.")
            c.drawString(100, 650, "It contains sample content for analysis and insights generation.")
            c.save()
            
            # Upload the test document
            with open(test_pdf_path, 'rb') as f:
                files = {'files': ('test_document.pdf', f, 'application/pdf')}
                data = {
                    'persona': 'Software Developer',
                    'job_to_be_done': 'Testing Integration'
                }
                response = self.session.post(f"{HARSHALADOBE_URL}/upload-pdfs", files=files, data=data)
                
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0:
                    self.log_test("Document Upload", True, f"Uploaded {len(result)} documents")
                    return result[0]['id']  # Return the document ID for further tests
                else:
                    self.log_test("Document Upload", False, "No documents returned")
            else:
                self.log_test("Document Upload", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Document Upload", False, str(e))
        finally:
            # Clean up test file
            if os.path.exists(test_pdf_path):
                os.remove(test_pdf_path)
        return None
        
    def test_document_analysis(self, doc_id: str):
        """Test document analysis using adobev4 backend"""
        print("\n🔍 Testing Document Analysis...")
        
        if not doc_id:
            self.log_test("Document Analysis", False, "No document ID available")
            return
            
        try:
            data = {
                "document_ids": [doc_id],
                "persona": "Software Developer",
                "job_to_be_done": "Testing Integration"
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/analyze-documents", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'analysis_results' in result:
                    self.log_test("Document Analysis", True, "Analysis completed successfully")
                else:
                    self.log_test("Document Analysis", False, "No analysis results")
            else:
                self.log_test("Document Analysis", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Document Analysis", False, str(e))
            
    def test_insights_generation(self):
        """Test insights generation"""
        print("\n💡 Testing Insights Generation...")
        
        try:
            data = {
                "text": "This is a test text for insights generation. It contains information about software development and testing methodologies.",
                "persona": "Software Developer",
                "job_to_be_done": "Testing Integration",
                "document_context": "Integration testing context"
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/insights", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'insights' in result:
                    self.log_test("Insights Generation", True, f"Generated {len(result['insights'])} insights")
                else:
                    self.log_test("Insights Generation", False, "No insights returned")
            else:
                self.log_test("Insights Generation", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Insights Generation", False, str(e))
            
    def test_comprehensive_insights(self):
        """Test comprehensive insights generation"""
        print("\n📊 Testing Comprehensive Insights...")
        
        try:
            data = {
                "text": "Advanced testing methodologies including unit testing, integration testing, and end-to-end testing are essential for software quality assurance.",
                "persona": "Software Developer",
                "job_to_be_done": "Testing Integration",
                "document_context": "Software testing context"
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/comprehensive-insights", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'insights' in result:
                    self.log_test("Comprehensive Insights", True, "Comprehensive analysis completed")
                else:
                    self.log_test("Comprehensive Insights", False, "No comprehensive insights")
            else:
                self.log_test("Comprehensive Insights", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Comprehensive Insights", False, str(e))
            
    def test_text_simplification(self):
        """Test text simplification"""
        print("\n📝 Testing Text Simplification...")
        
        try:
            data = {
                "text": "The implementation of sophisticated algorithmic paradigms necessitates the utilization of complex computational methodologies."
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/simplify", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'text' in result:
                    self.log_test("Text Simplification", True, "Text simplified successfully")
                else:
                    self.log_test("Text Simplification", False, "No simplified text")
            else:
                self.log_test("Text Simplification", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Text Simplification", False, str(e))
            
    def test_related_sections(self, doc_id: str):
        """Test related sections functionality"""
        print("\n🔗 Testing Related Sections...")
        
        if not doc_id:
            self.log_test("Related Sections", False, "No document ID available")
            return
            
        try:
            data = {
                "document_ids": doc_id,
                "current_page": 1,
                "current_section": "Testing methodologies",
                "persona": "Software Developer",
                "job_to_be_done": "Testing Integration"
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/related-sections", data=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'related_sections' in result:
                    self.log_test("Related Sections", True, f"Found {len(result['related_sections'])} related sections")
                else:
                    self.log_test("Related Sections", False, "No related sections")
            else:
                self.log_test("Related Sections", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Related Sections", False, str(e))
            
    def test_document_search(self):
        """Test document search functionality"""
        print("\n🔍 Testing Document Search...")
        
        try:
            data = {
                "query": "testing integration",
                "k": 5
            }
            response = self.session.post(f"{HARSHALADOBE_URL}/search-documents", data=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'results' in result:
                    self.log_test("Document Search", True, f"Found {len(result['results'])} results")
                else:
                    self.log_test("Document Search", False, "No search results")
            else:
                self.log_test("Document Search", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Document Search", False, str(e))
            
    def test_library_endpoints(self):
        """Test library-related endpoints"""
        print("\n📚 Testing Library Endpoints...")
        
        # Test documents endpoint
        try:
            response = self.session.get(f"{HARSHALADOBE_URL}/documents")
            if response.status_code == 200:
                self.log_test("Get Documents", True, "Documents retrieved successfully")
            else:
                self.log_test("Get Documents", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Documents", False, str(e))
            
        # Test personas endpoint
        try:
            response = self.session.get(f"{HARSHALADOBE_URL}/library/personas")
            if response.status_code == 200:
                self.log_test("Get Personas", True, "Personas retrieved successfully")
            else:
                self.log_test("Get Personas", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Personas", False, str(e))
            
        # Test jobs endpoint
        try:
            response = self.session.get(f"{HARSHALADOBE_URL}/library/jobs")
            if response.status_code == 200:
                self.log_test("Get Jobs", True, "Jobs retrieved successfully")
            else:
                self.log_test("Get Jobs", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Get Jobs", False, str(e))
            
    def test_adobev4_endpoints(self):
        """Test adobev4 specific endpoints"""
        print("\n🎙️ Testing AdobeV4 Endpoints...")
        
        # Test podcast generation
        try:
            data = {
                "query": "Testing integration between different systems",
                "output_filename": "test_podcast.mp3"
            }
            response = self.session.post(f"{ADOBEV4_URL}/generate-podcast", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    self.log_test("Podcast Generation", True, "Podcast generated successfully")
                else:
                    self.log_test("Podcast Generation", False, result.get('message', 'Unknown error'))
            else:
                self.log_test("Podcast Generation", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Podcast Generation", False, str(e))
            
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Integration Tests...")
        print("=" * 60)
        
        # Health checks
        self.test_backend_health()
        self.test_frontend_health()
        
        # Document operations
        doc_id = self.test_document_upload()
        
        # Analysis and insights
        self.test_document_analysis(doc_id)
        self.test_insights_generation()
        self.test_comprehensive_insights()
        self.test_text_simplification()
        
        # Search and related content
        self.test_related_sections(doc_id)
        self.test_document_search()
        
        # Library operations
        self.test_library_endpoints()
        
        # AdobeV4 specific features
        self.test_adobev4_endpoints()
        
        # Summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
                    
        print("\n🎉 Integration Test Complete!")

if __name__ == "__main__":
    tester = IntegratedSystemTester()
    tester.run_all_tests()
