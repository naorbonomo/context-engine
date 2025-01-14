import chromadb  # Import chromadb for vector database operations
import json
import os  # Import os for environment variables
import ollama  # Import ollama for embedding
from dotenv import load_dotenv  # Import dotenv to load environment variables
from chromadb.api.models.Collection import Collection  # Correct import for Collection type
from app.LLMs.llm_factory import LLMFactory  # Update import
from app.utils.logger import get_logger  # Add this import

load_dotenv()  # Load environment variables from .env file

logger = get_logger(__name__)  # Initialize logger for this module

class OllamaEmbeddings:
    """Class to handle embedding creation using Ollama."""

    def __init__(self, collection: Collection, default_model: str = os.getenv('OLLAMA_EMBEDDING_MODEL')):
        """
        Initialize the OllamaEmbed with a specific model and client.

        Args:
            model (str): The Ollama model to use for embeddings.
            collection: The ChromaDB collection instance.
        """
        self.collection = collection  # Store the ChromaDB collection
        self.model = default_model  # Store the model name
        self.client = ollama  # Initialize Ollama client
        # Use LLMFactory instead of direct OllamaChat instantiation
        self.chat_handler = LLMFactory.create_llm(os.getenv('DEFAULT_CHAT_PROVIDER'))
        logger.info(f"Initialized OllamaEmbeddings with model: {self.model}")

    def create_embedding(self, content: str) -> bool:
        """
        Generate an embedding for the given content and add it to the ChromaDB collection.

        Args:
            content (str): The text content to embed and store.

        Returns:
            bool: True if embedding was created and stored successfully, False otherwise.
        """
        try:
            if content.strip():  # Skip empty content
                embedding = self.client.embeddings(model=self.model, prompt=content)["embedding"]  # Generate embedding
                doc_id = f"doc_{self.collection.count()}"  # Generate unique ID based on current count
                
                # Add single document with its embedding to the collection
                self.collection.add(
                    embeddings=[embedding],  # List of embeddings (single item)
                    documents=[content.strip()],  # List of documents (single item)
                    ids=[doc_id]  # List of IDs (single item)
                )
                return True  # Return True if successful
            return False  # Return False if content was empty
        except Exception as e:
            print(f"Error creating embedding: {str(e)}")  # Log error for debugging
            return False  # Return False if any error occurred

    def search(self, query: str, top_k: int = 2) -> list:
        """
        Search the vector database for the most relevant documents based on the query.

        Args:
            query (str): The search query.
            top_k (int, optional): The number of top results to retrieve. Defaults to 2.

        Returns:
            list: A list of relevant context documents.
        """
        logger.debug(f"Searching for: {query}")  # Changed to debug level
        query_embedding = self.client.embeddings(model=self.model, prompt=query)["embedding"]  # Get query embedding
        
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Provide the query embedding
            n_results=top_k  # Number of results to retrieve
        )
        
        if results['documents'][0]:  # Check if there are any documents
            return results['documents'][0]  # Return the retrieved documents
        return []  # Return empty list if no documents found 
    
    def create_embeddings_batch(self, contents: list) -> bool:
        """
        Generate embeddings for multiple documents and add them to the ChromaDB collection in batch.

        Args:
            contents (list): List of text contents to embed and store.

        Returns:
            bool: True if embeddings were created and stored successfully, False otherwise.
        """
        try:
            logger.debug(f"Creating embeddings for {len(contents)} documents")
            embeddings = []
            ids = []
            documents = []
            
            for idx, content in enumerate(contents):
                if content.strip():# Skip empty content
                    logger.debug(f"Processing document {idx+1}/{len(contents)}")
                    embedding = self.client.embeddings(model=self.model, prompt=content)["embedding"]
                    embeddings.append(embedding)
                    ids.append(f"doc_{self.collection.count() + idx}")  # Generate unique IDs
                    documents.append(content.strip())
            
            if documents:  # Only add if we have valid documents
                logger.info(f"Adding {len(documents)} embeddings to collection")
                self.collection.add(
                    embeddings=embeddings,
                    documents=documents,
                    ids=ids
                )
                return True
            logger.warning("No valid documents to embed")
            return False
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {str(e)}")
            return False 
    
    def get_multiple_queries(self, user_input: str, max_tokens: int = 200) -> list:
        """
        Generate multiple search queries from user input using the model.

        Args:
            user_input (str): The user's question or input.
            max_tokens (int, optional): Maximum tokens for response. Defaults to 200.

        Returns:
            list: List of generated search queries.
        """
        prompt = """You are a documentation expert. Based on the user's question, generate 3-5 search queries 
        that would help find relevant information in technical documentation.
        Return only the queries, one per line, without numbering or additional text.
        
        User question: {question}
        """.format(question=user_input)
        
        response = self.chat_handler.generate_response(
            prompt=prompt,
            max_tokens=max_tokens,
        )
        
        # Split the response string into a list of queries
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        return queries
    
    def get_relevant_context(self, queries: list, top_k: int = 2) -> list:
        """
        Get relevant context using multiple queries.

        Args:
            queries (list): List of search queries.
            top_k (int, optional): Number of top results per query. Defaults to 2.

        Returns:
            list: List of unique relevant contexts.
        """
        all_contexts = []
        
        for query in queries:
            contexts = self.search(query, top_k)  # Use existing search method
            all_contexts.extend(contexts)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_contexts = [x for x in all_contexts if not (x in seen or seen.add(x))]
        return unique_contexts 
    
    def analyze_context_sufficiency(self, context_list: list, user_input: str, max_tokens: int = 200) -> tuple[str, list]:
        """
        Analyze if the retrieved context is sufficient to answer the user's question.
        
        Args:
            context_list (list): List of retrieved context passages
            user_input (str): The user's original question
            max_tokens (int, optional): Maximum tokens for response. Defaults to 200.
            
        Returns:
            tuple[str, list]: Analysis result and list of additional queries if needed
        """
        analysis_prompt = """You are a documentation expert. Review the retrieved context and the user's question. 
        Look for any mentions of commands or features that need more detailed explanation.
        
        User question: {question}
        
        Retrieved context:
        {context}
        """.format(
            question=user_input,
            context='\n'.join(context_list)
        )
        
        try:
            response = self.chat_handler.generate_response(
                prompt=analysis_prompt,
                max_tokens=max_tokens,
            )
            
            analysis = response.strip()  # Just clean up any whitespace
            logger.debug(f"Context analysis: {analysis}")
            
            # Extract additional queries if context is insufficient
            additional_queries = []
            if "SUFFICIENT" not in analysis.upper():
                additional_queries = [q.strip('- ') for q in analysis.split('\n') 
                                   if q.strip().startswith('-')]
            
            return analysis, additional_queries
            
        except Exception as e:
            logger.error(f"Error analyzing context: {str(e)}")
            return "Error analyzing context", [] 
    
    def list_documents(self) -> list:
        """
        List all documents stored in the ChromaDB collection.

        Returns:
            list: A list of dictionaries containing document IDs and their content.
        """
        try:
            # Get all documents from the collection
            results = self.collection.get()
            
            # Format the results into a list of dictionaries
            documents = []
            for doc_id, content in zip(results['ids'], results['documents']):
                documents.append({
                    'id': doc_id,
                    'content': content
                })
            
            logger.info(f"Retrieved {len(documents)} documents from collection")
            return documents
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return [] 