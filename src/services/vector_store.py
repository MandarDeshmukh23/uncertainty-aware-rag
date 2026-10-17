from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from src.core.config import settings

# Initialize connection to the local Docker container
qdrant_client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

COLLECTION_NAME = "document_chunks"
# all-MiniLM-L6-v2 outputs vectors with exactly 384 dimensions
VECTOR_SIZE = 384 

def init_vector_store():
    """Ensures the Qdrant collection exists before we try inserting data."""
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )