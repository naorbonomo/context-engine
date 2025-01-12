from fastapi import APIRouter, HTTPException  # Import necessary FastAPI components
from fastapi.responses import HTMLResponse  # Import HTMLResponse for returning HTML
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

@router.get("/hello-html", response_class=HTMLResponse)  # Define HTML endpoint
async def hello_world_html():
    """
    A Hello World endpoint that returns a styled HTML greeting.
    
    Returns:
        HTMLResponse: An HTML page with a styled greeting message
    
    Raises:
        HTTPException: If there's an unexpected error during execution
    """
    try:
        logger.info("Processing hello world HTML request")
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Hello World</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f0f2f5;
                    }
                    .greeting {
                        padding: 2rem;
                        background-color: white;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        text-align: center;
                    }
                    h1 {
                        color: #1a73e8;
                        margin: 0;
                    }
                </style>
            </head>
            <body>
                <div class="greeting">
                    <h1>Hello, World! 👋</h1>
                </div>
            </body>
        </html>
        """
        logger.debug("Returning HTML response")
        return HTMLResponse(content=html_content)
    except Exception as e:
        logger.error(f"Error in hello_world_html endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
