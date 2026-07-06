#!/bin/bash

# Autonomous Data Validation System - Startup Script for Linux/Mac

echo "========================================"
echo "🚀 Autonomous Data Validation System"
echo "========================================"
echo ""

# Check if Python is installed
echo "✓ Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "  ✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  Found: $PYTHON_VERSION"

# Check if Node.js is installed
echo "✓ Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "  ✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "  Found: $NODE_VERSION"

echo ""
echo "Setting up Backend..."
echo ""

# Install backend dependencies
if [ -f "backend/requirements.txt" ]; then
    echo "Installing Python dependencies..."
    python3 -m pip install -q -r backend/requirements.txt
    if [ $? -eq 0 ]; then
        echo "✓ Python dependencies installed"
    else
        echo "✓ Python dependencies already installed"
    fi
fi

echo ""
echo "Setting up Frontend..."
echo ""

# Install frontend dependencies
if [ -f "frontend-react/package.json" ]; then
    echo "Installing Node.js dependencies..."
    cd frontend-react
    npm install 2>/dev/null
    cd ..
    echo "✓ Node.js dependencies installed"
fi

echo ""
echo "========================================"
echo "🎯 Starting Servers"
echo "========================================"
echo ""

# Start backend server
echo "Launching Backend Server (http://localhost:8000)"
echo "  - API: http://localhost:8000"
echo "  - Swagger Docs: http://localhost:8000/docs"
echo ""

python3 run.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "Launching Frontend Server (http://localhost:5173)"
echo "  - Frontend: http://localhost:5173"
echo ""

cd frontend-react
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "✓ Both servers are running!"
echo "========================================"
echo ""
echo "📝 Backend API: http://localhost:8000"
echo "🖥️  Frontend UI: http://localhost:5173"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Handle Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT

# Wait for processes
wait
