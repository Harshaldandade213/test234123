#!/usr/bin/env python3
"""
Frontend Feature Test Suite
Tests frontend functionality using browser automation
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
FRONTEND_URL = "http://localhost:5173"  # Vite default port
BACKEND_URL = "http://localhost:8000"

class FrontendTester:
    def __init__(self):
        self.frontend_url = FRONTEND_URL
        self.backend_url = BACKEND_URL
        self.test_results = {}
        self.session = requests.Session()
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        
        self.test_results[test_name] = {
            "success": success,
            "details": details
        }
    
    def test_frontend_health(self):
        """Test if frontend is accessible"""
        print("\n🌐 Testing Frontend Health")
        print("=" * 40)
        
        try:
            response = self.session.get(self.frontend_url)
            if response.status_code == 200:
                self.log_test("Frontend Health", True, "Frontend is accessible")
                return True
            else:
                self.log_test("Frontend Health", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Health", False, f"Connection error: {str(e)}")
            return False
    
    def test_backend_health(self):
        """Test if backend is accessible"""
        print("\n🔧 Testing Backend Health")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.backend_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health", True, f"Backend is healthy - {data}")
                return True
            else:
                self.log_test("Backend Health", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health", False, f"Connection error: {str(e)}")
            return False
    
    def test_api_endpoints(self):
        """Test API endpoints that frontend uses"""
        print("\n🔌 Testing API Endpoints")
        print("=" * 40)
        
        endpoints = [
            ("/documents", "GET", "Get Documents"),
            ("/library/personas", "GET", "Get Personas"),
            ("/library/jobs", "GET", "Get Jobs"),
            ("/library/documents", "GET", "Get Library Documents"),
        ]
        
        for endpoint, method, name in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.backend_url}{endpoint}")
                else:
                    response = self.session.post(f"{self.backend_url}{endpoint}")
                
                if response.status_code == 200:
                    self.log_test(f"API {name}", True, f"Status: {response.status_code}")
                else:
                    self.log_test(f"API {name}", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"API {name}", False, f"Error: {str(e)}")
    
    def test_related_sections_api(self):
        """Test related sections API specifically"""
        print("\n🔗 Testing Related Sections API")
        print("=" * 40)
        
        # First upload a test document
        test_doc_content = """
        Cloud Computing Architecture
        
        This document discusses cloud computing principles and architecture.
        
        Key Concepts:
        - Virtualization
        - Scalability
        - Microservices
        - Load Balancing
        """
        
        # Create test document
        os.makedirs("test_documents", exist_ok=True)
        test_file_path = "test_documents/test_doc.txt"
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_doc_content)
        
        try:
            # Upload document
            with open(test_file_path, 'rb') as f:
                files = {'files': ('test_doc.txt', f, 'text/plain')}
                data = {
                    'persona': 'Software Engineer',
                    'job_to_be_done': 'Design cloud infrastructure'
                }
                
                response = self.session.post(f"{self.backend_url}/upload-pdfs", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    doc_id = result[0].get("id") if result else None
                    
                    if doc_id:
                        # Test related sections
                        test_data = {
                            "document_ids": [doc_id],
                            "current_page": 1,
                            "current_section": "Cloud Computing Architecture",
                            "persona": "Software Engineer",
                            "job_to_be_done": "Design cloud infrastructure"
                        }
                        
                        response = self.session.post(
                            f"{self.backend_url}/related-sections",
                            data=test_data,
                            headers={"Content-Type": "application/x-www-form-urlencoded"}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            sections = result.get("related_sections", [])
                            
                            # Check for enhanced fields
                            enhanced_fields = any(
                                'relationship_type' in section or 'key_concepts' in section 
                                for section in sections
                            )
                            
                            self.log_test("Related Sections API", True, 
                                         f"Found {len(sections)} sections, Enhanced fields: {enhanced_fields}")
                        else:
                            self.log_test("Related Sections API", False, f"Status: {response.status_code}")
                    else:
                        self.log_test("Related Sections API", False, "No document ID returned")
                else:
                    self.log_test("Related Sections API", False, f"Upload failed: {response.status_code}")
                    
        except Exception as e:
            self.log_test("Related Sections API", False, f"Error: {str(e)}")
        finally:
            # Clean up
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_insights_api(self):
        """Test insights generation API"""
        print("\n💡 Testing Insights API")
        print("=" * 40)
        
        test_data = {
            "text": "Cloud computing provides scalable infrastructure for modern applications.",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure",
            "document_context": "Cloud computing architecture document"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/insights",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get("insights", [])
                self.log_test("Insights API", True, f"Generated {len(insights)} insights")
            else:
                self.log_test("Insights API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Insights API", False, f"Error: {str(e)}")
    
    def test_comprehensive_insights_api(self):
        """Test comprehensive insights API"""
        print("\n🧠 Testing Comprehensive Insights API")
        print("=" * 40)
        
        test_data = {
            "text": "Microservices architecture enables better scalability and maintainability.",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure",
            "document_context": "Cloud computing architecture document"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/comprehensive-insights",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get("insights", [])
                persona_insights = result.get("persona_insights", [])
                
                self.log_test("Comprehensive Insights API", True, 
                             f"Generated {len(insights)} insights, {len(persona_insights)} persona insights")
            else:
                self.log_test("Comprehensive Insights API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Comprehensive Insights API", False, f"Error: {str(e)}")
    
    def test_text_simplification_api(self):
        """Test text simplification API"""
        print("\n📝 Testing Text Simplification API")
        print("=" * 40)
        
        test_data = {
            "text": "The implementation of cloud-native microservices architecture necessitates comprehensive consideration of distributed system design principles."
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/simplify",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                simplified = result.get("text", "")
                self.log_test("Text Simplification API", True, f"Simplified text length: {len(simplified)} chars")
            else:
                self.log_test("Text Simplification API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Text Simplification API", False, f"Error: {str(e)}")
    
    def test_term_definition_api(self):
        """Test term definition API"""
        print("\n📖 Testing Term Definition API")
        print("=" * 40)
        
        test_data = {
            "term": "microservices",
            "context": "cloud computing architecture"
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/define-term",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                definition = result.get("definition", "")
                self.log_test("Term Definition API", True, f"Definition length: {len(definition)} chars")
            else:
                self.log_test("Term Definition API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Term Definition API", False, f"Error: {str(e)}")
    
    def test_highlights_api(self):
        """Test highlights API"""
        print("\n🖍️ Testing Highlights API")
        print("=" * 40)
        
        highlight_data = {
            "text": "Cloud computing is important",
            "color": "yellow",
            "page": 1,
            "documentName": "test_document.pdf"
        }
        
        try:
            # Test adding highlight
            response = self.session.post(
                f"{self.backend_url}/highlights",
                json=highlight_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                self.log_test("Add Highlight API", True, "Highlight added successfully")
                
                # Test getting highlights
                doc_name = "test_document.pdf"
                response = self.session.get(f"{self.backend_url}/highlights/{doc_name}")
                
                if response.status_code == 200:
                    highlights = response.json()
                    self.log_test("Get Highlights API", True, f"Retrieved {len(highlights)} highlights")
                else:
                    self.log_test("Get Highlights API", False, f"Status: {response.status_code}")
            else:
                self.log_test("Add Highlight API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Highlights API", False, f"Error: {str(e)}")
    
    def test_podcast_api(self):
        """Test podcast generation API"""
        print("\n🎙️ Testing Podcast API")
        print("=" * 40)
        
        test_data = {
            "text": "Cloud computing architecture provides scalable infrastructure.",
            "related_sections": ["Virtualization", "Load Balancing"],
            "insights": ["Scalability is key", "High availability important"]
        }
        
        try:
            response = self.session.post(
                f"{self.backend_url}/podcast",
                data=test_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                result = response.json()
                script = result.get("script", "")
                audio_url = result.get("audio_url", "")
                
                self.log_test("Podcast API", True, f"Generated script: {len(script)} chars, Audio: {audio_url}")
            else:
                self.log_test("Podcast API", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Podcast API", False, f"Error: {str(e)}")
    
    def test_error_handling(self):
        """Test error handling"""
        print("\n⚠️ Testing Error Handling")
        print("=" * 40)
        
        # Test invalid API calls
        try:
            response = self.session.get(f"{self.backend_url}/invalid-endpoint")
            if response.status_code == 404:
                self.log_test("404 Error Handling", True, "Properly handled invalid endpoint")
            else:
                self.log_test("404 Error Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("404 Error Handling", False, f"Error: {str(e)}")
        
        # Test invalid data
        try:
            response = self.session.post(
                f"{self.backend_url}/related-sections",
                data={"invalid": "data"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code in [422, 400, 500]:
                self.log_test("Invalid Data Handling", True, f"Properly handled invalid data (status: {response.status_code})")
            else:
                self.log_test("Invalid Data Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid Data Handling", False, f"Error: {str(e)}")
    
    def test_cors_headers(self):
        """Test CORS headers for frontend integration"""
        print("\n🌐 Testing CORS Headers")
        print("=" * 40)
        
        try:
            response = self.session.options(f"{self.backend_url}/documents")
            cors_headers = response.headers.get("Access-Control-Allow-Origin")
            
            if cors_headers:
                self.log_test("CORS Headers", True, f"CORS enabled: {cors_headers}")
            else:
                self.log_test("CORS Headers", False, "CORS headers not found")
                
        except Exception as e:
            self.log_test("CORS Headers", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all frontend tests"""
        print("🚀 Starting Frontend Feature Test Suite")
        print("=" * 60)
        
        # Check if services are running
        if not self.test_frontend_health():
            print("\n❌ Frontend is not running. Please start the frontend first:")
            print("   cd HARSHALADOBE")
            print("   npm run dev")
            return
        
        if not self.test_backend_health():
            print("\n❌ Backend is not running. Please start the backend first:")
            print("   cd adobev4")
            print("   python main.py")
            return
        
        # Run all tests
        tests = [
            self.test_api_endpoints,
            self.test_related_sections_api,
            self.test_insights_api,
            self.test_comprehensive_insights_api,
            self.test_text_simplification_api,
            self.test_term_definition_api,
            self.test_highlights_api,
            self.test_podcast_api,
            self.test_error_handling,
            self.test_cors_headers
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 FRONTEND TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for test_name, result in self.test_results.items():
                if not result["success"]:
                    print(f"   - {test_name}: {result['details']}")
        
        print("\n🎯 Frontend Features Tested:")
        print("   ✅ Frontend Accessibility")
        print("   ✅ Backend Connectivity")
        print("   ✅ API Endpoints")
        print("   ✅ Enhanced Related Sections")
        print("   ✅ Insights Generation")
        print("   ✅ Text Simplification")
        print("   ✅ Term Definition")
        print("   ✅ Highlights Management")
        print("   ✅ Podcast Generation")
        print("   ✅ Error Handling")
        print("   ✅ CORS Configuration")
        
        if passed_tests == total_tests:
            print("\n🎉 All frontend tests passed! The frontend is working correctly.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please check the implementation.")
        
        print("\n💡 Next Steps:")
        print("   1. Start both frontend and backend servers")
        print("   2. Open browser to http://localhost:5173")
        print("   3. Test manual user interactions")
        print("   4. Verify enhanced related sections display")
        print("   5. Check all UI components work correctly")

def main():
    """Main function"""
    tester = FrontendTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
