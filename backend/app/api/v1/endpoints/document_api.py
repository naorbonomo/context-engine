from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Document  # Your Document model
from app.api.v1.endpoints.ollama_embedding_api import embedder  # Import the existing embedder

router = APIRouter(
    prefix="/api/v1/documents",  # Prefix for all routes in this router
    tags=["documents"]  # Tagging for documentation purposes
)

@router.get("/", response_model=List[Document])
async def list_documents():
    """
    Retrieve all documents from the ChromaDB collection.

    Returns:
        List[Document]: A list of Document objects containing IDs and content.
    """
    try:
        documents = embedder.list_documents()  # Fetch documents using the existing embedder
        return documents  # Return the list of documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Raise HTTP exception on error