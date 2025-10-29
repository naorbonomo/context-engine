from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
import fitz  # PyMuPDF
import PyPDF2
import io
import os
from app.models import Document  # Your Document model
from app.api.v1.endpoints.ollama_embedding_api import embedder  # Import the existing embedder
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/documents",  # Prefix for all routes in this router
    tags=["documents"]  # Tagging for documentation purposes
)

class PDFUploadResponse(BaseModel):
    success: bool
    message: str
    chunks_processed: int
    total_pages: int

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

@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    chunk_size: Optional[int] = Form(1000),  # Characters per chunk
    overlap: Optional[int] = Form(200)  # Overlap between chunks
):
    """
    Upload and process a PDF file, extracting text and creating embeddings.
    
    Args:
        file: The PDF file to upload
        chunk_size: Number of characters per text chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        PDFUploadResponse: Processing results
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        content = await file.read()
        logger.info(f"Processing PDF: {file.filename}, size: {len(content)} bytes")
        
        # Extract text from PDF
        text_chunks = extract_text_from_pdf(content, chunk_size, overlap)
        
        if not text_chunks:
            raise HTTPException(status_code=400, detail="No text could be extracted from PDF")
        
        # Create embeddings for each chunk
        success = embedder.create_embeddings_batch(text_chunks)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create embeddings")
        
        logger.info(f"Successfully processed {len(text_chunks)} chunks from PDF")
        
        return PDFUploadResponse(
            success=True,
            message=f"Successfully processed PDF with {len(text_chunks)} chunks",
            chunks_processed=len(text_chunks),
            total_pages=len(text_chunks)  # Approximate page count
        )
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def extract_text_from_pdf(pdf_content: bytes, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Extract text from PDF content and split into chunks.
    
    Args:
        pdf_content: Raw PDF file content
        chunk_size: Number of characters per chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    try:
        # Try PyMuPDF first (better text extraction)
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            logger.warning(f"PyMuPDF failed, trying PyPDF2: {str(e)}")
            # Fallback to PyPDF2
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Clean and normalize text
        text = clean_text(text)
        
        if not text.strip():
            logger.warning("No text extracted from PDF")
            return []
        
        # Split text into chunks
        chunks = split_text_into_chunks(text, chunk_size, overlap)
        
        logger.info(f"Extracted {len(chunks)} chunks from PDF")
        return chunks
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return []

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove common PDF artifacts
    text = text.replace('\x00', '')  # Remove null bytes
    text = text.replace('\r', ' ')   # Replace carriage returns
    text = text.replace('\n', ' ')   # Replace newlines with spaces
    
    # Remove multiple spaces
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def split_text_into_chunks(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to split
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text] if text.strip() else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at word boundary
        if end < len(text):
            # Look for the last space before the end
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks