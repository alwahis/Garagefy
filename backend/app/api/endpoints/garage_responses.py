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
        responses = airtable_service.get_records('Received Email')
        
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

@router.post("/test-create", status_code=status.HTTP_201_CREATED)
async def test_create_record() -> Dict[str, Any]:
    """
    Create a test record in the Received Email table
    """
    try:
        # Test email data
        test_email = {
            'from_email': 'test@garage.com',
            'subject': 'Test Quote Response - VIN: TEST1234567890123',
            'body': 'Dear Customer,\n\nWe can fix your car for EUR500.\n\nBest regards,\nTest Garage',
            'received_at': datetime.utcnow().isoformat(),
            'attachments': []
        }
        
        test_vin = 'TEST1234567890123'
        
        logger.info(f"Creating test record with VIN: {test_vin}")
        
        # Store the test email
        result = airtable_service.store_received_email(test_email, test_vin)
        
        if not result or not result.get('success'):
            error_msg = result.get('error', 'Unknown error') if result else 'No response'
            logger.error(f"Failed to create test record: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create test record: {error_msg}"
            )
        
        logger.info(f"Successfully created test record: {result.get('id')}")
        
        return {
            'success': True,
            'message': 'Test record created successfully',
            'record_id': result.get('id'),
            'vin': test_vin,
            'from_email': test_email['from_email']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating test record: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.post("/trigger-email-check", status_code=status.HTTP_200_OK)
async def trigger_email_check() -> Dict[str, Any]:
    """
    Manually trigger email check for testing
    """
    try:
        from ...services.email_monitor_service import email_monitor_service
        
        logger.info("Manually triggering email check...")
        
        # Trigger email check
        result = await email_monitor_service.check_and_process_new_emails(mark_as_read=False)
        
        return {
            'success': True,
            'message': 'Email check completed',
            'result': result
        }
        
    except Exception as e:
        logger.error(f"Error triggering email check: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
