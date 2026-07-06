# System Architecture

## Overview

The Autonomous Self-Correcting Data Validation System is a multi-agent orchestration system built with:
- **Backend**: FastAPI + Python
- **Frontend**: React + Vite
- **Database**: SQLite
- **Validation Engine**: Custom AI agents with specialized tools

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend                         │
│         (Validator, Escalations, Statistics Tabs)       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                         │
│  • /api/validate              (Main validation)          │
│  • /api/escalations           (Escalation management)    │
│  • /api/history               (Validation history)       │
│  • /api/stats                 (System statistics)        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   ┌─────────────┐          ┌──────────────┐
   │ Validation  │          │   Database   │
   │   Engine    │          │   (SQLite)   │
   └────┬────────┘          └──────────────┘
        │
   ┌────┴────────────────────────────────┐
   │      7 Specialized Agents            │
   ├───────────────────────────────────┬──┤
   │ Agent 1: Email Validator          │  │
   │ Agent 2: Phone Validator          │  │
   │ Agent 3: Age Validator            │  │ Validation Tools
   │ Agent 4: Blood Group Validator    │  │
   │ Agent 5: Date Validator           │  │
   │ Agent 6: Name Validator           │  │
   │ Agent 7: Consistency Checker      │  │
   └───────────────────────────────────┴──┘
```

---

## Component Details

### 1. Frontend (React + Vite)

**Location**: `frontend-react/`

**Key Files**:
- `src/App.jsx` - Main application component with three tabs
- `src/main.jsx` - Entry point
- `src/styles.css` - Complete styling
- `vite.config.js` - Vite configuration with API proxy

**Features**:
- **Validator Tab**: Input data and see real-time validation results
- **Escalations Tab**: Review and approve/reject uncertain fields
- **Statistics Tab**: View system-wide metrics

**Dependencies**:
- React 18.3
- Vite 5.4

---

### 2. Backend (FastAPI)

**Location**: `backend/`

**Core Modules**:

#### `app.py`
Main FastAPI application with endpoints:
- `POST /api/validate` - Submit data for validation
- `GET /api/history` - Retrieve validation history
- `GET /api/escalations` - Get pending escalations
- `POST /api/escalations/{id}/resolve` - Resolve an escalation
- `GET /api/stats` - Get system statistics
- `GET /api/validation/{id}` - Get detailed validation

#### `validation.py`
Main validation orchestration engine:
- `DataValidationEngine` class orchestrates all agents
- Processes raw input through 7 validation stages
- Returns corrected data with confidence scores
- Identifies fields that need human review

#### `tools.py`
Specialized validation tools (7 agents):

1. **Email Validator**
   - Pattern matching for valid email
   - Auto-correction of common mistakes
   - Returns: (is_valid, corrected_email)

2. **Phone Validator**
   - Digit extraction and normalization
   - International format support
   - Returns: (is_valid, corrected_phone)

3. **Age Validator**
   - Number extraction and text-to-number conversion
   - Range validation (0-150)
   - Returns: (is_valid, age_as_integer)

4. **Blood Group Validator**
   - Validates against known blood group types
   - Handles formatting variations
   - Returns: (is_valid, standardized_bg)

5. **Date Validator**
   - Supports multiple date formats
   - Converts to standard DD-MM-YYYY
   - Returns: (is_valid, standardized_date)

6. **Name Validator**
   - Validates name format
   - Applies proper capitalization
   - Returns: (is_valid, corrected_name)

7. **Consistency Checker**
   - Verifies data consistency across fields
   - Checks age vs DOB compatibility
   - Returns: consistency_issues

#### `database.py`
SQLite database operations:
- Initialize database schema
- Save validation results
- Save escalations
- Fetch validation history
- Manage escalation resolution

**Database Tables**:
- `validation_history` - All validation records
- `escalations` - Fields needing human review
- `user_feedback` - Human corrections and approvals

---

### 3. Database Schema

#### validation_history
```sql
CREATE TABLE validation_history (
    id INTEGER PRIMARY KEY,
    raw_input TEXT,
    corrected_data TEXT (JSON),
    validation_errors TEXT (JSON),
    confidence_scores TEXT (JSON),
    final_report TEXT (JSON),
    status TEXT,
    created_at TIMESTAMP
)
```

#### escalations
```sql
CREATE TABLE escalations (
    id INTEGER PRIMARY KEY,
    validation_id INTEGER (FK),
    field_name TEXT,
    original_value TEXT,
    corrected_value TEXT,
    confidence_score REAL,
    reason TEXT,
    status TEXT (pending/approved/rejected),
    created_at TIMESTAMP,
    resolved_at TIMESTAMP
)
```

#### user_feedback
```sql
CREATE TABLE user_feedback (
    id INTEGER PRIMARY KEY,
    validation_id INTEGER (FK),
    field_name TEXT,
    user_correction TEXT,
    approved BOOLEAN,
    feedback_text TEXT,
    created_at TIMESTAMP
)
```

---

## Validation Pipeline

### Execution Flow

```
1. User Input
   │
   ▼
2. Field Extraction
   Extract: name, email, phone, age, blood_group, date, address
   │
   ▼
3. Agent Processing (Parallel)
   ├─ Email Validator
   ├─ Phone Validator
   ├─ Age Validator
   ├─ Blood Group Validator
   ├─ Date Validator
   ├─ Name Validator
   └─ Consistency Checker
   │
   ▼
4. Confidence Scoring
   Each field gets a confidence score (0.0-1.0)
   │
   ▼
5. Escalation Decision
   If confidence < threshold (0.8):
   └─ Add to escalations for human review
   │
   ▼
6. Database Storage
   Save validation result and any escalations
   │
   ▼
7. Response to Frontend
   Return validated data + escalations + confidence scores
```

---

## API Response Format

### Validation Response
```json
{
  "validation_id": 1,
  "corrected_data": {
    "name": "John Doe",
    "email": "john@gmail.com",
    "phone": "+19876543210",
    "age": 25,
    "blood_group": "AB",
    "address": "Hyderabad"
  },
  "validation_errors": {
    "blood_group": "Invalid blood group: ABC"
  },
  "correction_log": [
    {
      "field": "email",
      "original": "john@gmail",
      "corrected": "john@gmail.com",
      "reason": "Format correction"
    }
  ],
  "confidence_scores": {
    "name": 0.85,
    "email": 0.95,
    "phone": 0.9,
    "age": 0.85,
    "blood_group": 0.2,
    "address": 1.0
  },
  "escalations": [
    {
      "field": "blood_group",
      "original": "ABC",
      "corrected": "AB",
      "confidence": 0.2,
      "reason": "Invalid blood group"
    }
  ],
  "final_report": {
    "total_fields": 6,
    "corrected_fields": 1,
    "validation_errors": 1,
    "escalations": 1,
    "average_confidence": 0.789,
    "timestamp": "2024-01-15T10:30:00",
    "status": "requires_review"
  }
}
```

---

## Data Flow Example

### Input
```
"Name : john doeEmail : john@gmailPhone : 9876543Age : twenty fiveBlood Group : ABCAddress : Hyderabad"
```

### Processing
1. **Extract Fields**
   - name: "john doe"
   - email: "john@gmail"
   - phone: "9876543"
   - age: "twenty five"
   - blood_group: "ABC"
   - address: "Hyderabad"

2. **Validate Each Field**
   - name → "John Doe" ✓ (confidence: 0.85)
   - email → "john@gmail.com" (auto-corrected) ✓ (confidence: 0.95)
   - phone → "+19876543" (needs 10 digits) ✗ (confidence: 0.2)
   - age → 25 (text converted) ✓ (confidence: 0.85)
   - blood_group → "AB" (invalid: ABC) ✗ (confidence: 0.2)
   - address → "Hyderabad" ✓ (confidence: 1.0)

3. **Create Escalations**
   - phone: "9876543" (invalid length)
   - blood_group: "ABC" (invalid)

4. **Generate Report**
   - 6 fields processed
   - 2 corrections needed
   - 2 fields escalated
   - Average confidence: 0.64

### Output
Corrected data with escalations ready for human review

---

## Deployment Architecture

### Development
```
Local Machine
├── Backend (localhost:8000)
├── Frontend (localhost:5173)
└── Database (./database/validation.db)
```

### Production (Docker)
```
Docker Container
├── FastAPI Backend (port 8000)
├── React Frontend (port 5173)
└── SQLite Database (volume mount)
```

### Cloud Deployment (Render/Heroku)
```
Cloud Platform
├── Backend Service (Python)
├── Frontend Service (Node.js)
└── Database Service (PostgreSQL/MySQL)
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Avg. Validation Time | < 100ms |
| Database Queries | 2-3 per validation |
| Max Fields Processed | Unlimited |
| Confidence Score Precision | 2 decimals |
| Escalation Threshold | 0.8 (80%) |

---

## Security Considerations

1. **CORS**: Configured to allow all origins (can be restricted)
2. **Input Validation**: Pydantic models validate all inputs
3. **Database**: SQLite with parameterized queries (SQL injection safe)
4. **Error Handling**: Proper HTTP status codes and error messages

---

## Future Enhancements

1. **Machine Learning**: Replace rule-based validation with ML models
2. **Real CrewAI Integration**: Integrate actual CrewAI framework
3. **Multi-language Support**: Support validation in multiple languages
4. **Advanced Analytics**: ML-based insights on validation patterns
5. **User Authentication**: Add user accounts and permission levels
6. **Webhooks**: Send validation results to external systems
7. **Batch Processing**: Handle bulk file uploads and validation
8. **Custom Rules**: Allow users to define custom validation rules

---

## Testing Strategy

1. **Unit Tests**: Test individual validation tools
2. **Integration Tests**: Test full validation pipeline
3. **API Tests**: Test all endpoints with various inputs
4. **UI Tests**: Test frontend components and interactions
5. **Load Tests**: Test system with high volume of validations

---

## Monitoring & Logging

- **Backend Logs**: FastAPI uvicorn logs
- **Database Logs**: SQLite transaction logs
- **Frontend Logs**: Browser console
- **Statistics Endpoint**: Real-time system metrics
- **History Endpoint**: Full validation audit trail

---

## Support & Documentation

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Setup Guide**: See SETUP.md
- **README**: See README.md

