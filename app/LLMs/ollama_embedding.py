import chromadb  # Import chromadb for vector database operations
import openai as OpenAI  # Importing ollama for embeddings
import json
import os  # Import os for environment variables
from dotenv import load_dotenv  # Import dotenv to load environment variables

class OllamaEmbeddings:
    """Class to handle embedding creation using Ollama."""

    def __init__(self, collection: chromadb.api.model.Collection, model: str):
        """
        Initialize the OllamaEmbed with a specific model and client.

        Args:
            model (str): The Ollama model to use for embeddings.
            collection: The ChromaDB collection instance.
        """
        load_dotenv()  # Load environment variables from .env file
        base_url = os.getenv('BASE_URL')  # Get base URL from environment
        api_key = os.getenv('API_KEY')  # Get API key from environment

        self.collection = collection  # Store the ChromaDB collection
        self.model = model  # Store the model name
        self.client = OpenAI(
            base_url=base_url,  # Set base URL from environment
            api_key=api_key  # Set API key from environment
        )  # Store the Ollama client
    
    def create_embedding(self, content: str) -> list:
        """
        Generate an embedding for the given content.

        Args:
            content (str): The text content to embed.

        Returns:
            list: The generated embedding vector.
        """
        embedding_response = self.client.embeddings(model=self.model, prompt=content)  # Generate embedding
        return embedding_response["embedding"]  # Return the embedding vector 
    
    def search(self, query: str, top_k: int = 2) -> list:
        """
        Search the vector database for the most relevant documents based on the query.

        Args:
            query (str): The search query.
            top_k (int, optional): The number of top results to retrieve. Defaults to 2.

        Returns:
            list: A list of relevant context documents.
        """
        print(f"Searching for: {query}")  # Print the search query
        query_embedding = self.client.embeddings(model=self.model, prompt=query)["embedding"]  # Get query embedding
        
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Provide the query embedding
            n_results=top_k  # Number of results to retrieve
        )
        
        if results['documents'][0]:  # Check if there are any documents
            return results['documents'][0]  # Return the retrieved documents
        return []  # Return empty list if no documents found 