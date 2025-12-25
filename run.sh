#!/bin/bash
# Garbage Classification System Launcher
# This script starts both backend and frontend servers

echo "========================================"
echo " Garbage Classification System"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then activate and install: pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "[INFO] Virtual environment activated"
echo ""

# Check if model file exists
if [ ! -f "backend/apps/model/renset50_model.pth" ]; then
    echo "[ERROR] Model file not found!"
    echo "Please ensure renset50_model.pth exists in backend/apps/model/"
    exit 1
fi

echo "[INFO] Model file found"
echo ""

# Kill any existing processes on ports 8000 and 5000
echo "[INFO] Checking for existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5000 | xargs kill -9 2>/dev/null

echo ""
echo "========================================"
echo " Starting Backend (FastAPI)..."
echo "========================================"
uvicorn backend.apps.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

echo ""
echo "========================================"
echo " Starting Frontend (Flask)..."
echo "========================================"
python frontend/app.py &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo " Application Started Successfully!"
echo "========================================"
echo ""
echo "Backend API:  http://localhost:8000"
echo "API Docs:     http://localhost:8000/docs"
echo "Frontend UI:  http://localhost:5000"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers"

# Trap Ctrl+C to clean up
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait
