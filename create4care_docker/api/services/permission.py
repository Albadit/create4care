from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Permission
from schemas.permission import PermissionRequest, PermissionUpdate
from schemas.common import Message

def get_all_permissions(db: Session) -> List[Permission]:
    return db.query(Permission).all()

def get_permission(db: Session, permission_id: int) -> Permission:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

def create_permission(db: Session, permission_in: PermissionRequest) -> Permission:
    existing = db.query(Permission).filter(Permission.name == permission_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    permission = Permission(name=permission_in.name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def update_permission(db: Session, permission_id: int, permission_in: PermissionUpdate) -> Permission:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    update_data = permission_in.dict(exclude_unset=True)
    
    # Check for duplicate permission names
    if "name" in update_data and update_data["name"] != permission.name:
        existing = db.query(Permission).filter(Permission.name == update_data["name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Permission name already exists")
    
    for key, value in update_data.items():
        setattr(permission, key, value)
    
    db.commit()
    db.refresh(permission)
    return permission

def delete_permission(db: Session, permission_id: int) -> Message:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    db.delete(permission)
    db.commit()
    return Message(detail="Permission deleted successfully")
