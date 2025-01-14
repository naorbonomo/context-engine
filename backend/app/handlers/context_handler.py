from typing import List, Tuple
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ContextHandler:
    """
    Handles document context operations including query generation, context retrieval,
    and context analysis for chat interactions.
    """

    def __init__(self, embedder):
        """
        Initialize ContextHandler with an embedder instance.
        
        Args:
            embedder: An embedding provider instance that handles vector operations
        """
        self.embedder = embedder

    def get_document_context(self, query: str, top_k: int = 5) -> List[str]:
        """
        Retrieves relevant document context using multi-query approach.
        
        Args:
            query (str): User's input query
            top_k (int): Number of top contexts to retrieve
            
        Returns:
            List[str]: List of relevant context passages
        """
        logger.debug("Generating search queries...")
        queries = self.get_multiple_queries(query)
        
        # Get initial context
        relevant_context = self.embedder.get_relevant_context(
            queries=queries,
            top_k=top_k
        )
        
        # Analyze and expand context if needed
        if relevant_context:
            analysis, additional_queries = self.analyze_context_sufficiency(
                context_list=relevant_context,
                user_input=query
            )
            
            logger.debug(f"Context analysis: {analysis}")
            
            # If context is insufficient and we have additional queries, get more context
            if additional_queries:
                additional_context = self.embedder.get_relevant_context(
                    queries=additional_queries,
                    top_k=top_k
                )
                relevant_context.extend(additional_context)
        
        return relevant_context

    def get_multiple_queries(self, query: str) -> List[str]:
        """
        Generates multiple search queries from a single user query.
        
        Args:
            query (str): Original user query
            
        Returns:
            List[str]: List of generated search queries
        """
        # TODO: Implement query expansion logic
        # For now, return the original query
        return [query]

    def analyze_context_sufficiency(self, context_list: List[str], user_input: str) -> Tuple[str, List[str]]:
        """
        Analyzes if the retrieved context is sufficient for answering the user query.
        
        Args:
            context_list (List[str]): Retrieved context passages
            user_input (str): Original user query
            
        Returns:
            Tuple[str, List[str]]: Analysis result and additional queries if needed
        """
        # TODO: Implement context analysis logic
        # For now, return no additional queries needed
        return "Context appears sufficient", [] 