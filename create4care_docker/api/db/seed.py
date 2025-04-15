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
