import logging
import logging.handlers
import os
import sys
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Create logs directory if it doesn't exist
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(log_dir, exist_ok=True)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Clear existing handlers
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create file handler for general logs
log_file = os.path.join(log_dir, 'garagefy.log')
file_handler = logging.handlers.RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)

# Create file handler for request logs
request_log_file = os.path.join(log_dir, 'requests.log')
request_handler = logging.handlers.RotatingFileHandler(
    request_log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
request_handler.setLevel(logging.INFO)

# Create formatters
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
detailed_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'

console_formatter = logging.Formatter(log_format)
file_formatter = logging.Formatter(detailed_format)
request_formatter = logging.Formatter('%(asctime)s - %(message)s')

# Set formatters
console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)
request_handler.setFormatter(request_formatter)

# Add handlers to root logger
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

# Create a separate logger for requests
request_logger = logging.getLogger('request_logger')
request_logger.setLevel(logging.INFO)
request_logger.addHandler(request_handler)
request_logger.propagate = False

# Create module logger
logger = logging.getLogger(__name__)
logger.info("Starting Garagefy API server")
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas
from .core.database import get_db, engine
from .api.endpoints import service_requests, quotes  # Import routers
from pydantic import BaseModel
from dotenv import load_dotenv

# Logger already configured above

# Import Base from core.database where it's now defined
from .core.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Garagefy API",
    description="API for connecting car owners with specialized body shops in Luxembourg",
    version="1.0.0"
)

# Import scheduler service
from app.services.scheduler_service import scheduler_service

# Startup event - start the scheduler
@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    try:
        logger.info("Application startup - initializing scheduler")
        scheduler_service.start()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}", exc_info=True)

# Shutdown event - stop the scheduler
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up background tasks on application shutdown"""
    try:
        logger.info("Application shutdown - stopping scheduler")
        scheduler_service.stop()
        logger.info("Scheduler stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {str(e)}", exc_info=True)

# Configure CORS
origins = [
    # Production domains
    "https://garagefy.app",
    "https://www.garagefy.app",
    # Local development
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3002",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
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

# Import the endpoint routers
from app.api.endpoints import garage_responses, fix_it

# Include the routers
app.include_router(
    service_requests.router,
    prefix="/api",
    tags=["service-requests"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    quotes.router,
    prefix="/api",
    tags=["quotes"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    garage_responses.router,
    prefix="/api",
    tags=["garage-responses"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)

app.include_router(
    fix_it.router,
    prefix="/api",
    tags=["fix-it"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


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
    return {"message": "Welcome to Garagefy API - Body Shop Quote Comparison Platform"}

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint with service status"""
    from app.services.scheduler_service import scheduler_service
    
    health_status = {
        "status": "healthy",
        "scheduler": scheduler_service.get_status(),
        "timestamp": datetime.now().isoformat()
    }
    
    return health_status

@app.post("/api/debug/check-emails")
async def debug_check_emails() -> Dict[str, Any]:
    """Manually trigger email check for debugging"""
    from app.services.email_monitor_service import email_monitor_service
    
    logger.info("🔍 Manual email check triggered via debug endpoint")
    
    try:
        result = await email_monitor_service.check_and_process_new_emails(mark_as_read=False)
        logger.info(f"📊 Email check result: {result}")
        return {
            "success": True,
            "message": "Email check completed",
            "result": result
        }
    except Exception as e:
        logger.error(f"❌ Error in debug email check: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }
