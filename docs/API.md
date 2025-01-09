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
<summary><b>POST /chat - Ollama Chat Generation</b></summary>

Generate a chat response using Ollama models.

**Request**
- Method: POST
- URL: `/api/v1/chat`
- Content-Type: `application/json`

**Request Body**
```json
{
    "prompt": "What is Python?",                           // Required
    "system_prompt": "You are a helpful assistant",        // Optional
    "model": "mistral",                                   // Optional
    "max_tokens": 500                                     // Optional
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
# Minimal request (only required prompt)
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d "{\"prompt\": \"What is Python?\"}"

# Full request with all options
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d "{
    \"prompt\": \"What is Python?\",
    \"system_prompt\": \"You are a helpful programming assistant.\",
    \"model\": \"mistral\",
    \"max_tokens\": 500
}"
```

**Notes**
- Default model is set via OLLAMA_MODEL environment variable
- Models must be pulled using Ollama CLI before use (e.g., `ollama pull mistral`)
- System prompt helps set the context for the AI response
- Max tokens parameter can limit response length
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
