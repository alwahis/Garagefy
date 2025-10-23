from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# First define Base
Base = declarative_base()

# Then import models to register them with Base
from ..models import garage, booking, quote

# Load environment variables
load_dotenv()

# Use SQLite for development
SQLALCHEMY_DATABASE_URL = "sqlite:///./garagefy.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
