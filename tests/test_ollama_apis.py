import unittest
import asyncio
from tests.api.test_chat_api import TestOllamaChatAPI
from tests.api.test_embedding_api import TestOllamaEmbeddingAPI

def main():
    """Run all API tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaChatAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaEmbeddingAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    main() 