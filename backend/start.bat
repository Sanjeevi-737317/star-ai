@echo off
echo ========================================
echo     STAR AI - Backend Startup
echo ========================================
cd /d "%~dp0"
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env >nul
)
echo Starting FastAPI server on http://localhost:8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
