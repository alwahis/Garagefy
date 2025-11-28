import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status

from ..models.quote import Quote, QuoteCreate, QuoteUpdate, QuoteSummary, QuoteStatus
from .baserow_service import baserow_service as airtable_service

logger = logging.getLogger(__name__)

class QuoteService:
    """Service for handling quote-related operations"""
    
    QUOTE_TABLE = "Quotes"
    SERVICE_REQUESTS_TABLE = "Service Requests"
    
    def __init__(self):
        self.airtable = airtable_service
    
    async def create_quote(self, quote: QuoteCreate) -> Quote:
        """Create a new quote"""
        try:
            # Create quote record
            quote_data = quote.dict()
            quote_data['created_at'] = datetime.utcnow().isoformat()
            quote_data['updated_at'] = datetime.utcnow().isoformat()
            
            # Save to Baserow via the Airtable-compatible wrapper
            record = self.airtable.create_record(self.QUOTE_TABLE, quote_data)
            fields = record.get('fields', {}) or {}
            # Expose the Baserow row ID as the quote ID in API responses
            fields['id'] = str(record.get('id')) if record.get('id') is not None else fields.get('id')
            
            # Update service request with new quote count
            self._update_service_request_quote_count(quote.request_id)
            
            # Check if we should send quote summary
            await self._check_and_send_quote_summary(quote.request_id)
            
            return Quote(**fields)
            
        except Exception as e:
            logger.error(f"Error creating quote: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create quote: {str(e)}"
            )
    
    def get_quote(self, quote_id: str) -> Optional[Quote]:
        """Get a quote by ID"""
        try:
            record = self.airtable.get_record(self.QUOTE_TABLE, int(quote_id))
            if not record:
                return None
            fields = record.get('fields', {}) or {}
            fields['id'] = str(record.get('id')) if record.get('id') is not None else fields.get('id')
            return Quote(**fields)
        except Exception as e:
            logger.error(f"Error getting quote {quote_id}: {str(e)}")
            return None
    
    def get_quotes_by_request(self, request_id: str) -> List[Quote]:
        """Get all quotes for a service request"""
        try:
            formula = f"{{Request ID}} = '{request_id}'"
            records = self.airtable.get_records(self.QUOTE_TABLE, formula=formula)
            quotes: List[Quote] = []
            for record in records:
                fields = record.get('fields', {}) or {}
                fields['id'] = str(record.get('id')) if record.get('id') is not None else fields.get('id')
                quotes.append(Quote(**fields))
            return quotes
        except Exception as e:
            logger.error(f"Error getting quotes for request {request_id}: {str(e)}")
            return []
    
    def update_quote(self, quote_id: str, update_data: QuoteUpdate) -> Optional[Quote]:
        """Update an existing quote"""
        try:
            # Get existing quote
            existing = self.get_quote(quote_id)
            if not existing:
                return None
                
            # Prepare update data
            update_dict = update_data.dict(exclude_unset=True)
            update_dict['updated_at'] = datetime.utcnow().isoformat()
            
            # Update in Baserow via the Airtable-compatible wrapper
            updated = self.airtable.update_record(
                self.QUOTE_TABLE,
                int(quote_id),
                update_dict
            )

            if not updated or not updated.get('fields'):
                return None
                
            # If status changed to accepted/rejected, check for summary
            if 'status' in update_dict and update_dict['status'] in [QuoteStatus.ACCEPTED, QuoteStatus.REJECTED]:
                self._check_and_send_quote_summary(existing.request_id)

            fields = updated.get('fields', {}) or {}
            fields['id'] = str(updated.get('id')) if updated.get('id') is not None else fields.get('id')
            return Quote(**fields)
            
        except Exception as e:
            logger.error(f"Error updating quote {quote_id}: {str(e)}")
            return None
    
    def _update_service_request_quote_count(self, request_id: str) -> None:
        """Update the quote count for a service request"""
        try:
            # Get current count of quotes for this request
            quotes = self.get_quotes_by_request(request_id)
            quote_count = len(quotes)
            
            # Update the service request
            self.airtable.update_record(
                self.SERVICE_REQUESTS_TABLE,
                request_id,
                {"Quote Count": quote_count}
            )
            
        except Exception as e:
            logger.error(f"Error updating quote count for request {request_id}: {str(e)}")
    
    async def _check_and_send_quote_summary(self, request_id: str) -> bool:
        """Check if we should send a quote summary and send it if needed"""
        try:
            # Get the service request
            request_record = self.airtable.get_record(self.SERVICE_REQUESTS_TABLE, request_id)
            if not request_record:
                logger.warning(f"Service request {request_id} not found")
                return False
                
            request_data = request_record['fields']
            
            # Get all quotes for this request
            quotes = self.get_quotes_by_request(request_id)
            
            # Check if we should send the summary
            should_send = False
            
            # Condition 1: All notified garages have responded
            notified_garages = request_data.get('Notified Garages Count', 0)
            if notified_garages > 0 and len(quotes) >= notified_garages:
                should_send = True
                logger.info(f"All {notified_garages} garages have responded")
            
            # Condition 2: 24 hours have passed since the first quote
            if quotes:
                first_quote = min(quotes, key=lambda q: q.created_at)
                time_since_first_quote = datetime.utcnow() - first_quote.created_at
                if time_since_first_quote >= timedelta(hours=24):
                    should_send = True
                    logger.info(f"24 hours have passed since first quote")
            
            if should_send:
                # Create and send quote summary
                summary = QuoteSummary(
                    request_id=request_id,
                    customer_name=request_data.get('Customer Name', ''),
                    customer_email=request_data.get('Customer Email', ''),
                    quotes=quotes
                )
                
                # Here you would typically send an email with the summary
                # For now, we'll just log it
                logger.info(f"Sending quote summary for request {request_id} to {summary.customer_email}")
                
                # Mark the request as having received quotes
                self.airtable.update_record(
                    self.SERVICE_REQUESTS_TABLE,
                    request_id,
                    {
                        "Status": "Quotes Received",
                        "Quote Summary Sent": True,
                        "Quote Summary Sent At": datetime.utcnow().isoformat()
                    }
                )
                
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error checking/sending quote summary for request {request_id}: {str(e)}")
            return False

# Singleton instance
quote_service = QuoteService()
