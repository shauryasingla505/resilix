# app/api/v1/endpoints/triage.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import TriageResponse

router = APIRouter()

@router.post("/triage-audio", response_model=TriageResponse)
async def triage_audio(file: UploadFile = File(...)):
    if not file.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(status_code=400, detail="Invalid audio format.")
    
    # Stub for Whisper + SpaCy integration (Person A/C collaboration)
    return {
        "transcript": "Water is entering our building near Central Bridge, send medical help!",
        "category": "MEDICAL",
        "extracted_location": "Central Bridge",
        "severity_score": 94,
        "coordinates": [12.9180, 79.1310]
    }