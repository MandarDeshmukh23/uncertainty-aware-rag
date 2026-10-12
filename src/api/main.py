from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json"
)

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