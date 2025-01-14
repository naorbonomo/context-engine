# API Documentation

This document provides detailed information about all available API endpoints in the Context Engine.

## Base URL

All API endpoints are prefixed with `/api/v1`

## Authentication

Currently, no authentication is required for the API endpoints.

## Endpoints

<details>
<summary><b>GET /hello - Hello World Test Endpoint</b></summary>

Returns a simple greeting message.

**Request**
- Method: GET
- URL: `/api/v1/hello`
- No parameters required

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
{
    "message": "Hello, World!"
}
```

**Error Responses**
- 500 Internal Server Error
  ```json
  {
      "detail": "Internal server error message"
  }
  ```

**Example Usage**
```bash
# Using curl
curl http://localhost:8000/api/v1/hello

# Using httpie
http GET http://localhost:8000/api/v1/hello
```
</details>

<details>
<summary><b>POST /chat - Multi-Provider Chat Generation</b></summary>

Generate a chat response using multiple LLM providers.

**Request**
- Method: POST
- URL: `/api/v1/chat`
- Content-Type: `application/json`

**Request Body**
```json
{
    "prompt": "What is Python?",                           // Required
    "system_prompt": "You are a helpful assistant",        // Optional
    "model": "mixtral-8x7b-32768",                        // Optional
    "max_tokens": 500,                                     // Optional
    "provider": "groq"                                     // Optional (defaults to DEFAULT_CHAT_PROVIDER)
}
```

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
{
    "response": "Generated text response from the model..."
}
```

**Error Responses**
- 500 Internal Server Error
  ```json
  {
      "detail": "Error message (e.g., model not found, connection error)"
  }
  ```

**Example Usage**
```bash
# Using default provider
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d "{\"prompt\": \"What is Python?\"}"

# Using specific provider
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d "{
    \"prompt\": \"What is Python?\",
    \"provider\": \"groq\",
    \"model\": \"mixtral-8x7b-32768\",
    \"max_tokens\": 500
}"
```

**Notes**
- Default provider is set via DEFAULT_CHAT_PROVIDER environment variable
- Supports multiple providers: Groq, OpenAI, Gemini, Ollama
- Automatic fallback to Ollama if primary provider fails
</details>

<details>
<summary><b>POST /ollama-embeddings/embed - Create Document Embeddings</b></summary>

Create embeddings for one or more documents using Ollama models.

**Request**
- Method: POST
- URL: `/api/v1/ollama-embeddings/embed`
- Content-Type: `application/json`

**Request Body**
```json
{
    "contents": ["Document text 1", "Document text 2"],    // Required
    "model": "nomic-embed-text"                           // Optional
}
```

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
{
    "success": true,
    "message": "Successfully embedded 2 documents"
}
```

**Error Responses**
- 500 Internal Server Error
  ```json
  {
      "detail": "Error message"
  }
  ```

**Example Usage**
```bash
curl -X POST "http://localhost:8000/api/v1/ollama-embeddings/embed" \
-H "Content-Type: application/json" \
-d "{
    \"contents\": [\"Document text 1\", \"Document text 2\"],
    \"model\": \"nomic-embed-text\"
}"
```
</details>

<details>
<summary><b>POST /ollama-embeddings/search - Search Embedded Documents</b></summary>

Search through embedded documents using semantic similarity.

**Request**
- Method: POST
- URL: `/api/v1/ollama-embeddings/search`
- Content-Type: `application/json`

**Request Body**
```json
{
    "query": "Your search query",                         // Required
    "top_k": 2,                                          // Optional (default: 2)
    "model": "nomic-embed-text"                          // Optional
}
```

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
{
    "contexts": ["Relevant document 1", "Relevant document 2"],
    "message": "Found 2 relevant documents"
}
```

**Error Responses**
- 500 Internal Server Error
  ```json
  {
      "detail": "Error message"
  }
  ```

**Example Usage**
```bash
curl -X POST "http://localhost:8000/api/v1/ollama-embeddings/search" \
-H "Content-Type: application/json" \
-d "{
    \"query\": \"What is machine learning?\",
    \"top_k\": 3
}"
```
</details>

<details>
<summary><b>POST /document-chat - Document Chat Endpoint</b></summary>

Chat with documents using context-aware responses.

**Request**
- Method: POST
- URL: `/api/v1/document-chat`
- Content-Type: `application/json`

**Request Body**
```json
{
    "query": "Your question about the documents",          // Required
    "context": ["Document context 1", "Document context 2"], // Required
    "max_tokens": 500                                     // Optional
}
```

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
{
    "response": "AI-generated response based on document context",
    "relevant_context": ["Used context pieces..."]
}
```

**Example Usage**
```bash
curl -X POST "http://localhost:8000/api/v1/document-chat" \
-H "Content-Type: application/json" \
-d "{
    \"query\": \"What does the document say about X?\",
    \"context\": [\"Document text 1\", \"Document text 2\"]
}"
```
</details>

<details>
<summary><b>GET /api/v1/documents - List Documents</b></summary>

Retrieve all documents stored in the database.

**Request**
- Method: GET
- URL: `/api/v1/documents`
- No parameters required

**Response**
- Status: 200 OK
- Content-Type: `application/json`

```json
[
    {
        "id": "doc_0",
        "content": "Document content..."
    },
    {
        "id": "doc_1",
        "content": "Another document content..."
    }
]
```

**Error Responses**
- 500 Internal Server Error
  ```json
  {
      "detail": "Error message"
  }
  ```

**Example Usage**
```bash
# Using curl
curl http://localhost:8000/api/v1/documents

# Using httpie
http GET http://localhost:8000/api/v1/documents
```
</details>

## Status Codes

The API uses the following standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting

Currently, no rate limiting is implemented.

## Versioning

The API uses URL versioning (v1). Future versions will be available under different version prefixes (e.g., `/api/v2/`).

## Environment Variables

For a complete list of environment variables and configuration options, see [Environment Variables Documentation](ENV.md).
