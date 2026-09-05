# app/api/v1/endpoints/routing.py
from fastapi import APIRouter, HTTPException
from app.models.schemas import RerouteRequest, RerouteResponse
from app.services.router_engine import pathfinder

router = APIRouter()

@router.post("/reroute", response_model=RerouteResponse)
async def dynamic_reroute(req: RerouteRequest):
    try:
        path, eta, hazards = pathfinder.compute_route(
            start=req.start,
            destination=req.destination,
            blocked_nodes=req.blocked_nodes
        )
        return {
            "path_coordinates": path,
            "eta_minutes": eta,
            "hazards_avoided": hazards
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))