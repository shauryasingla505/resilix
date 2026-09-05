# app/api/deps.py
from fastapi import WebSocket
from app.core.manager import manager

def get_websocket_manager():
    return manager