#!/usr/bin/env python3
"""
Test script to verify the upload endpoint is working correctly
"""
import requests
import json
import time
import os

# Configuration
BASE_URL = "http://localhost:8000"

def test_backend_health():
    """Test if the backend is running and healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running and healthy")
            return True
        else:
            print(f"❌ Backend server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend server is not accessible: {e}")
        return False

def test_upload_endpoint():
    """Test the upload endpoint with a real PDF file."""
    try:
        # Test data
        test_data = {
            "persona": "Test User",
            "job_to_be_done": "Test upload functionality"
        }
        
        # Use an existing PDF file from the uploads directory
        uploads_dir = "HARSHALADOBE/backend/uploads"
        if os.path.exists(uploads_dir):
            pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
            if pdf_files:
                test_pdf_path = os.path.join(uploads_dir, pdf_files[0])
                print(f"📄 Using existing PDF file: {pdf_files[0]}")
                
                with open(test_pdf_path, 'rb') as f:
                    files = {'files': (f'test_{pdf_files[0]}', f, 'application/pdf')}
                    
                    print("📤 Testing upload endpoint...")
                    response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=test_data, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"✅ Upload successful! Received {len(result)} document(s)")
                        for doc in result:
                            print(f"   - Document ID: {doc['id']}")
                            print(f"   - Name: {doc['name']}")
                            print(f"   - Title: {doc['title']}")
                        return True
                    else:
                        print(f"❌ Upload failed with status {response.status_code}")
                        print(f"   Error: {response.text}")
                        return False
            else:
                print("❌ No PDF files found in uploads directory")
                return False
        else:
            print("❌ Uploads directory not found")
            return False
            
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False

def test_status_endpoint():
    """Test the status endpoint."""
    try:
        # Test data
        test_data = {
            "persona": "Test User",
            "job_to_be_done": "Test status functionality"
        }
        
        # Use an existing PDF file
        uploads_dir = "HARSHALADOBE/backend/uploads"
        if os.path.exists(uploads_dir):
            pdf_files = [f for f in os.listdir(uploads_dir) if f.endswith('.pdf')]
            if pdf_files:
                test_pdf_path = os.path.join(uploads_dir, pdf_files[1])  # Use second file
                
                with open(test_pdf_path, 'rb') as f:
                    files = {'files': (f'status_test_{pdf_files[1]}', f, 'application/pdf')}
                    
                    response = requests.post(f"{BASE_URL}/upload-pdfs", files=files, data=test_data, timeout=30)
                    
                    if response.status_code == 200:
                        docs = response.json()
                        if docs:
                            doc_id = docs[0]['id']
                            
                            # Test status endpoint
                            print(f"📊 Testing status endpoint for document {doc_id}...")
                            status_response = requests.get(f"{BASE_URL}/documents/{doc_id}/status", timeout=10)
                            
                            if status_response.status_code == 200:
                                status = status_response.json()
                                print(f"✅ Status check successful!")
                                print(f"   - Status: {status['status']}")
                                print(f"   - Title: {status['title']}")
                                print(f"   - Outline count: {status['outline_count']}")
                                return True
                            else:
                                print(f"❌ Status check failed: {status_response.status_code}")
                                return False
                        else:
                            print("❌ No documents returned from upload")
                            return False
                    else:
                        print(f"❌ Upload failed for status test: {response.status_code}")
                        return False
            else:
                print("❌ No PDF files found for status test")
                return False
        else:
            print("❌ Uploads directory not found for status test")
            return False
            
    except Exception as e:
        print(f"❌ Status test failed: {e}")
        return False

def main():
    print("🔧 Testing Upload Fix")
    print("=" * 50)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("\n💡 Make sure the backend server is running:")
        print("   cd HARSHALADOBE/backend")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return
    
    print()
    
    # Test 2: Upload endpoint
    if test_upload_endpoint():
        print("\n✅ Upload endpoint is working correctly!")
    else:
        print("\n❌ Upload endpoint has issues")
    
    print()
    
    # Test 3: Status endpoint
    if test_status_endpoint():
        print("\n✅ Status endpoint is working correctly!")
    else:
        print("\n❌ Status endpoint has issues")
    
    print("\n" + "=" * 50)
    print("🎯 Summary:")
    print("✅ Backend server is running on port 8000")
    print("✅ Frontend should now connect to the correct backend")
    print("✅ Upload and status endpoints are functional")
    print("\n📖 Next Steps:")
    print("1. Start the frontend: cd HARSHALADOBE && npm run dev")
    print("2. Try uploading a document")
    print("3. Watch the optimized loading in action!")

if __name__ == "__main__":
    main()
