"""
Changi Airport RAG Chatbot - Main Flask Application
A full-stack Flask application with RAG capabilities for Changi Airport information
"""

import os
import logging
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime

# Import our modules
from modules.scraper import ChangiAirportScraper
from modules.text_splitter import TextProcessor
from modules.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Global variables
rag_pipeline = None
scraper = None
text_processor = None

def initialize_components():
    """Initialize RAG components"""
    global rag_pipeline, scraper, text_processor
    
    try:
        # Initialize components
        scraper = ChangiAirportScraper()
        text_processor = TextProcessor(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
        )
        
        # Initialize RAG pipeline
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.error("GOOGLE_API_KEY not found in environment variables")
            return False
        
        rag_pipeline = RAGPipeline(api_key)
        
        # Try to load existing vector store
        if not rag_pipeline.load_vector_store():
            logger.info("No existing vector store found. You may need to build the index.")
            # Don't fail initialization - just log the warning
            logger.warning("RAG pipeline initialized but vector store not loaded. Build the index to enable Q&A.")
        
        return True
        
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        return False

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('chat.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'rag_initialized': rag_pipeline is not None
    })

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to ask questions to the RAG chatbot"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        if not rag_pipeline:
            return jsonify({'error': 'RAG pipeline not initialized. Please check the server logs.'}), 500
        
        # Check if vector store is loaded
        if not rag_pipeline.vector_store:
            return jsonify({
                'error': 'Vector store not initialized. Please build the index first by calling /api/build-index',
                'answer': 'I need to build my knowledge base first. Please ask an administrator to build the index.'
            }), 500
        
        # Get response from RAG pipeline
        result = rag_pipeline.ask_question(
            question, 
            top_k=int(os.getenv('TOP_K_RESULTS', 5))
        )
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/build-index', methods=['POST'])
def build_index():
    """API endpoint to build the vector index from scraped data"""
    try:
        if not all([scraper, text_processor, rag_pipeline]):
            return jsonify({'error': 'Components not initialized'}), 500
        
        # Scrape websites
        logger.info("Starting website scraping...")
        scraped_data = scraper.scrape_all_sites()
        
        if not scraped_data:
            return jsonify({'error': 'No data scraped from websites'}), 500
        
        # Process text into chunks
        logger.info("Processing scraped data into chunks...")
        chunks = text_processor.process_scraped_data(scraped_data)
        chunks = text_processor.filter_chunks(chunks)
        
        if not chunks:
            return jsonify({'error': 'No valid chunks created from scraped data'}), 500
        
        # Build vector store
        logger.info("Building ChromaDB vector store...")
        rag_pipeline.build_vector_store(chunks)
        
        # Get stats
        stats = rag_pipeline.get_stats()
        
        return jsonify({
            'message': 'Index built successfully',
            'scraped_pages': len(scraped_data),
            'total_chunks': len(chunks),
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error building index: {str(e)}")
        return jsonify({
            'error': 'Error building index',
            'message': str(e)
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get statistics about the RAG system"""
    try:
        if not rag_pipeline:
            return jsonify({'error': 'RAG pipeline not initialized'}), 500
        
        stats = rag_pipeline.get_stats()
        return jsonify({
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': 'Error getting stats',
            'message': str(e)
        }), 500

@app.route('/api/example-questions')
def get_example_questions():
    """Get example questions for testing"""
    examples = [
        "What is the Rain Vortex at Jewel Changi Airport?",
        "How many terminals does Changi Airport have?",
        "What are the operating hours of Jewel Changi Airport?",
        "What airlines operate from Changi Airport?",
        "What shopping options are available at Changi Airport?",
        "How do I get to Jewel Changi Airport from the city?",
        "What restaurants are available at Changi Airport?",
        "What is the Shiseido Forest Valley?",
        "How far is Changi Airport from Singapore city center?",
        "What transportation options are available from Changi Airport?"
    ]
    
    return jsonify({
        'examples': examples,
        'count': len(examples)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the Flask app"""
    # Initialize components
    if not initialize_components():
        logger.error("Failed to initialize components. Check your environment variables.")
        return
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Changi Airport RAG Chatbot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()