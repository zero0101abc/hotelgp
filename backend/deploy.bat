@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    HotelSys - First Time Deployment
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher from https://python.org
    pause
    exit /b 1
)
echo      Python found!
echo.

echo [2/5] Setting up virtual environment...
if not exist "venv" (
    echo      Creating venv folder...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
) else (
    echo      venv already exists, skipping...
)
echo.

echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo      Installing packages (this may take a minute)...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo      Dependencies installed successfully!
echo.

echo [4/5] Creating database folder...
if not exist "database" (
    mkdir database
    echo      database folder created!
) else (
    echo      database folder already exists, skipping...
)
echo.

echo [5/5] Seeding database with initial data...
python seed_db.py
if errorlevel 1 (
    echo WARNING: Database seeding had issues, but tables should be created
) else (
    echo      Database seeded successfully!
)
echo.

echo ========================================
echo    Deployment Complete!
echo ========================================
echo.
echo    Next steps:
echo.
echo    1. Start the server:
echo       run: start.bat
echo.
echo    2. Open API Documentation:
echo       http://localhost:8000/docs
echo.
echo    3. Login with admin account:
echo       Email:    admin@hotelsys.com
echo       Password: admin123
echo.
echo ========================================
echo.
pause
