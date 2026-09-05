import json
import asyncio
from telemetry_generator import TelemetryGenerator
from open_meteo_client import OpenMeteoClient
from rich.console import Console

console = Console()

SCENARIOS = {
    "1": ("Normal Ops (Baseline)", 0),
    "2": ("Moderate Monsoonal Rain", 2),
    "3": ("Flash Flood Event (Demo Trigger: Node 101 Failure)", 4),
    "4": ("Total Blackout & Structural Overload", 5)
}

async def run_scenario_preview(choice: str):
    name, intensity = SCENARIOS.get(choice, SCENARIOS["1"])
    console.print(f"\n[bold green]=== RUNNING: {name} (Storm Level {intensity}) ===[/bold green]")
    
    meteo = OpenMeteoClient()
    generator = TelemetryGenerator()
    
    weather = await meteo.get_live_weather()
    frame = generator.compute_frame(intensity, weather)
    console.print_json(json.dumps(frame, indent=2))

if __name__ == "__main__":
    console.print("[bold yellow]Select a Scenario to Test:[/bold yellow]")
    for k, v in SCENARIOS.items():
        console.print(f"[{k}] {v[0]}")
    
    selected = input("\nType 1, 2, 3, or 4 and hit Enter: ").strip() or "1"
    asyncio.run(run_scenario_preview(selected))