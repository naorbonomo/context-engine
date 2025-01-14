from fastapi import APIRouter, HTTPException  # Import necessary FastAPI components
from typing import Optional  # Add this import at the top
from pydantic import BaseModel  # Import BaseModel for request validation
from app.LLMs.llm_factory import LLMFactory  # Add this import
from app.utils.logger import get_logger  # Add this import

router = APIRouter(
    prefix="/api/v1",  # Set the prefix for all routes in this router
    tags=["chat"]  # Updated from "ollama-chat" to "chat"
)

logger = get_logger(__name__)  # Initialize logger for this module

class ChatRequest(BaseModel):
    prompt: str  # The user's input prompt
    system_prompt: Optional[str] = None  # The system's prompt
    model: Optional[str] = None  # Optional model override
    max_tokens: Optional[int] = None  # Optional max tokens override
    provider: Optional[str] = None  # Remove default to use factory default

class ChatResponse(BaseModel):
    response: str  # The generated chat response

class AutocompleteRequest(BaseModel):
    partial_prompt: str  # The incomplete text to generate suggestions for
    model: Optional[str] = None  # Optional model override
    max_tokens: Optional[int] = 50  # Number of tokens to predict, defaults to 50
    provider: Optional[str] = None  # Remove default to use factory default

class AutocompleteResponse(BaseModel):
    suggestion: str  # The generated completion suggestion

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
        # Get LLM provider with chat defaults
        llm = LLMFactory.create_llm(request.provider, operation="chat")
        logger.debug(f"Using provider: {type(llm).__name__} for chat")
        
        response = llm.generate_response(
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

@router.post("/autocomplete", response_model=AutocompleteResponse)
def autocomplete(request: AutocompleteRequest):
    """
    Generate text completion suggestions for a partial prompt.

    Args:
        request (AutocompleteRequest): The request containing the partial prompt and optional parameters.

    Returns:
        AutocompleteResponse: The generated completion suggestion.
    """
    try:
        # Get LLM provider with autocomplete defaults
        llm = LLMFactory.create_llm(request.provider, operation="autocomplete")
        logger.debug(f"Using provider: {type(llm).__name__} for autocomplete")
        
        response = llm.generate_autocomplete(
            partial_prompt=request.partial_prompt,
            max_tokens=request.max_tokens,
            model=request.model
        )
        
        logger.debug("Successfully generated autocomplete suggestion")
        return AutocompleteResponse(suggestion=response)
    except Exception as e:
        logger.error(f"Autocomplete generation error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating autocomplete: {str(e)}"
        )  # Handle exceptions 