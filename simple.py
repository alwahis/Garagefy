from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from car_diagnostic import CarDiagnosticSystem
from data import CAR_BRANDS
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

diagnostic_system = None  # Initialize later to avoid slow startup

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/diagnose", response_class=HTMLResponse)
async def diagnose_page(request: Request):
    return templates.TemplateResponse("diagnose.html", {"request": request})

@app.get("/test")
async def test():
    return {"message": "API is working"}

@app.get("/api/brands")
async def get_brands():
    brands = list(CAR_BRANDS.keys())
    print(f"Returning brands: {brands}")  # Debug print
    return JSONResponse(content=brands)

@app.get("/api/models/{brand}")
async def get_models(brand: str):
    if brand not in CAR_BRANDS:
        raise HTTPException(status_code=404, detail="Brand not found")
    return JSONResponse(content=list(CAR_BRANDS[brand].keys()))

@app.get("/api/years/{brand}/{model}")
async def get_years(brand: str, model: str):
    if brand not in CAR_BRANDS or model not in CAR_BRANDS[brand]:
        raise HTTPException(status_code=404, detail="Brand or model not found")
    return JSONResponse(content=CAR_BRANDS[brand][model])

@app.post("/api/diagnose")
async def diagnose_car(request: Request):
    global diagnostic_system
    if diagnostic_system is None:
        diagnostic_system = CarDiagnosticSystem()
        
    try:
        data = await request.json()
        result = diagnostic_system.diagnose_issue(
            symptoms=data['symptoms'],
            car_brand=data['car_brand'],
            car_model=data['car_model'],
            year=data['year']
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
