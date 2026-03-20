# Hotel Management System - Backend

FastAPI + MySQL backend API for hotel booking and management.

## Features

- JWT Authentication (access + refresh tokens)
- User management (customer/staff roles)
- Room listings with filters (type, status, featured)
- Package management for rooms
- Booking system with price calculation
- Review system (edit/delete own reviews)
- Amenity management
- Admin capabilities

## Tech Stack

- **Framework**: FastAPI 0.115.0
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0
- **Auth**: python-jose (JWT)
- **Password Hashing**: passlib + bcrypt

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings & DB config
│   ├── database.py          # SQLAlchemy setup
│   ├── dependencies.py      # Auth dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── booking.py
│   │   ├── review.py
│   │   └── token.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── room.py
│   │   ├── booking.py
│   │   └── auth.py
│   ├── routers/            # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── rooms.py
│   │   ├── bookings.py
│   │   └── amenities.py
│   └── utils/
│       ├── auth.py          # JWT helpers
│       └── helpers.py
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── seed_db.py              # Seed script
```

## Database Initialization

This project uses a **hybrid approach** for database schema management:

### Method 1: Automatic (Development)
**SQLAlchemy `create_all()`** - Automatically creates tables on server startup.
- Runs automatically when you start the server
- Creates tables from `app/models/*.py` if they don't exist
- Best for: Local development, quick setup

```bash
# Just start the server - tables are created automatically
uvicorn app.main:app --reload
```

### Method 2: Alembic Migrations (Production)
**Alembic** - Version-controlled schema management with rollback support.
- Run manually when needed
- Best for: Production, schema changes, rollbacks

```bash
# Use the migration helper script
python run_migrations.py

# Or use alembic directly
alembic upgrade head          # Apply all migrations
alembic downgrade -1         # Rollback one step
alembic history              # Show migration history
alembic current              # Show current version

# Create a new migration after model changes
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Run Migrations Script Commands
```bash
python run_migrations.py --upgrade   # Upgrade to latest (default)
python run_migrations.py --downgrade # Downgrade one step
python run_migrations.py --current  # Show current version
python run_migrations.py --history  # Show migration history
python run_migrations.py --check    # Check if DB is up to date
python run_migrations.py --create "message"  # Create new migration
```

## Setup with Docker

```bash
# Start MySQL + Backend
docker-compose up -d

# Seed database (after containers are up)
docker-compose exec backend python seed_db.py

# View logs
docker-compose logs -f backend
```

## Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# Run server (tables auto-created on first run)
uvicorn app.main:app --reload

# OR run migrations explicitly
alembic upgrade head

# Seed database
python seed_db.py
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Admin Credentials

Email: `admin@hotelsys.com`
Password: `admin123`

## Endpoints

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout (invalidate refresh token)

### Users
- `GET /users/me` - Get current user info
- `PUT /users/me` - Update profile
- `GET /users/{id}` - Get user by id (admin only)

### Rooms
- `GET /rooms` - List rooms (with filters)
- `GET /rooms/{id}` - Get room details
- `GET /rooms/{id}/packages` - Get room packages
- `POST /rooms/{id}/packages` - Add package (admin)
- `DELETE /rooms/{id}/packages/{pkgId}` - Remove package (admin)
- `GET /rooms/{id}/reviews` - Get room reviews
- `POST /rooms/{id}/reviews` - Create review
- `DELETE /rooms/reviews/{review_id}` - Delete review

### Bookings
- `GET /bookings` - Get user's bookings
- `POST /bookings` - Create new booking
- `POST /bookings/{id}/cancel` - Cancel booking
- `PUT /bookings/{id}` - Update booking status (admin)

### Amenities
- `GET /amenities` - List amenities
- `POST /amenities` - Create amenity (admin)
- `DELETE /amenities/{id}` - Delete amenity (admin)

## Database Tables

| Table | Description |
|-------|-------------|
| `users` | User accounts (customer/staff) |
| `rooms` | Hotel rooms |
| `amenities` | Room amenities |
| `room_amenities` | Many-to-many rooms ↔ amenities |
| `packages` | Room packages (breakfast, VIP, etc.) |
| `bookings` | User bookings |
| `reviews` | Room reviews |
| `refresh_tokens` | JWT refresh tokens |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | - | MySQL connection string |
| `SECRET_KEY` | `supersecretkey123456789` | JWT secret |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token expiry |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token expiry |