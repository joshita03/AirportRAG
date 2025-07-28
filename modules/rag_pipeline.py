"""
RAG Pipeline Module for Changi Airport Chatbot
Handles embeddings, vector storage, and retrieval using ChromaDB and Gemini
"""

import os
import pickle
import logging
from typing import List, Dict, Optional
import numpy as np
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RAGPipeline:
    """RAG Pipeline for Changi Airport Chatbot"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        # Initialize Gemini
        genai.configure(api_key=self.api_key)
        self.llm = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.api_key
        )
        
        # Vector store
        self.vector_store = None
        self.db_path = "data/changi_airport_chroma"
        self.collection_name = "changi_airport_docs"
        
    def create_documents(self, chunks: List[Dict]) -> List[Document]:
        """Convert chunks to LangChain Documents"""
        documents = []
        
        for chunk in chunks:
            doc = Document(
                page_content=chunk['text'],
                metadata=chunk['metadata']
            )
            documents.append(doc)
        
        logger.info(f"Created {len(documents)} documents")
        return documents
    
    def build_vector_store(self, chunks: List[Dict]) -> None:
        """Build ChromaDB vector store from chunks"""
        if not chunks:
            logger.warning("No chunks provided for vector store building")
            return
        
        # Convert chunks to documents
        documents = self.create_documents(chunks)
        
        # Create vector store
        logger.info("Building ChromaDB vector store...")
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.db_path,
            collection_name=self.collection_name
        )
        
        # Persist the database
        self.vector_store.persist()
        
        logger.info(f"Vector store built and saved with {len(documents)} documents")
    
    def load_vector_store(self) -> bool:
        """Load existing vector store from disk"""
        try:
            if os.path.exists(self.db_path):
                logger.info("Loading existing vector store...")
                self.vector_store = Chroma(
                    persist_directory=self.db_path,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name
                )
                logger.info("Vector store loaded successfully")
                return True
            else:
                logger.info("No existing vector store found")
                return False
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            return False
    
    def search_similar(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar documents"""
        if not self.vector_store:
            logger.error("Vector store not initialized")
            return []
        
        try:
            # Search for similar documents
            docs = self.vector_store.similarity_search(query, k=top_k)
            
            # Convert to dictionary format
            results = []
            for doc in docs:
                results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': 0.0  # ChromaDB doesn't return scores by default
                })
            
            logger.info(f"Found {len(results)} similar documents for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """Generate response using Gemini LLM"""
        if not context_docs:
            return "I don't have enough information to answer that question about Changi Airport. Please try asking something else."
        
        # Prepare context
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        # Create prompt
        prompt = f"""You are a helpful assistant for Changi Airport and Jewel Changi Airport. 
        Answer the user's question based on the provided context. 
        If the context doesn't contain enough information to answer the question, say so.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:"""
        
        try:
            # Generate response
            response = self.llm.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I'm sorry, I encountered an error while generating a response. Please try again."
    
    def ask_question(self, query: str, top_k: int = 5) -> Dict:
        """Complete RAG pipeline: search + generate response"""
        if not self.vector_store:
            return {
                'answer': 'Vector store not initialized. Please build the index first.',
                'sources': [],
                'error': 'Vector store not available'
            }
        
        try:
            # Search for relevant documents
            similar_docs = self.search_similar(query, top_k)
            
            # Generate response
            answer = self.generate_response(query, similar_docs)
            
            # Prepare sources
            sources = []
            for doc in similar_docs:
                source_info = {
                    'url': doc['metadata'].get('url', ''),
                    'title': doc['metadata'].get('title', ''),
                    'source': doc['metadata'].get('source', ''),
                    'content_preview': doc['content'][:200] + '...' if len(doc['content']) > 200 else doc['content']
                }
                sources.append(source_info)
            
            return {
                'answer': answer,
                'sources': sources,
                'query': query
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {str(e)}")
            return {
                'answer': 'I encountered an error while processing your question. Please try again.',
                'sources': [],
                'error': str(e)
            }
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        if not self.vector_store:
            return {'status': 'not_initialized'}
        
        try:
            # Get basic stats
            stats = {
                'status': 'initialized',
                'db_path': self.db_path,
                'db_exists': os.path.exists(self.db_path),
                'collection_name': self.collection_name
            }
            
            # Try to get document count from ChromaDB
            try:
                if hasattr(self.vector_store, '_collection'):
                    stats['document_count'] = self.vector_store._collection.count()
                else:
                    stats['document_count'] = 'unknown'
            except:
                stats['document_count'] = 'unknown'
            
            return stats
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

def main():
    """Test the RAG pipeline"""
    # This is a test function - in production, you'd load from scraped data
    test_chunks = [
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
    
    # Initialize pipeline (requires API key)
    try:
        pipeline = RAGPipeline()
        
        # Build vector store
        pipeline.build_vector_store(test_chunks)
        
        # Test question
        result = pipeline.ask_question("What is the Rain Vortex?")
        print("Answer:", result['answer'])
        print("Sources:", result['sources'])
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure to set GOOGLE_API_KEY environment variable")

if __name__ == "__main__":
    main()