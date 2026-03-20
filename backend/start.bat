@echo off
chcp 65001 >nul

echo ========================================
echo    HotelSys - Starting Server
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv" (
    echo ERROR: Virtual environment not found!
    echo Please run deploy.bat first to set up the environment.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

echo ========================================
echo    Starting HotelSys Server...
echo ========================================
echo.
echo    API Documentation: http://localhost:7999/docs
echo    Health Check:      http://localhost:7999/health
echo.
echo    Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 7999
