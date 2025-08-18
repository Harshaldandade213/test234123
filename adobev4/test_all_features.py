#!/usr/bin/env python3
"""
Comprehensive Test Suite for All Application Features
Tests all major functionality including document upload, analysis, related sections, insights, and more.
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_DOCUMENTS_DIR = "test_documents"

class ApplicationTester:
    def __init__(self):
        self.base_url = BASE_URL
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
        
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n🔍 Testing Health Check")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Server is healthy - {data}")
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_document_upload(self):
        """Test document upload functionality"""
        print("\n📄 Testing Document Upload")
        print("=" * 40)
        
        # Create a test document
        test_doc_content = """
        Cloud Computing Architecture
        
        This document discusses the fundamental principles of cloud computing architecture.
        
        Key Components:
        1. Virtualization
        2. Load Balancing
        3. Auto-scaling
        4. Microservices
        
        Virtualization is a key technology that enables cloud computing by abstracting hardware resources.
        Load balancing ensures high availability and performance across multiple servers.
        Auto-scaling allows applications to automatically adjust capacity based on demand.
        Microservices architecture enables better scalability and maintainability.
        """
        
        # Create test document file
        os.makedirs(TEST_DOCUMENTS_DIR, exist_ok=True)
        test_file_path = os.path.join(TEST_DOCUMENTS_DIR, "cloud_computing_test.txt")
        
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_doc_content)
        
        try:
            # Upload the test document
            with open(test_file_path, 'rb') as f:
                files = {'files': ('cloud_computing_test.txt', f, 'text/plain')}
                data = {
                    'persona': 'Software Engineer',
                    'job_to_be_done': 'Design cloud infrastructure'
                }
                
                response = self.session.post(f"{self.base_url}/upload-pdfs", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_test("Document Upload", True, f"Uploaded {len(result)} document(s)")
                    
                    # Store document ID for later tests
                    if result:
                        self.test_results["uploaded_doc_id"] = result[0].get("id")
                        self.test_results["uploaded_doc_name"] = result[0].get("name")
                    
                    return True
                else:
                    self.log_test("Document Upload", False, f"Status: {response.status_code}, Response: {response.text}")
                    return False
                    
        except Exception as e:
            self.log_test("Document Upload", False, f"Error: {str(e)}")
            return False
        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_get_documents(self):
        """Test retrieving documents"""
        print("\n📚 Testing Get Documents")
        print("=" * 40)
        
        try:
            response = self.session.get(f"{self.base_url}/documents")
            
            if response.status_code == 200:
                documents = response.json()
                self.log_test("Get Documents", True, f"Retrieved {len(documents)} document(s)")
                return True
            else:
                self.log_test("Get Documents", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Get Documents", False, f"Error: {str(e)}")
            return False
    
    def test_related_sections(self):
        """Test enhanced related sections functionality"""
        print("\n🔗 Testing Related Sections")
        print("=" * 40)
        
        # Get uploaded document ID
        doc_id = self.test_results.get("uploaded_doc_id")
        if not doc_id:
            self.log_test("Related Sections", False, "No document ID available")
            return False
        
        test_data = {
            "document_ids": [doc_id],
            "current_page": 1,
            "current_section": "Cloud Computing Architecture",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/related-sections",
                data=test_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                result = response.json()
                sections = result.get("related_sections", [])
                
                # Check for enhanced fields
                enhanced_fields_present = False
                for section in sections:
                    if 'relationship_type' in section or 'key_concepts' in section:
                        enhanced_fields_present = True
                        break
                
                self.log_test("Related Sections", True, 
                             f"Found {len(sections)} sections, Enhanced fields: {enhanced_fields_present}")
                return True
            else:
                self.log_test("Related Sections", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Related Sections", False, f"Error: {str(e)}")
            return False
    
    def test_analyze_query(self):
        """Test query analysis functionality"""
        print("\n🔍 Testing Query Analysis")
        print("=" * 40)
        
        doc_id = self.test_results.get("uploaded_doc_id")
        if not doc_id:
            self.log_test("Query Analysis", False, "No document ID available")
            return False
        
        test_data = {
            "query": "cloud computing virtualization",
            "document_ids": json.dumps([doc_id])
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/analyze-query",
                data=test_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get("analysis", [])
                
                self.log_test("Query Analysis", True, f"Generated {len(analysis)} analysis items")
                return True
            else:
                self.log_test("Query Analysis", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Query Analysis", False, f"Error: {str(e)}")
            return False
    
    def test_generate_insights(self):
        """Test insights generation"""
        print("\n💡 Testing Insights Generation")
        print("=" * 40)
        
        test_data = {
            "text": "Cloud computing provides scalable infrastructure for modern applications.",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure",
            "document_context": "Cloud computing architecture document"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/insights",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get("insights", [])
                
                self.log_test("Insights Generation", True, f"Generated {len(insights)} insights")
                return True
            else:
                self.log_test("Insights Generation", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Insights Generation", False, f"Error: {str(e)}")
            return False
    
    def test_comprehensive_insights(self):
        """Test comprehensive insights generation"""
        print("\n🧠 Testing Comprehensive Insights")
        print("=" * 40)
        
        test_data = {
            "text": "Microservices architecture enables better scalability and maintainability in cloud applications.",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure",
            "document_context": "Cloud computing architecture document"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/comprehensive-insights",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result.get("insights", [])
                persona_insights = result.get("persona_insights", [])
                
                self.log_test("Comprehensive Insights", True, 
                             f"Generated {len(insights)} insights, {len(persona_insights)} persona insights")
                return True
            else:
                self.log_test("Comprehensive Insights", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Comprehensive Insights", False, f"Error: {str(e)}")
            return False
    
    def test_strategic_insights(self):
        """Test strategic insights generation"""
        print("\n🎯 Testing Strategic Insights")
        print("=" * 40)
        
        test_data = {
            "text": "Implementing cloud-native architecture requires careful planning and consideration of scalability factors.",
            "persona": "Software Engineer",
            "job_to_be_done": "Design cloud infrastructure",
            "document_context": "Cloud computing architecture document"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/strategic-insights",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                strategic = result.get("strategic_insights", {})
                
                opportunities = strategic.get("opportunities", [])
                risks = strategic.get("risks", [])
                action_items = strategic.get("action_items", [])
                
                self.log_test("Strategic Insights", True, 
                             f"Generated {len(opportunities)} opportunities, {len(risks)} risks, {len(action_items)} action items")
                return True
            else:
                self.log_test("Strategic Insights", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Strategic Insights", False, f"Error: {str(e)}")
            return False
    
    def test_simplify_text(self):
        """Test text simplification"""
        print("\n📝 Testing Text Simplification")
        print("=" * 40)
        
        test_data = {
            "text": "The implementation of cloud-native microservices architecture necessitates comprehensive consideration of distributed system design principles and scalability paradigms."
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/simplify",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                simplified = result.get("text", "")
                
                self.log_test("Text Simplification", True, f"Simplified text length: {len(simplified)} characters")
                return True
            else:
                self.log_test("Text Simplification", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Text Simplification", False, f"Error: {str(e)}")
            return False
    
    def test_define_term(self):
        """Test term definition"""
        print("\n📖 Testing Term Definition")
        print("=" * 40)
        
        test_data = {
            "term": "microservices",
            "context": "cloud computing architecture"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/define-term",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                definition = result.get("definition", "")
                
                self.log_test("Term Definition", True, f"Definition length: {len(definition)} characters")
                return True
            else:
                self.log_test("Term Definition", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Term Definition", False, f"Error: {str(e)}")
            return False
    
    def test_cross_connections(self):
        """Test cross-connections functionality"""
        print("\n🔗 Testing Cross-Connections")
        print("=" * 40)
        
        doc_id = self.test_results.get("uploaded_doc_id")
        if not doc_id:
            self.log_test("Cross-Connections", False, "No document ID available")
            return False
        
        try:
            response = self.session.get(f"{self.base_url}/cross-connections/{doc_id}")
            
            if response.status_code == 200:
                result = response.json()
                related_docs = result.get("related_documents", [])
                insights = result.get("insights", [])
                
                self.log_test("Cross-Connections", True, 
                             f"Found {len(related_docs)} related documents, {len(insights)} insights")
                return True
            else:
                self.log_test("Cross-Connections", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Cross-Connections", False, f"Error: {str(e)}")
            return False
    
    def test_podcast_generation(self):
        """Test podcast generation"""
        print("\n🎙️ Testing Podcast Generation")
        print("=" * 40)
        
        test_data = {
            "text": "Cloud computing architecture provides scalable infrastructure for modern applications.",
            "related_sections": ["Virtualization", "Load Balancing"],
            "insights": ["Scalability is key", "High availability important"]
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/podcast",
                data=test_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                result = response.json()
                script = result.get("script", "")
                audio_url = result.get("audio_url", "")
                
                self.log_test("Podcast Generation", True, f"Generated script: {len(script)} chars, Audio URL: {audio_url}")
                return True
            else:
                self.log_test("Podcast Generation", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Podcast Generation", False, f"Error: {str(e)}")
            return False
    
    def test_highlights(self):
        """Test highlights functionality"""
        print("\n🖍️ Testing Highlights")
        print("=" * 40)
        
        # Test adding highlight
        highlight_data = {
            "text": "Cloud computing is important",
            "color": "yellow",
            "page": 1,
            "documentName": "test_document.pdf"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/highlights",
                json=highlight_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                self.log_test("Add Highlight", True, "Highlight added successfully")
                
                # Test getting highlights
                doc_name = "test_document.pdf"
                response = self.session.get(f"{self.base_url}/highlights/{doc_name}")
                
                if response.status_code == 200:
                    highlights = response.json()
                    self.log_test("Get Highlights", True, f"Retrieved {len(highlights)} highlights")
                    return True
                else:
                    self.log_test("Get Highlights", False, f"Status: {response.status_code}")
                    return False
            else:
                self.log_test("Add Highlight", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Highlights", False, f"Error: {str(e)}")
            return False
    
    def test_library_endpoints(self):
        """Test library-related endpoints"""
        print("\n📚 Testing Library Endpoints")
        print("=" * 40)
        
        try:
            # Test get personas
            response = self.session.get(f"{self.base_url}/library/personas")
            if response.status_code == 200:
                personas = response.json()
                self.log_test("Get Personas", True, f"Retrieved {len(personas)} personas")
            else:
                self.log_test("Get Personas", False, f"Status: {response.status_code}")
            
            # Test get jobs
            response = self.session.get(f"{self.base_url}/library/jobs")
            if response.status_code == 200:
                jobs = response.json()
                self.log_test("Get Jobs", True, f"Retrieved {len(jobs)} jobs")
            else:
                self.log_test("Get Jobs", False, f"Status: {response.status_code}")
            
            # Test get library documents
            response = self.session.get(f"{self.base_url}/library/documents")
            if response.status_code == 200:
                documents = response.json()
                self.log_test("Get Library Documents", True, f"Retrieved {len(documents)} documents")
            else:
                self.log_test("Get Library Documents", False, f"Status: {response.status_code}")
            
            return True
            
        except Exception as e:
            self.log_test("Library Endpoints", False, f"Error: {str(e)}")
            return False
    
    def test_reading_progress(self):
        """Test reading progress tracking"""
        print("\n📊 Testing Reading Progress")
        print("=" * 40)
        
        doc_id = self.test_results.get("uploaded_doc_id")
        if not doc_id:
            self.log_test("Reading Progress", False, "No document ID available")
            return False
        
        test_data = {
            "doc_id": doc_id,
            "current_page": 5,
            "total_pages": 10,
            "time_spent": 300  # 5 minutes in seconds
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/reading-progress",
                data=test_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                result = response.json()
                progress = result.get("progress_percentage", 0)
                time_spent = result.get("time_spent_minutes", 0)
                
                self.log_test("Reading Progress", True, f"Progress: {progress}%, Time spent: {time_spent} minutes")
                return True
            else:
                self.log_test("Reading Progress", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Reading Progress", False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        print("\n⚠️ Testing Error Handling")
        print("=" * 40)
        
        # Test invalid endpoint
        try:
            response = self.session.get(f"{self.base_url}/invalid-endpoint")
            if response.status_code == 404:
                self.log_test("404 Error Handling", True, "Properly handled invalid endpoint")
            else:
                self.log_test("404 Error Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("404 Error Handling", False, f"Error: {str(e)}")
        
        # Test invalid data
        try:
            response = self.session.post(
                f"{self.base_url}/related-sections",
                data={"invalid": "data"},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            if response.status_code in [422, 400, 500]:
                self.log_test("Invalid Data Handling", True, f"Properly handled invalid data (status: {response.status_code})")
            else:
                self.log_test("Invalid Data Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid Data Handling", False, f"Error: {str(e)}")
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Application Test Suite")
        print("=" * 60)
        
        # Check if server is running
        if not self.test_health_check():
            print("\n❌ Server is not running. Please start the server first:")
            print("   cd adobev4")
            print("   python main.py")
            return
        
        # Run all tests
        tests = [
            self.test_document_upload,
            self.test_get_documents,
            self.test_related_sections,
            self.test_analyze_query,
            self.test_generate_insights,
            self.test_comprehensive_insights,
            self.test_strategic_insights,
            self.test_simplify_text,
            self.test_define_term,
            self.test_cross_connections,
            self.test_podcast_generation,
            self.test_highlights,
            self.test_library_endpoints,
            self.test_reading_progress,
            self.test_error_handling
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
        print("📊 TEST SUMMARY")
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
        
        print("\n🎯 Key Features Tested:")
        print("   ✅ Document Upload & Management")
        print("   ✅ Enhanced Related Sections")
        print("   ✅ Query Analysis")
        print("   ✅ Insights Generation (Basic, Comprehensive, Strategic)")
        print("   ✅ Text Simplification")
        print("   ✅ Term Definition")
        print("   ✅ Cross-Connections")
        print("   ✅ Podcast Generation")
        print("   ✅ Highlights Management")
        print("   ✅ Library Endpoints")
        print("   ✅ Reading Progress Tracking")
        print("   ✅ Error Handling")
        
        if passed_tests == total_tests:
            print("\n🎉 All tests passed! The application is working correctly.")
        else:
            print(f"\n⚠️ {failed_tests} test(s) failed. Please check the implementation.")

def main():
    """Main function"""
    tester = ApplicationTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
