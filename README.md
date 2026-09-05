# Resilix AI - Backend Engine

The high-performance Python FastAPI backend for **Resilix AI**, a multi-hazard urban disaster intelligence platform. This service powers real-time telemetry streaming via WebSockets, NetworkX-driven dynamic A* emergency rerouting, and audio triage endpoints.

---

## Tech Stack

* **Framework:** FastAPI (Python)
* **Real-Time Communication:** WebSockets
* **Spatial Analysis & Pathfinding:** NetworkX, OpenStreetMap (OSMnx)
* **Data Validation:** Pydantic v2
* **Concurrency:** Asyncio

---

## Project Directory Structure

```text
resilix-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entrypoint, app factory, CORS setup
│   ├── config.py                # Environment variables & configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── telemetry.py # WebSocket router & background broadcaster
│   │   │   │   ├── triage.py    # Audio triage endpoint integration stub
│   │   │   │   └── routing.py   # NetworkX A* dynamic rerouting endpoint
│   │   │   └── router.py        # Central API router aggregator
│   │   └── deps.py              # Dependency injection utilities
│   ├── core/
│   │   ├── __init__.py
│   │   └── manager.py           # WebSocket connection manager implementation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── simulator.py         # Telemetry simulation script & data generator
│   │   └── router_engine.py     # Graph loading & A* pathfinding logic
│   └── models/
│       ├── __init__.py
│       └── schemas.py           # Pydantic data validation models
├── tests/
│   ├── __init__.py
│   ├── test_routing.py          # Unit tests for NetworkX path calculation
│   └── test_websockets.py       # Connection and telemetry feed tests
├── .env                         # Environment variables
├── .gitignore
├── requirements.txt             # Python dependencies
└── README.md