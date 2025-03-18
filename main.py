from fastapi import FastAPI, Request, HTTPException, Depends, File, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from car_diagnostic import CarDiagnosticSystem
from car_database import car_database
from data import CAR_BRANDS
from luxembourg_garages import LUXEMBOURG_GARAGES
from typing import List, Optional, Dict, Any
from math import radians, sin, cos, sqrt, atan2
import hashlib
import time
import uuid
import os
import shutil
from datetime import datetime
from functools import lru_cache
from backend.app.schemas import BookingCreate, BookingResponse, UsedCarCheckRequest
from used_car_check import used_car_checker
import math

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for diagnosis results
diagnosis_cache = {}

# Initialize templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create uploads directory if it doesn't exist
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

diagnostic_system = CarDiagnosticSystem()

# In-memory storage for garages and bookings (in a real app, this would be a database)
garages_data = LUXEMBOURG_GARAGES
bookings_data = []

class DiagnosticRequest(BaseModel):
    car_brand: str
    car_model: str
    year: int
    symptoms: str

class GarageRequest(BaseModel):
    latitude: float
    longitude: float
    max_distance: float = 20  # Default max distance in kilometers

class GarageCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    specialties: List[str]
    repair_capabilities: Dict[str, List[str]]
    phone: str
    email: str
    website: str
    image_url: str

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/diagnose-page")
async def diagnose_page(request: Request):
    return templates.TemplateResponse("diagnose.html", {"request": request})

@app.get("/find-garage-page")
async def find_garage_page(request: Request):
    return templates.TemplateResponse("find_garage.html", {"request": request})

@app.get("/add-garage-page")
async def add_garage_page(request: Request):
    return templates.TemplateResponse("add_garage.html", {"request": request})

@app.get("/api/brands")
async def get_brands():
    return {"brands": list(car_database.keys())}

@app.get("/api/models/{brand}")
async def get_models(brand: str):
    if brand not in car_database:
        return JSONResponse(status_code=404, content={"error": "Brand not found"})
    return {"models": list(car_database[brand].keys())}

@app.get("/api/years/{brand}/{model}")
async def get_years(brand: str, model: str):
    if brand not in car_database:
        return JSONResponse(status_code=404, content={"error": "Brand not found"})
    if model not in car_database[brand]:
        return JSONResponse(status_code=404, content={"error": "Model not found"})
    return {"years": car_database[brand][model]}

@app.get("/api/garages")
async def get_garages():
    return {"garages": garages_data}

@app.post("/api/garages")
async def add_garage(garage: GarageCreate):
    try:
        new_garage = garage.dict()
        new_garage["id"] = max(g["id"] for g in garages_data) + 1
        new_garage["rating"] = 0.0  # New garages start with 0 rating
        garages_data.append(new_garage)
        return JSONResponse(
            status_code=200,
            content={"message": "Garage added successfully", "garage": new_garage}
        )
    except Exception as e:
        print(f"Error adding garage: {str(e)}")  # Add debug logging
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/find-garages")
async def find_garages(
    request: Request
):
    """
    Find garages near a specified location
    """
    try:
        # Parse request data
        body = await request.json()
        latitude = body.get('latitude')
        longitude = body.get('longitude')
        max_distance = body.get('max_distance', 20)  # Default to 20km if not specified
        
        if latitude is None or longitude is None:
            raise HTTPException(status_code=400, detail="Latitude and longitude are required")
        
        # Get all garages from the database
        all_garages = garages_data
        
        # Calculate distances and filter garages within max_distance
        nearby_garages = []
        for garage in all_garages:
            # Calculate distance using Haversine formula
            garage_lat = garage.get('latitude')
            garage_lon = garage.get('longitude')
            
            if garage_lat is None or garage_lon is None:
                continue  # Skip garages without location data
                
            distance = calculate_distance(latitude, longitude, garage_lat, garage_lon)
            
            if distance <= max_distance:
                garage_with_distance = garage.copy()
                garage_with_distance['distance'] = distance
                nearby_garages.append(garage_with_distance)
        
        # Sort by distance
        nearby_garages.sort(key=lambda x: x.get('distance', float('inf')))
        
        return {"garages": nearby_garages}
    except Exception as e:
        print(f"Error finding nearby garages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/diagnose")
async def diagnose_car(
    request: Request,
    car_brand: str = Form(None),
    car_model: str = Form(None),
    year: str = Form(None),
    symptoms: str = Form(None),
    audio_file: UploadFile = File(None)
):
    # Check if we received form data or need to extract from JSON
    if car_brand is None or car_model is None or year is None:
        try:
            # Try reading as JSON
            body = await request.json()
            car_brand = body.get('car_brand')
            car_model = body.get('model')
            year = body.get('year')
            symptoms = body.get('symptoms', '')
        except:
            raise HTTPException(
                status_code=400, 
                detail="Invalid request format. Please provide car_brand, car_model, year, and symptoms."
            )
    
    # Validate inputs
    if not car_brand or not car_model or not year or not symptoms:
        raise HTTPException(
            status_code=400,
            detail="Missing required fields: car_brand, car_model, year, and symptoms are required."
        )
    
    try:
        year_int = int(year)
    except ValueError:
        raise HTTPException(status_code=400, detail="Year must be a valid integer.")
    
    # Generate a cache key based on the request parameters
    cache_key = f"{car_brand}_{car_model}_{year}_{hashlib.md5(symptoms.encode()).hexdigest()}"
    
    # Check if we have a cached result
    if cache_key in diagnosis_cache:
        print("Using cached diagnosis result")
        return {"diagnosis": diagnosis_cache[cache_key]}
    
    # Process audio file if provided
    audio_path = None
    if audio_file:
        try:
            # Create a unique filename
            file_extension = os.path.splitext(audio_file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            audio_path = os.path.join(UPLOADS_DIR, unique_filename)
            
            # Save the file
            with open(audio_path, "wb") as buffer:
                shutil.copyfileobj(audio_file.file, buffer)
        except Exception as e:
            print(f"Error processing audio file: {str(e)}")
            # Continue without the audio file
            audio_path = None
    
    try:
        # Get diagnosis from the diagnostic system
        diagnosis_result = diagnostic_system.diagnose_issue(
            symptoms=symptoms,
            car_brand=car_brand,
            car_model=car_model,
            year=year_int,
            audio_path=audio_path
        )
        
        # Format the response
        diagnosis_response = {
            "vehicle_info": {
                "brand": car_brand,
                "model": car_model,
                "year": year_int
            },
            "symptoms": symptoms,
            "analysis": diagnosis_result.get("diagnosis", "No diagnosis available"),
            "severity": diagnosis_result.get("severity", "unknown"),
            "recommendations": diagnosis_result.get("recommendations", []),
            "cost_estimate": diagnosis_result.get("cost_estimate_text", "Cost estimation unavailable"),
            "disclaimer": "This diagnosis is provided for informational purposes only. Always consult with a certified mechanic for a professional assessment."
        }
        
        # Cache the result
        diagnosis_cache[cache_key] = diagnosis_response
        
        return {"diagnosis": diagnosis_response}
    except Exception as e:
        print(f"Error in diagnosis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")

@app.get("/api/car-data")
async def get_car_data():
    """
    Get all available car brands and their models
    """
    try:
        result = {}
        for brand, models_dict in car_database.items():
            models_list = list(models_dict.keys())
            result[brand] = {
                "models": models_list,
                "years": {}
            }
            for model in models_list:
                result[brand]["years"][model] = car_database[brand][model]
        
        return result
    except Exception as e:
        print(f"Error getting car data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bookings")
async def create_booking(booking: BookingCreate):
    """
    Create a new booking for a garage service
    """
    try:
        # Generate a unique booking reference
        booking_reference = str(uuid.uuid4())[:8].upper()
        
        # Create booking record
        new_booking = {
            "booking_id": booking_reference,
            "garage_id": booking.garage_id,
            "date": booking.date,
            "time": booking.time,
            "name": booking.name,
            "phone": booking.phone,
            "email": booking.email,
            "car_info": booking.car_info,
            "service": booking.service,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        bookings_data.append(new_booking)
        
        return BookingResponse(
            booking_id=booking_reference,
            garage_id=booking.garage_id,
            date=booking.date,
            time=booking.time,
            status="confirmed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create booking: {str(e)}")

@app.get("/api/bookings/{booking_reference}")
async def get_booking(booking_reference: str):
    """
    Get booking details by reference number
    """
    for booking in bookings_data:
        if booking["booking_id"] == booking_reference:
            return booking
    
    raise HTTPException(status_code=404, detail="Booking not found")

@app.get("/api/garages/{garage_id}/bookings")
async def get_garage_bookings(garage_id: int):
    """
    Get all bookings for a specific garage
    """
    garage_bookings = [
        booking for booking in bookings_data 
        if booking["garage_id"] == garage_id
    ]
    
    return {"bookings": garage_bookings}

@app.post("/api/used-car/check")
async def check_used_car(request: UsedCarCheckRequest):
    """
    Check if a used car is worth buying based on online research.
    """
    try:
        result = used_car_checker.check_car(
            brand=request.brand,
            model=request.model,
            year=request.year,
            mileage=request.mileage,
            price=request.price,
            description=request.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Used car check failed: {str(e)}")

@app.get("/api/used-car/options")
async def get_used_car_options():
    """Get all available options for car selection dropdowns"""
    try:
        # Create a sample response with the necessary data
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 30, -1))
        
        # Sample car makes and models
        makes = ["BMW", "Volkswagen", "Toyota", "Audi", "Mercedes-Benz"]
        models_by_make = {
            "BMW": ["3 Series", "5 Series"],
            "Volkswagen": ["Golf", "Passat"],
            "Toyota": ["Corolla", "Camry"],
            "Audi": ["A3", "A4", "Q5"],
            "Mercedes-Benz": ["C-Class", "E-Class"]
        }
        
        # Sample fuel types
        fuel_types = [
            {"id": "petrol", "name": "Petrol"},
            {"id": "diesel", "name": "Diesel"},
            {"id": "hybrid", "name": "Hybrid"},
            {"id": "electric", "name": "Electric"},
            {"id": "lpg", "name": "LPG"},
            {"id": "cng", "name": "CNG"}
        ]
        
        # Sample transmission types
        transmission_types = [
            {"id": "manual", "name": "Manual"},
            {"id": "automatic", "name": "Automatic"},
            {"id": "semi-auto", "name": "Semi-Automatic"},
            {"id": "cvt", "name": "CVT"},
            {"id": "dct", "name": "Dual-Clutch"}
        ]
        
        return {
            "makes": makes,
            "models_by_make": models_by_make,
            "years": years,
            "fuelTypes": fuel_types,
            "transmissionTypes": transmission_types
        }
    except Exception as e:
        print(f"Error fetching used car options: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running correctly
    """
    try:
        # Check if the diagnostic system is initialized
        if not diagnostic_system:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Diagnostic system not initialized"}
            )
        
        # Return a success response
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "diagnostic_system": "available",
                "database": "in-memory",
                "garages_count": len(garages_data),
                "bookings_count": len(bookings_data)
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    print("Starting Garagefy API server on http://localhost:8099")
    uvicorn.run(app, host="0.0.0.0", port=8099, ssl_keyfile=None, ssl_certfile=None)
