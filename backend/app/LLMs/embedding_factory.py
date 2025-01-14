import os
from app.LLMs.gemini_embedding import GeminiEmbeddings
from app.LLMs.ollama_embedding import OllamaEmbeddings
from app.utils.logger import get_logger

logger = get_logger(__name__)

class EmbeddingFactory:
    """Factory class for creating embedding providers."""
    
    @staticmethod
    def create_embedder(provider: str = None, collection=None):
        """Create embedding provider instance."""
        if not provider:
            provider = os.getenv('DEFAULT_EMBEDDING_PROVIDER', 'gemini')
            
        try:
            if provider.lower() == 'gemini':
                return GeminiEmbeddings(
                    collection=collection,
                    default_model=os.getenv('GEMINI_EMBEDDING_MODEL', 'models/text-embedding-004')
                )
            elif provider.lower() == 'ollama':
                return OllamaEmbeddings(
                    collection=collection,
                    default_model=os.getenv('OLLAMA_EMBEDDING_MODEL')
                )
            else:
                logger.warning(f"Unknown provider {provider}, falling back to Ollama")
                return OllamaEmbeddings(
                    collection=collection,
                    default_model=os.getenv('OLLAMA_EMBEDDING_MODEL')
                )
        except Exception as e:
            logger.error(f"Error creating embedder: {str(e)}")
            # Fallback to Ollama
            return OllamaEmbeddings(
                collection=collection,
                default_model=os.getenv('OLLAMA_EMBEDDING_MODEL')
            )