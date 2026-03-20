@echo off
chcp 65001 >nul

echo ========================================
echo    HotelSys - Starting All Services
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Backend Server...
start "Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 7999"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo    All Services Started!
echo ========================================
echo.
echo    Frontend: http://localhost:5174
echo    Backend:  http://localhost:7999
echo    API Docs: http://localhost:7999/docs
echo.
echo    Close this window to exit
echo ========================================
echo.
pause
