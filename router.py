# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import telemetry, triage, routing

api_router = APIRouter()

api_router.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry"])
api_router.include_router(triage.router, prefix="/triage", tags=["Audio Triage"])
api_router.include_router(routing.router, prefix="/routing", tags=["Dynamic Routing"])