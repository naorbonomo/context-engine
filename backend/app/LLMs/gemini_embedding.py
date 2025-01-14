import os
import google.generativeai as genai
from typing import List
from app.LLMs.base_embedding import BaseEmbedding
from app.utils.logger import get_logger

logger = get_logger(__name__)

class GeminiEmbeddings(BaseEmbedding):
    """Gemini embedding provider implementation."""
    
    def __init__(self, collection, default_model: str):
        super().__init__(collection, default_model)
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    def create_embedding(self, content: str) -> bool:
        try:
            if not content.strip():
                return False
                
            result = genai.embed_content(
                model=self.model,
                content=content
            )
            
            doc_id = f"doc_{self.collection.count()}"
            self.collection.add(
                embeddings=[result['embedding']],
                documents=[content.strip()],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            return False

    def create_embeddings_batch(self, contents: List[str]) -> bool:
        try:
            embeddings = []
            documents = []
            ids = []
            
            for idx, content in enumerate(contents):
                if content.strip():
                    result = genai.embed_content(
                        model=self.model,
                        content=content
                    )
                    embeddings.append(result['embedding'])
                    documents.append(content.strip())
                    ids.append(f"doc_{self.collection.count() + idx}")
            
            if documents:
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    ids=ids
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {str(e)}")
            return False

    def search(self, query: str, top_k: int = 2) -> List[str]:
        try:
            result = genai.embed_content(
                model=self.model,
                content=query
            )
            
            results = self.collection.query(
                query_embeddings=[result['embedding']],
                n_results=top_k
            )
            
            return results['documents'][0] if results['documents'][0] else []
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return []

    def get_relevant_context(self, queries: List[str], top_k: int = 5) -> List[str]:
        """
        Get relevant context from multiple queries.
        
        Args:
            queries (List[str]): List of search queries
            top_k (int): Number of top results to return per query
            
        Returns:
            List[str]: List of relevant document contexts
        """
        try:
            all_contexts = set()  # Use set to avoid duplicates
            
            for query in queries:
                contexts = self.search(query, top_k=top_k)
                if isinstance(contexts, list):
                    all_contexts.update(contexts)
                else:
                    logger.warning(f"Unexpected search result type for query: {query}")
            
            return list(all_contexts)  # Convert back to list
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {str(e)}")
            return []