# app/routers/__init__.py
from .user import router as user_router
from .role import router as role_router
from .permission import router as permission_router
from .patient import router as patient_router
from .measurement import router as measurement_router
from .session import router as session_router
from .log import router as log_router
from .auth import router as auth_router
from .db_seed import router as db_seed_router

__all__ = [
    "user_router",
    "role_router",
    "permission_router",
    "patient_router",
    "measurement_router",
    "user_patient_router",
    "session_router",
    "log_router",
    "auth_router",
    "db_seed_router",
]
