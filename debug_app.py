#!/usr/bin/env python3
"""
Debug script to test the Flask app and API responses
"""

import requests
import json
import os
from dotenv import load_dotenv

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🔍 Testing Changi Airport RAG Chatbot API")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test stats endpoint
    print("2. Testing stats endpoint...")
    try:
        response = requests.get(f"{base_url}/api/stats")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test example questions
    print("3. Testing example questions...")
    try:
        response = requests.get(f"{base_url}/api/example-questions")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Found {data.get('count', 0)} example questions")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Test asking a question
    print("4. Testing ask endpoint...")
    try:
        question = "What is the Rain Vortex?"
        response = requests.post(
            f"{base_url}/api/ask",
            headers={"Content-Type": "application/json"},
            json={"question": question}
        )
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Question: {question}")
        print(f"   Answer: {data.get('answer', 'No answer')}")
        print(f"   Sources: {len(data.get('sources', []))} sources")
        if 'error' in data:
            print(f"   Error: {data['error']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    print("🎯 Debug test completed!")

if __name__ == "__main__":
    test_api() 