from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.user import UserRequest, UserResponse, UserUpdate
from schemas.common import Message
from db.session import get_db
from services import user as user_service
from routers.auth import get_current_user 
from db.models import User

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def list_users(db: DBSession = Depends(get_db)):
    return user_service.get_all_users(db)

@router.post("/", response_model=UserResponse)
def create_user(user: UserRequest, db: DBSession = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/{uid}", response_model=UserResponse)
def get_user(uid: int, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_obj = user_service.get_user(db, uid)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj

@router.patch("/{uid}", response_model=UserResponse)
def update_user(uid: int, user: UserUpdate, db: DBSession = Depends(get_db)):
    # Partially update the user data.
    return user_service.update_user(db, uid, user)

@router.delete("/{uid}", response_model=Message)
def delete_user(uid: int, db: DBSession = Depends(get_db)):
    return user_service.delete_user(db, uid)