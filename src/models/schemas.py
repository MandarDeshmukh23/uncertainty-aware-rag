from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.document import DocumentStatus

# Schema for the incoming request when registering a new document
class DocumentCreate(BaseModel):
    filename: str
    content_hash: str

# Schema for the outgoing response
class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_hash: str
    status: DocumentStatus
    created_at: datetime
    updated_at: datetime

    # This tells Pydantic to read data directly from the SQLAlchemy ORM object
    model_config = ConfigDict(from_attributes=True)