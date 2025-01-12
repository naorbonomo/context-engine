"""
CORS configuration for the FastAPI application.
"""

from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """Add CORS middleware to the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 