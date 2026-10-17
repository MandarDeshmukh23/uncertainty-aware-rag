from fastapi import FastAPI
from src.core.config import settings
from src.api import documents
from src.api import search

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json"
)

# Mount the documents router under the /api/v1 prefix
app.include_router(documents.router, prefix=settings.api_v1_prefix)
app.include_router(search.router, prefix=settings.api_v1_prefix)

@app.get("/health", tags=["System"])
async def health_check():
    """
    Returns the operational status of the API and its environment.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "app_name": settings.app_name
    }