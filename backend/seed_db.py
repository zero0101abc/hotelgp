import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Room, Amenity, Package, RoomType, RoomStatus, UserRole, room_amenities
from app.utils.auth import hash_password

def seed_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
    
    db = SessionLocal()
    
    try:
        print("Seeding database...")
        
        # Create amenities
        amenities_data = [
            {"name": "Free WiFi", "icon": "wifi"},
            {"name": "Pool", "icon": "pool"},
            {"name": "Gym/Fitness Center", "icon": "dumbbell"},
            {"name": "Spa/Wellness", "icon": "spa"},
            {"name": "Restaurant", "icon": "utensils"},
            {"name": "24/7 Room Service", "icon": "bell"},
            {"name": "Air Conditioning", "icon": "wind"},
            {"name": "Smart TV", "icon": "tv"},
            {"name": "Double Bed", "icon": "bed"},
        ]
        
        existing_amenities = {a.name: a for a in db.query(Amenity).all()}
        for amenity_data in amenities_data:
            if amenity_data["name"] not in existing_amenities:
                amenity = Amenity(**amenity_data)
                db.add(amenity)
        db.commit()
        print(f"✓ Created {len(amenities_data)} amenities")
        
        # Create rooms matching frontend
        rooms_data = [
            {
                "id": 1,
                "name": "Premier King Room",
                "type": RoomType.Luxury,
                "price": 280,
                "image": "https://images.unsplash.com/photo-1590490359854-dfba19688d70?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBob3RlbCUyMHJvb20lMjBraW5nJTIwYmVkJTIwaW50ZXJpb3IlMjBsdXh1cnl8ZW58MXx8fHwxNzcwODUzMjk4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
                "size": "38 sq.m",
                "occupancy": "2 Adults",
                "description": "Our Premier King Room offers a sophisticated sanctuary with stunning city views and bespoke furnishings for the ultimate urban retreat.",
                "status": RoomStatus.available,
                "featured": False,
                "packages": [
                    {"name": "Room Only", "description": "Includes complimentary WiFi and pool access.", "price_multiplier": 0},
                    {"name": "Breakfast Included", "description": "Daily gourmet breakfast buffet for all guests.", "price_multiplier": 0.15},
                    {"name": "VIP Experience", "description": "Breakfast, airport transfer, and late check-out.", "price_multiplier": 0.35}
                ]
            },
            {
                "id": 2,
                "name": "Deluxe Twin Room",
                "type": RoomType.Luxury,
                "price": 240,
                "image": "https://images.unsplash.com/photo-1759221793465-4795ba2eaafc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdGFuZGFyZCUyMGhvdGVsJTIwcmVzb2x1dGlvbnxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
                "size": "35 sq.m",
                "occupancy": "2 Adults",
                "description": "Perfect for travelers sharing a space, the Deluxe Twin combines functional design with plush comfort and modern amenities.",
                "status": RoomStatus.available,
                "featured": False,
                "packages": [
                    {"name": "Room Only", "description": "Includes complimentary WiFi and pool access.", "price_multiplier": 0},
                    {"name": "Breakfast Delight", "description": "Daily buffet breakfast with premium selections.", "price_multiplier": 0.12}
                ]
            },
            {
                "id": 3,
                "name": "Presidential Suite",
                "type": RoomType.Suite,
                "price": 850,
                "image": "https://images.unsplash.com/photo-1767091116911-afd6612c53c6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkZWx1eGUlMjBob3RlbCUyMHN1aXRlJTIwbGl2aW5nJTIwYXJlYSUyMG1vZGVybiUyMGRlc2lnbnxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
                "size": "120 sq.m",
                "occupancy": "4 Adults",
                "description": "Experience the pinnacle of hospitality. Our Presidential Suite features a sprawling layout, private dining area, and panoramic harbor views.",
                "status": RoomStatus.available,
                "featured": True,
                "packages": [
                    {"name": "Luxury Stay", "description": "Full breakfast, minibar, and butler service.", "price_multiplier": 0.20},
                    {"name": "Ultimate VIP", "description": "All-inclusive: meals, spa, transfers, and concierge.", "price_multiplier": 0.45}
                ]
            },
            {
                "id": 4,
                "name": "Harbor View Executive",
                "type": RoomType.Business,
                "price": 420,
                "image": "https://images.unsplash.com/photo-1761049862641-16616dea7b32?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBob3RlbCUyMHNwYSUyMHdlbGxuZXNzJTIwY2VudGVyJTIwcG9vbHxlbnwxfHx8fDE3NzA4NTMyOTh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
                "size": "45 sq.m",
                "occupancy": "2 Adults",
                "description": "Designed for the discerning business traveler, featuring executive lounge access and the best harbor views in Nathan Road.",
                "status": RoomStatus.available,
                "featured": False,
                "packages": [
                    {"name": "Business Essentials", "description": "Lounge access, WiFi, and work desk setup.", "price_multiplier": 0},
                    {"name": "Executive Plus", "description": "Breakfast, meeting room access, and priority check-in.", "price_multiplier": 0.18}
                ]
            },
            {
                "id": 5,
                "name": "Family Deluxe Room",
                "type": RoomType.Family,
                "price": 380,
                "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYW1pbHklMjByb29tJTIwZGVsdXhlfGVufDF8fHx8MTc3MDg1MzI5OHww&ixlib=rb-4.1.0&q=80&w=1080",
                "size": "45 sq.m",
                "occupancy": "2 Adults, 2 Children",
                "description": "Spacious family room with double bed, perfect for families with children. Features extra space and child-friendly amenities.",
                "status": RoomStatus.available,
                "featured": False,
                "packages": [
                    {"name": "Room Only", "description": "Includes complimentary WiFi and pool access.", "price_multiplier": 0},
                    {"name": "Family Package", "description": "Breakfast for all, kids stay free, and pool access.", "price_multiplier": 0.20}
                ]
            },
            {
                "id": 6,
                "name": "Family Suite",
                "type": RoomType.Family,
                "price": 520,
                "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYW1pbHklMjBzdWl0ZSYlMjBtb3JnfGVufDF8fHx8MTc3MDg1MzI5OHww&ixlib=rb-4.1.0&q=80&w=1080",
                "size": "65 sq.m",
                "occupancy": "2 Adults, 3 Children",
                "description": "Large family suite with separate living area, double bed, and premium amenities. Ideal for larger families.",
                "status": RoomStatus.available,
                "featured": False,
                "packages": [
                    {"name": "Family Stay", "description": "Full breakfast, kids club access, and late check-out.", "price_multiplier": 0.25},
                    {"name": "Ultimate Family", "description": "All-inclusive: meals, kids activities, spa, and transfers.", "price_multiplier": 0.40}
                ]
            }
        ]
        
        # Get amenities for mapping
        all_amenities = {a.name: a for a in db.query(Amenity).all()}
        wifi = all_amenities.get("Free WiFi")
        pool = all_amenities.get("Pool")
        gym = all_amenities.get("Gym/Fitness Center")
        spa = all_amenities.get("Spa/Wellness")
        restaurant = all_amenities.get("Restaurant")
        smart_tv = all_amenities.get("Smart TV")
        aircon = all_amenities.get("Air Conditioning")
        roomservice = all_amenities.get("24/7 Room Service")
        double_bed = all_amenities.get("Double Bed")
        
        for room_data in rooms_data:
            existing_room = db.query(Room).filter(Room.id == room_data["id"]).first()
            packages = room_data.pop("packages", None)
            room_type = room_data.get("type")
            
            if not existing_room:
                room = Room(**room_data)
                db.add(room)
                db.flush()  # Get the ID
                
                # Add amenities - Family rooms get Double Bed
                if room_type == RoomType.Family:
                    room.amenities.extend([a for a in all_amenities.values() if a])
                else:
                    room.amenities.extend([a for a in all_amenities.values() if a])
                
                # Add packages
                if packages:
                    for pkg_data in packages:
                        package = Package(
                            room_id=room.id,
                            **pkg_data
                        )
                        db.add(package)
                
            else:
                # Update existing room
                for key, value in room_data.items():
                    setattr(existing_room, key, value)
                
        db.commit()
        print(f"✓ Created/updated {len(rooms_data)} rooms")
        
        # Create admin user
        admin_user = db.query(User).filter(User.email == "admin@hotelsys.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@hotelsys.com",
                password_hash=hash_password("admin123"),
                name="System Administrator",
                phone="+852 1234 5678",
                role=UserRole.staff
            )
            db.add(admin_user)
            db.commit()
            print("✓ Created admin user (admin@hotelsys.com / admin123)")
        else:
            print("✓ Admin user already exists")
        
        print("\\n✓ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()