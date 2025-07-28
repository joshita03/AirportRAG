#!/usr/bin/env python3
"""
Test script to verify embedding functionality
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def test_embeddings():
    """Test the embedding functionality"""
    print("🧪 Testing Embedding Functionality")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        return False
    
    try:
        # Initialize embeddings
        print("📦 Initializing embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        print("✅ Embeddings initialized successfully")
        
        # Test embedding generation
        print("🔍 Testing embedding generation...")
        test_text = "Changi Airport is Singapore's main international airport"
        embedding = embeddings.embed_query(test_text)
        
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        print(f"📏 Embedding length: {len(embedding)}")
        print(f"📝 Test text: '{test_text}'")
        
        # Test batch embedding
        print("📚 Testing batch embedding...")
        test_texts = [
            "Changi Airport is Singapore's main international airport",
            "Jewel Changi Airport features the Rain Vortex",
            "Singapore is a beautiful city"
        ]
        
        batch_embeddings = embeddings.embed_documents(test_texts)
        print(f"✅ Generated {len(batch_embeddings)} batch embeddings")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing embeddings: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_embeddings()
    if success:
        print("\n🎉 Embedding test completed successfully!")
        print("You can now run: python build_index.py")
    else:
        print("\n❌ Embedding test failed!")
        print("Please check your API key and try again.") 