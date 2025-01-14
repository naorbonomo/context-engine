from abc import ABC, abstractmethod
from typing import List, Optional
from chromadb.api.models.Collection import Collection

class BaseEmbedding(ABC):
    """Base class for embedding providers."""
    
    def __init__(self, collection: Collection, default_model: str):
        """Initialize embedding provider with collection and model."""
        self.collection = collection
        self.model = default_model

    @abstractmethod
    def create_embedding(self, content: str) -> bool:
        """Create embedding for single content."""
        pass

    @abstractmethod
    def create_embeddings_batch(self, contents: List[str]) -> bool:
        """Create embeddings for multiple contents."""
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 2) -> List[str]:
        """Search for relevant documents."""
        pass

    def list_documents(self) -> list:
        """List all documents in collection."""
        try:
            results = self.collection.get()
            return [
                {'id': doc_id, 'content': content}
                for doc_id, content in zip(results['ids'], results['documents'])
            ]
        except Exception as e:
            return []

    @abstractmethod
    def get_relevant_context(self, queries: List[str], top_k: int = 5) -> List[str]:
        """
        Get relevant context from multiple queries.
        
        Args:
            queries (List[str]): List of search queries
            top_k (int): Number of top results to return per query
            
        Returns:
            List[str]: List of relevant document contexts
        """
        pass