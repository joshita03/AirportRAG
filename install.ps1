# PowerShell Installation Script for Changi Airport RAG Chatbot
# Run this script in PowerShell with: .\install.ps1

Write-Host "🚀 Installing Changi Airport RAG Chatbot Dependencies" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies one by one
$packages = @(
    "Flask",
    "requests", 
    "python-dotenv",
    "beautifulsoup4",
    "lxml",
    "numpy",
    "chromadb",
    "langchain",
    "langchain-community",
    "langchain-google-genai",
    "google-generativeai",
    "gunicorn"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Yellow
    try {
        pip install $package
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
        Write-Host "Continuing with other packages..." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Installation completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy env_example.txt to .env and add your Google API key" -ForegroundColor White
Write-Host "2. Run: python test_setup.py" -ForegroundColor White
Write-Host "3. Run: python build_index.py" -ForegroundColor White
Write-Host "4. Run: python run.py" -ForegroundColor White

Read-Host "Press Enter to continue" 