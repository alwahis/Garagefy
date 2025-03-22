from pydantic import BaseModel
from typing import List, Optional, Dict

class DiagnosisRequest(BaseModel):
    car_brand: str
    model: str
    year: int
    symptoms: str

class VehicleInfo(BaseModel):
    brand: str
    model: str
    year: int

class DiagnosisContent(BaseModel):
    vehicle_info: VehicleInfo
    symptoms: str
    analysis: str
    references: List[str]
    disclaimer: Optional[str] = None

class DiagnosisResponse(BaseModel):
    diagnosis: DiagnosisContent


class GarageCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    phone: str
    services: Optional[Dict] = None
    opening_hours: Optional[str] = None
    url: Optional[str] = None
    

class Garage(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    phone: str
    website: Optional[str] = None
    opening_hours: Optional[str] = None
    services: Optional[List[str]] = None
    distance: Optional[float] = None


class BookingCreate(BaseModel):
    garage_id: int
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    name: str
    phone: str
    email: str
    car_info: Optional[str] = None
    service: str
    

class BookingResponse(BaseModel):
    booking_id: str
    garage_id: int
    date: str
    time: str
    status: str


class UsedCarCheckRequest(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    mileage: Optional[int] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = 0
    vin: Optional[str] = None
