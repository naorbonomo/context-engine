from app.LLMs.ollama_chat import OllamaChat
from app.LLMs.gemini_chat import GeminiChat
from app.LLMs.openai_chat import OpenAIChat
from app.LLMs.groq_chat import GroqChat
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class LLMFactory:
    """Factory class for creating LLM providers with defaults from environment variables."""
    
    # Load defaults from environment variables with fallbacks
    DEFAULT_CHAT_PROVIDER = os.getenv('DEFAULT_CHAT_PROVIDER', 'gemini')
    DEFAULT_AUTOCOMPLETE_PROVIDER = os.getenv('DEFAULT_AUTOCOMPLETE_PROVIDER', 'ollama')
    
    @staticmethod
    def create_llm(provider: str = None, operation: str = "chat"):
        """
        Create and return an LLM provider instance based on env configuration.
        
        Args:
            provider (str): The LLM provider to use ('ollama' or 'gemini')
            operation (str): The operation type ('chat' or 'autocomplete')
            
        Returns:
            BaseLLM: An instance of the specified LLM provider
        """
        try:
            if provider is None:
                provider = (LLMFactory.DEFAULT_CHAT_PROVIDER if operation == "chat"
                          else LLMFactory.DEFAULT_AUTOCOMPLETE_PROVIDER)
            
            provider = provider.lower()
            try:
                if provider == "ollama":
                    return OllamaChat()
                elif provider == "gemini":
                    return GeminiChat()
                elif provider == "openai":
                    return OpenAIChat()
                elif provider == "groq":
                    return GroqChat()
                else:
                    raise ValueError(f"Unsupported LLM provider: {provider}")
            except ValueError as e:
                # If primary provider fails, fallback to Ollama
                if provider in ["gemini", "openai", "groq"]:
                    logger.warning(f"{provider.capitalize()} initialization failed: {str(e)}. Falling back to Ollama.")
                    return OllamaChat()
                raise
                
        except Exception as e:
            logger.error(f"Error creating LLM provider: {str(e)}")
            raise