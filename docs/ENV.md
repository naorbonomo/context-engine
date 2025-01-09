# Environment Variables

This document details all environment variables used in the Context Engine.

## Required Variables

### Ollama Configuration
- `OLLAMA_MODEL`: Default model for chat generation (e.g., "llama3.2-vision:11b")
- `OLLAMA_EMBEDDING_MODEL`: Default model for creating embeddings (e.g., "snowflake-arctic-embed2:latest")

### Database Configuration
- `EMBEDDING_DB_PATH`: Path to ChromaDB storage directory (e.g., "./chromadb") ! - NOT used yet

## Optional Variables

### API Configuration
- `HOST`: API host (default: "0.0.0.0")
- `PORT`: API port (default: 8000)

### Logging Configuration
- `LOG_LEVEL`: Logging level (default: "INFO")
- `LOG_FILE`: Path to log file (default: "app.log")
- `DEBUG_MODE`: Enable detailed logging (default: False)

## Example .env File

```env
# Ollama Configuration
OLLAMA_MODEL=llama3.2-vision:11b
OLLAMA_EMBEDDING_MODEL=snowflake-arctic-embed2:latest

# Database Configuration
EMBEDDING_DB_PATH=./chromadb

# API Configuration
HOST=0.0.0.0
PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log
DEBUG_MODE=True
```

## Setting Up Environment Variables

1. Copy the example .env file:
```bash
cp .env.example .env
```

2. Edit the .env file with your preferred settings:
```bash
nano .env
```

3. The application will automatically load these variables using python-dotenv.

## Notes

- Never commit the `.env` file to version control
- Always use `.env.example` as a template for required variables
- Make sure to pull required Ollama models before using them:
  ```bash
  ollama pull llama3.2-vision:11b
  ollama pull snowflake-arctic-embed2:latest
  ``` 