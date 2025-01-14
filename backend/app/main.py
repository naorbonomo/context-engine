import uvicorn  # Importing uvicorn to run the server
from fastapi import FastAPI, HTTPException  # Import FastAPI and HTTPException for handling requests and errors
import logging
import os
from dotenv import load_dotenv

from app.utils.cors import add_cors_middleware  # Import the CORS configuration function

# API Endpoints
from app.api.v1.endpoints.hello_world import router as hello_world_router  # Import the hello world router
from app.api.v1.endpoints.chat_api import router as chat_router   # Import the chat router
from app.api.v1.endpoints.ollama_embedding_api import router as ollama_embedding_router  # Import the ollama embedding router
from app.api.v1.endpoints.document_chat_api import router as document_chat_router  # Import the document chat router
from app.api.v1.endpoints.document_api import router as document_router  # Import the new document router

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG_MODE') == 'True' else logging.INFO,  # Set log level based on environment
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Define log format
)

app = FastAPI(
    title="Context Engine",  # Title of the API
    description="A powerful context-aware search and retrieval system.",  # Description of the API
    version="1.0.0",  # Version of the API
    contact={
        "name": "Naor Bonomo",  # Contact name
        "email": "naorbonomo@gmail.com",  # Contact email
    },
)  
# Configure CORS
add_cors_middleware(app)  # Add CORS middleware to the FastAPI app

# Include API routers
app.include_router(hello_world_router)  # Include the hello world router
app.include_router(chat_router)  # Include the chat router
app.include_router(ollama_embedding_router)  # Include the ollama embedding router
app.include_router(document_chat_router)  # Include the document chat router
app.include_router(document_router)  # Include the new document router

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # Run the server with uvicorn