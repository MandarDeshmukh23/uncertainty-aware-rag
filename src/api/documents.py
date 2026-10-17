import os
import hashlib
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.models.document import Document
from src.models.schemas import DocumentResponse
from src.workers.tasks import process_document_task

router = APIRouter(prefix="/documents", tags=["Documents"])

# Ensure a local data directory exists to store uploads
os.makedirs("data", exist_ok=True)

@router.post("/", response_model=DocumentResponse, status_code=201)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads a PDF, saves it locally, and triggers background processing."""
    
    # 1. Read the file to compute a unique hash (prevents duplicate processing)
    content = file.file.read()
    content_hash = hashlib.sha256(content).hexdigest()
    file.file.seek(0) # Reset the file pointer after reading
    
    # 2. Check if this exact file was already uploaded
    existing = db.query(Document).filter(Document.content_hash == content_hash).first()
    if existing:
        raise HTTPException(status_code=400, detail="Document with this content already exists.")
    
    # 3. Save the file to the local disk
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 4. Save metadata to the database
    new_doc = Document(filename=file_path, content_hash=content_hash)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    # 5. Push the background job to RabbitMQ
    process_document_task.delay(new_doc.id)
    
    return new_doc

@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str, db: Session = Depends(get_db)):
    """Fetches the processing status of a specific document."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc