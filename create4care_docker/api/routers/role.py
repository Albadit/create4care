from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.role import RoleRequest, RoleResponse, RoleUpdate
from schemas.common import Message
from db.session import get_db
from services import role as role_service

router = APIRouter()

@router.get("/", response_model=List[RoleResponse])
def list_roles(db: DBSession = Depends(get_db)):
    return role_service.get_all_roles(db)

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleRequest, db: DBSession = Depends(get_db)):
    return role_service.create_role(db, role)

@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: DBSession = Depends(get_db)):
    role_obj = role_service.get_role(db, role_id)
    if not role_obj:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_obj

@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleUpdate, db: DBSession = Depends(get_db)):
    return role_service.update_role(db, role_id, role)

@router.delete("/{role_id}", response_model=Message)
def delete_role(role_id: int, db: DBSession = Depends(get_db)):
    return role_service.delete_role(db, role_id)
