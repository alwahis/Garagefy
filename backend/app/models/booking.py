from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, time

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    garage_id = Column(Integer, index=True)
    date = Column(String)  # Store as string in format YYYY-MM-DD
    time = Column(String)  # Store as string in format HH:MM
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    car_info = Column(String, nullable=True)
    service = Column(String)
    status = Column(String, default="confirmed")  # confirmed, completed, cancelled
    booking_reference = Column(String, unique=True, index=True)
