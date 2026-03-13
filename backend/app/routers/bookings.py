from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from app.database import get_db
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.dependencies import get_current_user, get_current_staff
from app.utils.helpers import generate_booking_id

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=List[BookingResponse])
def list_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    
    result = []
    for booking in bookings:
        result.append({
            "id": generate_booking_id(),
            "user_id": booking.user_id,
            "room_name": booking.room.name if booking.room else "Unknown",
            "room_image": booking.room.image if booking.room else None,
            "package_name": booking.package.name if booking.package else "Room Only",
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "total_price": booking.total_price,
            "status": booking.status,
            "created_at": booking.created_at
        })
    return result


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not booking_data.room_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="room_id is required"
        )
    
    room = db.query(Room).filter(Room.id == booking_data.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    if room.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available for booking"
        )
    
    package = None
    price_multiplier = 0
    if booking_data.package_id:
        from app.models.booking import Package
        package = db.query(Package).filter(Package.id == booking_data.package_id).first()
        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Package not found"
            )
        price_multiplier = package.price_multiplier
    
    nights = (booking_data.check_out - booking_data.check_in).days
    if nights <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date"
        )
    
    total_price = room.price * nights * (1 + price_multiplier)
    
    booking = Booking(
        user_id=current_user.id,
        room_id=booking_data.room_id,
        package_id=booking_data.package_id,
        check_in=booking_data.check_in,
        check_out=booking_data.check_out,
        total_price=total_price,
        status=BookingStatus.confirmed
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    return {
        "id": generate_booking_id(),
        "user_id": booking.user_id,
        "room_name": room.name,
        "room_image": room.image,
        "package_name": package.name if package else "Room Only",
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "total_price": booking.total_price,
        "status": booking.status,
        "created_at": booking.created_at
    }


@router.post("/{booking_id}/cancel")
def cancel_booking(
    booking_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.user_id == current_user.id,
        Booking.id == int(booking_id.split("-")[1]) if "-" in booking_id else int(booking_id)
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.status == BookingStatus.cancelled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )
    
    booking.status = BookingStatus.cancelled
    db.commit()
    return {"message": "Booking cancelled successfully"}


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: str,
    booking_update: BookingUpdate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == int(booking_id.split("-")[1]) if "-" in booking_id else int(booking_id)).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking_update.status:
        booking.status = booking_update.status
    
    db.commit()
    db.refresh(booking)
    
    return {
        "id": generate_booking_id(),
        "user_id": booking.user_id,
        "room_name": booking.room.name if booking.room else "Unknown",
        "room_image": booking.room.image if booking.room else None,
        "package_name": booking.package.name if booking.package else "Room Only",
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "total_price": booking.total_price,
        "status": booking.status,
        "created_at": booking.created_at
    }


@router.get("/all")
def list_all_bookings(
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get all bookings (staff/admin only)"""
    bookings = db.query(Booking).order_by(Booking.created_at.desc()).all()
    
    result = []
    for booking in bookings:
        result.append({
            "id": f"BK-{booking.id}",
            "user_id": booking.user_id,
            "customer_name": booking.user.name if booking.user else "Unknown",
            "customer_email": booking.user.email if booking.user else "Unknown",
            "room_name": booking.room.name if booking.room else "Unknown",
            "room_image": booking.room.image if booking.room else None,
            "package_name": booking.package.name if booking.package else "Room Only",
            "check_in": booking.check_in.isoformat() if booking.check_in else None,
            "check_out": booking.check_out.isoformat() if booking.check_out else None,
            "total_price": booking.total_price,
            "status": booking.status.value if booking.status else "confirmed",
            "created_at": booking.created_at.isoformat() if booking.created_at else None
        })
    return result