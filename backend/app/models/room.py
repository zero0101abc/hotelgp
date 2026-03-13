from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class RoomType(str, enum.Enum):
    Luxury = "Luxury"
    Suite = "Suite"
    Business = "Business"
    Family = "Family"


class RoomStatus(str, enum.Enum):
    available = "available"
    occupied = "occupied"
    maintenance = "maintenance"


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    type = Column(Enum(RoomType), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(500), nullable=True)
    size = Column(String(50), nullable=True)
    occupancy = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(RoomStatus), default=RoomStatus.available)
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    amenities = relationship("Amenity", secondary="room_amenities", back_populates="rooms")
    packages = relationship("Package", back_populates="room", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="room")
    reviews = relationship("Review", back_populates="room")


room_amenities = Table(
    "room_amenities",
    Base.metadata,
    Column("room_id", Integer, ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True)
)


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50), nullable=True)

    rooms = relationship("Room", secondary="room_amenities", back_populates="amenities")
