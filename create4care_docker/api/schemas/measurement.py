from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MeasurementResponse(BaseModel):
    id: int
    patient_id: int
    measured_by_user_id: int
    height_mm: float
    weight_kg: float
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image: str
    date: datetime

class MeasurementRequest(BaseModel):
    patient_id: int
    measured_by_user_id: int
    height_mm: float
    weight_kg: float
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image_base64: str

class MeasurementUpdate(BaseModel):
    patient_id: Optional[int]
    measured_by_user_id: Optional[int]
    height_mm: Optional[float]
    weight_kg: Optional[float]
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image: Optional[str]