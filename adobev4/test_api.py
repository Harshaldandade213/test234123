#!/usr/bin/env python3
"""
API Test Script
This script tests the basic functionality of the FastAPI backend server.
"""

import requests
import json
import time
import os

# API Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "health": "/health",
    "documents": "/documents",
    "personas": "/library/personas",
    "insights": "/insights",
    "simplify": "/simplify-text",
    "define": "/define-term"
}

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}{API_ENDPOINTS['health']}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_documents():
    """Test getting documents"""
    print("\n📚 Testing get documents...")
    try:
        response = requests.get(f"{BASE_URL}{API_ENDPOINTS['documents']}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get documents successful: {len(data)} documents found")
            return True
        else:
            print(f"❌ Get documents failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get documents error: {e}")
        return False

def test_get_personas():
    """Test getting personas"""
    print("\n👥 Testing get personas...")
    try:
        response = requests.get(f"{BASE_URL}{API_ENDPOINTS['personas']}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Get personas successful: {len(data)} personas found")
            return True
        else:
            print(f"❌ Get personas failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get personas error: {e}")
        return False

def test_generate_insights():
    """Test generating insights"""
    print("\n💡 Testing generate insights...")
    try:
        payload = {
            "text": "Artificial intelligence is transforming the way we work and live. Machine learning algorithms are becoming more sophisticated and accessible.",
            "persona": "Technology Professional",
            "job_to_be_done": "Understanding AI trends and applications"
        }
        
        response = requests.post(
            f"{BASE_URL}{API_ENDPOINTS['insights']}", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generate insights successful: {len(data.get('insights', []))} insights generated")
            return True
        else:
            print(f"❌ Generate insights failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Generate insights error: {e}")
        return False

def test_simplify_text():
    """Test text simplification"""
    print("\n📝 Testing simplify text...")
    try:
        payload = {
            "text": "The implementation of artificial intelligence algorithms necessitates comprehensive understanding of machine learning paradigms and neural network architectures."
        }
        
        response = requests.post(
            f"{BASE_URL}{API_ENDPOINTS['simplify']}", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Simplify text successful")
            print(f"Original: {data.get('original', '')[:50]}...")
            print(f"Simplified: {data.get('text', '')[:50]}...")
            return True
        else:
            print(f"❌ Simplify text failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Simplify text error: {e}")
        return False

def test_define_term():
    """Test term definition"""
    print("\n📖 Testing define term...")
    try:
        payload = {
            "term": "machine learning",
            "context": "In the context of artificial intelligence and data science"
        }
        
        response = requests.post(
            f"{BASE_URL}{API_ENDPOINTS['define']}", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Define term successful")
            print(f"Definition: {data.get('definition', '')[:100]}...")
            return True
        else:
            print(f"❌ Define term failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Define term error: {e}")
        return False

def test_comprehensive_insights():
    """Test comprehensive insights"""
    print("\n🔍 Testing comprehensive insights...")
    try:
        payload = {
            "text": "The rapid advancement of artificial intelligence technologies is reshaping industries across the globe. Companies are increasingly adopting AI solutions to improve efficiency and gain competitive advantages.",
            "persona": "Business Executive",
            "job_to_be_done": "Evaluating AI adoption strategies"
        }
        
        response = requests.post(
            f"{BASE_URL}/comprehensive-insights", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comprehensive insights successful")
            print(f"Insights: {len(data.get('insights', []))}")
            print(f"Persona insights: {len(data.get('persona_insights', []))}")
            print(f"Keywords: {len(data.get('keywords', []))}")
            return True
        else:
            print(f"❌ Comprehensive insights failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Comprehensive insights error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 API Test Suite")
    print("=" * 50)
    
    # Check if server is running
    print("🔌 Checking if server is running...")
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python run_server.py")
        return
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Get Documents", test_get_documents),
        ("Get Personas", test_get_personas),
        ("Generate Insights", test_generate_insights),
        ("Simplify Text", test_simplify_text),
        ("Define Term", test_define_term),
        ("Comprehensive Insights", test_comprehensive_insights)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the server logs for more details.")
    
    print("\n📚 API Documentation available at:")
    print(f"   {BASE_URL}/docs")
    print(f"   {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
