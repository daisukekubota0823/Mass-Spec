from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_compute_mean_success():
    response = client.post("/compute-mean", json={"values": [1, 2, 3, 4]})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["mean"] == 2.5

def test_compute_mean_failure():
    response = client.post("/compute-mean", json={"values": []})
    assert response.status_code == 400