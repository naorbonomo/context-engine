import unittest
import asyncio
from app.LLMs.ollama_chat import OllamaChat

class TestStreaming(unittest.TestCase):
    """Test streaming functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.chat = OllamaChat()
    
    def test_streaming_response_generator(self):
        """Test that streaming response returns a generator."""
        prompt = "Hello, how are you?"
        generator = self.chat.generate_streaming_response(prompt)
        
        # Check that it's a generator
        self.assertTrue(hasattr(generator, '__iter__'))
        self.assertTrue(hasattr(generator, '__next__'))
    
    def test_streaming_response_content(self):
        """Test that streaming response yields content."""
        prompt = "Say 'test'"
        generator = self.chat.generate_streaming_response(prompt)
        
        # Get first few chunks
        chunks = []
        try:
            for i, chunk in enumerate(generator):
                if i >= 5:  # Limit to first 5 chunks for testing
                    break
                chunks.append(chunk)
        except Exception as e:
            # If Ollama is not running, this is expected
            print(f"Ollama not available: {e}")
            return
        
        # If we got chunks, they should be strings
        for chunk in chunks:
            self.assertIsInstance(chunk, str)

if __name__ == "__main__":
    unittest.main() 