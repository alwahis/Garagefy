from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from datetime import datetime
import logging

from ...services.baserow_service import baserow_service as airtable_service
from ...models.garage_response import GarageResponse

router = APIRouter(prefix="/api/garage-responses", tags=["garage-responses"])
logger = logging.getLogger(__name__)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def record_garage_response(response: GarageResponse) -> Dict[str, Any]:
    """
    Record a garage's response to a service request
    
    - **garage_name**: Name of the garage
    - **garage_email**: Email of the garage
    - **request_id**: The service request ID this response is for
    - **vin**: Vehicle Identification Number (required for matching to customer request)
    - **quote_amount**: The quoted amount (optional)
    - **notes**: Additional notes from the garage (optional)
    - **status**: Status of the response (e.g., 'quoted', 'declined')
    """
    try:
        # Prepare the response data
        response_data = {
            'garage_name': response.garage_name,
            'garage_email': response.garage_email,
            'request_id': response.request_id,
            'vin': response.vin,
            'quote_amount': response.quote_amount,
            'notes': response.notes,
            'status': response.status or 'received',
            'response_date': datetime.utcnow().isoformat()
        }
        
        # Record the response in Baserow
        result = airtable_service.record_garage_response(response_data)
        
        if not result.get('success'):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Failed to record garage response')
            )
            
        return {
            'success': True,
            'message': 'Garage response recorded successfully',
            'record_id': result.get('record', {}).get('id')
        }
        
    except HTTPException as he:
        raise
    except Exception as e:
        logger.error(f"Error recording garage response: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while recording the garage response: {str(e)}"
        )

@router.get("/request/{request_id}", status_code=status.HTTP_200_OK)
async def get_garage_responses(request_id: str) -> Dict[str, Any]:
    """
    Get all garage responses for a specific service request
    """
    try:
        # Get responses from Baserow
        responses = airtable_service.get_records('Recevied email')
        
        return {
            'success': True,
            'count': len(responses),
            'responses': responses
        }
        
    except Exception as e:
        logger.error(f"Error fetching garage responses: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching garage responses: {str(e)}"
        )
