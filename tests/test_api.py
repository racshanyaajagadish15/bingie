from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OTT Recommender API is running"}

def test_recommendation():
    test_data = {
        "title": "Inception",
        "platform_filter": ["Netflix"],
        "year_range": [2000, 2025],
        "duration_range": [90, 150],
        "top_n": 5
    }
    response = client.post("/recommend", json=test_data)
    assert response.status_code == 200
    assert "results" in response.json()