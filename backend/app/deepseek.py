"""
DeepSeek API integration for car diagnostics
"""
import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Corrected URL
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

def call_deepseek_api(prompt):
    """
    Call DeepSeek API with the given prompt
    """
    if not DEEPSEEK_API_KEY:
        logger.error("DeepSeek API key not found")
        raise ValueError("DeepSeek API key not configured")
        
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",  # Using the chat model
        "messages": [
            {
                "role": "system",
                "content": "You are an expert automotive diagnostic system with access to service manuals for all major car brands."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500  # Reduced max tokens
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=60)  # Increased timeout to 60 seconds
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        logger.error("DeepSeek API request timed out")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"DeepSeek API error: {str(e)}")
        raise


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

from .services.ai_service import car_diagnostic_ai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DiagnosisRequest(BaseModel):
    car_brand: str
    model: str
    year: int
    problem_description: str

@app.post("/api/diagnose")
async def diagnose_car(request: DiagnosisRequest):
    """
    Endpoint to get car diagnosis based on symptoms
    """
    try:
        logger.info(f"Received diagnosis request for {request.car_brand} {request.model} {request.year}")
        
        if not request.problem_description:
            raise HTTPException(status_code=400, detail="Problem description is required")
            
        diagnosis = await car_diagnostic_ai.get_diagnosis(
            car_brand=request.car_brand,
            problem_description=request.problem_description
        )
        
        if not diagnosis or not isinstance(diagnosis, dict) or 'diagnosis' not in diagnosis:
            logger.error("Invalid diagnosis response format")
            raise HTTPException(status_code=500, detail="Failed to generate valid diagnosis")
            
        return diagnosis
        
    except Exception as e:
        logger.error(f"Error in diagnose_car: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
