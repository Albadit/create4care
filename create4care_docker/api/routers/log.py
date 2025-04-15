from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from typing import List
from schemas.log import LogRequest, LogResponse, LogUpdate
from schemas.common import Message
from db.session import get_db
from services import log as log_service

router = APIRouter()

@router.get("/", response_model=List[LogResponse])
def list_logs(db: DBSession = Depends(get_db)):
    return log_service.get_all_logs(db)

@router.post("/", response_model=LogResponse)
def create_new_log(log_req: LogRequest, db: DBSession = Depends(get_db)):
    return log_service.create_log(db, log_req)

@router.get("/{log_id}", response_model=LogResponse)
def get_log(log_id: int, db: DBSession = Depends(get_db)):
    return log_service.get_log(db, log_id)

@router.patch("/{log_id}", response_model=LogResponse)
def update_log(log_id: int, log_update: LogUpdate, db: DBSession = Depends(get_db)):
    return log_service.update_log(db, log_id, log_update)

@router.delete("/{log_id}", response_model=Message)
def remove_log(log_id: int, db: DBSession = Depends(get_db)):
    return log_service.delete_log(db, log_id)
