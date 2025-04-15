from fastapi import APIRouter, HTTPException
from schemas.common import Message
from db.seed import drop_tables, create_tables, seed_roles, seed_dummy_data

router = APIRouter()

@router.get("/reset_tables", response_model=Message)
def reset_tables():
    try:
        drop_tables()
        create_tables()
        return Message(detail="All tables dropped and created successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/seed_roles", response_model=Message)
def seed_roles_route():
    try:
        seed_roles()
        return Message(detail="Roles seeded successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/seed_dummy_data", response_model=Message)
def seed_dummy_data_route():
    try:
        seed_dummy_data()
        return Message(detail="Dummy data seeded successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))