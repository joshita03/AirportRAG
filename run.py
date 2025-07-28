#!/usr/bin/env python3
"""
Startup Script for Changi Airport RAG Chatbot
Checks setup and runs the Flask application
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import flask
        import requests
        import beautifulsoup4
        import langchain
        import chromadb
        import google.generativeai
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_index():
    """Check if the vector database exists"""
    db_path = "data/changi_airport_chroma"
    if os.path.exists(db_path):
        print("✅ Vector database found")
        return True
    else:
        print("⚠️  Vector database not found")
        print("You may need to build the index first:")
        print("python scripts/build_index.py")
        return True  # Don't fail, just warn

def main():
    """Main startup function"""
    print("🚀 Starting Changi Airport RAG Chatbot")
    print("=" * 50)
    
    # Check setup
    if not check_environment():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    check_index()
    
    print("\n🎯 Starting Flask application...")
    print("The application will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run the Flask app
    try:
        from app import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 