# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from typing import List
import os
from pydantic import BaseModel # <-- REQUIRED FOR SYMPTOM PAYLOAD
from fastapi.responses import FileResponse # <-- REQUIRED FOR AUDIO RESPONSE
from db import db
from models import PatientCreate, PatientDB
from misinformation import check_misinformation, get_medical_guidance # <-- NEW: Imports the guidance function
from speech_service import text_to_speech # <-- NEW: Imports the speech function
# --- CORE APP INITIALIZATION ---
app = FastAPI(title="Rural Healthcare API")
# Allow local frontend to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production restrict origins!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- NEW: Symptom Checker Schema ---
class SymptomCheckPayload(BaseModel):
    """Schema for the data sent from the frontend"""
    symptoms: str # The user's input symptom string
# --- HELPER FUNCTION (Your existing code) ---
class SymptomRequest(BaseModel):
    symptoms: str
def _doc_to_patient(doc) -> PatientDB:
    return PatientDB(
        id=str(doc["_id"]),
        name=doc.get("name"),
        age=doc.get("age"),
        phone=doc.get("phone"),
        symptoms=doc.get("symptoms")
    )
# --- NEW: AI SYMPTOM CHECKER ENDPOINT (Provides detailed medical guidance) ---
@app.post("/check-symptoms")
async def check_symptoms_and_misinformation(payload: SymptomCheckPayload):
    """
    Receives user symptoms, checks for misinformation, and returns detailed medical guidance.
    """
    symptoms_text = payload.symptoms
    # 1. Check for misinformation first
    misinfo_result = check_misinformation(symptoms_text)
    if misinfo_result["corrected_info"] != "No misinformation detected.":
        # Misinformation found, return the correction and stop there
        guidance = (
            f"**Misinformation Alert:** The statement '{symptoms_text}' matches a known myth. "
            f"**Correction:** {misinfo_result['corrected_info']}"
        )
    else:
        # 2. If no misinformation, look for medical guidance
        medical_guidance = get_medical_guidance(symptoms_text) # <-- This is the function call!
        if medical_guidance:
            # Found a specific match (e.g., fever, cough)
            guidance = (
                f"**Condition Found:** {medical_guidance['condition']}<br><br>"
                f"**Health Information:** {medical_guidance['information']}<br><br>"
                f"**Recommended Basic Treatment:** {medical_guidance['treatment']}<br><br>"
                f"**REMINDER:** This is AI guidance. Consult a local medical professional for a proper diagnosis."
            )
        else:
            # 3. Fallback to general advice (This is the output you were seeing)
            guidance = (
                f"**General Guidance:** The AI could not identify a common condition based on your symptoms: '{symptoms_text}'. "
                f"Please provide more detail or, for your safety, **immediately consult a local health worker or doctor.**"
            )
    return {
        "status": "success",
        "input": symptoms_text,
        "guidance": guidance
    }
# ------------------------------------------------------------------
# --- NEW: TEXT-TO-SPEECH ENDPOINT (For the Listen button) ---
# ------------------------------------------------------------------
@app.post("/speak-guidance")
async def generate_speech_audio(payload: SymptomCheckPayload):
    """
    Takes text input and uses speech_service to convert it to an MP3 file.
    """
    text_to_convert = payload.symptoms 
    # 1. Generate the audio file (saves to 'output.mp3')
    text_to_speech(text_to_convert, lang="en") 
    audio_file_path = "output.mp3"
    # 2. Return the generated audio file
    if os.path.exists(audio_file_path):
        return FileResponse(
            path=audio_file_path,
            media_type='audio/mpeg',
            filename='guidance_audio.mp3'
        )
    
    raise HTTPException(status_code=500, detail="Audio generation failed.")


# ------------------------------------------------------------------
# --- EXISTING: Patient CRUD Endpoints (Your original code) ---
# ------------------------------------------------------------------

@app.get("/patients", response_model=List[PatientDB])
async def list_patients():
    cursor = db.patients.find().sort("_id", -1)
    docs = []
    async for doc in cursor:
        docs.append(_doc_to_patient(doc))
    return docs

@app.post("/patients", response_model=PatientDB)
async def create_patient(payload: PatientCreate):
    doc = payload.dict()
    res = await db.patients.insert_one(doc)
    new_doc = await db.patients.find_one({"_id": res.inserted_id})
    return _doc_to_patient(new_doc)

@app.get("/patients/{patient_id}", response_model=PatientDB)
async def get_patient(patient_id: str):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await db.patients.find_one({"_id": ObjectId(patient_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return _doc_to_patient(doc)

@app.put("/patients/{patient_id}", response_model=PatientDB)
async def update_patient(patient_id: str, payload: PatientCreate):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    update = {"$set": payload.dict()}
    res = await db.patients.update_one({"_id": ObjectId(patient_id)}, update)
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    doc = await db.patients.find_one({"_id": ObjectId(patient_id)})
    return _doc_to_patient(doc)

@app.delete("/patients/{patient_id}")
async def delete_patient(patient_id: str):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await db.patients.delete_one({"_id": ObjectId(patient_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "deleted"}
@app.post("/predict")
async def predict(data: SymptomRequest):

    symptoms = data.symptoms.lower()

    # Your ML logic later
    if "fever" in symptoms:
        result = "You may have viral fever"

    elif "headache" in symptoms:
        result = "Possible migraine symptoms detected"

    elif "cough" in symptoms:
        result = "Possible cold or flu detected"

    else:
        result = "Please consult a doctor for proper diagnosis"

    return {
        "result": result
    }