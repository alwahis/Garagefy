from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import Dict, Any
import logging
from ...services.email_monitor_service import email_monitor_service
from ...services.customer_response_service import customer_response_service
from ...services.scheduler_service import scheduler_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/fix-it/check-emails", response_model=Dict[str, Any])
async def check_emails(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Check inbox for new emails from garages and save to Airtable
    
    This endpoint triggers the email monitoring service to:
    1. Connect to info@garagefy.app inbox
    2. Fetch unread emails
    3. Extract quote information
    4. Analyze attachments with DeepSeek if present
    5. Save to 'Recevied email' table in Airtable
    """
    try:
        logger.info("Starting email check process")
        
        # Run in background to avoid timeout
        result = await email_monitor_service.check_and_process_new_emails(mark_as_read=True)
        
        if result.get('success'):
            logger.info(f"Email check completed: {result.get('emails_processed', 0)} emails processed")
            return {
                'success': True,
                'message': f"Processed {result.get('emails_processed', 0)} new emails",
                'details': result
            }
        else:
            logger.error(f"Email check failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Failed to check emails')
            )
            
    except Exception as e:
        logger.error(f"Error in check_emails endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking emails: {str(e)}"
        )

@router.post("/fix-it/send-customer-responses", response_model=Dict[str, Any])
async def send_customer_responses() -> Dict[str, Any]:
    """
    Check for customers ready to receive compiled quotes and send responses
    
    This endpoint triggers the customer response service to:
    1. Check all customers in Customer details table
    2. Identify customers who are ready (all quotes received OR 2 business days passed)
    3. Compile quotes from Received email table
    4. Get garage details from Fix it table
    5. Send email with quote table to customer
    """
    try:
        logger.info("Starting customer response process")
        
        result = await customer_response_service.check_and_send_customer_responses()
        
        if result.get('success'):
            logger.info(f"Customer response process completed: {result.get('responses_sent', 0)} responses sent")
            return {
                'success': True,
                'message': f"Sent {result.get('responses_sent', 0)} customer responses",
                'details': result
            }
        else:
            logger.error(f"Customer response process failed: {result.get('error', 'Unknown error')}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Failed to send customer responses')
            )
            
    except Exception as e:
        logger.error(f"Error in send_customer_responses endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending customer responses: {str(e)}"
        )

@router.get("/fix-it/status", response_model=Dict[str, Any])
async def get_fix_it_status() -> Dict[str, Any]:
    """Get the status of the Fix it service including scheduler status"""
    try:
        scheduler_status = scheduler_service.get_status()
        
        return {
            'success': True,
            'status': 'operational',
            'message': 'Fix it service is running',
            'scheduler': scheduler_status
        }
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
