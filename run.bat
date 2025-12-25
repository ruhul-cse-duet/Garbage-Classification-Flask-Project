@echo off
REM Garbage Classification System Launcher
REM This script starts both backend and frontend servers

echo ========================================
echo  Garbage Classification System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate and install: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

echo [INFO] Virtual environment activated
echo.

REM Check if model file exists
if not exist "backend\apps\model\renset50_model.pth" (
    echo [ERROR] Model file not found!
    echo Please ensure renset50_model.pth exists in backend/apps/model/
    pause
    exit /b 1
)

echo [INFO] Model file found
echo.

REM Kill any existing processes on ports 8000 and 5000
echo [INFO] Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do taskkill /F /PID %%a >nul 2>&1

echo.
echo ========================================
echo  Starting Backend (FastAPI)...
echo ========================================
start "Garbage Classification - Backend" cmd /k "venv\Scripts\activate && uvicorn backend.apps.main:app --reload --port 8000"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo  Starting Frontend (Flask)...
echo ========================================
start "Garbage Classification - Frontend" cmd /k "venv\Scripts\activate && python frontend\app.py"

echo.
echo ========================================
echo  Application Started Successfully!
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend UI:  http://localhost:5000
echo.
echo Press any key to open the application in browser...
pause >nul

REM Open browser
start http://localhost:5000

echo.
echo [INFO] Application is running!
echo [INFO] Close this window or press Ctrl+C to stop all servers
pause
