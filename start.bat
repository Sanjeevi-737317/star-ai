@echo off
echo ========================================
echo   STAR AI - Starting Backend + Frontend
echo ========================================
echo.

cd backend
start "STAR AI Backend" cmd /k "uvicorn app.main:app --port 8000"

cd ../frontend
start "STAR AI Frontend" cmd /k "npm run dev"

echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this launcher...
pause >nul
