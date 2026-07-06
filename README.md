# Autonomous Self-Correcting Data Validation System

*Using CrewAI + RAG + Human-in-the-Loop*

---

## Problem Statement

Organizations like hospitals, banks, insurance companies, and HR departments receive thousands of forms every day.

These forms often contain:

* Missing information
* Invalid email addresses
* Incorrect phone numbers
* Wrong blood groups
* Wrong date formats
* Typographical mistakes
* Inconsistent information

Instead of manually checking every field, our system automatically validates, corrects, and escalates only uncertain fields to humans.

---

## Technologies Used

* **CrewAI** - AI agent orchestration framework
* **OpenAI GPT** - Large language model for validation and correction
* **RAG (Retrieval-Augmented Generation)** - Knowledge base integration
* **Python** - Backend logic
* **SQLite** - Data persistence
* **React + Vite** - Frontend UI
* **YAML** - Configuration management

---

## Architecture Overview

```
User
  │
  ▼
React Frontend (frontend-react/)
  │
  ▼
Backend API (backend/)
  │
  ▼
CrewAI Orchestration
  │
  ▼
10 Specialized AI Agents
  │
  ▼
Validated & Corrected Data
  │
  ▼
Database (SQLite)
```

---

## Project Structure

```
autonomous-self-correcting-data-validation-main/
├── frontend-react/          # React + Vite frontend application
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                 # Python backend API
│   ├── __init__.py
│   └── app.py
└── database/                # Database schemas & migrations
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key
- SQLite

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/blessy21mis7167/autonomous-self-correcting-data-validation
   cd autonomous-self-correcting-data-validation-main
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend-react
   npm install
   ```

### Running the Application

**Backend:**
```bash
cd backend
python app.py
```

**Frontend:**
```bash
cd frontend-react
npm run dev
```

---

## Features

✅ Automated data validation using AI agents  
✅ Automatic error correction suggestions  
✅ Human-in-the-loop escalation for uncertain fields  
✅ Knowledge base integration via RAG  
✅ Real-time feedback and validation reports  
✅ Database persistence of validation results  

---

## License

Specify your license here.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue.

---

## Contact

For questions or support, contact the development team.
