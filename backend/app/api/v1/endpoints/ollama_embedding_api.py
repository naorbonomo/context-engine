from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from app.LLMs.embedding_factory import EmbeddingFactory
from app.handlers.db_handler import DatabaseHandler

load_dotenv()

router = APIRouter(
    prefix="/api/v1/ollama-embeddings",
    tags=["ollama-embeddings"]
)

# Initialize handlers with error handling
try:
    db_handler = DatabaseHandler()  # Initialize with default path
    embedder = EmbeddingFactory.create_embedder(
        provider=os.getenv('DEFAULT_EMBEDDING_PROVIDER'),
        collection=db_handler.collection
    )
except Exception as e:
    print(f"Error initializing handlers: {str(e)}")
    raise

class EmbeddingRequest(BaseModel):
    """Request model for embedding creation."""
    contents: List[str]  # List of texts to embed
    model: Optional[str] = None  # Optional model override

class SearchRequest(BaseModel):
    """Request model for document search."""
    query: str  # Search query
    top_k: Optional[int] = 2  # Number of results to return
    model: Optional[str] = None  # Optional model override

class EmbeddingResponse(BaseModel):
    """Response model for embedding operations."""
    success: bool
    message: str

class SearchResponse(BaseModel):
    """Response model for search operations."""
    contexts: List[str]

@router.post("/embed", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """Create embeddings for provided contents and store in database."""
    try:
        if not request.contents:
            return EmbeddingResponse(
                success=True,
                message="Successfully embedded 0 documents"
            )

        if request.model:
            embedder.model = request.model

        # Use single document embedding for single items
        if len(request.contents) == 1:
            success = embedder.create_embedding(request.contents[0])
        # Use batch processing for multiple documents
        else:
            success = embedder.create_embeddings_batch(request.contents)
        
        if success:
            return EmbeddingResponse(
                success=True,
                message=f"Successfully embedded {len(request.contents)} documents"
            )
        else:
            return EmbeddingResponse(
                success=False,
                message="Failed to embed documents"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=dict)
async def search_documents(request: SearchRequest):
    """
    Search for relevant documents using embeddings.

    Args:
        request (SearchRequest): The search request containing query and parameters.

    Returns:
        dict: Dictionary containing search results.
    """
    try:
        # Update model if provided
        if request.model:
            embedder.model = request.model

        # Get relevant contexts
        contexts = embedder.search(
            query=request.query,
            top_k=request.top_k
        )

        return {
            "contexts": contexts,
            "message": f"Found {len(contexts)} relevant documents"
        }
    except Exception as e:
        print(f"Error in search: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e)) 