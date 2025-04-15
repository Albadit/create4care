from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.permission import PermissionRequest, PermissionUpdate, PermissionResponse
from schemas.common import Message
from db.session import get_db
from services import permission as permission_service

router = APIRouter()

@router.get("/", response_model=List[PermissionResponse])
def list_permissions(db: DBSession = Depends(get_db)):
    return permission_service.get_all_permissions(db)

@router.post("/", response_model=PermissionResponse)
def create_permission(permission: PermissionRequest, db: DBSession = Depends(get_db)):
    return permission_service.create_permission(db, permission)

@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int, db: DBSession = Depends(get_db)):
    permission_obj = permission_service.get_permission(db, permission_id)
    if not permission_obj:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission_obj

@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: int, permission: PermissionUpdate, db: DBSession = Depends(get_db)):
    return permission_service.update_permission(db, permission_id, permission)

@router.delete("/{permission_id}", response_model=Message)
def delete_permission(permission_id: int, db: DBSession = Depends(get_db)):
    return permission_service.delete_permission(db, permission_id)
