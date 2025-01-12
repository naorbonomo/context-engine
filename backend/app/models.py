from pydantic import BaseModel

class Document(BaseModel):
    """
    Pydantic model representing a Document.

    Attributes:
        id (str): Unique identifier for the document.
        content (str): The textual content of the document.
    """
    id: str  # Unique identifier for the document
    content: str  # Content of the document 