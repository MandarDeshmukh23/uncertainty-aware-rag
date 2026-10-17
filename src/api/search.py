from fastapi import APIRouter, Query
from src.services.retrieval import search_documents

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_knowledge_base(query: str = Query(..., description="The semantic search query")):
    """Searches the vector database for text chunks semantically similar to the query."""
    results = search_documents(query=query)
    return {"query": query, "results": results}