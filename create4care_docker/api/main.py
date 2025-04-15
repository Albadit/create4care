from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import IMAGE_DIR, IMAGES_URL
import os

from routers import (
    user_router, role_router, permission_router, patient_router,
    measurement_router, session_router, log_router, db_seed_router, auth_router 
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with appropriate prefixes and tags
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(role_router, prefix="/roles", tags=["roles"])
app.include_router(permission_router, prefix="/permissions", tags=["permissions"])
app.include_router(patient_router, prefix="/patients", tags=["patients"])
app.include_router(measurement_router, prefix="/measurements", tags=["measurements"])
app.include_router(session_router, prefix="/sessions", tags=["sessions"])
app.include_router(log_router, prefix="/logs", tags=["logs"])
app.include_router(db_seed_router, prefix="/database", tags=["database"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Ensure image directory exists and mount it
os.makedirs(IMAGE_DIR, exist_ok=True)
app.mount(f"/{IMAGES_URL}", StaticFiles(directory=IMAGE_DIR), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    # uvicorn main:app --reload

