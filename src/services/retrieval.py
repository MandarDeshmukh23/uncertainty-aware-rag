from src.services.ml import model
from src.services.vector_store import qdrant_client, COLLECTION_NAME

def search_documents(query: str, top_k: int = 3) -> list[dict]:
    """
    Embeds a user query and performs a cosine-similarity search against Qdrant.
    """
    # 1. Convert the text query into a 384-dimensional vector
    query_vector = model.encode(query).tolist()
    
    # 2. Search Qdrant for the nearest neighbors using the newer query_points API
    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True # Returns the actual text chunk, not just the vector ID
    )
    
    # 3. Format the results
    results = []
    # Qdrant's query_points returns an object that has a .points attribute
    for hit in search_results.points:
        results.append({
            "score": hit.score, # Cosine similarity score
            "document_id": hit.payload.get("document_id"),
            "text": hit.payload.get("text")
        })
        
    return results