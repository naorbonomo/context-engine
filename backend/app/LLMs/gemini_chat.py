from app.LLMs.base_llm import BaseLLM
import google.generativeai as genai
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class GeminiChat(BaseLLM):
    """Class to handle chat interactions using Google's Gemini."""

    def __init__(self):
        """Initialize GeminiChat with API key and model from environment."""
        self.model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self.api_key = os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        try:
            genai.configure(api_key=self.api_key)
            # Test API access
            model = genai.GenerativeModel(self.model)
            response = model.generate_content("test")  # Quick API test
            logger.info(f"Successfully initialized GeminiChat with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {str(e)}")
            raise ValueError(f"Gemini API initialization failed: {str(e)}. Please ensure the API is enabled in Google Cloud Console.")

    def generate_response(self, prompt: str, system_prompt: str = None, 
                         model: str = None, max_tokens: int = None) -> str:
        """Generate a chat response using Gemini."""
        try:
            model_name = model or self.model
            logger.info(f"Using model: {model_name}")
            
            model = genai.GenerativeModel(model_name)
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "max_output_tokens": max_tokens if max_tokens else 1024,
                }
            )
            
            return response.text

        except Exception as e:
            error_msg = str(e)
            if "SERVICE_DISABLED" in error_msg:
                raise ValueError(
                    "Gemini API is not enabled. Please enable it in Google Cloud Console: "
                    "https://console.developers.google.com/apis/api/generativelanguage.googleapis.com"
                )
            logger.error(f"Failed to generate response: {error_msg}")
            raise Exception(f"Error generating response with Gemini: {error_msg}")

    def generate_autocomplete(self, partial_prompt: str, max_tokens: int = 50, 
                            model: str = None) -> str:
        """Generate autocomplete suggestions using Gemini."""
        try:
            # Use provided model or fall back to instance default
            model_name = model or self.model
            logger.debug(f"Generating autocomplete with model: {model_name}")
            
            system_prompt = """Complete the following partial text naturally, 
            as if predicting what might come next. Provide only the continuation."""
            
            full_prompt = f"{system_prompt}\n\nPartial text: {partial_prompt}"
            
            # Initialize model
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(
                full_prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                }
            )
            
            return response.text

        except Exception as e:
            logger.error(f"Failed to generate autocomplete: {str(e)}")
            raise Exception(f"Error generating autocomplete with Gemini: {str(e)}")