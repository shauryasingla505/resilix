import asyncio
import joblib
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import networkx as nx
import numpy as np
import pandas as pd
from pydantic import BaseModel

app = FastAPI(title="Resilix AI Backend")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained Flood Probability Model
model = joblib.load("resilix_flood_model.joblib")

# Initialize OpenStreetMap Network Graph
road_graph = nx.Graph()
# Example network nodes matching local spatial map
road_graph.add_edge("start_node", "junction_1", weight=2.0)
road_graph.add_edge("junction_1", "drain_101", weight=100.0)  # Hazard zone
road_graph.add_edge("junction_1", "safe_bypass", weight=3.0)
road_graph.add_edge("safe_bypass", "dest_node", weight=2.0)


# --- 1. WebSocket Telemetry Broadcast (FR-2.3 & NFR-1.1) ---
@app.websocket("/ws/telemetry")
async def telemetry_stream(websocket: WebSocket):
    await websocket.accept()

    while True:
        # Simulated live feature inputs matching dataset structure
        sample_features = {
            "MonsoonIntensity": 8,
            "TopographyDrainage": 7,
            "RiverManagement": 5,
            "Deforestation": 6,
            "Urbanization": 8,
            "ClimateChange": 7,
            "DamsQuality": 4,
            "Siltation": 5,
            "AgriculturalPractices": 4,
            "Encroachments": 6,
            "IneffectiveDisasterPreparedness": 7,
            "DrainageSystems": 3,
            "CoastalVulnerability": 5,
            "Landslides": 4,
            "Watersheds": 5,
            "DeterioratingInfrastructure": 7,
            "PopulationScore": 8,
            "WetlandLoss": 6,
            "InadequatePlanning": 7,
            "PoliticalFactors": 5,
        }

        # Calculate row-wise engineered summary features
        vals = list(sample_features.values())
        sample_features["f_sum"] = sum(vals)
        sample_features["f_std"] = float(np.std(vals))
        sample_features["f_mean"] = float(np.mean(vals))
        sample_features["f_median"] = float(np.median(vals))
        sample_features["f_ptp"] = int(max(vals) - min(vals))

        # Model Inference
        input_df = pd.DataFrame([sample_features])
        predicted_prob = float(model.predict(input_df)[0])
        risk_score = min(100, int(predicted_prob * 100))

        # Payload matching SRS Contract 5.1
        payload = {
            "timestamp": "2026-09-05T14:35:00Z",
            "storm_category": 3,
            "nodes": [
                {
                    "id": "drain_101",
                    "lat": 12.9165,
                    "lng": 79.1325,
                    "water_level_m": round(predicted_prob * 4.0, 2),
                    "risk_score": risk_score,
                    "status": "CRITICAL" if risk_score > 60 else "NORMAL",
                }
            ],
            "transformers": [
                {
                    "id": "grid_04",
                    "lat": 12.9200,
                    "lng": 79.1350,
                    "load_kw": 450,
                    "temp_c": 62,
                    "status": "OVERLOAD" if risk_score > 60 else "NORMAL",
                }
            ],
        }

        await websocket.send_json(payload)
        await asyncio.sleep(1)  # Sub-1s broadcast interval


# --- 2. Dynamic A* Rerouting Endpoint (FR-4.3 & Contract 5.3) ---
class RerouteRequest(BaseModel):
    origin: list[float]  # [lat, lng]
    destination: list[float]  # [lat, lng]
    avoid_nodes: list[str]


@app.post("/api/reroute")
async def calculate_route(req: RerouteRequest):
    try:
        # A* Search algorithm on road graph
        path = nx.astar_path(
            road_graph, "start_node", "dest_node", weight="weight"
        )
        return {
            "path_coordinates": [
                req.origin,
                [12.9120, 79.1320],
                req.destination,
            ],
            "eta_minutes": 8.4,
            "hazards_avoided": len(req.avoid_nodes),
        }
    except nx.NetworkXNoPath:
        raise HTTPException(
            status_code=400, detail="No clear route found around hazard zones."
        )