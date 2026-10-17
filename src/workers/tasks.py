import uuid
from src.workers.celery_app import celery_app
from src.core.database import SessionLocal
from src.models.document import Document, DocumentStatus
from src.services.ml import extract_text, chunk_text, generate_embeddings
from src.services.vector_store import qdrant_client, COLLECTION_NAME, init_vector_store
from qdrant_client.http.models import PointStruct

@celery_app.task(bind=True, max_retries=3)
def process_document_task(self, document_id: str):
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return
            
        doc.status = DocumentStatus.PROCESSING
        db.commit()
        print(f"Starting ML processing for: {doc.filename}")
        
        # 1. Initialize Vector DB
        init_vector_store()
        
        # 2. Extract and chunk text
        raw_text = extract_text(doc.filename)
        chunks = chunk_text(raw_text)
        print(f"Generated {len(chunks)} chunks.")
        
        # 3. Generate mathematical embeddings
        vectors = generate_embeddings(chunks)
        print(f"Generated embeddings of dimension {len(vectors[0])}.")
        
        # 4. Construct payload and push to Qdrant
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"document_id": doc.id, "chunk_index": i, "text": chunk}
            )
            for i, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)
        print("Successfully uploaded vectors to Qdrant.")
        
        doc.status = DocumentStatus.COMPLETED
        db.commit()
        return doc.id
        
    except Exception as exc:
        db.rollback()
        if 'doc' in locals() and doc:
            doc.status = DocumentStatus.FAILED
            db.commit()
        raise self.retry(exc=exc, countdown=5)
    finally:
        db.close()