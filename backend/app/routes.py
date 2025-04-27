from fastapi import APIRouter, HTTPException
from typing import List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI router
router = APIRouter()

@router.get("/car-data")
async def get_car_data():
    """Get available car brands and models"""
    try:
        return {
            'Toyota': {'models': ['Camry', 'Corolla', 'RAV4']},
            'Honda': {'models': ['Civic', 'Accord', 'CR-V']},
            'Ford': {'models': ['F-150', 'Mustang', 'Explorer']}
        }
    except Exception as e:
        logger.error(f"Error fetching car data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/garages/nearby")
async def get_nearby_garages():
    """Get nearby garages with static test data"""
    try:
        return [
            {"id": 1, "name": "Test Garage", "services": ["oil change"]},
            {"id": 2, "name": "Quick Fix", "services": ["tire repair"]}
        ]
    except Exception as e:
        logger.error(f"Error fetching garages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch garages")


