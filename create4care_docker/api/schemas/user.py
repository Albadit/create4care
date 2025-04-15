from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    email_verified: Optional[datetime]
    image: Optional[str]  # Optional field for the image (if it's present)

class UserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str  # In production, remember to hash the password!
    email_verified: Optional[datetime]
    image: Optional[str]

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]  # Again, hash passwords in production
    email_verified: Optional[datetime]
    image: Optional[str]  # Optional field for the image