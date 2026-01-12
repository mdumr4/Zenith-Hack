# vector.py
"""
Team B - Vector Store for Semantic Memory
Uses ChromaDB for storing and querying clipboard/context history.
"""
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict

class MemoryStore:
    """Semantic memory store using ChromaDB"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB client and collection.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="frai_memory",
            metadata={"description": "Semantic memory for Frai AI Keyboard"}
        )
        print(f"Memory store initialized ({self.collection.count()} items)")
    
    def add(self, text: str, metadata: Dict = None):
        """
        Add text to semantic memory.
        
        Args:
            text: Text content to store
            metadata: Optional metadata (e.g., app_name, timestamp)
        """
        if not text or len(text.strip()) < 3:
            return  # Skip empty or very short text
        
        # Generate unique ID
        doc_id = str(uuid.uuid4())
        
        # Add to collection
        self.collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[metadata or {}]
        )
    
    def query(self, query_text: str, n_results: int = 3) -> List[str]:
        """
        Query semantic memory for relevant content.
        
        Args:
            query_text: Query string
            n_results: Number of results to return
        
        Returns:
            List of relevant text snippets
        """
        if not query_text:
            return []
        
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Extract documents
        if results and results['documents']:
            return results['documents'][0]
        return []
    
    def clear(self):
        """Clear all memory (for testing/reset)"""
        self.client.delete_collection("frai_memory")
        self.collection = self.client.get_or_create_collection(
            name="frai_memory",
            metadata={"description": "Semantic memory for Frai AI Keyboard"}
        )

# Global instance
_store = None

def get_memory_store() -> MemoryStore:
    """Get or create the global memory store"""
    global _store
    if _store is None:
        _store = MemoryStore()
    return _store
