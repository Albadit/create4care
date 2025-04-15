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