# Project Structure

This document details the organization and purpose of each component in the Context Engine.

## Overview

```
project-root/
├── README.md                 # Project overview and setup instructions
├── docker-compose.yml        # Docker configuration
├── requirements.txt          # Python dependencies
├── app/                     # Main application directory
│    ├── main.py              # Application entry point
│    ├── LLMs/                # Language Model implementations
│    │   ├── __init__.py
│    │   ├── ollama_chat.py       # Ollama chat implementation
│    │   └── ollama_embedding.py  # Ollama embedding implementation
│    ├── api/                 # API endpoints and routing
│    │   └── v1/
│    │       └── endpoints/
│    │           ├── __init__.py
│    │           ├── hello_world.py          # Basic test endpoint
│    │           ├── ollama_chat_api.py      # Chat generation endpoints
│    │           └── ollama_embedding_api.py  # Embedding and search endpoints
│    ├── handlers/            # Database and service handlers
│    │   ├── __init__.py
│    │   └── db_handler.py    # ChromaDB vector database handler
│    └── utils/               # Utility functions and helpers
│        ├── __init__.py
│        ├── cors.py          # CORS configuration
│        └── logger.py        # Logging configuration
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   └── utils/
    └── scripts/
        └── start.sh
```

## Core Components

### Main Application (`app/main.py`)
- FastAPI application initialization
- Router registration
- CORS and logging configuration
- Server startup configuration

### Language Models (`app/LLMs/`)

#### `ollama_chat.py`
- Handles chat interactions with Ollama models
- Manages chat response generation
- Supports system prompts and model switching
- Includes error handling and logging

#### `ollama_embedding.py`
- Manages document embedding creation
- Handles semantic search functionality
- Supports batch processing of documents
- Integrates with ChromaDB for storage

### API Endpoints (`app/api/v1/endpoints/`)

#### `hello_world.py`
- Basic test endpoint
- Demonstrates logging and error handling
- Used for health checks

#### `ollama_chat_api.py`
- Chat generation endpoints
- Request/response models for chat
- Model override capabilities
- Error handling and logging

#### `ollama_embedding_api.py`
- Document embedding creation
- Semantic search functionality
- Batch processing endpoints
- Integration with vector database

### Handlers (`app/handlers/`)

#### `db_handler.py`
- ChromaDB vector database management
- Document storage and retrieval
- Embedding persistence
- Query functionality

### Utilities (`app/utils/`)

#### `cors.py`
- CORS middleware configuration
- Security settings for API access

#### `logger.py`
- Colored logging configuration
- Debug mode support
- Structured logging format

## Key Features

### Logging System
- Colored output for different log levels
- Debug mode toggle via environment variables
- Structured logging format
- Module-level logging configuration

### Database Integration
- Persistent vector storage with ChromaDB
- Document embedding management
- Efficient similarity search
- Batch processing support

### API Structure
- Versioned API endpoints
- Clear separation of concerns
- Consistent error handling
- Request/response validation

### Security
- CORS configuration
- Environment variable management
- Error handling and logging
- Input validation

## Future Additions
- Authentication system
- Rate limiting
- Additional model support
- Enhanced search capabilities
- Frontend integration
