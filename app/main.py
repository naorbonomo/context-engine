import uvicorn  # Importing uvicorn to run the server
from fastapi import FastAPI, HTTPException  # Import FastAPI and HTTPException for handling requests and errors
import logging
import os
from dotenv import load_dotenv

from app.utils.cors import add_cors_middleware  # Import the CORS configuration function

# API Endpoints
from app.api.v1.endpoints.hello_world import router as hello_world_router  # Import the hello world router
from app.api.v1.endpoints.ollama_chat_api import router as ollama_chat_router  # Import the ollama chat router
from app.api.v1.endpoints.ollama_embedding_api import router as ollama_embedding  # Add this import

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG_MODE') == 'True' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI( # Create a FastAPI instance
    title="Context Engine",
    description="A powerful context-aware search and retrieval system.",
    version="1.0.0",
    contact={
        "name": "Naor Bonomo",
        "email": "naorbonomo@gmail.com",
    },
)  
# Configure CORS
add_cors_middleware(app)

app.include_router(hello_world_router)  # Include the hello world router
app.include_router(ollama_chat_router)  # Include the ollama chat router
app.include_router(ollama_embedding)  # Add this line
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)  # Run the server with uvicorn