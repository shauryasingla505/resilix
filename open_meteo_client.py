import httpx
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenMeteoClient")

class OpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, lat: float = 12.9165, lng: float = 79.1325):
        self.lat = lat
        self.lng = lng

    async def get_live_weather(self) -> Dict[str, Any]:
        """Fetch precipitation, surface temperature, and wind gusts."""
        params = {
            "latitude": self.lat,
            "longitude": self.lng,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_gusts_10m"],
            "timezone": "auto"
        }
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(self.BASE_URL, params=params)
                res.raise_for_status()
                data = res.json().get("current", {})
                return {
                    "temperature_c": data.get("temperature_2m", 31.0),
                    "precipitation_mm": data.get("precipitation", 0.0),
                    "humidity": data.get("relative_humidity_2m", 65),
                    "wind_gusts_kmh": data.get("wind_gusts_10m", 12.0),
                    "is_live": True
                }
        except Exception as e:
            logger.warning(f"Live fetch failed: {e}. Using fallback values.")
            return {
                "temperature_c": 31.5,
                "precipitation_mm": 2.4,
                "humidity": 70,
                "wind_gusts_kmh": 14.5,
                "is_live": False
            }