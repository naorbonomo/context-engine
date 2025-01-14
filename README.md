# Context Engine

A powerful context-aware search and retrieval system built with FastAPI and React.


## 🚧 Project Status & Progress 🚧
- ✅ Basic FastAPI backend structure
- ✅ Vite React frontend setup
- ✅ API - Hello World endpoint
- ✅ API - Ollama Chat API endpoint
- ✅ API - Ollama Embedding API endpoint
- ✅ API - Document Chat API endpoint
- ✅ Document Chat frontend component
- ✅ LLM Prompting
- ✅ Multiple LLM Providers Support
- 🔄 Frontend components development
- 🔄 Database integration (ChromaDB)
- ⏳ Authentication system pending
- 🔄 Search functionality
- ⏳ Chat History
- ⏳ Context Sidebar
- ✅ Document Viewer component
 

## New Features: Multi-Provider LLM Support

### Available Providers
- **Ollama** (Default for embeddings and fallback)
  - Local deployment
  - Multiple models support
  - Used for embeddings and as fallback

- **Gemini** (Google)
  - Fast response times
  - Good for general chat
  - Requires Google API key

- **OpenAI**
  - GPT-3.5 and GPT-4 support
  - High quality responses
  - Requires OpenAI API key

- **Groq**
  - High-performance inference
  - Low latency
  - Requires Groq API key

### Configuration
Add to your `.env` file:
```env
#---LLM Defaults---
DEFAULT_CHAT_PROVIDER=groq  # Options: ollama, gemini, openai, groq
DEFAULT_AUTOCOMPLETE_PROVIDER=ollama

#---API Keys---
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-pro

GROQ_API_KEY=your_key_here
GROQ_MODEL=mixtral-8x7b-32768

OLLAMA_MODEL=your_model_here
OLLAMA_EMBEDDING_MODEL=snowflake-arctic-embed2
```

### New Dependencies
```bash
# Install required packages
pip install google-generativeai  # For Gemini
pip install openai              # For OpenAI
pip install groq                # For Groq
```

### API Usage Examples
```python
# Chat with default provider
POST /api/v1/chat
{
    "prompt": "Hello, how are you?",
    "system_prompt": "Optional system prompt"
}

# Chat with specific provider
POST /api/v1/chat
{
    "prompt": "Hello, how are you?",
    "provider": "groq",
    "model": "mixtral-8x7b-32768"
}

# Document chat with provider selection
POST /api/v1/document-chat
{
    "messages": [{"role": "user", "content": "What do the docs say about X?"}],
    "provider": "gemini",
    "top_k": 5
}
```

### Error Handling
- Automatic fallback to Ollama if primary provider fails
- Detailed error logging for API issues
- Environment validation for required API keys
- Graceful degradation of services

## Requirements

- [Python 3.10](https://www.python.org/downloads/release/python-3100/) 
-  [Node.js 22+](https://nodejs.org/en/download/current)
- [Git](https://git-scm.com/downloads)

## Quick Setup Guide

### Automated Setup (Recommended)

We provide automated setup scripts for both Windows and Unix-based systems:

- Windows:
```powershell
.\setup.ps1
```

- Linux/MacOS:
```bash
./setup.sh
```

These scripts will:
- Check and install required dependencies
- Set up Python virtual environment
- Install Python packages
- Install Node.js packages
- Start both frontend and backend servers

<details>
<summary><b>🔹 Manual Backend Setup</b></summary>

1. Clone the repository:
```bash
git clone https://github.com/naorbonomo/context-engine
cd context-engine
```

2. Create a virtual environment:
```bash
py -3.10 -m venv .venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\.venv\Scripts\activate
```
- Linux/MacOS:
```bash
source .venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend root directory by copying the example:
```bash
cp .env.example .env
```

For detailed environment variable configuration, see [Environment Variables Documentation](docs/ENV.md).


### Starting the Backend

You can start the backend server using the provided scripts:

- Windows:
```bash
run.bat
```

- Linux/MacOS:
```bash
./run.sh
```

Note: Make sure to make the shell script executable on Unix systems:
```bash
chmod +x run.sh
```

### Available Endpoints
The API will be available at:
- API: http://localhost:8000/api/v1
  - GET /hello - Returns a simple JSON greeting
  - GET /hello-html - Returns a styled HTML greeting page
  - POST /chat - Multi-provider chat generation
  - POST /autocomplete - Smart text completion
  - POST /ollama-embeddings/embed - Create document embeddings
  - POST /ollama-embeddings/search - Search through embeddings
- [Detailed API Documentation](docs/API.md)

#### Example Endpoints
1. Basic JSON Greeting
```bash
curl http://localhost:8000/api/v1/hello
```
Response:
```json
{
    "message": "Hello, World!"
}
```

2. Styled HTML Greeting
- Open http://localhost:8000/api/v1/hello-html in your browser to see a styled greeting page




</details>
<details>
<summary><b>🔹 Frontend Setup</b></summary>

The frontend is built with:
- React 18+ with TypeScript
- Vite for build tooling
- Mantine UI for components
- React Query for API state management
- Axios for API requests

To run the frontend:

```bash
cd frontend
npm install
npm run dev
```

The development server will start at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
```
</details>
<details>
<summary><b>🔹 Project Structure</b></summary>

```
project-root/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── deps.py
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   └── endpoints/
│   │   │   └── deps.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   └── scripts/
│       └── start.sh
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
</details>

### Common Issues

1. If Python is not recognized as a command:
   - Verify Python installation: `python --version`
   - Make sure Python is added to your PATH
   - Windows users might need to use `py` instead of `python`

2. Virtual environment not activating:
   - Check that you're in the correct directory
   - On Windows, you might need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

[MIT](LICENSE)

## Troubleshooting

If you encounter any issues:

1. Ensure Python 3.10+ is properly installed
2. Verify your virtual environment is activated (you should see `(.venv)` in your terminal)
3. Check that all requirements are installed: `pip list`
4. Make sure ports 8000 (backend) and 3000 (frontend) are available

For more help, please [create an issue](https://github.com/naorbonomo/context-engine/issues).

## Logging

The application implements comprehensive logging throughout its endpoints. Each API endpoint includes:
- INFO level logging for request processing
- DEBUG level logging for response details
- ERROR level logging for exception handling

Logs are created using Python's built-in logging module and can be configured through the application's logging configuration.

### Features

- **Chat Generation**: Interact with Ollama models for text generation
- **Document Embeddings**: Create and store document embeddings using Ollama models
- **Semantic Search**: Search through embedded documents using natural language queries
- **Batch Processing**: Efficiently process multiple documents in batch
- **Vector Database**: Integrated ChromaDB for efficient vector storage and retrieval
- **Document Viewer**: Interactive component to view and expand stored documents

### Testing

Run the test suite using the provided scripts:

- Windows:
```bash
test.bat
```

- Linux/MacOS:
```bash
./test.sh
```

Note: Make sure to make the shell script executable on Unix systems:
```bash
chmod +x test.sh
```

Key test areas include:
- Chat API functionality
- Embedding creation and retrieval
- Search capabilities
- Batch processing
- Error handling

## 📚 Documentation

Explore our comprehensive documentation to get the most out of the Context Engine:

### Core Documentation
- [API Reference](docs/API.md) - Detailed API endpoints and usage
- [Environment Setup](docs/ENV.md) - Configuration and environment variables
- [Project Structure](docs/STRUCTURE.md) - Codebase organization and architecture

### Guides and Tutorials
- [Quick Start Guide](#quick-setup-guide) - Get up and running quickly
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Testing Guide](docs/TESTING.md) - Running and writing tests

### Technical Details
- [Database Schema](docs/DATABASE.md) - ChromaDB structure and usage
- [Model Configuration](docs/MODELS.md) - Ollama models and settings
- [Logging System](docs/LOGGING.md) - Logging configuration and debugging

### Additional Resources
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Changelog](CHANGELOG.md) - Version history and updates
- [License Information](LICENSE) - MIT License details

## Database Features

The application includes a document database with embedding capabilities:

- **Document Upload**: Users can upload text documents that are automatically embedded using Ollama's embedding model
- **Semantic Search**: Users can search through uploaded documents using natural language queries
- **Real-time Results**: Search results are displayed instantly with relevant context matches

To use these features:
1. Navigate to the Database section
2. Upload documents using the upload form
3. Use the search bar to find relevant content across all uploaded documents