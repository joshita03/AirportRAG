# ✈️ Changi Airport RAG Chatbot

A full-stack Flask application that functions as a Retrieval-Augmented Generation (RAG) chatbot for Changi Airport and Jewel Changi Airport information. The chatbot scrapes content from official websites and provides intelligent responses to user queries.

## 🚀 Features

- **Web Scraping**: Automatically scrapes content from Changi Airport and Jewel Changi Airport websites
- **RAG Pipeline**: Uses Google Gemini 2.0 Flash for embeddings and text generation
- **Vector Storage**: ChromaDB vector database for efficient similarity search
- **Modern UI**: Beautiful, responsive chat interface
- **RESTful API**: Complete API endpoints for integration
- **Production Ready**: Configured for deployment on Render.com

## 🏗️ Architecture

```
changi-airport-rag/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render.com deployment config
├── env_example.txt       # Environment variables template
├── README.md             # This file
├── modules/
│   ├── scraper.py        # Web scraping module
│   ├── text_splitter.py  # Text processing and chunking
│   └── rag_pipeline.py   # RAG pipeline with FAISS and Gemini
├── scripts/
│   └── build_index.py    # Standalone index building script
├── templates/
│   └── chat.html         # Chat interface template
└── data/                 # Vector index storage (created automatically)
```

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: Google Gemini Embeddings
- **Vector Database**: ChromaDB (Embedding Database)
- **Web Scraping**: BeautifulSoup4
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Render.com

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for web scraping

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd changi-airport-rag
```

### 2. Install Dependencies

```bash
# Use the simplified installation script (recommended)
python install_dependencies.py

# Or install manually with pre-built wheels
pip install Flask==2.3.3 requests==2.31.0 beautifulsoup4==4.12.2 python-dotenv==1.0.0 chromadb langchain==0.0.350 langchain-google-genai==0.0.5 google-generativeai==0.3.2 numpy==1.24.3 lxml==4.9.3 urllib3==2.0.7 gunicorn==21.2.0 --only-binary=all
```

### 3. Environment Configuration

Create a `.env` file based on `env_example.txt`:

```bash
cp env_example.txt .env
```

Edit `.env` and add your Google API key:

```env
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

### 4. Build the Index

Run the index building script to scrape websites and create the vector database:

```bash
python scripts/build_index.py
```

This will:
- Scrape content from Changi Airport and Jewel Changi Airport websites
- Process and chunk the text
- Generate embeddings using Google Gemini
- Store vectors in ChromaDB database

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🌐 API Endpoints

### Health Check
```
GET /api/health
```
Returns the health status of the application and RAG pipeline.

### Ask Question
```
POST /api/ask
Content-Type: application/json

{
    "question": "What is the Rain Vortex?"
}
```
Returns a response with answer and sources.

### Build Index
```
POST /api/build-index
```
Triggers the scraping and index building process.

### Get Statistics
```
GET /api/stats
```
Returns statistics about the vector store and system status.

### Example Questions
```
GET /api/example-questions
```
Returns a list of example questions for testing.

## 🎯 Example Usage

### Using the Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Type your question in the chat interface
3. Click "Send" or press Enter
4. View the response with source citations

### Using the API

```python
import requests

# Ask a question
response = requests.post('http://localhost:5000/api/ask', 
    json={'question': 'What is the Rain Vortex?'})
data = response.json()

print("Answer:", data['answer'])
print("Sources:", data['sources'])
```

### Example Questions to Try

- "What is the Rain Vortex at Jewel Changi Airport?"
- "How many terminals does Changi Airport have?"
- "What are the operating hours of Jewel Changi Airport?"
- "What airlines operate from Changi Airport?"
- "What shopping options are available at Changi Airport?"
- "How do I get to Jewel Changi Airport from the city?"
- "What restaurants are available at Changi Airport?"
- "What is the Shiseido Forest Valley?"
- "How far is Changi Airport from Singapore city center?"
- "What transportation options are available from Changi Airport?"

## 🚀 Deployment on Render.com

### 1. Prepare for Deployment

The application is already configured for Render.com deployment with:
- `Procfile` for process management
- `requirements.txt` for dependencies
- Environment variable support

### 2. Deploy on Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following environment variables in Render:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `False`

### 3. Build Command

The build command will automatically install dependencies and build the index:

```bash
python install_dependencies.py && python build_index.py
```

### 4. Start Command

```bash
gunicorn app:app
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Debug mode | `False` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `TOP_K_RESULTS` | Number of similar documents | `5` |

### Customization

#### Modify Scraping Behavior

Edit `modules/scraper.py` to:
- Change the number of pages to scrape
- Modify content extraction logic
- Add new websites to scrape

#### Adjust Text Processing

Edit `modules/text_splitter.py` to:
- Change chunk size and overlap
- Modify text cleaning rules
- Add custom text processing

#### Update RAG Pipeline

Edit `modules/rag_pipeline.py` to:
- Change the LLM model
- Modify the prompt template
- Adjust similarity search parameters

## 🧪 Testing

### Manual Testing

1. Start the application
2. Use the web interface to ask questions
3. Verify responses are relevant and accurate
4. Check that sources are properly cited

### API Testing

```bash
# Health check
curl http://localhost:5000/api/health

# Ask a question
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the Rain Vortex?"}'

# Get stats
curl http://localhost:5000/api/stats
```

## 📊 Monitoring and Logs

The application includes comprehensive logging:

- **Application logs**: Flask application events
- **Scraping logs**: Website scraping progress
- **RAG logs**: Vector search and generation events
- **Error logs**: Detailed error information

## 🔒 Security Considerations

- API keys are stored in environment variables
- Input validation on all API endpoints
- Rate limiting for web scraping
- Error handling for all external API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Changi Airport Group for the website content
- Google for the Gemini AI models
- ChromaDB for vector storage
- The open-source community for the tools and libraries used

## 📞 Support

For issues and questions:
1. Check the logs for error messages
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check that the index was built successfully

---

**Note**: This application scrapes publicly available information from Changi Airport websites. Please respect the websites' terms of service and robots.txt files when using this application. 