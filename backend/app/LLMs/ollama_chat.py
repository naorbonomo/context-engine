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
        
    def generate_autocomplete(self, partial_prompt: str, max_tokens: int = 50, model: str = None) -> str:
        """
        Generate autocomplete suggestions for a partial prompt.

        Args:
            partial_prompt (str): The incomplete text to generate suggestions for
            max_tokens (int, optional): Maximum tokens for the suggestion. Defaults to 50.
            model (str, optional): The model to use. Defaults to self.model.

        Returns:
            str: The suggested text completion
        """
        try:
            model_name = model or self.model
            logger.debug(f"Generating autocomplete with model: {model_name}")
            logger.debug(f"Partial prompt: {partial_prompt[:50]}...")

            # Add system prompt for autocomplete behavior
            system_prompt = """You are an autocomplete assistant. Your task is to continue the user's partial prompt naturally, 
            as if predicting what they might want to ask or say next. Do not provide answers or complete responses. 
            Instead, focus on completing the current sentence or thought in a way that makes sense given the context.
            Keep the continuation concise and natural. Respond only with the continuation text, no explanations or additional formatting."""

            response = ollama.generate(
                model=model_name,
                prompt=partial_prompt,
                system=system_prompt,  # Add system prompt
                stream=False,
                options={
                    "num_predict": max_tokens,
                }
            )
            logger.debug("Successfully received autocomplete response")

            return response['response']

        except Exception as e:
            logger.error(f"Failed to generate autocomplete: {str(e)}")
            raise Exception(f"Error generating autocomplete with model {model_name}: {str(e)}") 
        