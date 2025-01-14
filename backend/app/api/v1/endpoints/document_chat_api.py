from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.LLMs.llm_factory import LLMFactory
from app.LLMs.embedding_factory import EmbeddingFactory
from app.handlers.db_handler import DatabaseHandler
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv
from app.handlers.context_handler import ContextHandler

load_dotenv()
logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["document-chat"]
)

# Initialize handlers
try:
    db_handler = DatabaseHandler()
    # Use LLMFactory instead of direct OllamaChat instantiation
    chat_handler = LLMFactory.create_llm(os.getenv('DEFAULT_CHAT_PROVIDER'))
    embedder = EmbeddingFactory.create_embedder(
        provider=os.getenv('DEFAULT_EMBEDDING_PROVIDER'),
        collection=db_handler.collection
    )
except Exception as e:
    logger.error(f"Error initializing handlers: {str(e)}")
    raise

class DocumentChatRequest(BaseModel):
    messages: List[dict]  # Chat history
    top_k: Optional[int] = 5  # Number of relevant contexts to retrieve
    model: Optional[str] = None  # Optional model override
    provider: Optional[str] = None  # Add provider field

class DocumentChatResponse(BaseModel):
    response: str  # The generated chat response
    contexts: List[str]  # The relevant document contexts used
    provider: str  # Add provider field to show which LLM was used

@router.post("/document-chat", response_model=DocumentChatResponse)
async def document_chat(request: DocumentChatRequest):
    """
    Generate a chat response based on document context and chat history.
    Uses a multi-query approach with context analysis for better results.
    
    Args:
        request (DocumentChatRequest): Contains messages history, search parameters, and provider
    
    Returns:
        DocumentChatResponse: AI response, relevant document contexts, and provider used
    """
    try:
        # Get chat handler for requested provider or use default
        chat_handler = LLMFactory.create_llm(request.provider, operation="chat")
        logger.info(f"Using provider: {type(chat_handler).__name__}")

        # Get the latest user message
        current_query = request.messages[-1]["content"]
        logger.debug(f"Processing query: {current_query[:50]}...")

        # Initialize context handler
        context_handler = ContextHandler(embedder)
        
        # Get relevant context
        relevant_context = context_handler.get_document_context(
            query=current_query,
            top_k=request.top_k
        )
        
        # Construct system prompt with context
        context_prompt = "\n".join([
            "Relevant document contexts:",
            *[f"- {ctx}" for ctx in relevant_context],
            "\nAnswer the user's question based on the above contexts. If the contexts don't contain relevant information, say so."
        ])

        # Generate response using chat
        response = chat_handler.generate_response(
            prompt=current_query,
            system_prompt=context_prompt,
            model=request.model
        )

        return DocumentChatResponse(
            response=response,
            contexts=relevant_context,
            provider=type(chat_handler).__name__.replace('Chat', '').lower()  # Extract provider name
        )

    except Exception as e:
        logger.error(f"Document chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document chat: {str(e)}"
        ) 
    

