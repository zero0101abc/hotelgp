# Hotel Management System

A hotel booking and management system with React frontend and FastAPI backend.

## Quick Start

### One-Click Start (Windows)
```bash
run.bat
```
This starts both frontend and backend automatically.

### Manual Start

**Frontend:**
```bash
npm install
npm run dev
```

**Backend:**
```bash
cd backend
start.bat
```

## Requirements

- Node.js 18+
- Python 3.10+
- MySQL 8.0

## Setup

### 1. Database Setup

Create a MySQL database named `hotelsys`:

```sql
CREATE DATABASE hotelsys;
```

### 2. Backend Configuration

Create `backend/.env` file:

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/hotelsys
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
python seed_db.py  # Optional: seed sample data
```

### 4. Frontend Configuration (Optional)

Create `.env` file in project root to override API URL:

```env
VITE_API_URL=http://localhost:7999
```

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:7999 |
| API Docs | http://localhost:7999/docs |

## Default Admin Login

- Email: `admin@hotelsys.com`
- Password: `admin123`

## Tech Stack

- **Frontend:** React, Vite, Tailwind CSS, Radix UI
- **Backend:** FastAPI, SQLAlchemy, MySQL
- **Auth:** JWT (access + refresh tokens)
