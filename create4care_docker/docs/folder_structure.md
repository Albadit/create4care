# Folder structure
```
C:\Users\ardit\Documents\GitHub\School\year_3\sem6\create4care_docker
└── api
    ├── Dockerfile
    ├── core
    │   ├── auth.py
    │   └── config.py
    ├── db
    │   ├── models.py
    │   ├── seed.py
    │   └── session.py
    ├── main.py
    ├── requirements.txt
    ├── routers
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── db_seed.py
    │   ├── log.py
    │   ├── measurement.py
    │   ├── patient.py
    │   ├── permission.py
    │   ├── pose_detection.py
    │   ├── role.py
    │   ├── session.py
    │   └── user.py
    ├── schemas
    │   ├── __init__.py
    │   ├── common.py
    │   ├── log.py
    │   ├── measurement.py
    │   ├── patient.py
    │   ├── permission.py
    │   ├── role.py
    │   ├── session.py
    │   └── user.py
    ├── services
    │   ├── __init__.py
    │   ├── log.py
    │   ├── measurement.py
    │   ├── patient.py
    │   ├── permission.py
    │   ├── role.py
    │   ├── session.py
    │   └── user.py
    └── utils
        ├── image_utils.py
        ├── password_hash.py
        ├── pose_decection.py
        └── session.py
```

## api/Dockerfile
```txt
# Use official python image
FROM python:3.10

# Install netcat (optional) and OpenGL support for cv2
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libgl1-mesa-glx \
    libglib2.0-0 \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire project into the container
COPY api .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Start the FastAPI app with Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]

# Start the run the seed
# RUN python db/seed.py
# RUN python -m db.seed
```

## api/core/auth.py
```py
# api/core/auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

# Use a strong secret key and load it from an environment variable in production!
SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT token with an expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    """
    Decode and verify the token. Raises an exception if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

```

## api/core/config.py
```py
import os

IMAGE_DIR = os.getenv("IMAGE_DIR", "images")
IMAGES_URL = os.getenv("IMAGES_URL", "patient_images")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://root:admin@localhost:5432/mydb")

```

## api/db/models.py
```py
import logging
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Date, Text,
    ForeignKey, DateTime, Table
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from core.config import DATABASE_URL

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the engine with echo enabled for SQL debugging.
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define junction tables
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
)

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
)

user_patients = Table(
    'user_patients',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('patient_id', Integer, ForeignKey('patients.id'), primary_key=True),
)

# Define models
class User(Base):
    """Model representing an application user."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_verified = Column(DateTime)
    image = Column(String)

    roles = relationship("Role", secondary=user_roles, back_populates="users")
    sessions = relationship("Session", back_populates="user")
    patients = relationship("Patient", secondary=user_patients, back_populates="users")
    measurements = relationship("Measurement", back_populates="measured_by")

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"

class Role(Base):
    """Model representing a user role."""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role(name={self.name})>"

class Session(Base):
    """Model representing user sessions."""
    __tablename__ = 'sessions'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    session_token = Column(String, unique=True, nullable=False)
    expires = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")

class Permission(Base):
    """Model representing permissions."""
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class Patient(Base):
    """Model representing a patient."""
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(Integer, nullable=False)  # 0 = female, 1 = male
    father_height_mm = Column(Float, nullable=False)
    mother_height_mm = Column(Float, nullable=False)

    users = relationship("User", secondary=user_patients, back_populates="patients")
    measurements = relationship("Measurement", back_populates="patient")

    def __repr__(self):
        return f"<Patient(name={self.name}, birth_date={self.birth_date})>"

class Measurement(Base):
    """Model representing patient measurements."""
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    measured_by_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    height_mm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    sleep_hours = Column(Float)
    exercise_hours = Column(Float)
    image =  Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

    patient = relationship("Patient", back_populates="measurements")
    measured_by = relationship("User", back_populates="measurements")

    def __repr__(self):
        return f"<Measurement(patient_id={self.patient_id}, height_mm={self.height_mm})>"

class Log(Base):
    """Model representing logs."""
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    operation = Column(String, nullable=False)  # 'INSERT', 'UPDATE', or 'DELETE'
    changed_data = Column(Text)  # JSON data capturing the change details
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

## api/db/seed.py
```py
import logging
from datetime import date
from sqlalchemy.orm import sessionmaker
from db.models import Base, engine, Role, User, Patient, Measurement
from utils.password_hash import hash_password
from sqlalchemy import text

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all tables in the database."""
    try:
        Base.metadata.create_all(engine)
        logger.info("✅ All tables created successfully!")
    except Exception as e:
        logger.error("Error creating tables: %s", e)
        raise

def drop_tables():
    """Drop all tables in the database."""
    try:
        # Instead of using drop_all() with cascade, drop the entire schema with CASCADE.
        with engine.connect() as connection:
            connection = connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute(text("DROP SCHEMA public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))
        logger.info("✅ All tables dropped successfully")
    except Exception as e:
        logger.error("Error dropping tables: %s", e)
        raise

def seed_roles():
    """Insert default roles into the roles table."""
    Session = sessionmaker(bind=engine)
    try:
        with Session() as session:
            default_roles = ["admin", "doctor", "parent", "patient"]
            for role_name in default_roles:
                if not session.query(Role).filter_by(name=role_name).first():
                    session.add(Role(name=role_name))
                    logger.info("Adding role: %s", role_name)
            session.commit()
            logger.info("✅ Default roles inserted successfully!")
    except Exception as e:
        logger.error("Error seeding roles: %s", e)
        raise

def seed_dummy_data():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        if session.query(User).first():
            logger.info("Dummy data already exists")
            return

        # Get roles
        admin = session.query(Role).filter_by(name="admin").first()
        doctor = session.query(Role).filter_by(name="doctor").first()
        parent = session.query(Role).filter_by(name="parent").first()
        patient_role = session.query(Role).filter_by(name="patient").first()

        # Create users
        user1 = User(name="Alice Admin", email="alice@admin.com", password=hash_password("pass"))
        user1.roles.append(admin)
        user2 = User(name="Bob Doctor", email="bob@doctor.com", password=hash_password("pass"))
        user2.roles.append(doctor)
        user3 = User(name="Charlie Parent", email="charlie@parent.com", password=hash_password("pass"))
        user3.roles.append(parent)
        user4 = User(name="Daisy Patient", email="daisy@patient.com", password=hash_password("pass"))
        user4.roles.append(patient_role)
        session.add_all([user1, user2, user3, user4])
        session.commit()

        # Create patients
        patient1 = Patient(name="Patient One", birth_date=date(2000, 1, 1), gender=0, father_height_mm=170, mother_height_mm=160)
        patient2 = Patient(name="Patient Two", birth_date=date(1995, 5, 15), gender=1, father_height_mm=180, mother_height_mm=165)
        session.add_all([patient1, patient2])
        session.commit()

        # Associate patients with users
        user3.patients.extend([patient1, patient2])
        user2.patients.append(patient1)
        session.commit()

        # Insert measurements
        measurement1 = Measurement(
            patient_id=patient1.id, measured_by_user_id=user2.id, height_mm=165,
            weight_kg=60, sleep_hours=8, exercise_hours=1,
            image="localhost/test.png"
        )
        measurement2 = Measurement(
            patient_id=patient2.id, measured_by_user_id=user2.id, height_mm=170,
            weight_kg=70, sleep_hours=7, exercise_hours=0.5,
            image="localhost/test.png"
        )
        session.add_all([measurement1, measurement2])
        session.commit()

        logger.info("✅ Dummy data seeded")

if __name__ == "__main__":
    drop_tables()
    create_tables()
    seed_roles()
    seed_dummy_data()
    print("✅ All tasks and Seeding completed successfully!")

```

## api/db/session.py
```py
from sqlalchemy.orm import sessionmaker
from db.models import engine

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function that yields a new database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

## api/main.py
```py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.config import IMAGE_DIR, IMAGES_URL
import os

from routers import (
    user_router, role_router, permission_router, patient_router,
    measurement_router, session_router, log_router, db_seed_router, auth_router,
    pose_detection_router
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
app.include_router(pose_detection_router, prefix="/pose_detection", tags=["pose_detection"])

# Ensure image directory exists and mount it
os.makedirs(IMAGE_DIR, exist_ok=True)
app.mount(f"/{IMAGES_URL}", StaticFiles(directory=IMAGE_DIR), name="images")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    # uvicorn main:app --reload


```

## api/requirements.txt
```txt
fastapi
uvicorn[standard]
SQLAlchemy>=2.0
psycopg2-binary>=2.9
pydantic[email]
requests
python-multipart
bcrypt
python-jose[cryptography]
mediapipe
numpy
```

## api/routers/__init__.py
```py
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
from .pose_detection import router as pose_detection_router

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
    "pose_detection_router",
]

```

## api/routers/auth.py
```py
# api/routers/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DBSession

from core.auth import create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from db.session import get_db
from services import user as user_service  # We'll add a helper function here shortly.
from utils.password_hash import verify_password  # Using your existing password hash utilities

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: DBSession = Depends(get_db)):
    """
    Authenticate user and return a JWT token.
    """
    user = user_service.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: DBSession = Depends(get_db)):
    """
    Dependency to get the current user based on the JWT token.
    """
    payload = verify_token(token)
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = user_service.get_user(db, int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

```

## api/routers/db_seed.py
```py
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
```

## api/routers/log.py
```py
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

```

## api/routers/measurement.py
```py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from schemas.measurement import MeasurementRequest, MeasurementResponse, MeasurementUpdate
from schemas.common import Message
from db.session import get_db
from services import measurement as measurement_service

router = APIRouter()

@router.get("/", response_model=List[MeasurementResponse])
def list_measurements(db: DBSession = Depends(get_db)):
    return measurement_service.get_all_measurements(db)

@router.post("/", response_model=MeasurementResponse)
def create_measurement(measurement: MeasurementRequest, request: Request, db: DBSession = Depends(get_db)):
    return measurement_service.create_measurement(db, measurement, request)

@router.get("/{measurement_id}", response_model=MeasurementResponse)
def get_measurement(measurement_id: int, db: DBSession = Depends(get_db)):
    meas_obj = measurement_service.get_measurement(db, measurement_id)
    if not meas_obj:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return meas_obj

@router.patch("/{measurement_id}", response_model=MeasurementResponse)
def update_measurement(measurement_id: int, measurement: MeasurementUpdate, request: Request, db: DBSession = Depends(get_db)):
    return measurement_service.update_measurement(db, measurement_id, measurement, request)

@router.delete("/{measurement_id}", response_model=Message)
def delete_measurement(measurement_id: int, db: DBSession = Depends(get_db)):
    return measurement_service.delete_measurement(db, measurement_id)
```

## api/routers/patient.py
```py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.patient import PatientRequest, PatientResponse, PatientUpdate
from schemas.common import Message
from db.session import get_db
from services import patient as patient_service

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
def list_patients(db: DBSession = Depends(get_db)):
    return patient_service.get_all_patients(db)

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientRequest, db: DBSession = Depends(get_db)):
    return patient_service.create_patient(db, patient)

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: DBSession = Depends(get_db)):
    patient_obj = patient_service.get_patient(db, patient_id)
    if not patient_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_obj

@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientUpdate, db: DBSession = Depends(get_db)):
    return patient_service.update_patient(db, patient_id, patient)

@router.delete("/{patient_id}", response_model=Message)
def delete_patient(patient_id: int, db: DBSession = Depends(get_db)):
    return patient_service.delete_patient(db, patient_id)
```

## api/routers/permission.py
```py
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

```

## api/routers/pose_detection.py
```py
import os
import tempfile
import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import cv2

from utils.pose_decection import PoseDetector

router = APIRouter()
detector = PoseDetector()

class PostureRequest(BaseModel):
    image_base64: str

class PostureResponse(BaseModel):
    issues: Optional[List[str]] = None
    landmark_image: Optional[str] = None

@router.post("/detect_posture", response_model=PostureResponse)
async def detect_posture(req: PostureRequest):
    # 1. Decode base64 image
    try:
        header, encoded = req.image_base64.split(",", 1)
        img_data = base64.b64decode(encoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image format")

    # 2. Write to a temporary file for PoseDetector
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(img_data)
        tmp_path = tmp.name

    # 3. Run posture evaluation
    try:
        result = detector.evaluate_image(tmp_path)
    finally:
        os.unlink(tmp_path)

    # 4a. Return issues if found
    if "issues" in result:
        return PostureResponse(issues=result["issues"])

    # 4b. No issues: encode overlay and save via image_utils
    success, buffer = cv2.imencode(".png", result["landmark_image"])
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode landmark image")

    b64_img = base64.b64encode(buffer).decode("utf-8")
    data_url = f"data:image/png;base64,{b64_img}"

    return PostureResponse(landmark_image=data_url)

```

## api/routers/role.py
```py
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

```

## api/routers/session.py
```py
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

```

## api/routers/user.py
```py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from schemas.user import UserRequest, UserResponse, UserUpdate
from schemas.common import Message
from db.session import get_db
from services import user as user_service
from routers.auth import get_current_user 
from db.models import User

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def list_users(db: DBSession = Depends(get_db)):
    return user_service.get_all_users(db)

@router.post("/", response_model=UserResponse)
def create_user(user: UserRequest, db: DBSession = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/{uid}", response_model=UserResponse)
def get_user(uid: int, db: DBSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_obj = user_service.get_user(db, uid)
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj

@router.patch("/{uid}", response_model=UserResponse)
def update_user(uid: int, user: UserUpdate, db: DBSession = Depends(get_db)):
    # Partially update the user data.
    return user_service.update_user(db, uid, user)

@router.delete("/{uid}", response_model=Message)
def delete_user(uid: int, db: DBSession = Depends(get_db)):
    return user_service.delete_user(db, uid)
```

## api/schemas/__init__.py
```py
from .common import Message
from .user import *
from .role import *
from .permission import *
from .patient import *
from .measurement import *
from .measurement import *
from .session import *
from .log import *

```

## api/schemas/common.py
```py
from pydantic import BaseModel

class Message(BaseModel):
    detail: str

```

## api/schemas/log.py
```py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogResponse(BaseModel):
    id: int
    table_name: str
    record_id: int
    operation: str
    changed_data: Optional[str]
    changed_at: datetime

class LogRequest(BaseModel):
    table_name: str
    record_id: int
    operation: str
    changed_data: Optional[str]

class LogUpdate(BaseModel):
    table_name: Optional[str]
    record_id: Optional[int]
    operation: Optional[str]
    changed_data: Optional[str]


```

## api/schemas/measurement.py
```py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MeasurementResponse(BaseModel):
    id: int
    patient_id: int
    measured_by_user_id: int
    height_mm: float
    weight_kg: float
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image: str
    date: datetime

class MeasurementRequest(BaseModel):
    patient_id: int
    measured_by_user_id: int
    height_mm: float
    weight_kg: float
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image: str

class MeasurementUpdate(BaseModel):
    patient_id: Optional[int]
    measured_by_user_id: Optional[int]
    height_mm: Optional[float]
    weight_kg: Optional[float]
    sleep_hours: Optional[float]
    exercise_hours: Optional[float]
    image: Optional[str]
```

## api/schemas/patient.py
```py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientResponse(BaseModel):
    id: int
    name: str
    birth_date: date
    gender: int
    father_height_mm: float
    mother_height_mm: float

class PatientRequest(BaseModel):
    name: str
    birth_date: date
    gender: int
    father_height_mm: float
    mother_height_mm: float

class PatientUpdate(BaseModel):
    name: Optional[str]
    birth_date: Optional[date]
    gender: Optional[int]
    father_height_mm: Optional[float]
    mother_height_mm: Optional[float]
```

## api/schemas/permission.py
```py
from pydantic import BaseModel
from typing import Optional

class PermissionResponse(BaseModel):
    id: int
    name: str

class PermissionRequest(BaseModel):
    name: str

class PermissionUpdate(BaseModel):
    name: Optional[str]

```

## api/schemas/role.py
```py
from pydantic import BaseModel
from typing import Optional

class RoleResponse(BaseModel):
    id: int
    name: str

class RoleRequest(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: Optional[str]
```

## api/schemas/session.py
```py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionResponse(BaseModel):
    user_id: int
    session_token: str
    expires: datetime

class SessionRequest(BaseModel):
    user_id: int
    session_token: str
    expires: datetime

class SessionUpdate(BaseModel):
    user_id: Optional[int]
    session_token: Optional[str]
    expires: Optional[datetime]
```

## api/schemas/user.py
```py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    email_verified: Optional[datetime]
    image: Optional[str]  # Optional field for the image (if it's present)

class UserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str  # In production, remember to hash the password!
    email_verified: Optional[datetime]
    image: Optional[str]

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]  # Again, hash passwords in production
    email_verified: Optional[datetime]
    image: Optional[str]  # Optional field for the image
```

## api/services/__init__.py
```py
from . import user, role, permission, patient, measurement, session, log

```

## api/services/log.py
```py
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

```

## api/services/measurement.py
```py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from db.models import Measurement, Patient, User
from schemas.measurement import MeasurementRequest, MeasurementUpdate
from schemas.common import Message
from utils.image_utils import save_image

def get_all_measurements(db: Session) -> List[Measurement]:
    return db.query(Measurement).all()

def get_measurement(db: Session, measurement_id: int) -> Measurement:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

def create_measurement(db: Session, meas_in: MeasurementRequest, request: Request) -> Measurement:
    patient = db.query(Patient).filter(Patient.id == meas_in.patient_id).first()

    if not patient:
        raise HTTPException(status_code=400, detail="Patient does not exist")

    user = db.query(User).filter(User.id == meas_in.measured_by_user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Measured_by user does not exist")
    
    measurement = Measurement(
        patient_id=meas_in.patient_id,
        measured_by_user_id=meas_in.measured_by_user_id,
        height_mm=meas_in.height_mm,
        weight_kg=meas_in.weight_kg,
        sleep_hours=meas_in.sleep_hours,
        exercise_hours=meas_in.exercise_hours,
        image=save_image(meas_in.image, meas_in.patient_id, request)
    )

    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement

def update_measurement(db: Session, measurement_id: int, meas_in: MeasurementUpdate, request: Request) -> Measurement:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    patient = db.query(Patient).filter(Patient.id == meas_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient does not exist")

    user = db.query(User).filter(User.id == meas_in.measured_by_user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Measured_by user does not exist")

    update_data = meas_in.dict(exclude_unset=True)

    if "image_base64" in update_data:
        measurement.image = save_image(update_data.pop("image_base64"), measurement.patient_id, request)
    
    for key, value in update_data.items():
        setattr(measurement, key, value)
    
    db.commit()
    db.refresh(measurement)
    return measurement

def delete_measurement(db: Session, measurement_id: int) -> Message:
    measurement = db.query(Measurement).filter(Measurement.id == measurement_id).first()

    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    
    db.delete(measurement)
    db.commit()
    return Message(detail="Measurement deleted successfully")

```

## api/services/patient.py
```py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Patient
from schemas.patient import PatientRequest, PatientUpdate
from schemas.common import Message

def get_all_patients(db: Session) -> List[Patient]:
    return db.query(Patient).all()

def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def create_patient(db: Session, patient_in: PatientRequest) -> Patient:
    patient = Patient(
        name=patient_in.name,
        birth_date=patient_in.birth_date,
        gender=patient_in.gender,
        father_height_mm=patient_in.father_height_mm,
        mother_height_mm=patient_in.mother_height_mm,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def update_patient(db: Session, patient_id: int, patient_in: PatientUpdate) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_in.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: int) -> Message:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Optionally check associations (e.g., patient.measurements, patient.users)
    if patient.users:
        raise HTTPException(
            status_code=400, 
            detail="Patient is assigned to one or more users and cannot be deleted"
        )

    if patient.measurements:
        raise HTTPException(
            status_code=400, 
            detail="Patient is assigned to measurements and cannot be deleted"
        )
    
    db.delete(patient)
    db.commit()
    return Message(detail="Patient deleted successfully")

```

## api/services/permission.py
```py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Permission
from schemas.permission import PermissionRequest, PermissionUpdate
from schemas.common import Message

def get_all_permissions(db: Session) -> List[Permission]:
    return db.query(Permission).all()

def get_permission(db: Session, permission_id: int) -> Permission:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

def create_permission(db: Session, permission_in: PermissionRequest) -> Permission:
    existing = db.query(Permission).filter(Permission.name == permission_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    permission = Permission(name=permission_in.name)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def update_permission(db: Session, permission_id: int, permission_in: PermissionUpdate) -> Permission:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    update_data = permission_in.dict(exclude_unset=True)
    
    # Check for duplicate permission names
    if "name" in update_data and update_data["name"] != permission.name:
        existing = db.query(Permission).filter(Permission.name == update_data["name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Permission name already exists")
    
    for key, value in update_data.items():
        setattr(permission, key, value)
    
    db.commit()
    db.refresh(permission)
    return permission

def delete_permission(db: Session, permission_id: int) -> Message:
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    db.delete(permission)
    db.commit()
    return Message(detail="Permission deleted successfully")

```

## api/services/role.py
```py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import Role
from schemas.role import RoleRequest, RoleUpdate
from schemas.common import Message

def get_all_roles(db: Session) -> List[Role]:
    return db.query(Role).all()

def get_role(db: Session, role_id: int) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

def create_role(db: Session, role_in: RoleRequest) -> Role:
    existing = db.query(Role).filter(Role.name == role_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    role = Role(name=role_in.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_id: int, role_in: RoleUpdate) -> Role:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    update_data = role_in.dict(exclude_unset=True)

    if "name" in update_data and update_data["name"] != role.name:
        existing = db.query(Role).filter(Role.name == update_data["name"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Role name already exists")
    
    for key, value in update_data.items():
        setattr(role, key, value)
    
    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int) -> Message:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Optionally check for associations (e.g., role.users) before deletion.
    if role.users:
        raise HTTPException(status_code=400, detail="Role is assigned to users and cannot be deleted")
    
    db.delete(role)
    db.commit()
    return Message(detail="Role deleted successfully")

```

## api/services/session.py
```py
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

```

## api/services/user.py
```py
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from utils.password_hash import hash_password
from db.models import User
from schemas.user import UserRequest, UserUpdate
from schemas.common import Message

def get_all_users(db: Session) -> List[User]:
    return db.query(User).all()

def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user(db: Session, uid: int) -> User:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(db: Session, user_in: UserRequest) -> User:
    # Check if the email already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        name=user_in.name,
        email=user_in.email,
        password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, uid: int, user_in: UserUpdate) -> User:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_in.dict(exclude_unset=True)
    
    # If email is provided and it differs, check for duplicates.
    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # If password is provided, hash it.
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, uid: int) -> Message:
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Optionally, check for associations here before deleting.
    if user.measurements_taken:
        raise HTTPException(
            status_code=400,
            detail="User is assigned to measurements and cannot be deleted"
        )
    
    if user.patients:
        raise HTTPException(
            status_code=400,
            detail="User is assigned to one or more patients and cannot be deleted"
        )

    db.delete(user)
    db.commit()
    return Message(detail="User deleted successfully")

```

## api/utils/image_utils.py
```py
import os
import base64
from datetime import datetime
from fastapi import HTTPException, Request
from core.config import IMAGE_DIR, IMAGES_URL

ALLOWED_MIME = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif"}

def save_image(image_base64: str, patient_id: int, request: Request) -> str:
    try:
        header, encoded = image_base64.split(",", 1)
        mime = header.split(";")[0].split(":")[1]
        ext = ALLOWED_MIME[mime]
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image format")

    try:
        image_data = base64.b64decode(encoded)
    except Exception:
        raise HTTPException(status_code=400, detail="Decoding error")

    file_name = f"{patient_id}{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    file_path = os.path.join(IMAGE_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(image_data)

    return f"{request.base_url}{IMAGES_URL}/{file_name}"

```

## api/utils/password_hash.py
```py
import bcrypt

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt and returns the hashed password as a string.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compares a plaintext password with the hashed password.
    Returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

```

## api/utils/pose_decection.py
```py
import cv2
import math
import mediapipe as mp
import numpy as np

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            model_complexity=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def evaluate_neck_alignment(self, landmarks, ear_shoulder_angle_threshold=50):
        left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value]
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2
        ear_center_x = (left_ear.x + right_ear.x) / 2
        ear_center_y = (left_ear.y + right_ear.y) / 2

        delta_x = shoulder_center_x - ear_center_x
        delta_y = shoulder_center_y - ear_center_y
        theta = math.degrees(math.atan2(delta_x, delta_y))
        return abs(theta) < ear_shoulder_angle_threshold

    def evaluate_torso_alignment(self, landmarks, alignment_factor=0.1):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
        right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]

        torso_length = abs(((left_shoulder.y + right_shoulder.y) / 2) - ((left_hip.y + right_hip.y) / 2))
        threshold = torso_length * alignment_factor

        shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
        hip_center_x = (left_hip.x + right_hip.x) / 2
        knee_center_x = (left_knee.x + right_knee.x) / 2

        return (abs(shoulder_center_x - hip_center_x) < threshold and
                abs(hip_center_x - knee_center_x) < threshold)

    def evaluate_knee_alignment(self, landmarks, knee_angle_threshold=160):
        def calculate_angle(a, b, c):
            ba = (a[0] - b[0], a[1] - b[1])
            bc = (c[0] - b[0], c[1] - b[1])
            dot = ba[0]*bc[0] + ba[1]*bc[1]
            norm_ba = math.hypot(*ba)
            norm_bc = math.hypot(*bc)
            if norm_ba * norm_bc == 0:
                return 0
            angle = math.degrees(math.acos(dot / (norm_ba * norm_bc)))
            return angle

        left = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]]
        right = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                 landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]]

        left_angle = calculate_angle((left[0].x, left[0].y),
                                     (left[1].x, left[1].y),
                                     (left[2].x, left[2].y))
        right_angle = calculate_angle((right[0].x, right[0].y),
                                      (right[1].x, right[1].y),
                                      (right[2].x, right[2].y))

        return left_angle >= knee_angle_threshold and right_angle >= knee_angle_threshold

    def evaluate_feet_flat(self, landmarks, foot_y_diff_threshold=0.02):
        left_heel = landmarks[self.mp_pose.PoseLandmark.LEFT_HEEL.value]
        right_heel = landmarks[self.mp_pose.PoseLandmark.RIGHT_HEEL.value]
        left_toe = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]
        right_toe = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        left_flat = abs(left_heel.y - left_toe.y) < foot_y_diff_threshold
        right_flat = abs(right_heel.y - right_toe.y) < foot_y_diff_threshold
        return left_flat and right_flat

    # ----------------------------
    # Main Processing Functions
    # ----------------------------

    def evaluate_image(self, image_path):
        """
        Evaluate a single image for posture correctness.
        Returns:
            - {'issues': [...]} if posture is incorrect
            - {'landmark_image': np.ndarray} if posture is correct (image with landmarks only)
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot load image from {image_path}")

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if not results.pose_landmarks:
            return {'issues': ['No pose detected in the image']}

        landmarks = results.pose_landmarks.landmark
        issues = []

        if not self.evaluate_neck_alignment(landmarks):
            issues.append('Adjust neck alignment: keep ears over shoulders')
        if not self.evaluate_torso_alignment(landmarks):
            issues.append('Straighten torso: align shoulders, hips, and knees vertically')
        if not self.evaluate_knee_alignment(landmarks):
            issues.append('Extend knees: keep legs straight')
        if not self.evaluate_feet_flat(landmarks):
            issues.append('Place feet flat on the ground')

        if issues:
            return {'issues': issues}
        else:
            # Create a transparent background image (4-channel)
            h, w = image.shape[:2]
            transparent = np.zeros((h, w, 4), dtype=np.uint8)
            # Draw landmarks onto a separate BGR canvas
            canvas = np.zeros((h, w, 3), dtype=np.uint8)
            self.mp_drawing.draw_landmarks(
                canvas,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )
            # Convert canvas to BGRA and set alpha where landmarks exist
            canvas_bgra = cv2.cvtColor(canvas, cv2.COLOR_BGR2BGRA)
            # Alpha channel: non-black pixels become opaque
            alpha = np.any(canvas != 0, axis=2).astype(np.uint8) * 255
            canvas_bgra[:, :, 3] = alpha
            return {'landmark_image': canvas_bgra}

if __name__ == "__main__":
    detector = PoseDetector()
    # Replace with your image path (use raw string, double backslashes, or forward slashes)
    img_path = r'C:/Users/ardit/Documents/GitHub/School/year_3/sem6/pose_decection/dummy_correct.jpg'
    result = detector.evaluate_image(img_path)
    if 'issues' in result:
        print("Posture improvements needed:")
        for issue in result['issues']:
            print("-", issue)
    else:
        landmark_img = result['landmark_image']
        # Save landmark-only image to current working directory
        save_filename = 'landmarks_only.png'
        cv2.imwrite(save_filename, landmark_img)
        print(f"Landmark image saved as {save_filename} in the current folder.")
```

## api/utils/session.py
```py
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

```
