#!/usr/bin/env python3
"""
Simple PDF Document Testing Script
This script uploads PDF documents and tests endpoints directly.
"""

import requests
import json
import time
import random
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

def upload_pdf_document():
    """Upload the PDF document from the documents directory"""
    print_section("Document Upload - PDF Document")
    
    documents_dir = Path("documents")
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print_test_result("Upload PDF", False, "No PDF files found in documents directory")
        return None
    
    pdf_file = pdf_files[0]  # Use the first PDF file
    print(f"📄 Found PDF file: {pdf_file.name}")
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {'files': (pdf_file.name, f, 'application/pdf')}
            data = {
                'persona': 'Research Analyst',
                'job_to_be_done': 'Analyzing academic documents for insights'
            }
            
            response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
            
            if response.status_code == 200:
                uploaded_docs = response.json()
                print_test_result("Upload PDF", True, f"Uploaded {len(uploaded_docs)} documents")
                
                if uploaded_docs:
                    doc_id = uploaded_docs[0]['id']
                    doc_name = uploaded_docs[0]['name']
                    print(f"   📄 Document ID: {doc_id}")
                    print(f"   📄 Document Name: {doc_name}")
                    print(f"   📄 Title: {uploaded_docs[0]['title']}")
                    print(f"   📄 Language: {uploaded_docs[0]['language']}")
                    print(f"   📄 Upload Time: {uploaded_docs[0]['upload_timestamp']}")
                    
                    # Print outline preview
                    outline = uploaded_docs[0].get('outline', [])
                    if outline:
                        print(f"   📄 Outline Preview:")
                        for i, section in enumerate(outline[:3]):  # Show first 3 sections
                            print(f"      {i+1}. {section['text'][:80]}...")
                    
                    return doc_id
                else:
                    print_test_result("Upload PDF", False, "No documents returned from upload")
                    return None
            else:
                print_test_result("Upload PDF", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                return None
    except Exception as e:
        print_test_result("Upload PDF", False, f"Error: {e}")
        return None

def test_analyze_documents(doc_id):
    """Test document analysis with the uploaded document"""
    print_section("Document Analysis Testing")
    
    # Generate different analysis queries
    queries = [
        "Analyze the design principles discussed in this document",
        "What are the key insights about usability mentioned?",
        "Summarize the main findings and recommendations"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 Testing Analysis Query {i}: {query}")
        
        try:
            payload = {
                "document_ids": [doc_id],
                "persona": "Research Analyst",
                "job_to_be_done": f"Analyzing document for insights about design and usability"
            }
            
            response = requests.post(
                f"{BASE_URL}/analyze-documents",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                insights_count = len(data.get('insights', []))
                print_test_result(f"Analyze Documents - Query {i}", True, f"Generated {insights_count} insights")
                
                # Show sample insights
                if insights_count > 0:
                    print(f"   📊 Sample insights:")
                    for j, insight in enumerate(data['insights'][:2], 1):  # Show first 2 insights
                        print(f"      {j}. {insight[:100]}...")
            else:
                print_test_result(f"Analyze Documents - Query {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Analyze Documents - Query {i}", False, f"Error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_insights_generation(doc_id):
    """Test insights generation with document-related content"""
    print_section("AI Insights Generation Testing")
    
    # Test with design and usability related content
    test_texts = [
        "Design principles and usability guidelines for user-centered design",
        "Good and bad design examples with user experience insights",
        "Human-centered design methodology and implementation strategies"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🔍 Testing Insights Generation {i}: {text[:50]}...")
        
        try:
            payload = {
                "text": text,
                "persona": "UX Designer",
                "job_to_be_done": "Understanding design principles and usability guidelines",
                "document_context": f"Analyzing document about design and usability: {doc_id}"
            }
            
            response = requests.post(
                f"{BASE_URL}/insights",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                insights_count = len(data.get('insights', []))
                print_test_result(f"Generate Insights - Test {i}", True, f"Generated {insights_count} insights")
                
                # Show insights
                if insights_count > 0:
                    print(f"   📊 Sample insights:")
                    for j, insight in enumerate(data['insights'][:2], 1):
                        print(f"      {j}. [{insight['type']}] {insight['content'][:80]}...")
            else:
                print_test_result(f"Generate Insights - Test {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Generate Insights - Test {i}", False, f"Error: {e}")
        
        time.sleep(1)

def test_comprehensive_insights(doc_id):
    """Test comprehensive insights generation"""
    print_section("Comprehensive Insights Testing")
    
    test_text = "Design principles and usability guidelines for creating user-centered interfaces that enhance user experience and improve overall product effectiveness"
    
    print(f"🔍 Testing with comprehensive analysis: {test_text[:60]}...")
    
    try:
        payload = {
            "text": test_text,
            "persona": "UX Research Manager",
            "job_to_be_done": "Comprehensive analysis of design and usability principles",
            "document_context": f"Analyzing design document: {doc_id}"
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
            
            # Show sample data
            if keywords_count > 0:
                print(f"   🔑 Keywords: {', '.join(data['keywords'][:5])}")
            
            if 'topic_analysis' in data:
                topic_analysis = data['topic_analysis']
                print(f"   📊 Topic Analysis:")
                print(f"      Main themes: {topic_analysis.get('main_themes', 'N/A')[:50]}...")
                print(f"      Trending topics: {topic_analysis.get('trending_topics', 'N/A')[:50]}...")
        else:
            print_test_result("Comprehensive Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Comprehensive Insights", False, f"Error: {e}")

def test_text_simplification():
    """Test text simplification with complex design terminology"""
    print_section("Text Simplification Testing")
    
    complex_texts = [
        "The implementation of user-centered design methodologies necessitates comprehensive understanding of human-computer interaction paradigms and cognitive psychology principles",
        "Usability heuristics and interface design guidelines require systematic evaluation of user experience metrics and accessibility compliance standards",
        "Human-centered design processes involve iterative prototyping methodologies and user feedback integration mechanisms"
    ]
    
    for i, text in enumerate(complex_texts, 1):
        print(f"\n🔍 Testing simplification {i}: {text[:50]}...")
        
        try:
            payload = {
                "text": text
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
                
                print_test_result(f"Simplify Text - Test {i}", True, f"Original: {len(original)} chars, Simplified: {len(simplified)} chars")
                print(f"   📝 Original: {original[:60]}...")
                print(f"   ✨ Simplified: {simplified[:60]}...")
            else:
                print_test_result(f"Simplify Text - Test {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Simplify Text - Test {i}", False, f"Error: {e}")
        
        time.sleep(1)

def test_term_definition():
    """Test term definition with design and UX terms"""
    print_section("Term Definition Testing")
    
    terms_and_contexts = [
        ("usability", "In the context of user interface design and user experience"),
        ("heuristics", "When discussing design evaluation methods and user interface guidelines"),
        ("prototyping", "In the context of iterative design processes and user testing")
    ]
    
    for i, (term, context) in enumerate(terms_and_contexts, 1):
        print(f"\n🔍 Testing term definition {i}: {term}")
        
        try:
            payload = {
                "term": term,
                "context": context
            }
            
            response = requests.post(
                f"{BASE_URL}/define-term",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                definition = data.get('definition', '')
                
                print_test_result(f"Define Term - Test {i}", True, f"Definition length: {len(definition)} chars")
                print(f"   📖 Definition: {definition[:120]}...")
            else:
                print_test_result(f"Define Term - Test {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Define Term - Test {i}", False, f"Error: {e}")
        
        time.sleep(1)

def test_reading_progress(doc_id):
    """Test reading progress tracking"""
    print_section("Reading Progress Testing")
    
    # Test multiple progress updates
    progress_scenarios = [
        {"current_page": 5, "total_pages": 20, "time_spent": 600},   # 10 minutes
        {"current_page": 12, "total_pages": 20, "time_spent": 1200}, # 20 minutes
        {"current_page": 18, "total_pages": 20, "time_spent": 1800}  # 30 minutes
    ]
    
    for i, scenario in enumerate(progress_scenarios, 1):
        print(f"\n🔍 Testing reading progress scenario {i}: Page {scenario['current_page']}/{scenario['total_pages']}")
        
        try:
            payload = {
                "doc_id": doc_id,
                "current_page": scenario['current_page'],
                "total_pages": scenario['total_pages'],
                "time_spent": scenario['time_spent']
            }
            
            response = requests.post(
                f"{BASE_URL}/reading-progress",
                data=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                progress = data.get('progress_percentage', 0)
                time_spent_minutes = data.get('time_spent_minutes', 0)
                
                print_test_result(f"Track Reading Progress - Scenario {i}", True, 
                                f"Progress: {progress:.1f}%, Time spent: {time_spent_minutes:.1f} minutes")
                print(f"   📖 Page {scenario['current_page']} of {scenario['total_pages']}")
                print(f"   ⏱️ Time spent: {time_spent_minutes:.1f} minutes")
                print(f"   📊 Progress: {progress:.1f}%")
            else:
                print_test_result(f"Track Reading Progress - Scenario {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Track Reading Progress - Scenario {i}", False, f"Error: {e}")
        
        time.sleep(1)

def test_library_functions():
    """Test library-related functions"""
    print_section("Library Functions Testing")
    
    try:
        # Test getting all documents
        response = requests.get(f"{BASE_URL}/documents")
        if response.status_code == 200:
            documents = response.json()
            print_test_result("Get All Documents", True, f"Found {len(documents)} documents")
        
        # Test getting personas
        response = requests.get(f"{BASE_URL}/library/personas")
        if response.status_code == 200:
            personas = response.json()
            print_test_result("Get Personas", True, f"Found {len(personas)} personas: {personas}")
        
        # Test library documents with different filters
        filters = [
            "?persona=research",
            "?persona=designer", 
            "?job_to_be_done=analysis",
            "?persona=research&job_to_be_done=analysis"
        ]
        
        for i, filter_query in enumerate(filters, 1):
            response = requests.get(f"{BASE_URL}/library/documents{filter_query}")
            if response.status_code == 200:
                filtered_docs = response.json()
                print_test_result(f"Get Library Documents (filter {i})", True, f"Found {len(filtered_docs)} documents")
        
        return True
    except Exception as e:
        print_test_result("Library Functions", False, f"Error: {e}")
        return False

def main():
    """Run comprehensive PDF document testing"""
    print("🚀 Simple PDF Document Testing")
    print("=" * 60)
    print(f"🌐 Testing server at: {BASE_URL}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Upload PDF document
    doc_id = upload_pdf_document()
    if not doc_id:
        print("❌ Failed to upload PDF document. Exiting.")
        return
    
    # Step 2: Test all endpoints with the document
    test_analyze_documents(doc_id)
    test_insights_generation(doc_id)
    test_comprehensive_insights(doc_id)
    test_text_simplification()
    test_term_definition()
    test_reading_progress(doc_id)
    test_library_functions()
    
    # Print summary
    print_section("Test Summary")
    print(f"📄 Document ID: {doc_id}")
    print(f"📊 Tested all major endpoints with design/UX focused content")
    print(f"🎯 Focused on design principles, usability, and user experience topics")
    
    print(f"\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")
    
    print(f"\n🎉 PDF Document Testing Complete!")

if __name__ == "__main__":
    main()
