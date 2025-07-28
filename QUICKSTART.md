# 🚀 Quick Start Guide - Changi Airport RAG Chatbot

Get your Changi Airport RAG chatbot up and running in 5 minutes!

## ⚡ Super Quick Setup

### 1. Install Dependencies

**Option A: Simple Installation (Recommended for Python 3.13)**
```bash
# Use the simple installation script
python install_simple.py

# Or use PowerShell (Windows)
.\install.ps1

# Or use batch file (Windows)
.\install.bat
```

**Option B: Advanced Installation**
```bash
# Use the advanced installation script
python install_dependencies.py

# Or install manually
pip install Flask requests python-dotenv beautifulsoup4 lxml numpy chromadb langchain langchain-google-genai google-generativeai gunicorn
```

### 2. Set Up Environment
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Test Embeddings
```bash
python test_embeddings.py
```

### 5. Build the Index
```bash
python build_index.py
```

### 6. Run the Application
```bash
python run.py
```

### 7. Open in Browser
Navigate to: http://localhost:5000

## 🎯 Test Questions

Try these example questions in the chat interface:

- "What is the Rain Vortex?"
- "How many terminals does Changi Airport have?"
- "What are the operating hours of Jewel Changi Airport?"
- "What airlines operate from Changi Airport?"
- "What shopping options are available?"

## 🔧 Troubleshooting

### Common Issues:

**❌ "GOOGLE_API_KEY not found"**
- Make sure you created a `.env` file
- Verify your API key is correct
- Get a free API key from: https://makersuite.google.com/app/apikey

**❌ "Module not found"**
- Run: `python install_simple.py`
- Or install manually: `pip install Flask requests python-dotenv beautifulsoup4 lxml numpy chromadb langchain langchain-community langchain-google-genai google-generativeai gunicorn`
- Make sure you're in the correct directory

**❌ "Vector store not initialized"**
- Run: `python scripts/build_index.py`
- This scrapes the websites and builds the search database

**❌ "Scraping failed"**
- Check your internet connection
- The websites might be temporarily unavailable
- Try running the build script again

## 📱 API Usage

### Ask a Question via API:
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the Rain Vortex?"}'
```

### Check Health:
```bash
curl http://localhost:5000/api/health
```

## 🚀 Deploy to Render.com

1. Push your code to GitHub
2. Connect to Render.com
3. Set environment variables:
   - `GOOGLE_API_KEY`: Your API key
   - `FLASK_ENV`: `production`
4. Deploy!

## 📞 Need Help?

1. Check the logs for error messages
2. Run `python test_setup.py` to diagnose issues
3. Verify your API key is working
4. Make sure all dependencies are installed

---

**Happy chatting! ✈️** 