import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_compute_mean_valid_payload():
    payload = {
        "values": [1.0, 2.0, 3.0, 4.0, 5.0]
    }
    response = client.post("/compute-mean", json=payload)
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "mean": 3.0
    }

def test_compute_mean_invalid_payload():
    payload = {
        "values": ["a", 2, 3.0]
    }
    response = client.post("/compute-mean", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"] == "All values must be numeric"

def test_compute_mean_empty_payload():
    payload = {
        "values": []
    }
    response = client.post("/compute-mean", json=payload)
    assert response.status_code == 400
    assert "Error processing request" in response.json()["detail"]

def test_compute_mean_no_payload():
    response = client.post("/compute-mean", json={})
    assert response.status_code == 422
