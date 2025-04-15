from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from db.models import Measurement, Patient, User
from schemas.measurement import MeasurementRequest, MeasurementUpdate
from schemas.common import Message
from utils.image_utils import save_image

def get_all_measurements(db: Session) -> List[Measurement]:
    return db.query(Measurement).all()

def get_measurement(db: Session, measurement_id: int) -> Measurement:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

def create_measurement(db: Session, meas_in: MeasurementRequest, request: Request) -> Measurement:
    patient = db.query(Patient).filter(Patient.id == meas_in.patient_id).first()

    if not patient:
        raise HTTPException(status_code=400, detail="Patient does not exist")

    user = db.query(User).filter(User.id == meas_in.measured_by_user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Measured_by user does not exist")

    image_url = None
    if meas_in.image_base64:
        image_url = save_image(meas_in.image_base64, meas_in.patient_id, request)
    
    measurement = Measurement(
        patient_id=meas_in.patient_id,
        measured_by_user_id=meas_in.measured_by_user_id,
        height_mm=meas_in.height_mm,
        weight_kg=meas_in.weight_kg,
        sleep_hours=meas_in.sleep_hours,
        exercise_hours=meas_in.exercise_hours,
        image=image_url
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement

def update_measurement(db: Session, measurement_id: int, meas_in: MeasurementUpdate, request: Request) -> Measurement:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    patient = db.query(Patient).filter(Patient.id == meas_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient does not exist")

    user = db.query(User).filter(User.id == meas_in.measured_by_user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Measured_by user does not exist")

    update_data = meas_in.dict(exclude_unset=True)

    if "image_base64" in update_data:
        measurement.image = save_image(update_data.pop("image_base64"), measurement.patient_id, request)
    
    for key, value in update_data.items():
        setattr(measurement, key, value)
    
    db.commit()
    db.refresh(measurement)
    return measurement

def delete_measurement(db: Session, measurement_id: int) -> Message:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    db.delete(measurement)
    db.commit()
    return Message(detail="Measurement deleted successfully")
