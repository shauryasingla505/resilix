# tests/test_websockets.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_connection():
    with client.websocket_connect("/ws/telemetry") as websocket:
        data = websocket.receive_json()
        assert data is not None

def test_websocket_payload_schema():
    with client.websocket_connect("/ws/telemetry") as websocket:
        data = websocket.receive_json()
        assert "timestamp" in data
        assert "storm_intensity" in data
        assert "nodes" in data
        assert "transformers" in data
        assert isinstance(data["nodes"], list)

def test_websocket_multiple_frames():
    with client.websocket_connect("/ws/telemetry") as websocket:
        frame_1 = websocket.receive_json()
        frame_2 = websocket.receive_json()
        assert "timestamp" in frame_1
        assert "timestamp" in frame_2