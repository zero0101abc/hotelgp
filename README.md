# Hotel Management System

A hotel booking and management system with React frontend and FastAPI backend.

## Quick Start (One-Click)

```bash
run.bat
```

This starts both frontend and backend automatically.

## Manual Setup

### 1. Install Dependencies

**Frontend:**
```bash
npm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Servers

**Both at once (Windows):**
```bash
run.bat
```

**Or start separately:**

Frontend:
```bash
npm run dev
```

Backend:
```bash
cd backend
start.bat
```

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:7999 |
| API Docs | http://localhost:7999/docs |

## Optional: Seed Sample Data

```bash
cd backend
python seed_db.py
```

**Default Admin Login:**
- Email: `admin@hotelsys.com`
- Password: `admin123`

## Requirements

- Node.js 18+
- Python 3.10+

## Tech Stack

- **Frontend:** React, Vite, Tailwind CSS, Radix UI
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Auth:** JWT (access + refresh tokens)
