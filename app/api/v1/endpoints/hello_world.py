from fastapi import APIRouter, HTTPException  # Import necessary FastAPI components
import logging  # Import logging module

# Configure logger for this module
logger = logging.getLogger(__name__)  # Create a logger instance for this file

router = APIRouter(
    prefix="/api/v1",  # Set the prefix for all routes in this router
    tags=["hello-world"]  # Add tags for API documentation
)

@router.get("/hello")  # Define the GET endpoint
async def hello_world():
    """
    A simple Hello World endpoint that returns a greeting message.
    
    Returns:
        dict: A dictionary containing a greeting message
    
    Raises:
        HTTPException: If there's an unexpected error during execution
    """
    try:
        logger.info("Processing hello world request")  # Log the request
        response = {"message": "Hello, World!"}
        logger.debug(f"Returning response: {response}")  # Log the response
        return response  # Return greeting message
    except Exception as e:
        logger.error(f"Error in hello_world endpoint: {str(e)}")  # Log any errors
        raise HTTPException(status_code=500, detail=str(e))  # Handle any unexpected errors
