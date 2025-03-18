from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas
from .core.database import get_db, engine
from .services.ai_service import CarDiagnosticAI
from .services.used_car_service import UsedCarService
from pydantic import BaseModel
import logging
import json
import math
from pathlib import Path
import pandas as pd
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Garagefy API",
    description="API for connecting car owners with specialized garages in Luxembourg",
    version="1.0.0"
)

# CORS middleware configuration
origins = [
    "http://localhost:3000",  # React development server
    "http://127.0.0.1:3000",
    "http://localhost:3001",  # Additional React port
    "http://127.0.0.1:3001",
    "http://localhost:3002",  # Another React port
    "http://127.0.0.1:3002",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8005",
    "http://127.0.0.1:8005"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
car_diagnostic_ai = CarDiagnosticAI()
used_car_service = UsedCarService()

class DiagnosisRequest(BaseModel):
    car_brand: str
    model: str
    year: int
    symptoms: str

class UsedCarCheckRequest(BaseModel):
    make: str
    model: str
    year: int
    mileage: int
    fuel_type: str
    transmission: str

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to Garagefy API"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@app.get("/api/car-data")
async def get_car_data():
    """Get available car brands and models"""
    try:
        car_data = {
            'Toyota': {
                'models': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Prius', 'Land Cruiser', 'Tundra', 'Tacoma', 'Sienna', '4Runner']
            },
            'Honda': {
                'models': ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V', 'Odyssey', 'Ridgeline', 'Fit', 'Passport', 'Insight']
            },
            'Ford': {
                'models': ['F-150', 'Mustang', 'Explorer', 'Escape', 'Focus', 'Bronco', 'Ranger', 'Edge', 'Expedition', 'Maverick']
            },
            'BMW': {
                'models': ['3 Series', '5 Series', 'X3', 'X5', 'M3', '7 Series', 'X1', 'X7', 'i4', 'iX']
            },
            'Mercedes-Benz': {
                'models': ['C-Class', 'E-Class', 'S-Class', 'GLC', 'GLE', 'A-Class', 'GLA', 'GLB', 'EQS', 'G-Class']
            },
            'Audi': {
                'models': ['A4', 'A6', 'Q5', 'Q7', 'TT', 'A3', 'Q3', 'e-tron', 'RS6', 'S5']
            },
            'Nissan': {
                'models': ['Altima', 'Sentra', 'Rogue', 'Pathfinder', 'Maxima', 'Frontier', 'Kicks', 'Murano', 'Armada', 'Leaf']
            },
            'Hyundai': {
                'models': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona', 'Palisade', 'Venue', 'IONIQ', 'Accent', 'Genesis']
            },
            'Chevrolet': {
                'models': ['Silverado', 'Equinox', 'Malibu', 'Tahoe', 'Camaro', 'Traverse', 'Blazer', 'Colorado', 'Suburban', 'Bolt']
            },
            'Kia': {
                'models': ['Soul', 'Sportage', 'Sorento', 'Optima', 'Forte', 'Telluride', 'Seltos', 'Carnival', 'Niro', 'EV6']
            },
            'Volkswagen': {
                'models': ['Golf', 'Passat', 'Tiguan', 'Atlas', 'Jetta', 'ID.4', 'Taos', 'Arteon', 'GTI', 'R']
            },
            'Lexus': {
                'models': ['RX', 'ES', 'NX', 'IS', 'GX', 'UX', 'LS', 'LC', 'RC', 'LX']
            },
            'Porsche': {
                'models': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan', '718 Cayman', '718 Boxster', 'Cayenne Coupe']
            },
            'Subaru': {
                'models': ['Outback', 'Forester', 'Crosstrek', 'Impreza', 'Legacy', 'Ascent', 'WRX', 'BRZ', 'Solterra']
            },
            'Mazda': {
                'models': ['CX-5', 'Mazda3', 'CX-30', 'CX-9', 'MX-5 Miata', 'CX-50', 'Mazda6', 'MX-30']
            },
            'Volvo': {
                'models': ['XC90', 'XC60', 'S60', 'V60', 'XC40', 'S90', 'V90', 'C40', 'Polestar 2']
            },
            'Land Rover': {
                'models': ['Range Rover', 'Discovery', 'Defender', 'Range Rover Sport', 'Range Rover Velar', 'Discovery Sport', 'Evoque']
            },
            'Jeep': {
                'models': ['Grand Cherokee', 'Wrangler', 'Cherokee', 'Compass', 'Renegade', 'Gladiator', 'Wagoneer', 'Grand Wagoneer']
            },
            'Acura': {
                'models': ['MDX', 'RDX', 'TLX', 'ILX', 'NSX', 'Integra']
            },
            'Infiniti': {
                'models': ['Q50', 'QX60', 'QX80', 'QX50', 'Q60', 'QX55']
            }
        }
        return car_data
    except Exception as e:
        logger.error(f"Error fetching car data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/diagnose")
async def diagnose_car(request: DiagnosisRequest):
    """Diagnose car issues using technical documentation and AI"""
    try:
        # Format the problem description
        problem_description = f"Vehicle: {request.year} {request.car_brand} {request.model}\nSymptoms: {request.symptoms}"
        
        # Get AI-powered diagnosis with technical documentation
        diagnosis = await car_diagnostic_ai.get_diagnosis(request.car_brand, problem_description)
        
        return {
            'diagnosis': {
                'vehicle_info': {
                    'brand': request.car_brand,
                    'model': request.model,
                    'year': request.year
                },
                'symptoms': request.symptoms,
                'analysis': diagnosis,
                'disclaimer': (
                    'This diagnosis is provided by an AI system with access to technical documentation. '
                    'Always consult with a qualified mechanic for a professional inspection.'
                )
            }
        }
    except Exception as e:
        logger.error(f"Error in diagnosis endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
async def test_diagnostic_system():
    """
    Test the diagnostic system with a sample problem.
    """
    try:
        # Test diagnosis for a common issue
        test_brand = "Toyota"
        test_symptoms = "Engine makes knocking sound and check engine light is on"
        
        diagnosis = await car_diagnostic_ai.get_diagnosis(test_brand, test_symptoms)
        
        return {
            "status": "success",
            "message": "Diagnostic system is working",
            "test_diagnosis": diagnosis
        }
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Test failed: {str(e)}"
        )

@app.get("/api/garages")
async def get_garages(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    search: Optional[str] = None,
    service: Optional[str] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    Get list of garages with optional filtering and distance calculation
    """
    try:
        return await list_garages(lat, lon, search, service, db, skip, limit)
    except Exception as e:
        logger.error(f"Error fetching garages: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch garages"
        )

@app.get("/api/garages/", response_model=List[schemas.Garage])
async def list_garages(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    search: Optional[str] = None,
    service: Optional[str] = None,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[Dict]:
    """
    Get list of garages with optional filtering and distance calculation
    """
    try:
        # Load garage data
        garages = load_garage_data()

        # Filter by search term
        if search:
            search = search.lower()
            garages = [
                g for g in garages 
                if search in g["name"].lower() or 
                   search in g["address"].lower() or 
                   any(search in s.lower() for s in g["services"])
            ]

        # Filter by service
        if service:
            service = service.lower()
            garages = [
                g for g in garages 
                if any(service in s.lower() for s in g["services"])
            ]

        # Calculate distances if coordinates provided
        if lat is not None and lon is not None:
            for garage in garages:
                garage["distance"] = calculate_distance(
                    lat, lon,
                    garage["latitude"],
                    garage["longitude"]
                )
            # Sort by distance
            garages = [g for g in garages if g["distance"] is not None]
            garages.sort(key=lambda x: x["distance"])

        # Apply pagination
        garages = garages[skip:skip+limit]

        return garages
    except Exception as e:
        logger.error(f"Error fetching garages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch garages")

@app.get("/api/garages/{garage_id}", response_model=schemas.Garage)
async def get_garage(garage_id: int, db: Session = Depends(get_db)) -> Dict:
    """
    Get detailed information about a specific garage
    """
    try:
        garages = load_garage_data()
        if 0 <= garage_id < len(garages):
            return garages[garage_id]
        raise HTTPException(status_code=404, detail="Garage not found")
    except Exception as e:
        logger.error(f"Error fetching garage: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch garage details")

@app.post("/api/bookings")
async def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking appointment
    """
    try:
        # Verify garage exists
        garage = await get_garage(booking.garage_id, db)
        if not garage:
            raise HTTPException(
                status_code=404,
                detail=f"Garage with ID {booking.garage_id} not found"
            )
            
        # Create booking
        new_booking = models.Booking(
            garage_id=booking.garage_id,
            date=booking.date,
            time=booking.time,
            name=booking.name,
            phone=booking.phone,
            email=booking.email,
            service=booking.service
        )
        
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        
        return {
            "status": "success",
            "message": "Booking created successfully",
            "booking_id": new_booking.id
        }
        
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create booking"
        )
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create booking"
        )

@app.get("/api/used-car/options")
def get_used_car_options():
    """Get all available options for car selection dropdowns"""
    try:
        options = used_car_service.get_car_options()
        return options
    except Exception as e:
        logger.error(f"Error fetching used car options: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/used-car/check")
async def check_used_car(request: UsedCarCheckRequest):
    """Perform a comprehensive used car check based on trusted online sources"""
    try:
        result = await used_car_service.check_used_car(
            make=request.make,
            model=request.model,
            year=request.year,
            mileage=request.mileage,
            fuel_type=request.fuel_type,
            transmission=request.transmission
        )
        return result
    except Exception as e:
        logger.error(f"Error in used car check endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-options")
def test_options():
    """Test endpoint for debugging"""
    return {"message": "Test endpoint is working"}

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    if not all([lat1, lon1, lat2, lon2]):  # If any coordinate is missing
        return None
        
    R = 6371  # Earth's radius in kilometers

    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return round(distance, 2)

def clean_garage_data(df):
    """Clean and format garage data"""
    # Remove rows without a name
    df = df.dropna(subset=['name'])
    
    # Clean up services
    df['services'] = df['services'].fillna('')
    df['services'] = df['services'].apply(lambda x: [
        service.strip()
        for service in re.split('[,.]', str(x))
        if service.strip() and len(service.strip()) > 3
    ])
    
    # Clean up hours
    df['hours'] = df['hours'].fillna('Contact for hours')
    df['hours'] = df['hours'].apply(lambda x: x.replace('Monday to', 'Mon-Fri:'))
    
    # Convert coordinates to float, replacing invalid values with Luxembourg City coordinates
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    
    # Set default coordinates for missing values (Luxembourg City center)
    df['Latitude'] = df['Latitude'].fillna(49.6116)
    df['Longitude'] = df['Longitude'].fillna(6.1319)
    
    # Clean up phone numbers
    df['phone'] = df['phone'].fillna('')
    
    # Clean up website URLs
    df['website'] = df['website'].fillna('')
    df['website'] = df['website'].apply(lambda x: 
        'https://' + x if x and not x.startswith(('http://', 'https://')) else x
    )
    
    return df

def load_garage_data():
    """Load garage data from CSV file"""
    csv_path = Path(__file__).parent.parent.parent / "luxembourg_garages_with_coordinates.csv"
    df = pd.read_csv(csv_path)
    df = clean_garage_data(df)
    
    # Convert DataFrame to list of dictionaries
    garages = df.to_dict('records')
    
    # Format the data for API response
    formatted_garages = []
    for garage in garages:
        formatted_garage = {
            'name': garage['name'],
            'address': garage['address'],
            'phone': garage['phone'],
            'website': garage['website'],
            'opening_hours': garage['hours'],
            'services': garage['services'],
            'latitude': garage['Latitude'],
            'longitude': garage['Longitude']
        }
        formatted_garages.append(formatted_garage)
    
    return formatted_garages
