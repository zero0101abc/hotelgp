from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, rooms, bookings, amenities
from app.database import engine, Base

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