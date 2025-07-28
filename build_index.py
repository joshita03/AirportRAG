#!/usr/bin/env python3
"""
Build Index Script for Changi Airport RAG Chatbot
Standalone script to scrape websites and build the vector database
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.scraper import ChangiAirportScraper
from modules.text_splitter import TextProcessor
from modules.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to build the index"""
    logger.info("🚀 Starting Changi Airport RAG Index Builder")
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("❌ GOOGLE_API_KEY not found in environment variables")
        logger.error("Please set your Google API key in the .env file")
        return False
    
    try:
        # Initialize components
        logger.info("📦 Initializing components...")
        scraper = ChangiAirportScraper()
        text_processor = TextProcessor(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
        )
        rag_pipeline = RAGPipeline(api_key)
        
        # Step 1: Scrape websites
        logger.info("🌐 Starting website scraping...")
        scraped_data = scraper.scrape_all_sites()
        
        if not scraped_data:
            logger.error("❌ No data scraped from websites")
            return False
        
        logger.info(f"✅ Scraped {len(scraped_data)} pages")
        
        # Step 2: Process text into chunks
        logger.info("📝 Processing scraped data into chunks...")
        chunks = text_processor.process_scraped_data(scraped_data)
        chunks = text_processor.filter_chunks(chunks)
        
        if not chunks:
            logger.error("❌ No valid chunks created from scraped data")
            return False
        
        logger.info(f"✅ Created {len(chunks)} chunks")
        
        # Step 3: Build vector store
        logger.info("🔍 Building ChromaDB vector store...")
        rag_pipeline.build_vector_store(chunks)
        
        # Step 4: Get and display stats
        stats = rag_pipeline.get_stats()
        logger.info("📊 Index Statistics:")
        logger.info(f"   - Status: {stats.get('status', 'unknown')}")
        logger.info(f"   - Database path: {stats.get('db_path', 'unknown')}")
        logger.info(f"   - Database exists: {stats.get('db_exists', 'unknown')}")
        logger.info(f"   - Document count: {stats.get('document_count', 'unknown')}")
        
        logger.info("🎉 Index built successfully!")
        logger.info("You can now run the Flask application with: python app.py")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error building index: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 