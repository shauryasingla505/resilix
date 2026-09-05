# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["*"]  # Changed to uppercase to match main.py

    model_config = {
        "extra": "ignore",
        "env_file": ".env"
    }

settings = Settings()
DRAINAGE_NODES_BASE = [
    {"id": "node_101", "lat": 12.9165, "lng": 79.1325, "base_level": 1.2, "capacity_m": 4.0},
    {"id": "node_102", "lat": 12.9180, "lng": 79.1340, "base_level": 1.5, "capacity_m": 4.5}
]

TRANSFORMERS_BASE = [
    {"id": "grid_04", "lat": 12.9200, "lng": 79.1350, "max_load_kw": 500, "nominal_temp_c": 45.0},
    {"id": "grid_05", "lat": 12.9220, "lng": 79.1370, "max_load_kw": 600, "nominal_temp_c": 42.0}
]