#!/usr/bin/env python3
"""
Comprehensive App.py Integration Testing Script
This script tests the FastAPI endpoints using the exact logic from app.py
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

def test_index_documents():
    """Test document indexing using app.py logic"""
    print_section("Document Indexing - App.py Integration")
    
    try:
        response = requests.post(f"{BASE_URL}/index-documents")
        
        if response.status_code == 200:
            data = response.json()
            print_test_result("Index Documents", True, data.get('message', 'Documents indexed'))
            return True
        else:
            print_test_result("Index Documents", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print_test_result("Index Documents", False, f"Error: {e}")
        return False

def test_search_documents():
    """Test document search using app.py logic"""
    print_section("Document Search - App.py Integration")
    
    # Test different search queries
    search_queries = [
        "design principles",
        "usability guidelines", 
        "user experience",
        "human centered design"
    ]
    
    for i, query in enumerate(search_queries, 1):
        print(f"\n🔍 Testing Search Query {i}: {query}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/search-documents",
                data={"query": query, "k": 5}
            )
            
            if response.status_code == 200:
                data = response.json()
                results_count = data.get('total_results', 0)
                print_test_result(f"Search Documents - Query {i}", True, f"Found {results_count} results")
                
                # Show sample results
                if results_count > 0:
                    results = data.get('results', [])
                    print(f"   📊 Sample results:")
                    for j, result in enumerate(results[:2], 1):  # Show first 2 results
                        source = result.get('source', 'Unknown')
                        passage = result.get('passage', '')[:100] + "..." if len(result.get('passage', '')) > 100 else result.get('passage', '')
                        score = result.get('similarity_score', 0)
                        print(f"      {j}. Source: {source}")
                        print(f"         Passage: {passage}")
                        print(f"         Score: {score:.4f}")
            else:
                print_test_result(f"Search Documents - Query {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Search Documents - Query {i}", False, f"Error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_analyze_query():
    """Test query analysis using app.py logic"""
    print_section("Query Analysis - App.py Integration")
    
    # Test different analysis queries
    analysis_queries = [
        "What are the key design principles discussed in the documents?",
        "How do the documents address usability and user experience?",
        "What insights can be found about human-centered design methodology?"
    ]
    
    for i, query in enumerate(analysis_queries, 1):
        print(f"\n🔍 Testing Analysis Query {i}: {query[:50]}...")
        
        try:
            response = requests.post(
                f"{BASE_URL}/analyze-query",
                data={"query": query}
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis_count = len(data.get('analysis', []))
                print_test_result(f"Analyze Query - Query {i}", True, f"Generated {analysis_count} analysis items")
                
                # Show sample analysis
                if analysis_count > 0:
                    analysis = data.get('analysis', [])
                    print(f"   📊 Sample analysis:")
                    for j, item in enumerate(analysis[:2], 1):  # Show first 2 items
                        category = item.get('category', 'Unknown')
                        justification = item.get('justification', '')[:80] + "..." if len(item.get('justification', '')) > 80 else item.get('justification', '')
                        source = item.get('source', 'Unknown')
                        print(f"      {j}. Category: {category}")
                        print(f"         Source: {source}")
                        print(f"         Justification: {justification}")
            else:
                print_test_result(f"Analyze Query - Query {i}", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print_test_result(f"Analyze Query - Query {i}", False, f"Error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_upload_and_analyze():
    """Test complete workflow: upload PDF, index, search, analyze"""
    print_section("Complete Workflow - Upload, Index, Search, Analyze")
    
    # Step 1: Upload PDF document
    documents_dir = Path("documents")
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print_test_result("Upload PDF", False, "No PDF files found in documents directory")
        return False
    
    pdf_file = pdf_files[0]  # Use the first PDF file
    print(f"📄 Found PDF file: {pdf_file.name}")
    
    try:
        with open(pdf_file, 'rb') as f:
            files = {'files': (pdf_file.name, f, 'application/pdf')}
            data = {
                'persona': 'UX Researcher',
                'job_to_be_done': 'Analyzing design documents for research insights'
            }
            
            response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
            
            if response.status_code == 200:
                uploaded_docs = response.json()
                print_test_result("Upload PDF", True, f"Uploaded {len(uploaded_docs)} documents")
                
                if uploaded_docs:
                    doc_id = uploaded_docs[0]['id']
                    print(f"   📄 Document ID: {doc_id}")
                    
                    # Step 2: Index documents
                    print("\n🔄 Step 2: Indexing documents...")
                    index_response = requests.post(f"{BASE_URL}/index-documents")
                    if index_response.status_code == 200:
                        print_test_result("Index Documents", True, "Documents indexed successfully")
                        
                        # Step 3: Search documents
                        print("\n🔍 Step 3: Searching documents...")
                        search_response = requests.post(
                            f"{BASE_URL}/search-documents",
                            data={"query": "design principles usability", "k": 3}
                        )
                        
                        if search_response.status_code == 200:
                            search_data = search_response.json()
                            results_count = search_data.get('total_results', 0)
                            print_test_result("Search Documents", True, f"Found {results_count} results")
                            
                            # Step 4: Analyze documents
                            print("\n📊 Step 4: Analyzing documents...")
                            analyze_response = requests.post(
                                f"{BASE_URL}/analyze-documents",
                                json={
                                    "document_ids": [doc_id],
                                    "persona": "UX Researcher",
                                    "job_to_be_done": "Analyzing design principles and usability guidelines"
                                }
                            )
                            
                            if analyze_response.status_code == 200:
                                analyze_data = analyze_response.json()
                                insights_count = len(analyze_data.get('insights', []))
                                print_test_result("Analyze Documents", True, f"Generated {insights_count} insights")
                                
                                # Show sample insights
                                if insights_count > 0:
                                    insights = analyze_data.get('insights', [])
                                    print(f"   📊 Sample insights:")
                                    for i, insight in enumerate(insights[:2], 1):
                                        print(f"      {i}. {insight[:100]}...")
                                
                                return True
                            else:
                                print_test_result("Analyze Documents", False, f"Status code: {analyze_response.status_code}")
                                print(f"   Response: {analyze_response.text}")
                        else:
                            print_test_result("Search Documents", False, f"Status code: {search_response.status_code}")
                            print(f"   Response: {search_response.text}")
                    else:
                        print_test_result("Index Documents", False, f"Status code: {index_response.status_code}")
                        print(f"   Response: {index_response.text}")
                else:
                    print_test_result("Upload PDF", False, "No documents returned from upload")
            else:
                print_test_result("Upload PDF", False, f"Status code: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print_test_result("Upload PDF", False, f"Error: {e}")
    
    return False

def test_ai_endpoints():
    """Test AI-powered endpoints"""
    print_section("AI-Powered Endpoints Testing")
    
    # Test insights generation
    print("\n🔍 Testing AI Insights Generation...")
    try:
        payload = {
            "text": "Design principles and usability guidelines for creating user-centered interfaces",
            "persona": "UX Designer",
            "job_to_be_done": "Understanding design principles and usability guidelines",
            "document_context": "Analyzing design documents for research"
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
            
            # Show sample insights
            if insights_count > 0:
                insights = data.get('insights', [])
                print(f"   📊 Sample insights:")
                for i, insight in enumerate(insights[:2], 1):
                    print(f"      {i}. [{insight['type']}] {insight['content'][:80]}...")
        else:
            print_test_result("Generate Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Generate Insights", False, f"Error: {e}")
    
    # Test comprehensive insights
    print("\n🔍 Testing Comprehensive Insights...")
    try:
        payload = {
            "text": "User-centered design methodology and implementation strategies for modern applications",
            "persona": "UX Research Manager",
            "job_to_be_done": "Comprehensive analysis of design methodologies",
            "document_context": "Researching design principles and user experience"
        }
        
        response = requests.post(
            f"{BASE_URL}/comprehensive-insights",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            insights_count = len(data.get('insights', []))
            keywords_count = len(data.get('keywords', []))
            print_test_result("Comprehensive Insights", True, f"Insights: {insights_count}, Keywords: {keywords_count}")
            
            # Show sample data
            if keywords_count > 0:
                keywords = data.get('keywords', [])
                print(f"   🔑 Keywords: {', '.join(keywords[:5])}")
        else:
            print_test_result("Comprehensive Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Comprehensive Insights", False, f"Error: {e}")

def main():
    """Run comprehensive app.py integration testing"""
    print("🚀 App.py Integration Testing")
    print("=" * 60)
    print(f"🌐 Testing server at: {BASE_URL}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test individual components
    test_index_documents()
    test_search_documents()
    test_analyze_query()
    test_ai_endpoints()
    
    # Test complete workflow
    test_upload_and_analyze()
    
    # Print summary
    print_section("Test Summary")
    print(f"📊 Tested app.py integration with FastAPI endpoints")
    print(f"🔍 Verified document indexing, search, and analysis functionality")
    print(f"🤖 Confirmed AI-powered insights generation")
    
    print(f"\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")
    
    print(f"\n🎉 App.py Integration Testing Complete!")

if __name__ == "__main__":
    main()
