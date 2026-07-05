from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from autonomous_self_correcting_data_validation_system.validation import run_validation_pipeline
from autonomous_self_correcting_data_validation_system.database import fetch_validation_history

app = FastAPI(title="Autonomous Data Validation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ValidationRequest(BaseModel):
    raw_input: str = Field(..., description="Messy input text to validate")


class ValidationResponse(BaseModel):
    corrected_data: dict
    validation_errors: dict
    correction_log: list
    confidence_scores: dict
    final_report: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/validate", response_model=ValidationResponse)
def validate_payload(payload: ValidationRequest) -> dict:
    if not payload.raw_input.strip():
        raise HTTPException(status_code=400, detail="raw_input cannot be empty")

    result = run_validation_pipeline(payload.raw_input)
    return {
        "corrected_data": result["corrected_data"],
        "validation_errors": result["validation_errors"],
        "correction_log": result["correction_log"],
        "confidence_scores": result["confidence_scores"],
        "final_report": result["final_report"],
    }


@app.get("/history")
def history(limit: int = 5) -> list:
    return fetch_validation_history(limit=limit)
