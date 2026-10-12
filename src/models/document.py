import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum
from src.core.database import Base
import enum

class DocumentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Document(Base):
    __tablename__ = "documents"

    # We use UUIDs instead of auto-incrementing integers. 
    # This prevents ID collision in distributed environments and obscures database size.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    filename = Column(String, nullable=False)
    content_hash = Column(String, unique=True, index=True, nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)