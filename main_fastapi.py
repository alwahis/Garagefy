from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from car_diagnostic import CarDiagnosticSystem
from car_database import car_database
from luxembourg_garages import LUXEMBOURG_GARAGES
from typing import Optional, List, Dict
import uvicorn

app = FastAPI(title="Garagefy", description="Luxembourg Garage Finder and Car Diagnostic System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize diagnostic system
diagnostic_system = CarDiagnosticSystem()

class DiagnosticRequest(BaseModel):
    symptoms: List[str]
    car_brand: str
    car_model: str
    year: int

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/diagnose", response_class=HTMLResponse)
async def diagnose_page(request: Request):
    try:
        brands = list(car_database.keys())
        print(f"Available brands: {brands}")  # Debug print
        return templates.TemplateResponse(
            "diagnose.html", 
            {
                "request": request,
                "brands": brands,
                "models": [],
                "years": [],
                "car_brand": None,
                "car_model": None,
                "year": None,
                "symptoms": None
            }
        )
    except Exception as e:
        print(f"Error in diagnose_page: {str(e)}")  # Debug print
        return templates.TemplateResponse(
            "diagnose.html",
            {
                "request": request,
                "error": str(e),
                "brands": [],
                "models": [],
                "years": [],
                "car_brand": None,
                "car_model": None,
                "year": None,
                "symptoms": None
            }
        )

@app.post("/diagnose", response_class=HTMLResponse)
async def diagnose_submit(
    request: Request,
    symptoms: str = Form(...),
    car_brand: str = Form(...),
    car_model: str = Form(...),
    year: int = Form(...)
):
    print(f"Received diagnosis request: brand={car_brand}, model={car_model}, year={year}, symptoms={symptoms}")
    try:
        # Get available models for the selected brand
        models = list(car_database[car_brand].keys()) if car_brand in car_database else []
        print(f"Available models: {models}")
        
        # Get available years for the selected model
        years = car_database[car_brand][car_model] if car_brand in car_database and car_model in car_database[car_brand] else []
        print(f"Available years: {years}")
        
        # Get diagnosis
        result = diagnostic_system.diagnose(
            symptoms=symptoms,
            car_brand=car_brand,
            car_model=car_model,
            year=year
        )
        print(f"Diagnosis result: {result}")

        # Return the diagnosis result along with form data
        return templates.TemplateResponse(
            "diagnose.html",
            {
                "request": request,
                "brands": list(car_database.keys()),
                "models": models,
                "years": years,
                "car_brand": car_brand,
                "car_model": car_model,
                "year": year,
                "symptoms": symptoms,
                "diagnosis": {
                    "diagnosis": result,
                    "severity": "medium",  # This could be determined by analyzing the response
                    "category": "Engine",  # This could be determined by analyzing the response
                }
            }
        )
    except Exception as e:
        print(f"Error in diagnose_submit: {str(e)}")
        return templates.TemplateResponse(
            "diagnose.html",
            {
                "request": request,
                "error": f"Error during diagnosis: {str(e)}",
                "brands": list(car_database.keys()),
                "models": models if 'models' in locals() else [],
                "years": years if 'years' in locals() else [],
                "car_brand": car_brand,
                "car_model": car_model,
                "year": year,
                "symptoms": symptoms
            }
        )

@app.get("/garages", response_class=HTMLResponse)
async def garages_page(request: Request):
    return templates.TemplateResponse(
        "garages.html", 
        {
            "request": request,
            "garages": LUXEMBOURG_GARAGES
        }
    )

@app.get("/api/garages")
async def get_garages():
    return {"garages": LUXEMBOURG_GARAGES}

@app.get("/api/brands")
async def get_brands():
    return list(car_database.keys())

@app.get("/api/models/{brand}")
async def get_models(brand: str):
    if brand not in car_database:
        raise HTTPException(status_code=404, detail="Brand not found")
    return list(car_database[brand].keys())

@app.get("/api/years/{brand}/{model}")
async def get_years(brand: str, model: str):
    if brand not in car_database:
        raise HTTPException(status_code=404, detail="Brand not found")
    if model not in car_database[brand]:
        raise HTTPException(status_code=404, detail="Model not found")
    return car_database[brand][model]

@app.get("/api/services")
async def get_available_services():
    all_services = set()
    for garage in LUXEMBOURG_GARAGES:
        services = [s.strip() for s in garage['Services'].split(',')]
        all_services.update(services)
    return list(all_services)

if __name__ == "__main__":
    uvicorn.run("main_fastapi:app", host="127.0.0.1", port=8080, reload=True)
