# tests/test_routing.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_reroute():
    response = client.post("/api/v1/routing/reroute", json={
        "start": [12.9100, 79.1300],
        "destination": [12.9250, 79.1400],
        "blocked_nodes": []
    })
    assert response.status_code == 200
    data = response.json()
    assert "path_coordinates" in data
    assert "eta_minutes" in data
    assert "hazards_avoided" in data
    assert len(data["path_coordinates"]) > 0

def test_reroute_with_blocked_nodes():
    response = client.post("/api/v1/routing/reroute", json={
        "start": [12.9100, 79.1300],
        "destination": [12.9250, 79.1400],
        "blocked_nodes": ["node_101"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["hazards_avoided"] == 1

def test_invalid_reroute_payload():
    response = client.post("/api/v1/routing/reroute", json={
        "start": [12.9100],
        "destination": "invalid_coord"
    })
    assert response.status_code == 422