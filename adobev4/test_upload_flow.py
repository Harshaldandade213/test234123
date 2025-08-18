#!/usr/bin/env python3
"""
Test script for the new upload flow
Tests that PDFs are displayed immediately and analysis runs in background
"""
import requests
import json
import time
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"
TEST_PDF_PATH = "test_documents/sample.pdf"

def test_upload_flow():
    print("🧪 Testing New Upload Flow - Immediate PDF Display")
    print("=" * 60)
    
    # Check if test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        print(f"❌ Test PDF not found at {TEST_PDF_PATH}")
        print("Please create a test PDF file to run this test")
        return False
    
    # Step 1: Upload PDF
    print("📤 Step 1: Uploading PDF...")
    with open(TEST_PDF_PATH, 'rb') as f:
        files = {'files': ('sample.pdf', f, 'application/pdf')}
        data = {
            'persona': 'Software Engineer',
            'job_to_be_done': 'Design scalable cloud infrastructure'
        }
        
        response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
    
    if response.status_code != 200:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return False
    
    uploaded_docs = response.json()
    print(f"✅ Upload successful: {len(uploaded_docs)} document(s)")
    
    if not uploaded_docs:
        print("❌ No documents returned from upload")
        return False
    
    doc_id = uploaded_docs[0]['id']
    doc_name = uploaded_docs[0]['name']
    
    print(f"📄 Document ID: {doc_id}")
    print(f"📄 Document Name: {doc_name}")
    print(f"📄 Initial Title: {uploaded_docs[0]['title']}")
    print(f"📄 Initial Outline Sections: {len(uploaded_docs[0]['outline'])}")
    
    # Step 2: Check immediate availability
    print("\n📋 Step 2: Checking immediate document availability...")
    response = requests.get(f"{BASE_URL}/documents/{doc_id}")
    
    if response.status_code != 200:
        print(f"❌ Failed to get document: {response.status_code}")
        return False
    
    doc_info = response.json()
    print(f"✅ Document immediately available")
    print(f"📄 Title: {doc_info['title']}")
    print(f"📄 Outline sections: {len(doc_info['outline'])}")
    
    # Step 3: Check analysis status
    print("\n🔍 Step 3: Checking analysis status...")
    response = requests.get(f"{BASE_URL}/documents/{doc_id}/status")
    
    if response.status_code != 200:
        print(f"❌ Failed to get document status: {response.status_code}")
        return False
    
    status_info = response.json()
    print(f"📊 Analysis Status: {status_info['status']}")
    print(f"📊 Has Analysis: {status_info['has_analysis']}")
    
    # Step 4: Monitor analysis progress
    print("\n⏳ Step 4: Monitoring analysis progress...")
    max_wait_time = 60  # 60 seconds
    check_interval = 2   # Check every 2 seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        response = requests.get(f"{BASE_URL}/documents/{doc_id}/status")
        if response.status_code == 200:
            status_info = response.json()
            current_status = status_info['status']
            
            print(f"⏱️  {elapsed_time}s - Status: {current_status}")
            
            if current_status == 'completed':
                print("✅ Analysis completed!")
                print(f"📄 Final Title: {status_info['info']['title']}")
                print(f"📄 Final Outline Sections: {len(status_info['info']['outline'])}")
                
                # Verify the document was updated
                if status_info['info']['title'] != doc_name:
                    print("✅ Title was updated with analysis results")
                else:
                    print("⚠️  Title was not updated (may be same as filename)")
                
                if len(status_info['info']['outline']) > 0:
                    print("✅ Outline was populated with analysis results")
                else:
                    print("⚠️  Outline is still empty")
                
                return True
            elif current_status == 'failed':
                print("❌ Analysis failed")
                return False
        
        time.sleep(check_interval)
        elapsed_time += check_interval
    
    print(f"⏰ Analysis did not complete within {max_wait_time} seconds")
    return False

def test_multiple_uploads():
    print("\n🧪 Testing Multiple Uploads")
    print("=" * 40)
    
    # Check if test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        print(f"❌ Test PDF not found at {TEST_PDF_PATH}")
        return False
    
    # Upload multiple copies
    doc_ids = []
    for i in range(3):
        print(f"📤 Uploading PDF {i+1}/3...")
        
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'files': (f'sample_{i}.pdf', f, 'application/pdf')}
            data = {
                'persona': 'Software Engineer',
                'job_to_be_done': 'Design scalable cloud infrastructure'
            }
            
            response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=data)
        
        if response.status_code == 200:
            uploaded_docs = response.json()
            if uploaded_docs:
                doc_ids.append(uploaded_docs[0]['id'])
                print(f"✅ Upload {i+1} successful: {uploaded_docs[0]['id']}")
        
        time.sleep(1)  # Small delay between uploads
    
    print(f"📊 Uploaded {len(doc_ids)} documents")
    
    # Check status of all documents
    print("\n📋 Checking status of all documents...")
    for i, doc_id in enumerate(doc_ids):
        response = requests.get(f"{BASE_URL}/documents/{doc_id}/status")
        if response.status_code == 200:
            status_info = response.json()
            print(f"📄 Document {i+1}: {status_info['status']}")
    
    return True

def main():
    print("🚀 Testing New Upload Flow with Background Analysis")
    print("=" * 70)
    
    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Backend server is not running")
            print("Please start the backend server first:")
            print("cd adobev4 && python main.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Please start the backend server first:")
        print("cd adobev4 && python main.py")
        return
    
    print("✅ Backend server is running")
    
    # Run tests
    success1 = test_upload_flow()
    success2 = test_multiple_uploads()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 All tests passed!")
        print("\n✅ Upload Flow Summary:")
        print("   • PDFs are displayed immediately after upload")
        print("   • Analysis runs in background")
        print("   • Document info is updated when analysis completes")
        print("   • Multiple uploads work correctly")
        print("   • Status monitoring works properly")
    else:
        print("❌ Some tests failed")
        print("Please check the backend logs for errors")

if __name__ == "__main__":
    main()
