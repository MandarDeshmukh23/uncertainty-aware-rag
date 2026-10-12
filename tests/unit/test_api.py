from fastapi.testclient import TestClient
from src.api.main import app
from src.core.config import settings

client = TestClient(app)

def test_health_check_returns_200():
    """
    Ensure the health check endpoint responds with 200 OK
    and correctly reflects the application configuration.
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert data["environment"] == settings.environment
    assert data["app_name"] == settings.app_name