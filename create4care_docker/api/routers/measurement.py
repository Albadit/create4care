from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from schemas.measurement import MeasurementRequest, MeasurementResponse, MeasurementUpdate
from schemas.common import Message
from db.session import get_db
from services import measurement as measurement_service

router = APIRouter()

@router.get("/", response_model=List[MeasurementResponse])
def list_measurements(db: DBSession = Depends(get_db)):
    return measurement_service.get_all_measurements(db)

@router.post("/", response_model=MeasurementResponse)
def create_measurement(measurement: MeasurementRequest, request: Request, db: DBSession = Depends(get_db)):
    return measurement_service.create_measurement(db, measurement, request)

@router.get("/{measurement_id}", response_model=MeasurementResponse)
def get_measurement(measurement_id: int, db: DBSession = Depends(get_db)):
    meas_obj = measurement_service.get_measurement(db, measurement_id)
    if not meas_obj:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return meas_obj

@router.patch("/{measurement_id}", response_model=MeasurementResponse)
def update_measurement(measurement_id: int, measurement: MeasurementUpdate, request: Request, db: DBSession = Depends(get_db)):
    return measurement_service.update_measurement(db, measurement_id, measurement, request)

@router.delete("/{measurement_id}", response_model=Message)
def delete_measurement(measurement_id: int, db: DBSession = Depends(get_db)):
    return measurement_service.delete_measurement(db, measurement_id)