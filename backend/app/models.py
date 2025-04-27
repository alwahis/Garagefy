from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .core.database import Base

class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    description = Column(Text)
    specialties = Column(String)  # Comma-separated list of specialties
    is_active = Column(Boolean, default=True)

    bookings = relationship("Booking", back_populates="garage")

class DiagnosticSession(Base):
    __tablename__ = "diagnostic_sessions"

    id = Column(Integer, primary_key=True, index=True)
    car_brand = Column(String, index=True)
    model = Column(String)
    car_year = Column(Integer)
    problem_description = Column(Text)
    diagnosis = Column(Text)
    created_at = Column(String)  # ISO format timestamp
    references = Column(Text)  # JSON string of reference list

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    garage_id = Column(Integer, ForeignKey("garages.id"))
    date = Column(String)  # Format: YYYY-MM-DD
    time = Column(String)  # Format: HH:MM
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    service = Column(String)
    status = Column(String, default="pending")  # pending, confirmed, completed, cancelled
    created_at = Column(String)  # ISO format timestamp

    # Relationship
    garage = relationship("Garage", back_populates="bookings")
