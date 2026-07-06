# ⚡ Quick Start Guide

## 30-Second Setup (Windows)

### Easiest Way - Use the Startup Script

1. **Open PowerShell** in the project root directory
2. **Run this single command:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; .\start.ps1
   ```
3. **Open your browser to:**
   - 🖥️ **Frontend**: http://localhost:5173
   - 📚 **API Docs**: http://localhost:8000/docs

**That's it! The app is running.** ✅

---

## Manual Setup (3 Easy Steps)

### Step 1: Install Backend Dependencies
```powershell
cd backend
pip install -r requirements.txt
python ..\run.py
```
→ Backend starts at http://localhost:8000

### Step 2: Install Frontend Dependencies (New Terminal)
```powershell
cd frontend-react
npm install
npm run dev
```
→ Frontend starts at http://localhost:5173

### Step 3: Open in Browser
Navigate to http://localhost:5173

---

## What You'll See

### Validator Tab (Main Interface)
- Paste messy data into the text area
- Click "Validate Data"
- See corrected data instantly
- Review confidence scores for each field
- View any corrections that were made

### Escalations Tab
- See fields that need human review
- Review original vs. suggested correction
- Click "Approve" to accept the correction
- Click "Reject" if the correction is wrong

### Statistics Tab
- Total validations processed
- Fields corrected
- Escalations requiring review
- Average confidence scores

---

## Sample Data to Try

### Sample 1: Messy Input
```
Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad
```

### Sample 2: Mixed Formats
```
Name: JANE SMITH
Email: jane.smith@yahoo.com
Phone: (555) 123-4567
Age: 32
Blood Group: O+
Date: 15-March-2000
```

### Sample 3: Pipe-Delimited
```
Name:Bob Johnson|Email:bob@gmail|Phone:9876543210|Age:45|BG:B-|DOB:01/01/1979
```

---

## System Architecture

```
Your Input (Messy Data)
        ↓
React Frontend (5173)
        ↓
FastAPI Backend (8000)
        ↓
7 AI Validation Agents:
├─ Email Validator
├─ Phone Validator
├─ Age Validator
├─ Blood Group Validator
├─ Date Validator
├─ Name Validator
└─ Consistency Checker
        ↓
Database (SQLite)
        ↓
Corrected Data + Escalations
```

---

## What Gets Validated & Corrected

| Field | What It Does | Example |
|-------|-------------|---------|
| **Email** | Validates format, auto-corrects common mistakes | `john@gmail` → `john@gmail.com` |
| **Phone** | Normalizes phone numbers to standard format | `9876543` → `+19876543` |
| **Age** | Converts text numbers to integers | `twenty five` → `25` |
| **Blood Group** | Validates blood type formats | `ABC` → `AB` |
| **Date** | Standardizes multiple date formats | `15-March-2000` → `15-03-2000` |
| **Name** | Cleans and capitalizes names | `JOHN DOE` → `John Doe` |
| **Consistency** | Checks if data makes sense together | Age vs DOB check |

---

## Troubleshooting

### Port Already in Use?
```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill it (replace 12345 with actual PID)
taskkill /PID 12345 /F
```

### Dependencies Won't Install?
```powershell
# Clear cache and reinstall
pip cache purge
pip install -r backend/requirements.txt --no-cache-dir
```

### Frontend not connecting to backend?
Make sure backend is running first. The frontend needs to connect to port 8000.

---

## Project Structure

```
autonomous-self-correcting-data-validation-main/
├── backend/                    # FastAPI Backend
│   ├── app.py                 # Main API application
│   ├── validation.py          # Validation engine
│   ├── tools.py              # 7 validation tools
│   ├── database.py           # Database operations
│   └── requirements.txt       # Python dependencies
├── frontend-react/            # React Frontend
│   ├── src/
│   │   ├── App.jsx           # Main component
│   │   ├── main.jsx          # Entry point
│   │   └── styles.css        # Styling
│   ├── package.json
│   └── vite.config.js
├── database/                  # SQLite Database
│   └── validation.db
├── README.md                  # Project overview
├── SETUP.md                   # Full setup guide
├── ARCHITECTURE.md            # System architecture
├── run.py                     # Backend startup
├── start.ps1                  # Windows startup script
└── start.sh                   # Linux/Mac startup script
```

---

## API Endpoints Cheat Sheet

### Validation
- `POST /api/validate` - Validate data
  ```json
  {"raw_input": "Name : john doe Email : john@gmail"}
  ```

### History
- `GET /api/history?limit=10` - Get past validations
- `GET /api/stats` - Get system statistics

### Escalations
- `GET /api/escalations` - Get pending escalations
- `POST /api/escalations/1/resolve` - Approve/reject

### Documentation
- `GET /docs` - Interactive Swagger UI
- `GET /redoc` - ReDoc documentation

---

## Next Steps

1. ✅ **Run the application** using the quick start above
2. 📝 **Test with sample data** provided in the UI
3. 👀 **Review escalations** that need human approval
4. 📊 **Check statistics** to see system performance
5. 📚 **Explore API** at http://localhost:8000/docs

---

## Features

✅ Real-time data validation with AI agents  
✅ Automatic error correction  
✅ Human-in-the-loop escalation system  
✅ Confidence scoring for each field  
✅ Complete audit trail in database  
✅ Beautiful, responsive UI  
✅ RESTful API with Swagger documentation  
✅ Statistical dashboard  

---

## Support

- 🐛 **Issues?** Check TROUBLESHOOTING in SETUP.md
- 📚 **Need Details?** Read ARCHITECTURE.md
- 🔧 **Full Setup?** See SETUP.md
- 📖 **Code Docs?** Visit http://localhost:8000/docs

---

**Ready to validate?** 🚀 Start with the startup script above!

