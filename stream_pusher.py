import asyncio
import json
import logging
import websockets
from open_meteo_client import OpenMeteoClient
from telemetry_generator import TelemetryGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SIMULATOR] - %(message)s")
logger = logging.getLogger("TelemetryPusher")

# Person C's ingestion WebSocket endpoint
BACKEND_WS_URL = "ws://localhost:8000/ws/telemetry/ingest"

async def stream_telemetry(interval_sec: float = 1.0, storm_intensity: int = 2):
    meteo = OpenMeteoClient()
    generator = TelemetryGenerator()
    
    logger.info(f"Targeting FastAPI ingestion endpoint: {BACKEND_WS_URL}")
    while True:
        try:
            async with websockets.connect(BACKEND_WS_URL) as ws:
                logger.info("Connected to Person C's backend.")
                while True:
                    weather = await meteo.get_live_weather()
                    payload = generator.compute_frame(storm_intensity, weather)
                    await ws.send(json.dumps(payload))
                    logger.info(f"Pushed frame | Nodes: {len(payload['nodes'])} | Transformers: {len(payload['transformers'])}")
                    await asyncio.sleep(interval_sec)
        except (websockets.ConnectionClosed, ConnectionRefusedError):
            logger.warning("Person C's server (localhost:8000) not running yet. Retrying in 3 seconds...")
            await asyncio.sleep(3.0)
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            await asyncio.sleep(3.0)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Resilix AI Real-Time Telemetry Streamer")
    parser.add_argument("--storm", type=int, default=2, help="Storm level 0-5 (default: 2)")
    parser.add_argument("--interval", type=float, default=1.0, help="Push rate in seconds (default: 1.0)")
    args = parser.parse_args()

    asyncio.run(stream_telemetry(interval_sec=args.interval, storm_intensity=args.storm))