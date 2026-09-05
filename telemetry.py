# app/api/v1/endpoints/telemetry.py
import asyncio
import json
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.manager import manager
from app.services.simulator import simulator

router = APIRouter()

@router.websocket("/ws/telemetry")
async def telemetry_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            storm_level = random.choice([2, 3, 4, 5])
            payload = simulator.compute_frame(storm_intensity=storm_level)
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)