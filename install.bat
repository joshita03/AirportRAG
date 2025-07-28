@echo off
echo 🚀 Installing Changi Airport RAG Chatbot Dependencies
echo ====================================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and setuptools
echo Upgrading pip and setuptools...
python -m pip install --upgrade pip setuptools wheel

REM Install dependencies with minimal versions
echo Installing dependencies...
pip install Flask
pip install requests
pip install python-dotenv
pip install beautifulsoup4
pip install lxml
pip install numpy
pip install chromadb
pip install langchain
pip install langchain-community
pip install langchain-google-genai
pip install google-generativeai
pip install gunicorn

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 Installation completed successfully!
    echo.
    echo Next steps:
    echo 1. Copy env_example.txt to .env and add your Google API key
    echo 2. Run: python test_setup.py
    echo 3. Run: python build_index.py
    echo 4. Run: python run.py
) else (
    echo.
    echo ❌ Installation failed. Please check the error messages above.
)

pause 