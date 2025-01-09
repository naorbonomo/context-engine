import os
from dotenv import load_dotenv
import ollama  # Import Ollama for chat completions
from app.utils.logger import get_logger  # Add this import

load_dotenv()

logger = get_logger(__name__)  # Initialize logger for this module

class OllamaChat:
    """Class to handle chat interactions using Ollama."""

    def __init__(self, default_model: str = os.getenv('OLLAMA_MODEL')):
        """
        Initialize the OllamaChat with a specific model.

        Args:
            default_model (str): The default model to use.
        """
        self.model = default_model  # Store the model name
        logger.info(f"Initialized OllamaChat with model: {self.model}")

    def generate_response(self, prompt: str, system_prompt: str = None, model: str = None, max_tokens: int = None) -> str:
        """
        Generate a chat response using Ollama.

        Args:
            prompt (str): The input prompt for the chat.
            system_prompt (str, optional): The system prompt for context.
            model (str, optional): The model to use. Defaults to self.model.
            max_tokens (int, optional): Maximum tokens for response.

        Returns:
            str: The generated chat response.
        """
        try:
            # Use provided model or fall back to default
            model_name = model or self.model
            logger.debug(f"Generating response with model: {model_name}")
            logger.debug(f"Prompt: {prompt[:50]}...")  # Log first 50 chars of prompt
            
            # Verify model exists
            try:
                # You might want to add a model verification step here
                print(f"Using model: {model_name}")
            except Exception as model_error:
                raise Exception(f"Model verification failed: {str(model_error)}")

            # Prepare the messages
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
                logger.debug(f"System prompt: {system_prompt[:50]}...")
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })

            logger.debug(f"Sending request to Ollama with {len(messages)} messages")
            response = ollama.chat(
                model=model_name,
                messages=messages,
                stream=False
            )
            logger.debug("Successfully received response from Ollama")

            # Extract and return the response text
            return response['message']['content']

        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            raise Exception(f"Error generating response with model {model_name}: {str(e)}") 
        