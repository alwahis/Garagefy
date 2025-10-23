from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta

from ...models.quote import Quote, QuoteCreate, QuoteUpdate, QuoteSummary
from ...services.quote_service import quote_service

router = APIRouter(prefix="/api/quotes", tags=["quotes"])

@router.post("/", response_model=Quote, status_code=status.HTTP_201_CREATED)
async def create_quote(quote: QuoteCreate):
    """
    Create a new quote for a service request
    
    - **request_id**: ID of the service request
    - **customer_id**: ID of the customer
    - **customer_name**: Name of the customer
    - **customer_email**: Email of the customer
    - **garage_id**: ID of the garage
    - **garage_name**: Name of the garage
    - **amount**: Quote amount in euros
    - **notes**: Additional notes from the garage (optional)
    - **valid_until**: Date until the quote is valid (YYYY-MM-DD)
    """
    try:
        return await quote_service.create_quote(quote)
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating quote: {str(e)}"
        )

@router.get("/{quote_id}", response_model=Quote)
async def get_quote(quote_id: str):
    """
    Get a quote by ID
    """
    quote = quote_service.get_quote(quote_id)
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with ID {quote_id} not found"
        )
    return quote

@router.get("/request/{request_id}", response_model=List[Quote])
async def get_quotes_by_request(request_id: str):
    """
    Get all quotes for a service request
    """
    return quote_service.get_quotes_by_request(request_id)

@router.patch("/{quote_id}", response_model=Quote)
async def update_quote(quote_id: str, update_data: QuoteUpdate):
    """
    Update a quote
    
    - **status**: New status of the quote (optional)
    - **amount**: Updated quote amount (optional)
    - **notes**: Updated notes (optional)
    - **valid_until**: New valid until date (YYYY-MM-DD, optional)
    """
    updated_quote = quote_service.update_quote(quote_id, update_data)
    if not updated_quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quote with ID {quote_id} not found"
        )
    return updated_quote

@router.get("/summary/{request_id}", response_model=QuoteSummary)
async def get_quote_summary(request_id: str):
    """
    Get a summary of all quotes for a service request
    """
    quotes = quote_service.get_quotes_by_request(request_id)
    if not quotes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No quotes found for request {request_id}"
        )
    
    # Get customer details from the first quote
    customer_name = quotes[0].customer_name if quotes else ""
    customer_email = quotes[0].customer_email if quotes else ""
    
    return QuoteSummary(
        request_id=request_id,
        customer_name=customer_name,
        customer_email=customer_email,
        quotes=quotes
    )

@router.post("/{request_id}/send-summary", status_code=status.HTTP_200_OK)
async def send_quote_summary(request_id: str):
    """
    Manually trigger sending the quote summary for a request
    """
    try:
        success = await quote_service._check_and_send_quote_summary(request_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not send quote summary. Not all conditions are met."
            )
        return {"message": "Quote summary sent successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending quote summary: {str(e)}"
        )
