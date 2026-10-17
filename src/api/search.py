from fastapi import APIRouter, Query
from src.services.retrieval import search_documents
from src.services.generation import generate_answer # NEW IMPORT

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_knowledge_base(query: str = Query(..., description="The semantic search query")):
    """Searches the vector database for text chunks semantically similar to the query."""
    results = search_documents(query=query)
    return {"query": query, "results": results}

# NEW ENDPOINT
@router.get("/ask")
def ask_knowledge_base(query: str = Query(..., description="The question to answer based on documents")):
    """Retrieves context and generates an uncertainty-aware answer."""
    # 1. Retrieval Phase
    retrieval_results = search_documents(query=query, top_k=3)
    
    # Evaluate Retrieval Uncertainty (Thresholding cosine similarity)
    if not retrieval_results or retrieval_results[0]["score"] < 0.20:
        return {
            "query": query,
            "answer": "System Refusal: No highly relevant documents found. I cannot answer this reliably.",
            "retrieval_top_score": retrieval_results[0]["score"] if retrieval_results else 0,
            "generation_confidence": None,
            "is_uncertain": True
        }
        
    # 2. Generation Phase
    generation_result = generate_answer(query, retrieval_results)
    
    return {
        "query": query,
        "answer": generation_result["answer"],
        "retrieval_top_score": retrieval_results[0]["score"],
        "generation_confidence": generation_result["confidence_score"],
        "is_uncertain": generation_result["is_uncertain"],
        "sources": [res["document_id"] for res in retrieval_results]
    }