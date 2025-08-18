#!/usr/bin/env python3
"""
Comprehensive PDF Document Testing Script
This script uploads PDF documents, extracts content, generates random queries, and tests all related endpoints.
"""

import requests
import json
import time
import os
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

def get_document_content(doc_id):
    """Get the uploaded document content for query generation"""
    print_section("Document Content Retrieval")
    
    try:
        response = requests.get(f"{BASE_URL}/documents")
        if response.status_code == 200:
            documents = response.json()
            for doc in documents:
                if doc['id'] == doc_id:
                    content = doc.get('content', '')
                    print_test_result("Get Document Content", True, f"Retrieved {len(content)} characters")
                    return content
        return None
    except Exception as e:
        print_test_result("Get Document Content", False, f"Error: {e}")
        return None

def generate_random_queries(content, num_queries=5):
    """Generate random queries from document content"""
    print_section("Query Generation")
    
    if not content:
        print_test_result("Generate Queries", False, "No content available")
        return []
    
    # Split content into sentences and extract meaningful phrases
    sentences = content.split('.')
    meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(meaningful_sentences) < 3:
        print_test_result("Generate Queries", False, "Not enough content for query generation")
        return []
    
    # Generate different types of queries
    queries = []
    
    # 1. Random sentence queries
    for i in range(min(2, len(meaningful_sentences))):
        sentence = random.choice(meaningful_sentences)
        if len(sentence) > 50:
            sentence = sentence[:50] + "..."
        queries.append({
            "type": "sentence",
            "query": sentence,
            "description": f"Random sentence from document"
        })
    
    # 2. Keyword-based queries
    words = content.split()
    meaningful_words = [w for w in words if len(w) > 5 and w.isalpha()]
    if meaningful_words:
        keywords = random.sample(meaningful_words, min(3, len(meaningful_words)))
        queries.append({
            "type": "keywords",
            "query": " ".join(keywords),
            "description": f"Keywords: {', '.join(keywords)}"
        })
    
    # 3. Topic-based queries
    topics = ["analysis", "research", "findings", "methodology", "conclusion"]
    selected_topic = random.choice(topics)
    queries.append({
        "type": "topic",
        "query": f"discuss {selected_topic}",
        "description": f"Topic-based query: {selected_topic}"
    })
    
    # 4. Summary query
    queries.append({
        "type": "summary",
        "query": "provide a summary of the main points",
        "description": "Summary request"
    })
    
    print_test_result("Generate Queries", True, f"Generated {len(queries)} queries")
    for i, query in enumerate(queries, 1):
        print(f"   {i}. [{query['type']}] {query['query'][:60]}...")
    
    return queries

def test_analyze_documents(doc_id, queries):
    """Test document analysis with generated queries"""
    print_section("Document Analysis Testing")
    
    if not queries:
        print_test_result("Analyze Documents", False, "No queries available")
        return
    
    for i, query_info in enumerate(queries[:3], 1):  # Test first 3 queries
        print(f"\n🔍 Testing Query {i}: {query_info['type']}")
        print(f"   Query: {query_info['query']}")
        
        try:
            payload = {
                "document_ids": [doc_id],
                "persona": "Research Analyst",
                "job_to_be_done": f"Analyzing document for {query_info['type']} insights"
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

def test_insights_generation(doc_id, queries):
    """Test insights generation with document content"""
    print_section("AI Insights Generation Testing")
    
    if not queries:
        print_test_result("Generate Insights", False, "No queries available")
        return
    
    # Test with a sample query
    query_info = queries[0]
    print(f"🔍 Testing with query: {query_info['query']}")
    
    try:
        payload = {
            "text": query_info['query'],
            "persona": "Research Analyst",
            "job_to_be_done": "Extracting insights from academic document",
            "document_context": f"Analyzing document ID: {doc_id}"
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
            
            # Show insights
            if insights_count > 0:
                print(f"   📊 Insights:")
                for i, insight in enumerate(data['insights'], 1):
                    print(f"      {i}. [{insight['type']}] {insight['content'][:100]}...")
        else:
            print_test_result("Generate Insights", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Generate Insights", False, f"Error: {e}")

def test_comprehensive_insights(doc_id, queries):
    """Test comprehensive insights generation"""
    print_section("Comprehensive Insights Testing")
    
    if not queries:
        print_test_result("Comprehensive Insights", False, "No queries available")
        return
    
    # Test with a sample query
    query_info = queries[1] if len(queries) > 1 else queries[0]
    print(f"🔍 Testing with query: {query_info['query']}")
    
    try:
        payload = {
            "text": query_info['query'],
            "persona": "Research Analyst",
            "job_to_be_done": "Comprehensive analysis of academic document",
            "document_context": f"Analyzing document ID: {doc_id}"
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

def test_text_simplification(queries):
    """Test text simplification with complex queries"""
    print_section("Text Simplification Testing")
    
    if not queries:
        print_test_result("Simplify Text", False, "No queries available")
        return
    
    # Find a complex query for simplification
    complex_query = None
    for query_info in queries:
        if len(query_info['query']) > 30:  # Look for longer queries
            complex_query = query_info['query']
            break
    
    if not complex_query:
        complex_query = queries[0]['query']
    
    print(f"🔍 Testing with complex text: {complex_query[:50]}...")
    
    try:
        payload = {
            "text": complex_query
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
        else:
            print_test_result("Simplify Text", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Simplify Text", False, f"Error: {e}")

def test_term_definition(queries):
    """Test term definition with terms from queries"""
    print_section("Term Definition Testing")
    
    if not queries:
        print_test_result("Define Term", False, "No queries available")
        return
    
    # Extract potential terms from queries
    terms = []
    for query_info in queries:
        words = query_info['query'].split()
        for word in words:
            if len(word) > 5 and word.isalpha() and word.lower() not in ['analysis', 'research', 'document', 'provide', 'discuss']:
                terms.append(word)
                break
    
    if not terms:
        terms = ['analysis', 'research']
    
    term = random.choice(terms)
    context = f"From document analysis query: {queries[0]['query']}"
    
    print(f"🔍 Testing term definition for: {term}")
    
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
            
            print_test_result("Define Term", True, f"Definition length: {len(definition)} chars")
            print(f"   📖 Definition: {definition[:150]}...")
        else:
            print_test_result("Define Term", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Define Term", False, f"Error: {e}")

def test_reading_progress(doc_id):
    """Test reading progress tracking"""
    print_section("Reading Progress Testing")
    
    try:
        # Simulate reading progress
        current_page = random.randint(1, 10)
        total_pages = random.randint(15, 25)
        time_spent = random.randint(300, 1800)  # 5-30 minutes in seconds
        
        payload = {
            "doc_id": doc_id,
            "current_page": current_page,
            "total_pages": total_pages,
            "time_spent": time_spent
        }
        
        response = requests.post(
            f"{BASE_URL}/reading-progress",
            data=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            progress = data.get('progress_percentage', 0)
            time_spent_minutes = data.get('time_spent_minutes', 0)
            
            print_test_result("Track Reading Progress", True, 
                            f"Progress: {progress:.1f}%, Time spent: {time_spent_minutes:.1f} minutes")
            print(f"   📖 Page {current_page} of {total_pages}")
            print(f"   ⏱️ Time spent: {time_spent_minutes:.1f} minutes")
            print(f"   📊 Progress: {progress:.1f}%")
        else:
            print_test_result("Track Reading Progress", False, f"Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print_test_result("Track Reading Progress", False, f"Error: {e}")

def test_library_functions(doc_id):
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
        
        # Test library documents with filters
        response = requests.get(f"{BASE_URL}/library/documents?persona=research")
        if response.status_code == 200:
            filtered_docs = response.json()
            print_test_result("Get Library Documents (filtered)", True, f"Found {len(filtered_docs)} documents")
        
        return True
    except Exception as e:
        print_test_result("Library Functions", False, f"Error: {e}")
        return False

def main():
    """Run comprehensive PDF document testing"""
    print("🚀 Comprehensive PDF Document Testing")
    print("=" * 60)
    print(f"🌐 Testing server at: {BASE_URL}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Upload PDF document
    doc_id = upload_pdf_document()
    if not doc_id:
        print("❌ Failed to upload PDF document. Exiting.")
        return
    
    # Step 2: Get document content
    content = get_document_content(doc_id)
    if not content:
        print("❌ Failed to get document content. Exiting.")
        return
    
    # Step 3: Generate random queries
    queries = generate_random_queries(content, num_queries=5)
    if not queries:
        print("❌ Failed to generate queries. Exiting.")
        return
    
    # Step 4: Test all endpoints with the document
    test_analyze_documents(doc_id, queries)
    test_insights_generation(doc_id, queries)
    test_comprehensive_insights(doc_id, queries)
    test_text_simplification(queries)
    test_term_definition(queries)
    test_reading_progress(doc_id)
    test_library_functions(doc_id)
    
    # Print summary
    print_section("Test Summary")
    print(f"📄 Document ID: {doc_id}")
    print(f"🔍 Generated {len(queries)} queries from document content")
    print(f"📊 Tested all major endpoints with real document data")
    
    print(f"\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")
    
    print(f"\n🎉 PDF Document Testing Complete!")

if __name__ == "__main__":
    main()
