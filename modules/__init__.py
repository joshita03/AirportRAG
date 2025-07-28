"""
Changi Airport RAG Chatbot Modules
A collection of modules for web scraping, text processing, and RAG pipeline
"""

__version__ = "1.0.0"
__author__ = "Changi Airport RAG Team"

from .scraper import ChangiAirportScraper
from .text_splitter import TextProcessor
from .rag_pipeline import RAGPipeline

__all__ = [
    'ChangiAirportScraper',
    'TextProcessor', 
    'RAGPipeline'
] 