#!/usr/bin/env python3
"""
Simplified Dependency Installation Script
Installs dependencies without pandas to avoid build issues
Compatible with Python 3.13
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

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  Python 3.13+ detected - using compatible package versions")
        return "3.13+"
    elif version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return "3.8-3.12"
    else:
        print("❌ Python 3.8+ is required")
        return None

def main():
    """Main installation function"""
    print("🚀 Installing Changi Airport RAG Chatbot Dependencies")
    print("=" * 60)
    
    # Check Python version
    python_version = check_python_version()
    if not python_version:
        return False
    
    # Check if virtual environment is active
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("Please activate your virtual environment first:")
        print("  .\\venv\\Scripts\\Activate.ps1")
        return False
    
    # Upgrade pip and setuptools with specific versions for Python 3.13
    if python_version == "3.13+":
        print("🔧 Installing Python 3.13+ compatible versions...")
        if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
            return False
        if not run_command("pip install setuptools>=69.0.0 wheel>=0.42.0", "Installing compatible setuptools and wheel"):
            return False
    else:
        if not run_command("python -m pip install --upgrade pip setuptools wheel", "Upgrading pip and setuptools"):
            return False
    
    # Install dependencies in order with specific versions for Python 3.13
    if python_version == "3.13+":
        dependencies = [
            ("Flask==3.0.0", "Flask web framework"),
            ("requests==2.31.0", "HTTP requests library"),
            ("python-dotenv==1.0.0", "Environment variable management"),
            ("beautifulsoup4==4.12.2", "HTML parsing library"),
            ("lxml==5.1.0", "XML/HTML parser"),
            ("urllib3==2.1.0", "HTTP client library"),
            ("numpy==1.26.4", "Numerical computing library"),
            ("chromadb==0.4.22", "Vector database"),
            ("langchain==0.1.0", "LangChain framework"),
            ("langchain-google-genai==0.0.6", "Google GenAI integration"),
            ("google-generativeai==0.3.2", "Google Generative AI"),
            ("gunicorn==21.2.0", "WSGI server for production")
        ]
    else:
        dependencies = [
            ("Flask==2.3.3", "Flask web framework"),
            ("requests==2.31.0", "HTTP requests library"),
            ("python-dotenv==1.0.0", "Environment variable management"),
            ("beautifulsoup4==4.12.2", "HTML parsing library"),
            ("lxml==4.9.3", "XML/HTML parser"),
            ("urllib3==2.0.7", "HTTP client library"),
            ("numpy==1.24.3", "Numerical computing library"),
            ("chromadb==0.4.22", "Vector database"),
            ("langchain==0.0.350", "LangChain framework"),
            ("langchain-google-genai==0.0.5", "Google GenAI integration"),
            ("google-generativeai==0.3.2", "Google Generative AI"),
            ("gunicorn==21.2.0", "WSGI server for production")
        ]
    
    for package, description in dependencies:
        # Try with --only-binary=all first
        command = f"pip install {package} --only-binary=all"
        if not run_command(command, f"Installing {description}"):
            print(f"⚠️  Trying without --only-binary flag for {package}")
            command = f"pip install {package}"
            if not run_command(command, f"Installing {description} (fallback)"):
                print(f"⚠️  Trying with --no-deps for {package}")
                command = f"pip install {package} --no-deps"
                if not run_command(command, f"Installing {description} (no-deps)"):
                    return False
    
    print("\n" + "=" * 60)
    print("🎉 All dependencies installed successfully!")
    print("\nNext steps:")
    print("1. Set up your .env file with GOOGLE_API_KEY")
    print("2. Run: python test_setup.py")
    print("3. Run: python build_index.py")
    print("4. Run: python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 