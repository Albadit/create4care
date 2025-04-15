from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime
from db.models import Session as SessionModel  # our Session model from SQLAlchemy
from db.session import get_db

def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Expecting a header like "Authorization: Bearer <session_token>"
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="No session token provided")
    
    # Remove the "Bearer " prefix if present.
    token = auth_header.replace("Bearer ", "")
    
    # Query the session using the provided token
    session_obj = db.query(SessionModel).filter(SessionModel.session_token == token).first()
    if not session_obj:
        raise HTTPException(status_code=401, detail="Invalid session token")
    
    # Check if the session has expired
    if session_obj.expires < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Return the user linked to the session
    return session_obj.user
