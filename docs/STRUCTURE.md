# Project Structure

This document details the organization and purpose of each component in the Context Engine.

## Overview

<details>
<summary>Backend Structure</summary>

```
backend/
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
```

### Core Backend Components

#### Main Application (`app/main.py`)
- FastAPI application initialization
- Router registration
- CORS and logging configuration
- Server startup configuration

#### Language Models (`app/LLMs/`)
- **ollama_chat.py**: Chat interactions, response generation, system prompts
- **ollama_embedding.py**: Document embedding, semantic search, ChromaDB integration

#### API Endpoints (`app/api/v1/endpoints/`)
- **hello_world.py**: Basic test endpoint, health checks
- **ollama_chat_api.py**: Chat generation endpoints, model overrides
- **ollama_embedding_api.py**: Document embedding, semantic search endpoints

#### Handlers (`app/handlers/`)
- **db_handler.py**: ChromaDB management, document storage/retrieval

#### Utilities (`app/utils/`)
- **cors.py**: CORS middleware configuration
- **logger.py**: Logging system configuration

</details>

<details>
<summary>Frontend Structure</summary>

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Chat/
│   │   │   ├── ChatWindow.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── MessageInput.tsx
│   │   ├── Search/
│   │   │   ├── SearchBar.tsx
│   │   │   └── SearchResults.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Loading.tsx
│   ├── pages/              # Page components
│   │   ├── Chat.tsx
│   │   ├── Search.tsx
│   │   └── Home.tsx
│   ├── services/           # API integration
│   │   ├── api.ts
│   │   ├── chatService.ts
│   │   └── searchService.ts
│   ├── types/             # TypeScript interfaces
│   │   ├── chat.ts
│   │   └── search.ts
│   ├── utils/             # Utility functions
│   │   ├── constants.ts
│   │   └── helpers.ts
│   ├── App.tsx
│   └── main.tsx
```

### Core Frontend Components

#### Components (`src/components/`)
- **Chat/**: Chat interface components
  - ChatWindow: Main chat interface
  - MessageList: Chat history display
  - MessageInput: User input handling
- **Search/**: Search functionality
  - SearchBar: Query input
  - SearchResults: Results display
- **common/**: Reusable UI elements

#### Pages (`src/pages/`)
- **Chat.tsx**: Chat page layout and logic
- **Search.tsx**: Search page layout and logic
- **Home.tsx**: Landing page

#### Services (`src/services/`)
- **api.ts**: Axios configuration, base API setup
- **chatService.ts**: Chat-related API calls
- **searchService.ts**: Search-related API calls

#### Types (`src/types/`)
- **chat.ts**: Chat-related interfaces
- **search.ts**: Search-related interfaces

#### Utils (`src/utils/`)
- **constants.ts**: Global constants
- **helpers.ts**: Utility functions

</details>

## Key Features

### Backend Features
- Colored logging system with debug mode
- ChromaDB vector database integration
- Versioned API endpoints
- CORS and security configuration

### Frontend Features
- React 18+ with TypeScript
- Vite for build tooling
- Mantine UI components
- React Query for API state
- Axios for API requests

## Future Additions
- Authentication system
- Rate limiting
- Additional model support
- Enhanced search capabilities
- Real-time chat updates
- Progressive Web App support
