from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List
from enum import Enum
from datetime import datetime

class ResponseStatus(str, Enum):
    RECEIVED = "received"
    QUOTED = "quoted"
    DECLINED = "declined"
    ACCEPTED = "accepted"
    COMPLETED = "completed"

class GarageResponseBase(BaseModel):
    """Base model for garage responses"""
    garage_name: str = Field(..., description="Name of the garage")
    garage_email: str = Field(..., description="Email of the garage")
    request_id: str = Field(..., description="The service request ID this response is for")
    quote_amount: Optional[float] = Field(None, description="The quoted amount (optional)")
    notes: Optional[str] = Field(None, description="Additional notes from the garage")
    status: ResponseStatus = Field(ResponseStatus.RECEIVED, description="Status of the response")

class GarageResponseCreate(GarageResponseBase):
    """Model for creating a new garage response"""
    pass

class GarageResponseUpdate(BaseModel):
    """Model for updating an existing garage response"""
    quote_amount: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[ResponseStatus] = None

class GarageResponse(GarageResponseBase):
    """Complete garage response model with system fields"""
    id: str = Field(..., description="Unique identifier for the response")
    response_date: datetime = Field(..., description="When the response was recorded")
    created_at: datetime = Field(..., description="When the record was created")
    updated_at: datetime = Field(..., description="When the record was last updated")

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
