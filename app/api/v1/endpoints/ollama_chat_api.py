from fastapi import APIRouter, HTTPException  # Import necessary FastAPI components
from typing import Optional  # Add this import at the top
from pydantic import BaseModel  # Import BaseModel for request validation
from app.LLMs.ollama_chat import OllamaChat  # Import the OllamaChat class

router = APIRouter(
    prefix="/api/v1",  # Set the prefix for all routes in this router
    tags=["ollama-chat"]  # Update tag for API documentation
)

# Initialize OllamaChat with the desired model
ollama_chat = OllamaChat()  # Initialize with default model

class ChatRequest(BaseModel):
    prompt: str  # The user's input prompt
    system_prompt: Optional[str] = None  # The system's prompt
    model: Optional[str] = None  # Optional model override
    max_tokens: Optional[int] = None  # Optional max tokens override

class ChatResponse(BaseModel):
    response: str  # The generated chat response

@router.post("/generate", response_model=ChatResponse)  # Fixed response_model syntax
def generate_chat_response(request: ChatRequest):
    """
    Generate a chat response based on the provided prompts.

    Args:
        request (ChatRequest): The request containing prompts and optional parameters.

    Returns:
        ChatResponse: The generated chat response.
    """
    try:
        # Configure model if provided
        if request.model:
            ollama_chat.model = request.model
            
        # Generate response using OllamaChat instance
        response = ollama_chat.generate_response(
            prompt=request.prompt,  # User's prompt
            system_prompt=request.system_prompt,  # System's prompt
            model=request.model,  # Optional model
            max_tokens=request.max_tokens  # Optional max tokens
        )
        
        return ChatResponse(response=response)  # Return the response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Handle exceptions 