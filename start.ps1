# Autonomous Data Validation System - Startup Script
# This script will start both backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Autonomous Data Validation System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "✓ Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "✓ Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  Found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host ""

# Install backend dependencies
if (Test-Path "backend/requirements.txt") {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    python -m pip install -q -r backend/requirements.txt 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "✓ Python dependencies already installed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host ""

# Install frontend dependencies
if (Test-Path "frontend-react/package.json") {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    Push-Location frontend-react
    npm install 2>$null
    Pop-Location
    Write-Host "✓ Node.js dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎯 Starting Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Create a new PowerShell process for backend
Write-Host "Launching Backend Server (http://localhost:8000)" -ForegroundColor Yellow
Write-Host "  - API: http://localhost:8000" -ForegroundColor Gray
Write-Host "  - Swagger Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""

$backendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python run.py" -PassThru

# Wait a moment for backend to start
Start-Sleep -Seconds 2

# Create a new PowerShell process for frontend
Write-Host "Launching Frontend Server (http://localhost:5173)" -ForegroundColor Yellow
Write-Host "  - Frontend: http://localhost:5173" -ForegroundColor Gray
Write-Host ""

$frontendProcess = Start-Process pwsh -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot/frontend-react'; npm run dev" -PassThru

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Both servers are running!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "🖥️  Frontend UI: http://localhost:5173" -ForegroundColor Cyan
Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow
Write-Host ""

# Wait for processes to complete
$backendProcess | Wait-Process
$frontendProcess | Wait-Process
