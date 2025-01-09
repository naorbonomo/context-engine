import chromadb  # Import chromadb for vector database operations

class DatabaseHandler:
    """Class to handle read and write operations with the ChromaDB vector database."""

    def __init__(self, db_path: str = "./vector_db"):
        """
        Initialize the DatabaseHandler with a specific database path.

        Args:
            db_path (str, optional): Path to the ChromaDB persistent storage. Defaults to "./vector_db".
        """
        self.client = chromadb.PersistentClient(path=db_path)  # Initialize PersistentClient
        self.collection = self._initialize_collection()  # Initialize or retrieve the collection

    def _initialize_collection(self) -> chromadb.api.model.Collection:
        """
        Initialize and return the ChromaDB collection.

        Returns:
            chromadb.api.model.Collection: The ChromaDB collection for embeddings.
        """
        try:
            collection = self.client.get_collection("vault_embeddings")  # Try to get existing collection
            print("Loading existing vector database...")  # Log loading existing DB
        except:
            collection = self.client.create_collection(
                name="vault_embeddings",
                metadata={"hnsw:space": "cosine"}  # Define similarity metric
            )
            print("Creating new vector database...")  # Log creation of new DB
        return collection  # Return the collection instance

    def add_documents(self, documents: list, embeddings: list, ids: list):
        """
        Add documents and their embeddings to the ChromaDB collection.

        Args:
            documents (list): List of document texts to add.
            embeddings (list): List of embedding vectors corresponding to the documents.
            ids (list): List of unique identifiers for each document.
        """
        if documents and embeddings and ids:
            self.collection.add(
                embeddings=embeddings,  # Add embeddings to the collection
                documents=documents,    # Add document texts
                ids=ids                 # Add unique document IDs
            )
            print("Documents added to the vector database.")  # Log successful addition
        else:
            print("No documents to add.")  # Log if there's nothing to add

    def query_embeddings(self, query_embedding: list, top_k: int = 2) -> list:
        """
        Query the collection for the top_k most similar documents to the query_embedding.

        Args:
            query_embedding (list): The embedding vector for the search query.
            top_k (int, optional): Number of top results to retrieve. Defaults to 2.

        Returns:
            list: List of the most relevant context documents.
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],  # Embed the search query
            n_results=top_k                      # Specify number of results
        )
        if results['documents'][0]:
            return results['documents'][0]  # Return found documents
        return []  # Return empty list if no documents found

    def count_documents(self) -> int:
        """
        Get the total number of documents in the collection.

        Returns:
            int: The count of documents in the collection.
        """
        return self.collection.count()  # Return the number of documents

    def load_documents_from_file(self, filepath: str) -> list:
        """
        Load documents from a specified text file.

        Args:
            filepath (str): Path to the text file containing documents.

        Returns:
            list: List of document texts.
        """
        with open(filepath, 'r', encoding='utf-8') as infile:
            return [line.strip() for line in infile if line.strip()]  # Read and clean lines

    def generate_embeddings(self, contents: list, embedder) -> list:
        """
        Generate embeddings for a list of document contents using the provided embedder.

        Args:
            contents (list): List of document texts to embed.
            embedder: Instance of a class that can generate embeddings.

        Returns:
            list: List of embedding vectors.
        """
        embeddings = []
        for content in contents:
            embedding = embedder.create_embedding(content)  # Generate embedding for each content
            embeddings.append(embedding)  # Append to embeddings list
        return embeddings  # Return all embeddings 