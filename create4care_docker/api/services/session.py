from typing import List
from sqlalchemy.orm import Session as DBSession
from fastapi import HTTPException
from db.models import Session
from schemas.session import SessionRequest, SessionUpdate
from schemas.common import Message

def get_all_sessions(db: DBSession) -> List[Session]:
    return db.query(Session).all()

def get_session_by_token(db: DBSession, token: str) -> Session:
    session_obj = db.query(Session).filter(Session.session_token == token).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_obj

def create_session(db: DBSession, session_in: SessionRequest) -> Session:
    existing = db.query(Session).filter(Session.session_token == session_in.session_token).first()
    if existing:
        raise HTTPException(status_code=400, detail="Session already exists")
    
    session_obj = Session(
        user_id=session_in.user_id,
        session_token=session_in.session_token,
        expires=session_in.expires
    )
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj

def update_session(db: DBSession, token: str, session_update: SessionUpdate) -> Session:
    session_obj = db.query(Session).filter(Session.session_token == token).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    update_data = session_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(session_obj, key, value)
    
    db.commit()
    db.refresh(session_obj)
    return session_obj

def delete_session(db: DBSession, token: str) -> Message:
    session_obj = db.query(Session).filter(Session.session_token == token).first()
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session_obj)
    db.commit()
    return Message(detail="Session deleted successfully")
