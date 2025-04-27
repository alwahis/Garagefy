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
import re

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
            car_model = body.get('car_model')
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

class UsedCarCheckRequest(BaseModel):
    brand: Optional[str]
    model: Optional[str]
    year: Optional[int]
    mileage: Optional[int]
    price: Optional[float]
    description: Optional[str]
    vin: Optional[str]

@app.post("/api/check-used-car")
async def check_used_car(request: UsedCarCheckRequest):
    """
    Check if a used car is worth buying based on online research.
    """
    try:
        if not request.brand and not request.model and not request.year and not request.mileage:
            raise HTTPException(status_code=400, detail="Missing required car information")
            
        result = await used_car_checker.check_used_car(
            brand=request.brand,
            model=request.model,
            year=request.year,
            mileage=request.mileage,
            price=request.price if hasattr(request, 'price') else 0,
            description=request.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Used car check failed: {str(e)}")

@app.post("/api/check-used-car/vin")
async def check_used_car_by_vin(request: UsedCarCheckRequest):
    """
    Check if a used car is worth buying based on its VIN.
    """
    try:
        if not request.vin:
            raise HTTPException(status_code=400, detail="VIN is required")
            
        # In a real system, we'd use the VIN to lookup the car details
        # For now, simulate a lookup by returning placeholder data
        
        # Extract some basic info from VIN (demonstration only - not real VIN decoding)
        # VIN format example: WDB2030461A123456
        # First 3 chars typically represent manufacturer
        manufacturer_code = request.vin[:3] if len(request.vin) >= 3 else "UNK"
        year_char = request.vin[9] if len(request.vin) >= 10 else "0"
        
        # Simple mapping for demo purposes
        brand_mapping = {
            "WDB": "Mercedes-Benz",
            "WBA": "BMW",
            "WAU": "Audi",
            "WVW": "Volkswagen",
            "JTD": "Toyota",
            "1HG": "Honda",
            "JHM": "Honda",
        }
        
        # Very simplistic year mapping
        year_mapping = {
            "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014,
            "F": 2015, "G": 2016, "H": 2017, "J": 2018, "K": 2019,
            "L": 2020, "M": 2021, "N": 2022, "P": 2023, "R": 2024
        }
        
        # Get brand and estimated year
        brand = brand_mapping.get(manufacturer_code, "Unknown")
        year = year_mapping.get(year_char, 2020)  # Default to 2020 if unknown
        
        # Use a generic model for simplicity
        model = "Unknown Model"
        
        # For a real VIN decoder, we'd use a more sophisticated approach
        
        result = await used_car_checker.check_used_car(
            brand=brand,
            model=model,
            year=year,
            mileage=request.mileage if request.mileage else 100000,
            description=f"VIN: {request.vin}"
        )
        
        # Add VIN to the result
        result['car_info']['vin'] = request.vin
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"VIN check failed: {str(e)}")

@app.post("/api/local-diagnosis")
async def local_diagnosis(request: Request):
    """
    Process car diagnostics locally using AI.
    """
    try:
        body = await request.json()
        query_type = body.get("query_type", "")
        vehicle_info = body.get("vehicle_info", "")
        
        if query_type == "used_car_check":
            # In a real implementation, this would use DeepSeek API or another LLM
            # Extract car info from the vehicle_info if possible
            brand = None
            model = None
            year = None
            mileage = None
            
            # Simple regex extractions
            if "Make:" in vehicle_info:
                brand_match = re.search(r"Make:\s*(\w+)", vehicle_info)
                if brand_match:
                    brand = brand_match.group(1)
            
            if "Model:" in vehicle_info:
                model_match = re.search(r"Model:\s*([^\n]+)", vehicle_info)
                if model_match:
                    model = model_match.group(1).strip()
            
            if "Year:" in vehicle_info:
                year_match = re.search(r"Year:\s*(\d{4})", vehicle_info)
                if year_match:
                    year = int(year_match.group(1))
            
            if "Mileage:" in vehicle_info:
                mileage_match = re.search(r"Mileage:\s*(\d+)", vehicle_info)
                if mileage_match:
                    mileage = int(mileage_match.group(1))
            
            # Generate a response that simulates market research and Eastern European factors
            current_year = datetime.now().year
            age = current_year - year if year else 5
            
            # Adjust scores based on Eastern European market preferences
            reliability_score = 8 - (0.5 * age if age <= 10 else 5 + (0.3 * (age - 10)))
            reliability_score = max(3, min(10, reliability_score))  # Cap between 3-10
            
            # Brand-specific adjustments (simplified)
            brand_reliability = {
                "Toyota": 1.5,
                "Honda": 1.2,
                "Volkswagen": 0.8,
                "BMW": 0.7,
                "Mercedes-Benz": 0.7,
                "Audi": 0.7,
                "Ford": 0.5,
                "Hyundai": 0.8,
                "Kia": 0.8,
                "Skoda": 1.0,
                "Renault": 0.6,
                "Dacia": 0.9,
            }
            
            if brand in brand_reliability:
                reliability_score *= brand_reliability[brand]
                
            # Clamp final score
            reliability_score = max(3, min(10, reliability_score))
            final_score = int(reliability_score)
            
            # Generate common issues based on brand and age
            issues = []
            
            if age > 10:
                issues.append("Older vehicle - inspect for rust, especially in wheel arches and underbody")
                issues.append("Check all rubber components (hoses, belts) for age deterioration")
            
            if mileage and mileage > 150000:
                issues.append("High mileage - check engine compression and transmission shifting")
                
            if brand == "Volkswagen" or brand == "Skoda" or brand == "Audi":
                if 2008 <= year <= 2013:
                    issues.append("TSI engine timing chain issues common in this generation - verify if replaced")
                if 2004 <= year <= 2009:
                    issues.append("DSG transmission mechatronics unit may need inspection")
                    
            if brand == "BMW":
                if 2005 <= year <= 2013:
                    issues.append("N54/N55 engines - check for oil leaks and turbo wastegate rattle")
                    issues.append("Potential issues with VANOS system - listen for rattling on startup")
                    
            if brand == "Mercedes-Benz":
                if 2004 <= year <= 2010:
                    issues.append("Inspect for rust in rear wheel arches - common issue in Eastern Europe")
                if year > 2012:
                    issues.append("Check electronics and infotainment system functionality")
                    
            # Eastern European specific issues
            issues.append("Verify fuel quality compatibility - Eastern European fuel can vary in quality")
            issues.append("Check undercarriage for damage from poor road conditions")
            
            # Market value estimation based on Eastern European factors
            base_value = ((current_year - year) * 1000) # Simple age-based depreciation
            if brand in ["Volkswagen", "Skoda", "BMW", "Mercedes-Benz", "Audi"]:
                base_value *= 1.2  # Premium for German cars in Eastern Europe
            if model and "SUV" in model.upper() or any(suv in model.upper() for suv in ["X5", "Q7", "GLE"]):
                base_value *= 1.15  # SUV premium
                
            # Mileage adjustment
            if mileage:
                mileage_factor = 1 - (mileage / 300000)  # Simplified depreciation
                base_value *= max(0.6, mileage_factor)
                
            # Format market value
            market_value = f"€{int(base_value):,}"
            price_range = f"€{int(base_value * 0.9):,} - €{int(base_value * 1.1):,}"
            
            # Recommendation based on score
            recommendation = "RECOMMENDED" if final_score >= 7 else "PROCEED WITH CAUTION" if final_score >= 5 else "NOT RECOMMENDED"
            
            # Format response
            response = {
                "diagnosis": f"""
USED CAR EVALUATION - EASTERN EUROPEAN MARKET ANALYSIS

Based on the information provided:
{vehicle_info}

SUMMARY: This {brand or 'vehicle'} {model or ''} from {year or 'unknown year'} with {mileage or 'unknown'} km scores {final_score}/10 in our assessment. {
"It appears to be a good purchase option with expected reliability for its age and mileage." if final_score >= 7 else 
"Some caution is advised, but could be a reasonable purchase with proper inspection." if final_score >= 5 else
"Major concerns exist that make this a risky purchase. Consider alternatives."
}

ISSUES:
{chr(10).join(f"- {issue}" for issue in issues)}

RELIABILITY: {
"Excellent" if final_score >= 8 else
"Good" if final_score >= 6 else
"Average" if final_score >= 5 else
"Below Average" if final_score >= 4 else
"Poor"
} for Eastern European conditions. Common problems include:
- Check for service records, especially timing belt/chain service
- Inspect for oil leaks around valve cover and oil pan
- Test all electronic features thoroughly
- Get a professional pre-purchase inspection

MARKET VALUE: 
Eastern European average market value: {market_value}
Expected price range: {price_range} (depending on condition and location)

RECOMMENDATION: {recommendation} {
"This vehicle presents good value and reliability for the Eastern European market." if final_score >= 7 else
"This vehicle needs careful inspection before purchase." if final_score >= 5 else
"Major concerns exist with this vehicle. Consider alternatives with better reliability."
}
"""
            }
            return response
            
        return {"error": "Unsupported query type"}
    except Exception as e:
        print(f"Local diagnosis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Local diagnosis failed: {str(e)}")

@app.get("/api/used-car/options")
async def get_used_car_options():
    """
    Get options for used car check form (brands, models, fuel types, etc.)
    """
    try:
        # Expanded car data with focus on Eastern European market popularity
        car_brands = [
            "Audi", "BMW", "Chevrolet", "Citroen", "Dacia", "Fiat", "Ford", "Honda", "Hyundai", 
            "Kia", "Mazda", "Mercedes-Benz", "Mitsubishi", "Nissan", "Opel", "Peugeot", "Renault", 
            "Seat", "Skoda", "Suzuki", "Toyota", "Volkswagen", "Volvo"
        ]
        
        # Models for each brand with focus on common models in Eastern Europe
        car_models = {
            "Audi": ["A3", "A4", "A6", "Q3", "Q5", "Q7"],
            "BMW": ["1 Series", "3 Series", "5 Series", "X1", "X3", "X5"],
            "Chevrolet": ["Aveo", "Captiva", "Cruze", "Lacetti", "Spark"],
            "Citroen": ["C3", "C4", "C5", "Berlingo", "Jumper"],
            "Dacia": ["Duster", "Logan", "Sandero", "Lodgy", "Dokker"],
            "Fiat": ["500", "Panda", "Punto", "Tipo", "Doblo"],
            "Ford": ["Fiesta", "Focus", "Kuga", "Mondeo", "Transit"],
            "Honda": ["Civic", "Accord", "CR-V", "Jazz", "HR-V"],
            "Hyundai": ["i20", "i30", "Tucson", "Santa Fe", "Elantra"],
            "Kia": ["Ceed", "Sportage", "Rio", "Sorento", "Picanto"],
            "Mazda": ["2", "3", "6", "CX-3", "CX-5"],
            "Mercedes-Benz": ["A-Class", "C-Class", "E-Class", "GLC", "Sprinter"],
            "Mitsubishi": ["ASX", "Outlander", "Lancer", "Pajero", "L200"],
            "Nissan": ["Qashqai", "Juke", "X-Trail", "Micra", "Navara"],
            "Opel": ["Astra", "Corsa", "Insignia", "Mokka", "Zafira"],
            "Peugeot": ["208", "308", "3008", "508", "Partner"],
            "Renault": ["Clio", "Megane", "Captur", "Kadjar", "Trafic"],
            "Seat": ["Ibiza", "Leon", "Ateca", "Arona", "Alhambra"],
            "Skoda": ["Fabia", "Octavia", "Superb", "Kodiaq", "Karoq"],
            "Suzuki": ["Swift", "Vitara", "SX4", "Jimny", "Ignis"],
            "Toyota": ["Corolla", "Yaris", "RAV4", "Avensis", "Land Cruiser"],
            "Volkswagen": ["Golf", "Passat", "Polo", "Tiguan", "Transporter"],
            "Volvo": ["V40", "V60", "XC60", "XC90", "S60"]
        }
        
        # Comprehensive fuel types
        fuel_types = [
            "Gasoline", "Diesel", "Hybrid", "Plug-in Hybrid", "Electric", 
            "Liquefied Petroleum Gas (LPG)", "Compressed Natural Gas (CNG)", 
            "Ethanol (E85)", "Biodiesel"
        ]
        
        # All common transmission types
        transmission_types = [
            "Manual", "Automatic", "Semi-automatic", "CVT (Continuously Variable Transmission)",
            "Dual-clutch (DCT/DSG)", "AMT (Automated Manual Transmission)",
            "Tiptronic"
        ]
        
        # Eastern European specific market segments
        market_segments = [
            "Family Car", "City Car", "SUV/Crossover", "Executive", 
            "Budget", "Luxury", "Commercial", "Off-road"
        ]
        
        # Common Eastern European countries for region-specific data
        countries = [
            "Poland", "Czech Republic", "Hungary", "Romania", "Bulgaria", 
            "Slovakia", "Slovenia", "Croatia", "Serbia", "Ukraine"
        ]
        
        # Return comprehensive options
        return {
            "brands": car_brands,
            "models": car_models,
            "fuel_types": fuel_types,
            "transmission_types": transmission_types,
            "market_segments": market_segments,
            "countries": countries,
            "years": list(range(2000, datetime.now().year + 1))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching car options: {str(e)}")

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
