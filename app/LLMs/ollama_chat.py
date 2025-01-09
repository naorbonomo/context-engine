import os
from dotenv import load_dotenv
import ollama  # Import Ollama for chat completions

load_dotenv()

class OllamaChat:
    """Class to handle chat interactions using Ollama."""

    def __init__(self, default_model: str = os.getenv('OLLAMA_MODEL')):
        """
        Initialize the OllamaChat with a specific model.

        Args:
            default_model (str): The default model to use.
        """
        self.model = default_model  # Store the model name

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

            # Prepare the messages
            messages = []
            
            # Add system message if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })

            # Generate response using Ollama
            response = ollama.chat(
                model=model_name,
                messages=messages,
                stream=False
            )

            # Extract and return the response text
            return response['message']['content']

        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}") 
        