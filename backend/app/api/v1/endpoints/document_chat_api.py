from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
from app.LLMs.llm_factory import LLMFactory
from app.LLMs.embedding_factory import EmbeddingFactory
from app.handlers.db_handler import DatabaseHandler
from app.utils.logger import get_logger
import os
from dotenv import load_dotenv
from app.handlers.context_handler import ContextHandler
import json

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
        
        # Enhanced system prompt for user manual RAG experience
        system_prompt = f"""You are a technical support assistant for the GrandMA3 lighting console. You have access to the official user manual and should provide accurate, helpful responses based on the documentation.

IMPORTANT GUIDELINES:
1. **Always base your answers on the provided manual excerpts** - if the context doesn't contain relevant information, clearly state this
2. **Provide structured, step-by-step instructions** when explaining procedures
3. **Include specific page references or section names** when possible
4. **Use technical terminology accurately** as defined in the manual
5. **If a user asks about features not covered in the provided context, suggest they check other sections of the manual**

RELEVANT MANUAL EXCERPTS:
{chr(10).join([f"• {ctx}" for ctx in relevant_context])}

RESPONSE FORMAT:
- Start with a direct answer to the user's question
- Reference specific manual sections when applicable
- Provide step-by-step instructions if explaining a procedure
- Include any important warnings or notes from the manual
- If the context is insufficient, suggest what additional information might be needed

Remember: You are helping users understand and operate the GrandMA3 console safely and effectively."""

        # Generate response using chat
        response = chat_handler.generate_response(
            prompt=current_query,
            system_prompt=system_prompt,
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

@router.get("/document-chat/stream")
async def document_chat_stream_get(
    messages: str = Query(..., description="JSON string of messages"),
    top_k: int = Query(5, description="Number of relevant contexts to retrieve"),
    model: Optional[str] = Query(None, description="Optional model override"),
    provider: Optional[str] = Query(None, description="Optional provider override")
):
    """
    GET endpoint for streaming chat response using EventSource.
    
    Args:
        messages: JSON string of chat messages
        top_k: Number of relevant contexts to retrieve
        model: Optional model override
        provider: Optional provider override
    
    Returns:
        StreamingResponse: Server-Sent Events stream of response tokens
    """
    try:
        # Parse messages from JSON string
        parsed_messages = json.loads(messages)
        
        # Create request object
        request = DocumentChatRequest(
            messages=parsed_messages,
            top_k=top_k,
            model=model,
            provider=provider
        )
        
        # Use the same streaming logic as POST endpoint
        return await document_chat_stream_post(request)
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing messages JSON: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON in messages parameter: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Document chat streaming GET error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing streaming chat: {str(e)}"
        )

@router.post("/document-chat/stream")
async def document_chat_stream_post(request: DocumentChatRequest):
    """
    Generate a streaming chat response based on document context and chat history.
    Uses Server-Sent Events (SSE) to stream the response tokens.
    
    Args:
        request (DocumentChatRequest): Contains messages history, search parameters, and provider
    
    Returns:
        StreamingResponse: Server-Sent Events stream of response tokens
    """
    async def generate_stream():
        try:
            # Get chat handler for requested provider or use default
            chat_handler = LLMFactory.create_llm(request.provider, operation="chat")
            logger.info(f"Using provider: {type(chat_handler).__name__}")

            # Get the latest user message
            current_query = request.messages[-1]["content"]
            logger.debug(f"Processing streaming query: {current_query[:50]}...")

            # Initialize context handler
            context_handler = ContextHandler(embedder)
            
            # Get relevant context
            relevant_context = context_handler.get_document_context(
                query=current_query,
                top_k=request.top_k
            )
            
            # Enhanced system prompt for user manual RAG experience
            system_prompt = f"""You are a technical support assistant for the GrandMA3 lighting console. You have access to the official user manual and should provide accurate, helpful responses based on the documentation.

IMPORTANT GUIDELINES:
1. **Always base your answers on the provided manual excerpts** - if the context doesn't contain relevant information, clearly state this
2. **Provide structured, step-by-step instructions** when explaining procedures
3. **Include specific page references or section names** when possible
4. **Use technical terminology accurately** as defined in the manual
5. **If a user asks about features not covered in the provided context, suggest they check other sections of the manual**

RELEVANT MANUAL EXCERPTS:
{chr(10).join([f"• {ctx}" for ctx in relevant_context])}

RESPONSE FORMAT:
- Start with a direct answer to the user's question
- Reference specific manual sections when applicable
- Provide step-by-step instructions if explaining a procedure
- Include any important warnings or notes from the manual
- If the context is insufficient, suggest what additional information might be needed

Remember: You are helping users understand and operate the GrandMA3 console safely and effectively."""

            # Send initial context data
            yield f"data: {json.dumps({'type': 'context', 'contexts': relevant_context, 'provider': type(chat_handler).__name__.replace('Chat', '').lower()})}\n\n"

            # Check if the chat handler supports streaming
            if hasattr(chat_handler, 'generate_streaming_response'):
                # Generate streaming response
                for chunk in chat_handler.generate_streaming_response(
                    prompt=current_query,
                    system_prompt=system_prompt,
                    model=request.model
                ):
                    if chunk and chunk.strip():  # Only send non-empty chunks
                        yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            else:
                # Fallback to non-streaming if streaming is not supported
                response = chat_handler.generate_response(
                    prompt=current_query,
                    system_prompt=system_prompt,
                    model=request.model
                )
                yield f"data: {json.dumps({'type': 'token', 'content': response})}\n\n"

            # Send completion signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Document chat streaming error: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )
    

