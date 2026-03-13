from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.models.room import RoomType, RoomStatus


class AmenityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    icon: Optional[str] = None


class AmenityResponse(AmenityBase):
    id: int

    class Config:
        from_attributes = True


class PackageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price_multiplier: float = Field(default=0, ge=0)


class PackageCreate(PackageBase):
    pass


class PackageResponse(PackageBase):
    id: int
    room_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    type: RoomType
    price: float = Field(..., gt=0)
    image: Optional[str] = None
    size: Optional[str] = None
    occupancy: Optional[str] = None
    description: Optional[str] = None
    featured: bool = False


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    type: Optional[RoomType] = None
    price: Optional[float] = Field(None, gt=0)
    image: Optional[str] = None
    size: Optional[str] = None
    occupancy: Optional[str] = None
    description: Optional[str] = None
    status: Optional[RoomStatus] = None
    featured: Optional[bool] = None


class RoomResponse(BaseModel):
    id: int
    name: str
    type: RoomType
    price: float
    image: Optional[str]
    size: Optional[str]
    occupancy: Optional[str]
    description: Optional[str]
    status: RoomStatus
    featured: bool
    created_at: datetime
    amenities: List[AmenityResponse] = []
    packages: List[PackageResponse] = []

    class Config:
        from_attributes = True


class RoomWithDetails(RoomResponse):
    reviews: List["ReviewResponse"] = []


from app.schemas.booking import ReviewResponse
RoomWithDetails.model_rebuild()