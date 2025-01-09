import unittest
import asyncio
import aiohttp
from typing import List
from dotenv import load_dotenv
import os

class TestOllamaEmbeddingAPI(unittest.TestCase):
    """Test class for Ollama Embedding API endpoints."""
    
    def setUp(self):
        """Initialize test configuration."""
        load_dotenv()
        self.base_url = "http://localhost:8000/api/v1/ollama-embeddings"
        self.model = os.getenv('OLLAMA_EMBEDDING_MODEL')
        self.timeout = aiohttp.ClientTimeout(total=30)
        
        # Test data
        self.test_documents = [
            "This is a test document about Python programming.",
            "FastAPI is a modern web framework for building APIs.",
            "Vector databases are used for semantic search."
        ]
        self.test_query = "How does Python programming work?"

    async def _make_request(self, endpoint: str, payload: dict) -> tuple:
        """Make async HTTP request to API endpoint."""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(f"{self.base_url}/{endpoint}", json=payload) as response:
                return response.status, await response.json()

    async def async_test_embedding_creation(self):
        """Async test for embedding creation."""
        payload = {
            "contents": self.test_documents,
            "model": self.model
        }
        
        status, data = await self._make_request("embed", payload)
        return status, data


    def test_embedding_creation(self):
        """Test creating embeddings for documents."""
        async def run_test():
            status, data = await self.async_test_embedding_creation()
            self.assertEqual(status, 200)
            self.assertTrue(data["success"])
            self.assertIn("Successfully embedded", data["message"])
            self.assertIn(str(len(self.test_documents)), data["message"])  # Verify correct count

            # Test failed embedding case
            payload = {
                "contents": [""],  # Empty content should fail
                "model": self.model
            }
            status, data = await self._make_request("embed", payload)
            self.assertEqual(status, 200)
            self.assertFalse(data["success"])
            self.assertIn("Failed", data["message"])

        asyncio.run(run_test())

    async def async_test_embedding_search(self):
        """Async test for embedding search."""
        # First, ensure we have some embeddings to search through
        await self.async_test_embedding_creation()
        
        payload = {
            "query": self.test_query,
            "top_k": 2,
            "model": self.model
        }
        
        status, data = await self._make_request("search", payload)
        return status, data

    def test_embedding_search(self):
        """Test searching through embedded documents."""
        async def run_test():
            status, data = await self.async_test_embedding_search()
            self.assertEqual(status, 200)
            self.assertIn("contexts", data)
            self.assertIsInstance(data["contexts"], list)

        asyncio.run(run_test())

    async def async_test_empty_content(self):
        """Async test for empty content handling."""
        payload = {
            "contents": [],
            "model": self.model
        }
        
        status, data = await self._make_request("embed", payload)
        return status, data

    def test_empty_content(self):
        """Test behavior with empty content."""
        async def run_test():
            status, data = await self.async_test_empty_content()
            self.assertEqual(status, 200)
            self.assertTrue(data["success"])
            self.assertIn("embedded 0 documents", data["message"].lower())

        asyncio.run(run_test())

    async def async_test_large_batch(self):
        """Async test for large batch processing."""
        large_batch = ["Test document " + str(i) for i in range(100)]
        
        payload = {
            "contents": large_batch,
            "model": self.model
        }
        
        status, data = await self._make_request("embed", payload)
        return status, data

    def test_large_batch(self):
        """Test handling of large batch of documents."""
        async def run_test():
            status, data = await self.async_test_large_batch()
            self.assertEqual(status, 200)
            self.assertTrue(data["success"])
            self.assertIn("100", data["message"])  # Verify 100 documents were processed

        asyncio.run(run_test())

    def test_single_embedding_creation(self):
        """Test creating embedding for a single document."""
        async def run_test():
            # Test single document embedding
            payload = {
                "contents": [self.test_documents[0]],  # Single document
                "model": self.model
            }
            status, data = await self._make_request("embed", payload)
            self.assertEqual(status, 200)
            self.assertTrue(data["success"])
            self.assertIn("Successfully embedded 1", data["message"])

            # Test failed single embedding case
            payload = {
                "contents": [""],  # Empty content should fail
                "model": self.model
            }
            status, data = await self._make_request("embed", payload)
            self.assertEqual(status, 200)
            self.assertFalse(data["success"])
            self.assertIn("Failed", data["message"])

        asyncio.run(run_test())

    def test_batch_embedding_creation(self):
        """Test creating embeddings for multiple documents."""
        async def run_test():
            # Test multiple documents embedding
            payload = {
                "contents": self.test_documents,  # Multiple documents
                "model": self.model
            }
            status, data = await self._make_request("embed", payload)
            self.assertEqual(status, 200)
            self.assertTrue(data["success"])
            self.assertIn(f"Successfully embedded {len(self.test_documents)}", data["message"])

        asyncio.run(run_test())

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Add cleanup if needed, like removing test documents from the database
        pass 