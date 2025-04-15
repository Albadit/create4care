from pydantic import BaseModel
from typing import Optional

class PermissionResponse(BaseModel):
    id: int
    name: str

class PermissionRequest(BaseModel):
    name: str

class PermissionUpdate(BaseModel):
    name: Optional[str]
