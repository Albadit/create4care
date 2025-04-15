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
