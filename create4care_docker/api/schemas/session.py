from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionResponse(BaseModel):
    user_id: int
    session_token: str
    expires: datetime

class SessionRequest(BaseModel):
    user_id: int
    session_token: str
    expires: datetime

class SessionUpdate(BaseModel):
    user_id: Optional[int]
    session_token: Optional[str]
    expires: Optional[datetime]