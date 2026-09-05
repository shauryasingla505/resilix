import asyncio
import json
import logging
import websockets
from open_meteo_client import OpenMeteoClient
from telemetry_generator import TelemetryGenerator

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("PitchDemo")

BACKEND_WS_URL = "ws://localhost:8000/ws/telemetry/ingest"

# The 3-minute pitch progression sequence
SCRIPTED_STAGES = [
    {"name": "Stage 1: Normal City Baseline", "storm": 0, "duration": 8},
    {"name": "Stage 2: Heavy Inflow Warning", "storm": 2, "duration": 10},
    {"name": "Stage 3: Subterranean Saturation (Node 101 Failure)", "storm": 4, "duration": 12},
    {"name": "Stage 4: Severe Cascading Blackout & Critical Flooding", "storm": 5, "duration": 15},
]

async def run_pitch_sequence():
    meteo = OpenMeteoClient()
    generator = TelemetryGenerator()
    
    print("\n--- RESILIX AI LIVE PITCH DEMO CONTROLLER ---\n")
    try:
        async with websockets.connect(BACKEND_WS_URL) as ws:
            logger.info("Connected to Backend. Starting dynamic pitch progression...")
            for stage in SCRIPTED_STAGES:
                print(f"\n>>> NOW RUNNING: {stage['name']} (Storm Level {stage['storm']})")
                for _ in range(stage['duration']):
                    weather = await meteo.get_live_weather()
                    payload = generator.compute_frame(stage['storm'], weather)
                    await ws.send(json.dumps(payload))
                    await asyncio.sleep(1.0)
            print("\n>>> Pitch Demo Simulation Completed Successfully.")
    except (websockets.ConnectionClosed, ConnectionRefusedError):
        print("\n[!] Person C's backend is not running at localhost:8000.")
        print("[!] Start Person C's server first before launching this pitch runner.")

if __name__ == "__main__":
    asyncio.run(run_pitch_sequence())