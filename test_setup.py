#!/usr/bin/env python3
"""
Test Setup Script for Changi Airport RAG Chatbot
Verifies that all components are working correctly
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported"""
    logger.info("🔍 Testing imports...")
    
    try:
        from modules.scraper import ChangiAirportScraper
        logger.info("✅ Scraper module imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import scraper module: {e}")
        return False
    
    try:
        from modules.text_splitter import TextProcessor
        logger.info("✅ Text processor module imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import text processor module: {e}")
        return False
    
    try:
        from modules.rag_pipeline import RAGPipeline
        logger.info("✅ RAG pipeline module imported successfully")
    except ImportError as e:
        logger.error(f"❌ Failed to import RAG pipeline module: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables"""
    logger.info("🔍 Testing environment variables...")
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("❌ GOOGLE_API_KEY not found in environment variables")
        logger.error("Please set your Google API key in the .env file")
        return False
    
    logger.info("✅ GOOGLE_API_KEY found")
    
    # Test other environment variables
    chunk_size = os.getenv('CHUNK_SIZE', '1000')
    chunk_overlap = os.getenv('CHUNK_OVERLAP', '200')
    top_k = os.getenv('TOP_K_RESULTS', '5')
    
    logger.info(f"✅ Configuration: CHUNK_SIZE={chunk_size}, CHUNK_OVERLAP={chunk_overlap}, TOP_K={top_k}")
    
    return True

def test_components():
    """Test component initialization"""
    logger.info("🔍 Testing component initialization...")
    
    try:
        from modules.scraper import ChangiAirportScraper
        from modules.text_splitter import TextProcessor
        from modules.rag_pipeline import RAGPipeline
        
        # Initialize components
        scraper = ChangiAirportScraper()
        text_processor = TextProcessor()
        rag_pipeline = RAGPipeline()
        
        logger.info("✅ All components initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize components: {e}")
        return False

def test_sample_data():
    """Test with sample data"""
    logger.info("🔍 Testing with sample data...")
    
    try:
        from modules.text_splitter import TextProcessor
        from modules.rag_pipeline import RAGPipeline
        
        # Create sample data
        sample_chunks = [
            {
                'text': 'Changi Airport is Singapore\'s main international airport and one of the largest transportation hubs in Asia.',
                'metadata': {
                    'url': 'https://www.changiairport.com',
                    'title': 'Changi Airport Overview',
                    'source': 'changi_airport'
                }
            },
            {
                'text': 'Jewel Changi Airport features the world\'s tallest indoor waterfall, the Rain Vortex, and the Shiseido Forest Valley.',
                'metadata': {
                    'url': 'https://www.jewelchangiairport.com',
                    'title': 'Jewel Changi Features',
                    'source': 'jewel_changi'
                }
            }
        ]
        
        # Test text processing
        text_processor = TextProcessor()
        processed_chunks = text_processor.process_scraped_data([
            {
                'url': 'https://example.com',
                'title': 'Test Page',
                'content': 'Changi Airport is Singapore\'s main international airport.',
                'source': 'test'
            }
        ])
        
        logger.info(f"✅ Text processing test passed: {len(processed_chunks)} chunks created")
        
        # Test RAG pipeline (without building index)
        rag_pipeline = RAGPipeline()
        logger.info("✅ RAG pipeline test passed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting Changi Airport RAG Chatbot Setup Tests")
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Component Test", test_components),
        ("Sample Data Test", test_sample_data)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Results: {passed}/{total} tests passed")
    logger.info(f"{'='*50}")
    
    if passed == total:
        logger.info("🎉 All tests passed! Your setup is ready.")
        logger.info("Next steps:")
        logger.info("1. Run: python scripts/build_index.py")
        logger.info("2. Run: python app.py")
        logger.info("3. Open http://localhost:5000 in your browser")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 