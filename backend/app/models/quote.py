from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

class QuoteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class QuoteBase(BaseModel):
    """Base model for quote data validation"""
    request_id: str = Field(..., description="ID of the service request")
    customer_id: str = Field(..., description="ID of the customer")
    customer_name: str = Field(..., description="Name of the customer")
    customer_email: str = Field(..., description="Email of the customer")
    garage_id: str = Field(..., description="ID of the garage")
    garage_name: str = Field(..., description="Name of the garage")
    amount: float = Field(..., gt=0, description="Quote amount in euros")
    notes: Optional[str] = Field(None, description="Additional notes from the garage")
    valid_until: str = Field(..., description="Date until the quote is valid (YYYY-MM-DD)")
    status: QuoteStatus = Field(default=QuoteStatus.PENDING, description="Current status of the quote")

    @validator('valid_until')
    def validate_date_format(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

class QuoteCreate(QuoteBase):
    """Model for creating a new quote"""
    pass

class QuoteUpdate(BaseModel):
    """Model for updating an existing quote"""
    status: Optional[QuoteStatus] = None
    amount: Optional[float] = None
    notes: Optional[str] = None
    valid_until: Optional[str] = None

    @validator('valid_until')
    def validate_date_format(cls, v):
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
                return v
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        return v

class Quote(QuoteBase):
    """Model for quote response"""
    id: str = Field(default_factory=lambda: f"quote_{uuid.uuid4().hex}", description="Unique identifier for the quote")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the quote was created")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When the quote was last updated")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "id": "quote_123",
                "request_id": "req_456",
                "customer_id": "cust_789",
                "customer_name": "John Doe",
                "customer_email": "john@example.com",
                "garage_id": "garage_101",
                "garage_name": "Best Auto Repair",
                "amount": 299.99,
                "notes": "This includes parts and labor",
                "valid_until": (datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d'),
                "status": "pending",
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
        }

class QuoteSummary(BaseModel):
    """Model for quote summary sent to customers"""
    request_id: str
    customer_name: str
    customer_email: str
    quotes: List[Quote]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_quotes: int = 0
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    average_amount: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.total_quotes = len(self.quotes)
        if self.quotes:
            amounts = [q.amount for q in self.quotes]
            self.min_amount = min(amounts)
            self.max_amount = max(amounts)
            self.average_amount = sum(amounts) / len(amounts)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "request_id": "req_456",
                "customer_name": "John Doe",
                "customer_email": "john@example.com",
                "quotes": [],
                "created_at": datetime.utcnow().isoformat(),
                "total_quotes": 0
            }
        }
