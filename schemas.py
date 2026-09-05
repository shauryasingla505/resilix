# app/models/schemas.py
from pydantic import BaseModel
from typing import List

class RerouteRequest(BaseModel):
    start: List[float]
    destination: List[float]
    blocked_nodes: List[str] = []

class RerouteResponse(BaseModel):
    path_coordinates: List[List[float]]
    eta_minutes: float
    hazards_avoided: int

class TriageResponse(BaseModel):
    transcript: str
    category: str
    extracted_location: str
    severity_score: int
    coordinates: List[float]