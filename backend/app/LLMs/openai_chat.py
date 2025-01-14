from app.LLMs.base_llm import BaseLLM
from openai import OpenAI
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class OpenAIChat(BaseLLM):
    """Class to handle chat interactions using OpenAI."""

    def __init__(self):
        """Initialize OpenAIChat with API key and model from environment."""
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            # Test API access
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            logger.info(f"Successfully initialized OpenAIChat with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI API: {str(e)}")
            raise ValueError(f"OpenAI API initialization failed: {str(e)}")

    def generate_response(self, prompt: str, system_prompt: str = None, 
                         model: str = None, max_tokens: int = None) -> str:
        """Generate a chat response using OpenAI."""
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
                    "Invalid OpenAI API key. Please check your OPENAI_API_KEY environment variable."
                )
            logger.error(f"Failed to generate response: {error_msg}")
            raise Exception(f"Error generating response with OpenAI: {error_msg}")

    def generate_autocomplete(self, partial_prompt: str, max_tokens: int = 50, 
                            model: str = None) -> str:
        """Generate autocomplete suggestions using OpenAI."""
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
            raise Exception(f"Error generating autocomplete with OpenAI: {str(e)}") 