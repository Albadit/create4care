from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Patient
from schemas.patient import PatientRequest, PatientUpdate
from schemas.common import Message

def get_all_patients(db: Session) -> List[Patient]:
    return db.query(Patient).all()

def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def create_patient(db: Session, patient_in: PatientRequest) -> Patient:
    patient = Patient(
        name=patient_in.name,
        birth_date=patient_in.birth_date,
        gender=patient_in.gender,
        father_height_mm=patient_in.father_height_mm,
        mother_height_mm=patient_in.mother_height_mm,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def update_patient(db: Session, patient_id: int, patient_in: PatientUpdate) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_in.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int) -> Message:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Optionally check associations (e.g., patient.measurements, patient.users)
    if patient.users:
        raise HTTPException(
            status_code=400, 
            detail="Patient is assigned to one or more users and cannot be deleted"
        )

    if patient.measurements:
        raise HTTPException(
            status_code=400, 
            detail="Patient is assigned to measurements and cannot be deleted"
        )
    
    db.delete(patient)
    db.commit()
    return Message(detail="Patient deleted successfully")
