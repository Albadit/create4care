from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from typing import List
from schemas.session import SessionRequest, SessionResponse, SessionUpdate
from schemas.common import Message
from db.session import get_db
from services import session as session_service

router = APIRouter()

@router.get("/", response_model=List[SessionResponse])
def list_sessions(db: DBSession = Depends(get_db)):
    return session_service.get_all_sessions(db)

@router.post("/", response_model=SessionResponse)
def create_new_session(session_req: SessionRequest, db: DBSession = Depends(get_db)):
    return session_service.create_session(db, session_req)

@router.get("/{token}", response_model=SessionResponse)
def get_session(token: str, db: DBSession = Depends(get_db)):
    return session_service.get_session_by_token(db, token)

@router.patch("/{token}", response_model=SessionResponse)
def update_session(token: str, session_update: SessionUpdate, db: DBSession = Depends(get_db)):
    return session_service.update_session(db, token, session_update)

@router.delete("/{token}", response_model=Message)
def remove_session(token: str, db: DBSession = Depends(get_db)):
    return session_service.delete_session(db, token)
