from pydantic import BaseModel
from typing import Optional

class RoleResponse(BaseModel):
    id: int
    name: str

class RoleRequest(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: Optional[str]