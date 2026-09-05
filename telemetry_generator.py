import random
from datetime import datetime, timezone
from typing import Dict, Any, List
from config import DRAINAGE_NODES_BASE, TRANSFORMERS_BASE

class TelemetryGenerator:
    def __init__(self):
        self.nodes = [dict(n) for n in DRAINAGE_NODES_BASE]
        self.transformers = [dict(t) for t in TRANSFORMERS_BASE]

    def compute_frame(self, storm_intensity: int, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        precip_mm = weather_data.get("precipitation_mm", 0.0) + (storm_intensity * 25.0)
        ambient_temp = weather_data.get("temperature_c", 30.0)

        output_nodes: List[Dict[str, Any]] = []
        for node in self.nodes:
            surge = (precip_mm * 0.04) + random.uniform(-0.05, 0.1)
            water_level = round(max(0.1, node["base_level"] + surge), 2)
            fill_pct = (water_level / node["capacity_m"]) * 100
            risk_score = int(min(100, max(5, fill_pct + random.randint(-4, 4))))

            if risk_score >= 85:
                status = "CRITICAL"
            elif risk_score >= 60:
                status = "WARNING"
            else:
                status = "CLEAR"

            output_nodes.append({
                "id": node["id"],
                "lat": node["lat"],
                "lng": node["lng"],
                "water_level_m": water_level,
                "risk_score": risk_score,
                "status": status
            })

        output_transformers: List[Dict[str, Any]] = []
        for grid in self.transformers:
            load_factor = 0.5 + (storm_intensity * 0.12) + random.uniform(-0.03, 0.05)
            load_kw = int(min(grid["max_load_kw"] * 1.3, grid["max_load_kw"] * load_factor))
            temp_c = round(grid["nominal_temp_c"] + (load_kw / grid["max_load_kw"] * 20.0) + (ambient_temp * 0.1), 1)

            if load_kw >= grid["max_load_kw"] * 0.95 or temp_c > 65.0:
                status = "OVERLOAD"
            elif load_kw >= grid["max_load_kw"] * 0.80:
                status = "WARNING"
            else:
                status = "NOMINAL"

            output_transformers.append({
                "id": grid["id"],
                "lat": grid["lat"],
                "lng": grid["lng"],
                "load_kw": load_kw,
                "temp_c": temp_c,
                "status": status
            })

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "storm_intensity": storm_intensity,
            "nodes": output_nodes,
            "transformers": output_transformers
        }