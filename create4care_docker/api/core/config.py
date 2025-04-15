import os

IMAGE_DIR = os.getenv("IMAGE_DIR", "images")
IMAGES_URL = os.getenv("IMAGES_URL", "patient_images")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://root:admin@localhost:5432/mydb")
