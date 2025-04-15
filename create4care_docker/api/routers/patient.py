from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.patient import PatientRequest, PatientResponse, PatientUpdate
from schemas.common import Message
from db.session import get_db
from services import patient as patient_service

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
def list_patients(db: DBSession = Depends(get_db)):
    return patient_service.get_all_patients(db)

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientRequest, db: DBSession = Depends(get_db)):
    return patient_service.create_patient(db, patient)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: DBSession = Depends(get_db)):
    patient_obj = patient_service.get_patient(db, patient_id)
    if not patient_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_obj

@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientUpdate, db: DBSession = Depends(get_db)):
    return patient_service.update_patient(db, patient_id, patient)

@router.delete("/{patient_id}", response_model=Message)
def delete_patient(patient_id: int, db: DBSession = Depends(get_db)):
    return patient_service.delete_patient(db, patient_id)