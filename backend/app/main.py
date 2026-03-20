from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, rooms, bookings, amenities
from app.database import engine, Base
from app.models import *  # Import all models to register them with Base.metadata

"""
Database Initialization Strategy (Hybrid Approach):
==================================================

1. create_all() - Auto-creates tables from SQLAlchemy models on startup.
   - Used for: Local development, quick setup
   - Location: Below
   - Behavior: Creates tables if they don't exist (idempotent)
   - Models MUST be imported before this call for tables to be created

2. Alembic Migrations - For production and version-controlled schema changes.
   - Used for: Production deployments, rollbacks, schema versioning
   - Run manually: alembic upgrade head OR python run_migrations.py
   - Location: alembic/versions/001_initial.py

Both methods create the same schema from app/models/*.py definitions.
"""

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hotel Management System API",
    description="Backend API for hotel booking and management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(amenities.router)


@app.get("/")
def root():
    return {
        "message": "Hotel Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}