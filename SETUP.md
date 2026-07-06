# 🚀 Setup & Installation Guide

## Prerequisites

- **Python 3.8+** - Download from [python.org](https://www.python.org)
- **Node.js 16+** - Download from [nodejs.org](https://nodejs.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)

---

## Quick Start (Windows)

### Option 1: Using PowerShell Script

1. **Open PowerShell** in the project root directory
2. **Run:**
   ```powershell
   .\start.ps1
   ```

This will automatically:
- Install Python dependencies
- Install Node.js dependencies
- Start the backend API server
- Start the frontend development server

### Option 2: Manual Setup

#### Step 1: Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend server
python ..\run.py
```

The backend will start at: **http://localhost:8000**

#### Step 2: Frontend Setup (in a new terminal)

```powershell
# Navigate to frontend directory
cd frontend-react

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at: **http://localhost:5173**

---

## API Endpoints

### Core Validation
- **POST** `/api/validate` - Validate messy input data
  ```json
  {
    "raw_input": "Name : john doe Email : john@gmail Phone : 9876543"
  }
  ```

### Escalation Management
- **GET** `/api/escalations` - Get all pending escalations
- **GET** `/api/escalations?validation_id=1` - Get escalations for specific validation
- **POST** `/api/escalations/{id}/resolve` - Resolve an escalation
  ```json
  {
    "escalation_id": 1,
    "approved": true,
    "user_correction": "corrected value"
  }
  ```

### History & Stats
- **GET** `/api/history?limit=10` - Get validation history
- **GET** `/api/stats` - Get system statistics
- **GET** `/api/validation/{id}` - Get detailed validation result

### Health Check
- **GET** `/health` - Check API health status

---

## Architecture Overview

### Backend Components

1. **app.py** - FastAPI application with REST endpoints
2. **validation.py** - Main validation engine orchestrating AI agents
3. **tools.py** - Data validation tools (7 specialized agents)
4. **database.py** - SQLite database operations
5. **requirements.txt** - Python dependencies

### Agents & Tools

The system uses 7 specialized validation agents:

1. **Email Validator Agent** - Validates and corrects email formats
2. **Phone Validator Agent** - Validates and normalizes phone numbers
3. **Age Validator Agent** - Converts text numbers to integers
4. **Blood Group Validator Agent** - Validates blood group types
5. **Date Validator Agent** - Parses and standardizes date formats
6. **Name Validator Agent** - Cleans and capitalizes names
7. **Consistency Checker Agent** - Checks data consistency across fields

### Frontend Features

- **Validator Tab** - Input data and see validation results
- **Escalations Tab** - Review and approve/reject uncertain fields
- **Statistics Tab** - View system-wide validation statistics
- **Sample Data** - Pre-loaded examples to test the system

### Database Schema

- **validation_history** - Stores all validation results
- **escalations** - Tracks fields needing human review
- **user_feedback** - Saves human corrections and approvals

---

## Testing the Application

### Sample Input 1
```
Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad
```

### Sample Input 2
```
Name: JANE SMITH
Email: jane.smith@yahoo.com
Phone: (555) 123-4567
Age: 32
Blood Group: O+
Date: 15-March-2000
```

### Sample Input 3
```
Name:Bob Johnson|Email:bob@gmail|Phone:9876543210|Age:45|BG:B-|DOB:01/01/1979
```

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Dependencies not installing:**
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --no-cache-dir
```

### Frontend Issues

**Dependencies not installing:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install
```

**Port 5173 already in use:**
```bash
# Kill process on port 5173 or specify different port
npm run dev -- --port 5174
```

---

## Deployment

### Using Docker

```bash
# Build image
docker build -t data-validation .

# Run container
docker run -p 8000:8000 -p 5173:5173 data-validation
```

### Using Render/Heroku

1. Push to GitHub
2. Connect repository to Render/Heroku
3. Set build command: `pip install -r requirements.txt && npm install`
4. Set start command: `python run.py`

---

## Development

### Adding New Validation Tools

Edit `backend/tools.py` to add new validation methods:

```python
@staticmethod
def validate_custom_field(value: str) -> Tuple[bool, str]:
    """Validate custom field"""
    # Your validation logic here
    return True, corrected_value
```

### Customizing UI

Edit `frontend-react/src/App.jsx` and `frontend-react/src/styles.css` to customize the interface.

---

## Documentation

- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **GitHub Repository:** [autonomous-self-correcting-data-validation](https://github.com/blessy21mis7167/autonomous-self-correcting-data-validation)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Create an issue on GitHub

---

**Happy Validating!** 🎉
