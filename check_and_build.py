#!/usr/bin/env python3
"""
Check and build the vector store if needed
"""

import os
from dotenv import load_dotenv
from modules.scraper import ChangiAirportScraper
from modules.text_splitter import TextProcessor
from modules.rag_pipeline import RAGPipeline

def main():
    """Check and build vector store if needed"""
    print("🔍 Checking Changi Airport RAG Chatbot Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        return False
    
    print("✅ API key found")
    
    # Check if vector store exists
    db_path = "data/changi_airport_chroma"
    if os.path.exists(db_path):
        print("✅ Vector store exists")
        
        # Test loading it
        try:
            rag_pipeline = RAGPipeline(api_key)
            if rag_pipeline.load_vector_store():
                print("✅ Vector store loaded successfully")
                stats = rag_pipeline.get_stats()
                print(f"📊 Document count: {stats.get('document_count', 'unknown')}")
                return True
            else:
                print("⚠️  Vector store exists but failed to load")
        except Exception as e:
            print(f"❌ Error loading vector store: {e}")
    else:
        print("❌ Vector store not found")
    
    # Build the vector store
    print("\n🔨 Building vector store...")
    try:
        # Initialize components
        scraper = ChangiAirportScraper()
        text_processor = TextProcessor(
            chunk_size=int(os.getenv('CHUNK_SIZE', 1000)),
            chunk_overlap=int(os.getenv('CHUNK_OVERLAP', 200))
        )
        rag_pipeline = RAGPipeline(api_key)
        
        # Scrape websites
        print("📡 Scraping websites...")
        scraped_data = scraper.scrape_all_sites()
        
        if not scraped_data:
            print("❌ No data scraped from websites")
            return False
        
        print(f"✅ Scraped {len(scraped_data)} pages")
        
        # Process text into chunks
        print("✂️  Processing text into chunks...")
        chunks = text_processor.process_scraped_data(scraped_data)
        chunks = text_processor.filter_chunks(chunks)
        
        if not chunks:
            print("❌ No valid chunks created")
            return False
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Build vector store
        print("🏗️  Building vector store...")
        rag_pipeline.build_vector_store(chunks)
        
        print("✅ Vector store built successfully!")
        
        # Test it
        stats = rag_pipeline.get_stats()
        print(f"📊 Document count: {stats.get('document_count', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error building vector store: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Setup completed successfully!")
        print("You can now run: python run.py")
    else:
        print("\n❌ Setup failed!")
        print("Please check the error messages above.") 