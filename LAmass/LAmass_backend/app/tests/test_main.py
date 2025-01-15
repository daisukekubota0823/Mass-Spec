from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Python-R Integration API"}

def test_process_data():
    payload = {"values": [1, 2, 3, 4, 5]}
    response = client.post("/process-data", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["result"]["sum"] == 15