import unittest
import asyncio
import aiohttp
from typing import Optional
import os
from dotenv import load_dotenv


class TestOllamaChatAPI(unittest.TestCase):
    """Test class for Ollama Chat API endpoints."""
    
    def setUp(self):
        """Initialize test configuration."""
        load_dotenv()
        self.base_url = "http://localhost:8000/api/v1"
        self.model = os.getenv('OLLAMA_MODEL')
        self.test_chat_prompt = "Explain what FastAPI is."
        self.test_system_prompt = "You are a helpful programming assistant."
        self.timeout = aiohttp.ClientTimeout(total=30)
        
    async def _make_request(self, endpoint: str, payload: dict) -> tuple:
        """Make async HTTP request to API endpoint."""
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(f"{self.base_url}/{endpoint}", json=payload) as response:
                return response.status, await response.json()

    async def async_test_chat_generation(self):
        """Async test for chat response generation."""
        payload = {
            "prompt": self.test_chat_prompt,
            "system_prompt": self.test_system_prompt,
            "model": self.model
        }
        
        status, data = await self._make_request("generate", payload)
        return status, data

    def test_chat_generation(self):
        """Test chat response generation."""
        async def run_test():
            status, data = await self.async_test_chat_generation()
            self.assertEqual(status, 200)
            self.assertIn("response", data)
            self.assertIsInstance(data["response"], str)

        asyncio.run(run_test())

    async def async_test_invalid_model(self):
        """Async test for invalid model behavior."""
        payload = {
            "prompt": self.test_chat_prompt,
            "model": "invalid_model_name"
        }
        
        status, _ = await self._make_request("generate", payload)
        return status

    def test_invalid_model(self):
        """Test behavior with invalid model name."""
        async def run_test():
            status = await self.async_test_invalid_model()
            self.assertEqual(status, 500)

        asyncio.run(run_test()) 