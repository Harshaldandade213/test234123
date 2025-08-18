#!/usr/bin/env python3
"""
Debug script to test upload and status endpoints
"""
import requests
import json
import os

BASE_URL = "http://localhost:8000"

def debug_upload_and_status():
    """Debug the upload and status flow."""
    
    # Test data
    test_data = {
        "persona": "Debug User",
        "job_to_be_done": "Debug upload functionality"
    }
    
    # Use an existing PDF file
    uploads_dir = "HARSHALADOBE/backend/uploads"
    if os.path.exists(uploads_dir):
        pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
        if pdf_files:
            test_pdf_path = os.path.join(uploads_dir, pdf_files[0])
            print(f"📄 Using PDF file: {pdf_files[0]}")
            
            with open(test_pdf_path, 'rb') as f:
                files = {'files': (f'debug_test.pdf', f, 'application/pdf')}
                
                print("📤 Uploading document...")
                response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=test_data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Upload successful!")
                    print(f"   Response: {json.dumps(result, indent=2)}")
                    
                    if result:
                        doc_id = result[0]['id']
                        print(f"   Document ID: {doc_id}")
                        print(f"   Document ID length: {len(doc_id)}")
                        
                        # Test status endpoint
                        print(f"\n📊 Testing status for document ID: {doc_id}")
                        status_response = requests.get(f"{BASE_URL}/documents/{doc_id}/status", timeout=10)
                        
                        print(f"   Status response code: {status_response.status_code}")
                        if status_response.status_code == 200:
                            status = status_response.json()
                            print(f"   Status response: {json.dumps(status, indent=2)}")
                        else:
                            print(f"   Status error: {status_response.text}")
                        
                        # Test getting all documents
                        print(f"\n📋 Getting all documents...")
                        docs_response = requests.get(f"{BASE_URL}/documents", timeout=10)
                        if docs_response.status_code == 200:
                            all_docs = docs_response.json()
                            print(f"   Found {len(all_docs)} documents")
                            for doc in all_docs:
                                print(f"   - {doc['id']}: {doc['name']}")
                        else:
                            print(f"   Error getting documents: {docs_response.text}")
                    else:
                        print("❌ No documents returned from upload")
                else:
                    print(f"❌ Upload failed: {response.status_code}")
                    print(f"   Error: {response.text}")
        else:
            print("❌ No PDF files found")
    else:
        print("❌ Uploads directory not found")

if __name__ == "__main__":
    debug_upload_and_status()
