#!/usr/bin/env python3
"""
Test script to add a PDF file to documents_db and test the PDF endpoint
"""
import os
import sys
import uuid
from datetime import datetime

# Add the current directory to the path so we can import from main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the documents_db from main.py
from main import documents_db, get_document_metadata

def test_pdf_endpoint():
    print("🧪 Testing PDF Endpoint")
    print("=" * 50)
    
    # Find a PDF file in the documents directory
    documents_dir = "documents"
    pdf_files = [f for f in os.listdir(documents_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in documents directory")
        return False
    
    # Use the first PDF file
    pdf_filename = pdf_files[0]
    pdf_path = os.path.join(documents_dir, pdf_filename)
    
    print(f"📄 Using PDF file: {pdf_filename}")
    print(f"📄 Full path: {pdf_path}")
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    # Generate a test document ID
    test_doc_id = "7b6dd023-3d8f-4574-969e-caa4808e52fa"  # Use the same ID from the error
    
    # Create document metadata
    metadata = get_document_metadata(pdf_path, pdf_filename)
    if not metadata:
        print("❌ Failed to extract metadata from PDF")
        return False
    
    # Override the ID to match the one from the error
    metadata["id"] = test_doc_id
    
    # Add to documents_db
    documents_db[test_doc_id] = metadata
    
    print(f"✅ Added document to documents_db:")
    print(f"   ID: {metadata['id']}")
    print(f"   Name: {metadata['name']}")
    print(f"   File path: {metadata['file_path']}")
    print(f"   Title: {metadata['title']}")
    
    # Test the PDF endpoint
    print("\n🔍 Testing PDF endpoint...")
    
    import requests
    try:
        response = requests.get(f"http://localhost:8000/pdf/{test_doc_id}")
        if response.status_code == 200:
            print("✅ PDF endpoint working correctly!")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Content-Length: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ PDF endpoint failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing PDF endpoint: {e}")
        return False

if __name__ == "__main__":
    success = test_pdf_endpoint()
    if success:
        print("\n🎉 PDF endpoint test completed successfully!")
    else:
        print("\n❌ PDF endpoint test failed!")
        sys.exit(1)
