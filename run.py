#!/usr/bin/env python
"""
Main entry point for the Autonomous Data Validation System backend
Run with: python run.py
"""

import uvicorn
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

if __name__ == "__main__":
    print("🚀 Starting Autonomous Data Validation Backend API")
    print("📍 Server will start at http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
