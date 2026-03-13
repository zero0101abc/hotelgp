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

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=List[RoomResponse])
def list_rooms(
    type: Optional[str] = Query(None),
    status: Optional[str] = Query("available"),
    featured: Optional[bool] = Query(None),
    children: Optional[int] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    from app.models.room import Room, RoomStatus, RoomType, room_amenities, Amenity
    query = db.query(Room)
    
    if type:
        try:
            room_type = RoomType(type)
            query = query.filter(Room.type == room_type)
        except ValueError:
            pass
    
    if status:
        try:
            room_status = RoomStatus(status)
            query = query.filter(Room.status == room_status)
        except ValueError:
            pass
    
    if featured is not None:
        query = query.filter(Room.featured == featured)
    
    # If children > 0, filter to Family rooms only
    if children is not None and children > 0:
        query = query.filter(Room.type == RoomType.Family)
    
    rooms = query.offset(skip).limit(limit).all()
    return rooms


@router.get("/{room_id}", response_model=RoomWithDetails)
def get_room(room_id: int, db: Session = Depends(get_db)):
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return room


@router.get("/{room_id}/packages", response_model=List[PackageResponse])
def get_room_packages(room_id: int, db: Session = Depends(get_db)):
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return room.packages


@router.post("/{room_id}/packages", response_model=PackageResponse, status_code=status.HTTP_201_CREATED)
def add_package_to_room(
    room_id: int,
    package_data: PackageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    package = Package(
        room_id=room_id,
        **package_data.model_dump()
    )
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


@router.delete("/{room_id}/packages/{package_id}")
def remove_package_from_room(
    room_id: int,
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_staff)
):
    from app.models.room import Room
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.room_id == room_id
    ).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    db.delete(package)
    db.commit()
    return {"message": "Package removed successfully"}


@router.get("/{room_id}/reviews", response_model=List[dict])
def get_room_reviews(room_id: int, db: Session = Depends(get_db)):
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    reviews = db.query(Review).filter(Review.room_id == room_id).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "user_name": r.user.name,
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at
        }
        for r in reviews
    ]


@router.post("/{room_id}/reviews", status_code=status.HTTP_201_CREATED)
def create_review(
    room_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from app.models.room import Room
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    review = Review(
        user_id=current_user.id,
        room_id=room_id,
        **review_data.model_dump()
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}