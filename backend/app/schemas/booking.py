from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional
from app.models.booking import BookingStatus


class PackageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price_multiplier: float = Field(default=0, ge=0)


class BookingBase(BaseModel):
    room_id: int
    check_in: datetime
    check_out: datetime
    package_id: Optional[int] = None

    @validator('check_out')
    def check_out_after_check_in(cls, v, values):
        if 'check_in' in values and v <= values['check_in']:
            raise ValueError('check_out must be after check_in')
        return v


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: str
    user_id: int
    room_name: str
    room_image: Optional[str]
    package_name: Optional[str]
    check_in: datetime
    check_out: datetime
    total_price: float
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    room_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True