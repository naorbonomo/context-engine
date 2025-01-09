from fastapi import APIRouter, HTTPException  # Import necessary FastAPI components
from typing import Optional  # Add this import at the top
from pydantic import BaseModel  # Import BaseModel for request validation
from app.LLMs.ollama_chat import OllamaChat  # Import the OllamaChat class
from app.utils.logger import get_logger  # Add this import

router = APIRouter(
    prefix="/api/v1",  # Set the prefix for all routes in this router
    tags=["ollama-chat"]  # Update tag for API documentation
)

# Initialize OllamaChat with the desired model
ollama_chat = OllamaChat()  # Initialize with default model

logger = get_logger(__name__)  # Initialize logger for this module

class ChatRequest(BaseModel):
    prompt: str  # The user's input prompt
    system_prompt: Optional[str] = None  # The system's prompt
    model: Optional[str] = None  # Optional model override
    max_tokens: Optional[int] = None  # Optional max tokens override

class ChatResponse(BaseModel):
    response: str  # The generated chat response

@router.post("/chat", response_model=ChatResponse)
def chat_response(request: ChatRequest):
    """
    Generate a chat response based on the provided prompts.

    Args:
        request (ChatRequest): The request containing prompts and optional parameters.

    Returns:
        ChatResponse: The generated chat response.
    """
    try:
        logger.debug(f"Received chat request with model: {request.model}")
        
        if request.model:
            logger.info(f"Overriding default model with: {request.model}")
            ollama_chat.model = request.model
        
        logger.debug(f"Generating response for prompt: {request.prompt[:50]}...")
        response = ollama_chat.generate_response(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            model=request.model,
            max_tokens=request.max_tokens
        )
        
        logger.debug("Successfully generated response")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Chat generation error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating chat response: {str(e)}"
        )  # Handle exceptions 