import time
from src.workers.celery_app import celery_app
from src.core.database import SessionLocal
from src.models.document import Document, DocumentStatus

@celery_app.task(bind=True, max_retries=3)
def process_document_task(self, document_id: str):
    """
    Simulates the heavy processing of a document.
    Updates the database state as it progresses.
    """
    db = SessionLocal()
    try:
        # 1. Fetch the document and update status to processing
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return f"Document {document_id} not found."
            
        doc.status = DocumentStatus.PROCESSING
        db.commit()
        
        # 2. Simulate ML embedding generation (e.g., chunking, calling models)
        print(f"Starting ML processing for document: {doc.filename}")
        time.sleep(10) # Simulating a 10-second heavy compute job
        
        # 3. Mark as completed
        doc.status = DocumentStatus.COMPLETED
        db.commit()
        print(f"Finished processing document: {doc.filename}")
        
        return doc.id
        
    except Exception as exc:
        db.rollback()
        # Mark as failed in DB or retry the task
        if doc:
            doc.status = DocumentStatus.FAILED
            db.commit()
        raise self.retry(exc=exc, countdown=5)
    finally:
        db.close()