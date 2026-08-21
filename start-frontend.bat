@echo off
echo ========================================
echo     STAR AI - Frontend Startup
echo ========================================
cd /d "%~dp0frontend"
echo Starting Next.js dev server on http://localhost:3000
npm run dev
pause
