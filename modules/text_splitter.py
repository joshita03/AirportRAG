"""
Text Processing Module for Changi Airport RAG Chatbot
Handles text splitting and preprocessing for vectorization
"""

import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """Handles text processing and chunking for RAG pipeline"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove special characters but keep punctuation
        import re
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\[\]]', '', text)
        
        return text.strip()
    
    def split_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Split text into chunks with metadata"""
        if not text or len(text.strip()) == 0:
            return []
        
        # Clean the text first
        cleaned_text = self.clean_text(text)
        
        if not cleaned_text:
            return []
        
        # Split the text
        chunks = self.text_splitter.split_text(cleaned_text)
        
        # Add metadata to each chunk
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = metadata.copy() if metadata else {}
            chunk_metadata.update({
                'chunk_id': i,
                'chunk_size': len(chunk),
                'total_chunks': len(chunks)
            })
            
            chunk_docs.append({
                'text': chunk,
                'metadata': chunk_metadata
            })
        
        logger.info(f"Split text into {len(chunk_docs)} chunks")
        return chunk_docs
    
    def process_scraped_data(self, scraped_data: List[Dict]) -> List[Dict]:
        """Process scraped data into chunks for vectorization"""
        all_chunks = []
        
        for item in scraped_data:
            if not item.get('content') or 'error' in item:
                continue
            
            # Prepare metadata
            metadata = {
                'url': item.get('url', ''),
                'title': item.get('title', ''),
                'source': item.get('source', ''),
                'content_length': len(item.get('content', ''))
            }
            
            # Split content into chunks
            chunks = self.split_text(item['content'], metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Processed {len(scraped_data)} pages into {len(all_chunks)} chunks")
        return all_chunks
    
    def filter_chunks(self, chunks: List[Dict], min_length: int = 50) -> List[Dict]:
        """Filter out chunks that are too short or empty"""
        filtered_chunks = []
        
        for chunk in chunks:
            text = chunk.get('text', '').strip()
            if len(text) >= min_length:
                filtered_chunks.append(chunk)
        
        logger.info(f"Filtered {len(chunks)} chunks to {len(filtered_chunks)} valid chunks")
        return filtered_chunks

def main():
    """Test the text processor"""
    processor = TextProcessor(chunk_size=500, chunk_overlap=100)
    
    # Test with sample text
    sample_text = """
    Changi Airport is Singapore's main international airport and one of the largest transportation hubs in Asia.
    It serves as a major hub for Singapore Airlines and is a focus city for many other airlines.
    The airport has won numerous awards for its design and service quality.
    
    Jewel Changi Airport is a nature-themed entertainment and retail complex located on the grounds of Changi Airport.
    It features the world's tallest indoor waterfall, the Rain Vortex, and the Shiseido Forest Valley.
    The complex includes retail outlets, restaurants, and attractions for visitors.
    """
    
    metadata = {
        'url': 'https://example.com',
        'title': 'Changi Airport Information',
        'source': 'changi_airport'
    }
    
    chunks = processor.split_text(sample_text, metadata)
    
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk['text'][:100]}...")
        print(f"Metadata: {chunk['metadata']}")
        print("-" * 50)

if __name__ == "__main__":
    main() 