from typing import List
from sqlalchemy.orm import Session as DBSession
from fastapi import HTTPException
from db.models import Log
from schemas.log import LogRequest, LogUpdate
from schemas.common import Message

def get_all_logs(db: DBSession) -> List[Log]:
    return db.query(Log).all()

def get_log(db: DBSession, log_id: int) -> Log:
    log_obj = db.query(Log).filter(Log.id == log_id).first()
    if not log_obj:
        raise HTTPException(status_code=404, detail="Log not found")
    return log_obj

def create_log(db: DBSession, log_in: LogRequest) -> Log:
    log_obj = Log(
        table_name=log_in.table_name,
        record_id=log_in.record_id,
        operation=log_in.operation,
        changed_data=log_in.changed_data
    )
    db.add(log_obj)
    db.commit()
    db.refresh(log_obj)
    return log_obj

def update_log(db: DBSession, log_id: int, log_update: LogUpdate) -> Log:
    log_obj = db.query(Log).filter(Log.id == log_id).first()
    if not log_obj:
        raise HTTPException(status_code=404, detail="Log not found")

    update_data = log_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(log_obj, key, value)
    
    db.commit()
    db.refresh(log_obj)
    return log_obj

def delete_log(db: DBSession, log_id: int) -> Message:
    log_obj = db.query(Log).filter(Log.id == log_id).first()
    if not log_obj:
        raise HTTPException(status_code=404, detail="Log not found")
    db.delete(log_obj)
    db.commit()
    return Message(detail="Log deleted successfully")
