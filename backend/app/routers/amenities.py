from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.models.review import Review
from app.models.booking import Package
from app.schemas.room import (
    AmenityResponse, PackageResponse, PackageCreate,
    RoomCreate, RoomUpdate, RoomResponse, RoomWithDetails
)
from app.schemas.booking import ReviewCreate, ReviewUpdate
from app.dependencies import get_current_user, get_current_staff
from app.utils.helpers import generate_booking_id

router = APIRouter(prefix="/amenities", tags=["amenities"])


@router.get("", response_model=List[AmenityResponse])
def list_amenities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    from app.models.room import Amenity
    amenities = db.query(Amenity).offset(skip).limit(limit).all()
    return amenities


@router.post("", response_model=AmenityResponse, status_code=status.HTTP_201_CREATED)
def create_amenity(
    amenity_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    from app.models.room import Amenity
    if db.query(Amenity).filter(Amenity.name == amenity_data["name"]).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amenity already exists"
        )
    amenity = Amenity(**amenity_data)
    db.add(amenity)
    db.commit()
    db.refresh(amenity)
    return amenity


@router.delete("/{amenity_id}")
def delete_amenity(
    amenity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    from app.models.room import Amenity
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found"
        )
    db.delete(amenity)
    db.commit()
    return {"message": "Amenity deleted successfully"}