from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientResponse(BaseModel):
    id: int
    name: str
    birth_date: date
    gender: int
    father_height_mm: float
    mother_height_mm: float

class PatientRequest(BaseModel):
    name: str
    birth_date: date
    gender: int
    father_height_mm: float
    mother_height_mm: float

class PatientUpdate(BaseModel):
    name: Optional[str]
    birth_date: Optional[date]
    gender: Optional[int]
    father_height_mm: Optional[float]
    mother_height_mm: Optional[float]