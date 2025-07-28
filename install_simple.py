#!/usr/bin/env python3
"""
Simple Installation Script - Minimal Dependencies
Installs only essential packages to get the RAG chatbot working
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a pip command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main installation function"""
    print("🚀 Simple Installation - Changi Airport RAG Chatbot")
    print("=" * 60)
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("Please activate your virtual environment first:")
        print("  .\\venv\\Scripts\\Activate.ps1")
        return False
    
    # Install minimal set of packages that should work on Python 3.13
    minimal_packages = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install Flask", "Flask web framework"),
        ("pip install requests", "HTTP requests library"),
        ("pip install python-dotenv", "Environment variable management"),
        ("pip install beautifulsoup4", "HTML parsing library"),
        ("pip install lxml", "XML/HTML parser"),
        ("pip install numpy", "Numerical computing library"),
        ("pip install chromadb", "Vector database"),
        ("pip install langchain", "LangChain framework"),
        ("pip install langchain-community", "LangChain community modules"),
        ("pip install langchain-google-genai", "Google GenAI integration"),
        ("pip install google-generativeai", "Google Generative AI"),
        ("pip install gunicorn", "WSGI server for production")
    ]
    
    for command, description in minimal_packages:
        if not run_command(command, description):
            print(f"⚠️  Skipping {description} due to error")
            continue
    
    print("\n" + "=" * 60)
    print("🎉 Installation completed!")
    print("\nNext steps:")
    print("1. Set up your .env file with GOOGLE_API_KEY")
    print("2. Run: python test_setup.py")
    print("3. Run: python build_index.py")
    print("4. Run: python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 