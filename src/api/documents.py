from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.document import Document
from src.models.schemas import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/", response_model=DocumentResponse, status_code=201)
def register_document(doc_in: DocumentCreate, db: Session = Depends(get_db)):
    """Registers a new document in the system to be processed."""
    
    # Enforce uniqueness on the content hash
    existing = db.query(Document).filter(Document.content_hash == doc_in.content_hash).first()
    if existing:
        raise HTTPException(status_code=400, detail="Document with this content hash already exists.")
    
    new_doc = Document(filename=doc_in.filename, content_hash=doc_in.content_hash)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str, db: Session = Depends(get_db)):
    """Fetches the processing status of a specific document."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc