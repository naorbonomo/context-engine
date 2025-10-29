from typing import List, Tuple
from app.utils.logger import get_logger
import re

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
        Generates multiple search queries from a single user query for user manual searches.
        
        Args:
            query (str): Original user query
            
        Returns:
            List[str]: List of generated search queries
        """
        queries = [query]
        
        # Extract technical terms and create variations
        technical_terms = self.extract_technical_terms(query)
        
        # Add technical term variations
        for term in technical_terms:
            if term.lower() not in query.lower():
                queries.append(f"{query} {term}")
        
        # Add common user manual search patterns
        if any(word in query.lower() for word in ['how', 'setup', 'configure', 'install']):
            queries.append(f"{query} procedure steps")
            queries.append(f"{query} instructions")
        
        if any(word in query.lower() for word in ['error', 'problem', 'issue', 'trouble']):
            queries.append(f"{query} troubleshooting")
            queries.append(f"{query} solution")
        
        if any(word in query.lower() for word in ['button', 'knob', 'switch', 'control']):
            queries.append(f"{query} interface")
            queries.append(f"{query} panel")
        
        # Add GrandMA3 specific terms
        if 'grandma' in query.lower() or 'ma3' in query.lower():
            queries.append(f"{query} console")
            queries.append(f"{query} lighting")
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            if q.lower() not in seen:
                seen.add(q.lower())
                unique_queries.append(q)
        
        logger.debug(f"Generated queries: {unique_queries}")
        return unique_queries

    def extract_technical_terms(self, query: str) -> List[str]:
        """
        Extracts potential technical terms from the query.
        
        Args:
            query (str): User query
            
        Returns:
            List[str]: List of technical terms
        """
        # Common GrandMA3 technical terms
        grandma3_terms = [
            'fixture', 'patch', 'programmer', 'executor', 'sequence', 'cue',
            'macro', 'effect', 'palette', 'preset', 'group', 'world',
            'dmx', 'artnet', 'sACN', 'midi', 'osc', 'timecode',
            'grandma3', 'ma3', 'console', 'desk', 'fader', 'encoder',
            'touchscreen', 'display', 'network', 'backup', 'showfile'
        ]
        
        # Extract terms that match technical vocabulary
        found_terms = []
        query_lower = query.lower()
        
        for term in grandma3_terms:
            if term.lower() in query_lower:
                found_terms.append(term)
        
        # Also look for capitalized technical terms
        capitalized_terms = re.findall(r'\b[A-Z][a-zA-Z0-9]*\b', query)
        found_terms.extend(capitalized_terms)
        
        return found_terms

    def analyze_context_sufficiency(self, context_list: List[str], user_input: str) -> Tuple[str, List[str]]:
        """
        Analyzes if the retrieved context is sufficient for answering the user query.
        
        Args:
            context_list (List[str]): Retrieved context passages
            user_input (str): Original user query
            
        Returns:
            Tuple[str, List[str]]: Analysis result and additional queries if needed
        """
        if not context_list:
            return "No context found", [user_input]
        
        # Check if context contains key terms from the query
        query_terms = set(user_input.lower().split())
        context_text = ' '.join(context_list).lower()
        
        # Count how many query terms appear in context
        matching_terms = sum(1 for term in query_terms if term in context_text)
        coverage_ratio = matching_terms / len(query_terms) if query_terms else 0
        
        additional_queries = []
        
        if coverage_ratio < 0.5:  # Less than 50% of terms found
            # Try to find missing terms
            missing_terms = [term for term in query_terms if term not in context_text]
            if missing_terms:
                additional_queries.append(f"{user_input} {' '.join(missing_terms[:3])}")
        
        # Check for procedure-related queries that might need step-by-step info
        if any(word in user_input.lower() for word in ['how', 'step', 'procedure', 'setup']):
            if 'step' not in context_text and 'procedure' not in context_text:
                additional_queries.append(f"{user_input} step by step procedure")
        
        analysis = f"Context coverage: {coverage_ratio:.2f}, Additional queries: {len(additional_queries)}"
        
        return analysis, additional_queries 