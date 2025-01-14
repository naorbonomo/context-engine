from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class BaseLLM(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = None, 
                         model: str = None, max_tokens: int = None) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def generate_autocomplete(self, partial_prompt: str, max_tokens: int = 50, 
                            model: str = None) -> str:
        """Generate autocomplete suggestions."""
        pass