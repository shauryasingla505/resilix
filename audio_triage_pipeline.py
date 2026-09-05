import os
import json
import numpy as np
import librosa
import torch
import whisper
import spacy

# Load SpaCy small English model for Named Entity Recognition
print("[*] Loading SpaCy NER Engine...")
nlp = spacy.load("en_core_web_sm")

# Lazy-load Whisper base model
print("[*] Loading Whisper ASR Model...")
whisper_model = whisper.load_model("base")

def categorize_hazard(text: str) -> str:
    """
    Categorizes the hazard type based on emergency keywords.
    """
    text_lower = text.lower()
    if any(word in text_lower for word in ['water', 'flood', 'submerged', 'drain', 'overflow', 'lake', 'river']):
        return "FLOOD"
    elif any(word in text_lower for word in ['power', 'electricity', 'transformer', 'spark', 'blackout', 'grid', 'wire']):
        return "GRID_FAILURE"
    elif any(word in text_lower for word in ['fire', 'smoke', 'explosion', 'burn']):
        return "FIRE"
    elif any(word in text_lower for word in ['medical', 'hospital', 'injured', 'trapped', 'ambulance', 'hurt', 'bleeding']):
        return "MEDICAL"
    else:
        return "GENERAL_EMERGENCY"

def calculate_severity(text: str) -> int:
    """
    Assigns an urgency/severity score (0-100) based on critical keywords.
    """
    text_lower = text.lower()
    critical_keywords = ['trapped', 'dying', 'bleeding', 'explosion', 'immediate', 'drowning', 'collapsed', 'urgent']
    warning_keywords = ['rising', 'blocked', 'smoke', 'stuck', 'help', 'danger', 'outage']
    
    score = 50  # Baseline score
    for word in critical_keywords:
        if word in text_lower:
            score += 15
    for word in warning_keywords:
        if word in text_lower:
            score += 8
            
    return min(score, 100)

def process_audio_triage(audio_file_path: str) -> dict:
    """
    Processes an emergency voice recording and extracts structured metadata.
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file '{audio_file_path}' not found.")

    print(f"[*] Loading and resampling audio: {audio_file_path}...")
    
    # Load audio explicitly at 16kHz mono as float32
    audio_data, sr = librosa.load(audio_file_path, sr=16000, mono=True)
    audio_data = audio_data.astype(np.float32)

    # Check if the audio file contains actual sound energy
    max_amplitude = np.max(np.abs(audio_data))
    print(f"[*] Audio Peak Amplitude: {max_amplitude:.4f}")
    if max_amplitude < 0.001:
        print("[!] Warning: Audio file appears to be silent or extremely quiet!")

    print(f"[*] Transcribing audio via Whisper...")
    # Anti-hallucination configuration
    result = whisper_model.transcribe(
        audio_data, 
        fp16=False,
        language="en",
        condition_on_previous_text=False,  # Prevents repetitive loop hallucinations
        no_speech_threshold=0.6,           # Filters out silent/ambient background noise
        compression_ratio_threshold=2.4     # Catches repetitive text output
    )
    transcript = result['text'].strip()
    
    # Extract Named Entities via SpaCy
    doc = nlp(transcript)
    locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'FAC']]
    extracted_location = locations[0] if locations else "Unknown Location"
    
    # Categorize and Score Urgency
    category = categorize_hazard(transcript)
    severity_score = calculate_severity(transcript)
    
    # Construct Payload
    triage_payload = {
        "transcript": transcript,
        "category": category,
        "extracted_location": extracted_location,
        "severity_score": severity_score,
        "status": "TRIAGED"
    }
    
    return triage_payload

if __name__ == "__main__":
    test_audio = "sample_emergency.wav"
    
    if os.path.exists(test_audio):
        output = process_audio_triage(test_audio)
        print("\n--- TRIAGE OUTPUT JSON ---")
        print(json.dumps(output, indent=2))
    else:
        print(f"\n[!] Place a test file named '{test_audio}' in this folder to run a live test.")
        print("[+] Audio Triage Script compiled and ready for FastAPI integration!")