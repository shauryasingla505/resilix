from typing import List, Dict, Any

TARGET_CITY = "Vellore, Tamil Nadu"
DEFAULT_LAT = 12.9165
DEFAULT_LNG = 79.1325

# Base drainage nodes across the urban watershed
DRAINAGE_NODES_BASE: List[Dict[str, Any]] = [
    {"id": "node_101", "lat": 12.9165, "lng": 79.1325, "capacity_m": 3.0, "base_level": 0.4},
    {"id": "node_102", "lat": 12.9210, "lng": 79.1380, "capacity_m": 2.5, "base_level": 0.3},
    {"id": "node_103", "lat": 12.9120, "lng": 79.1290, "capacity_m": 4.0, "base_level": 0.6},
    {"id": "node_104", "lat": 12.9280, "lng": 79.1410, "capacity_m": 2.0, "base_level": 0.2},
    {"id": "node_105", "lat": 12.9090, "lng": 79.1350, "capacity_m": 3.5, "base_level": 0.5},
]

# Base electrical grid transformers
TRANSFORMERS_BASE: List[Dict[str, Any]] = [
    {"id": "grid_01", "lat": 12.9200, "lng": 79.1350, "max_load_kw": 500, "nominal_temp_c": 45.0},
    {"id": "grid_02", "lat": 12.9140, "lng": 79.1310, "max_load_kw": 400, "nominal_temp_c": 42.0},
    {"id": "grid_03", "lat": 12.9250, "lng": 79.1420, "max_load_kw": 600, "nominal_temp_c": 46.0},
    {"id": "grid_04", "lat": 12.9180, "lng": 79.1270, "max_load_kw": 450, "nominal_temp_c": 44.0},
]