from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.password_hash import hash_password
from db.models import User
from schemas.user import UserRequest, UserUpdate
from schemas.common import Message

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user(db: Session, uid: int) -> User:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(db: Session, user_in: UserRequest) -> User:
    # Check if the email already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, uid: int, user_in: UserUpdate) -> User:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_in.dict(exclude_unset=True)
    
    # If email is provided and it differs, check for duplicates.
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # If password is provided, hash it.
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, uid: int) -> Message:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Optionally, check for associations here before deleting.
    if user.measurements_taken:
        raise HTTPException(
            status_code=400,
            detail="User is assigned to measurements and cannot be deleted"
        )
    
    if user.patients:
        raise HTTPException(
            status_code=400,
            detail="User is assigned to one or more patients and cannot be deleted"
        )

    db.delete(user)
    db.commit()
    return Message(detail="User deleted successfully")
