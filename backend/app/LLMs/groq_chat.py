from app.LLMs.base_llm import BaseLLM
from groq import Groq
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class GroqChat(BaseLLM):
    """Class to handle chat interactions using Groq."""

    def __init__(self):
        """Initialize GroqChat with API key and model from environment."""
        self.model = os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')  # Default to mixtral
        self.api_key = os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        try:
            self.client = Groq(api_key=self.api_key)
            # Test API access
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            logger.info(f"Successfully initialized GroqChat with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Groq API: {str(e)}")
            raise ValueError(f"Groq API initialization failed: {str(e)}")

    def generate_response(self, prompt: str, system_prompt: str = None, 
                         model: str = None, max_tokens: int = None) -> str:
        """Generate a chat response using Groq."""
        try:
            model_name = model or self.model
            logger.info(f"Using model: {model_name}")
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content

        except Exception as e:
            error_msg = str(e)
            if "invalid_api_key" in error_msg.lower():
                raise ValueError(
                    "Invalid Groq API key. Please check your GROQ_API_KEY environment variable."
                )
            logger.error(f"Failed to generate response: {error_msg}")
            raise Exception(f"Error generating response with Groq: {error_msg}")

    def generate_autocomplete(self, partial_prompt: str, max_tokens: int = 50, 
                            model: str = None) -> str:
        """Generate autocomplete suggestions using Groq."""
        try:
            model_name = model or self.model
            logger.debug(f"Generating autocomplete with model: {model_name}")
            
            system_prompt = """Complete the following partial text naturally, 
            as if predicting what might come next. Provide only the continuation."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": partial_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
            )
            
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Failed to generate autocomplete: {str(e)}")
            raise Exception(f"Error generating autocomplete with Groq: {str(e)}") 