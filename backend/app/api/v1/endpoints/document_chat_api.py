from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.LLMs.llm_factory import LLMFactory
from app.LLMs.ollama_embedding import OllamaEmbeddings
from app.handlers.db_handler import DatabaseHandler
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv

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
    embedder = OllamaEmbeddings(
        collection=db_handler.collection,
        default_model=os.getenv('OLLAMA_EMBEDDING_MODEL')
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

        # Generate multiple search queries
        logger.debug("Generating search queries...")
        queries = embedder.get_multiple_queries(current_query)
        
        # Get initial context
        relevant_context = embedder.get_relevant_context(
            queries=queries,
            top_k=request.top_k
        )
        
        # Analyze context sufficiency
        if relevant_context:
            analysis, additional_queries = embedder.analyze_context_sufficiency(
                context_list=relevant_context,
                user_input=current_query
            )
            
            logger.debug(f"Context analysis: {analysis}")
            
            # If context is insufficient and we have additional queries, get more context
            if additional_queries:
                additional_context = embedder.get_relevant_context(
                    queries=additional_queries,
                    top_k=request.top_k
                )
                relevant_context.extend(additional_context)
        
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
    

