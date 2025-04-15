from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Role
from schemas.role import RoleRequest, RoleUpdate
from schemas.common import Message

def get_all_roles(db: Session) -> List[Role]:
    return db.query(Role).all()

def get_role(db: Session, role_id: int) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

def create_role(db: Session, role_in: RoleRequest) -> Role:
    existing = db.query(Role).filter(Role.name == role_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = Role(name=role_in.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_id: int, role_in: RoleUpdate) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role_in.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] != role.name:
        existing = db.query(Role).filter(Role.name == update_data["name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Role name already exists")
    
    for key, value in update_data.items():
        setattr(role, key, value)
    
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int) -> Message:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Optionally check for associations (e.g., role.users) before deletion.
    if role.users:
        raise HTTPException(status_code=400, detail="Role is assigned to users and cannot be deleted")
    
    db.delete(role)
    db.commit()
    return Message(detail="Role deleted successfully")
