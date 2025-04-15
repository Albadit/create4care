from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogResponse(BaseModel):
    id: int
    table_name: str
    record_id: int
    operation: str
    changed_data: Optional[str]
    changed_at: datetime

class LogRequest(BaseModel):
    table_name: str
    record_id: int
    operation: str
    changed_data: Optional[str]

class LogUpdate(BaseModel):
    table_name: Optional[str]
    record_id: Optional[int]
    operation: Optional[str]
    changed_data: Optional[str]

