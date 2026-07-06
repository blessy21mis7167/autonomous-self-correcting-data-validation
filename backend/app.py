from pathlib import Path
import sys
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import csv
from io import StringIO

# Import local modules
from validation import run_validation_pipeline
from database import (
    fetch_validation_history, 
    fetch_escalations, 
    resolve_escalation
)

app = FastAPI(
    title="Autonomous Data Validation API",
    description="Self-correcting data validation system with CrewAI agents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ValidationRequest(BaseModel):
    raw_input: str = Field(..., description="Messy input text to validate", min_length=1)


class ValidationResponse(BaseModel):
    validation_id: int
    corrected_data: dict
    validation_errors: dict
    correction_log: list
    confidence_scores: dict
    escalations: list
    final_report: dict
    agent_metadata: dict


class FileUploadResponse(BaseModel):
    total_records: int
    processed_records: int
    failed_records: int
    validations: list
    errors: Optional[list] = None


class EscalationResolution(BaseModel):
    escalation_id: int
    approved: bool
    user_correction: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    raw_input: str
    corrected_data: dict
    validation_errors: dict
    confidence_scores: dict
    created_at: str


class EscalationItem(BaseModel):
    id: int
    validation_id: int
    field_name: str
    original_value: str
    corrected_value: Optional[str]
    confidence_score: float
    reason: str
    status: str
    created_at: str


# Health Check
@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "Autonomous Data Validation API",
        "version": "1.0.0"
    }


# Main Validation Endpoint
@app.post("/api/validate", response_model=ValidationResponse)
def validate_payload(payload: ValidationRequest) -> dict:
    """
    Validate messy input data using AI agents
    
    Agents involved:
    - Email Validator Agent
    - Phone Number Validator Agent
    - Age Validator Agent
    - Blood Group Validator Agent
    - Date Validator Agent
    - Name Validator Agent
    - Consistency Checker Agent
    """
    if not payload.raw_input.strip():
        raise HTTPException(status_code=400, detail="raw_input cannot be empty")

    try:
        result = run_validation_pipeline(payload.raw_input)
        return {
            "validation_id": result["validation_id"],
            "corrected_data": result["corrected_data"],
            "validation_errors": result["validation_errors"],
            "correction_log": result["correction_log"],
            "confidence_scores": result["confidence_scores"],
            "escalations": result["escalations"],
            "final_report": result["final_report"],
            "agent_metadata": result.get("agent_metadata", {}),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


# File Upload Endpoint
@app.post("/api/validate-file", response_model=FileUploadResponse)
async def validate_file(file: UploadFile = File(...)) -> dict:
    """
    Upload a CSV or text file for batch validation
    
    Supported formats:
    - CSV (comma/tab/pipe separated)
    - TXT (one record per line)
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    if not file.filename.endswith(('.csv', '.txt', '.tsv')):
        raise HTTPException(status_code=400, detail="Only CSV, TXT, or TSV files are supported")
    
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        validations = []
        errors = []
        
        # Process based on file type
        if file.filename.endswith('.csv'):
            # Parse CSV
            reader = csv.DictReader(StringIO(text))
            for row_num, row in enumerate(reader, 1):
                try:
                    # Convert row dict to string format
                    raw_input = " ".join([f"{k}:{v}" for k, v in row.items() if v])
                    if raw_input.strip():
                        result = run_validation_pipeline(raw_input)
                        validations.append({
                            "row": row_num,
                            "validation_id": result["validation_id"],
                            "corrected_data": result["corrected_data"],
                            "confidence": result["final_report"]["average_confidence"],
                            "has_escalations": len(result["escalations"]) > 0
                        })
                except Exception as e:
                    errors.append({
                        "row": row_num,
                        "error": str(e)
                    })
        
        else:  # TXT file
            # Process line by line
            lines = text.strip().split('\n')
            for row_num, line in enumerate(lines, 1):
                if line.strip():
                    try:
                        result = run_validation_pipeline(line.strip())
                        validations.append({
                            "row": row_num,
                            "validation_id": result["validation_id"],
                            "corrected_data": result["corrected_data"],
                            "confidence": result["final_report"]["average_confidence"],
                            "has_escalations": len(result["escalations"]) > 0
                        })
                    except Exception as e:
                        errors.append({
                            "row": row_num,
                            "error": str(e)
                        })
        
        return {
            "total_records": len(validations) + len(errors),
            "processed_records": len(validations),
            "failed_records": len(errors),
            "validations": validations,
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")


# History Endpoint
@app.get("/api/history")
def get_history(limit: int = 10) -> dict:
    """
    Retrieve validation history
    """
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    history = fetch_validation_history(limit=limit)
    return {
        "count": len(history),
        "items": history
    }


# Escalations Endpoints
@app.get("/api/escalations")
def get_escalations(validation_id: Optional[int] = None) -> dict:
    """
    Get all pending escalations or escalations for a specific validation
    """
    escalations = fetch_escalations(validation_id=validation_id)
    return {
        "count": len(escalations),
        "items": escalations
    }


@app.post("/api/escalations/{escalation_id}/resolve")
def resolve_escalation_endpoint(escalation_id: int, resolution: EscalationResolution) -> dict:
    """
    Resolve an escalation with human feedback
    """
    if resolution.escalation_id != escalation_id:
        raise HTTPException(status_code=400, detail="Escalation ID mismatch")
    
    try:
        resolve_escalation(
            escalation_id,
            resolution.approved,
            resolution.user_correction
        )
        return {
            "status": "success",
            "escalation_id": escalation_id,
            "resolution": "approved" if resolution.approved else "rejected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve: {str(e)}")


# Statistics Endpoint
@app.get("/api/stats")
def get_stats() -> dict:
    """
    Get overall validation statistics
    """
    history = fetch_validation_history(limit=100)
    escalations = fetch_escalations()
    
    total_validations = len(history)
    total_fields_corrected = sum(
        len(item.get('correction_log', [])) for item in history
    )
    total_escalations = len(escalations)
    pending_escalations = sum(1 for e in escalations if e['status'] == 'pending')
    
    avg_confidence = 0
    if history:
        all_scores = []
        for item in history:
            scores = item.get('confidence_scores', {})
            if scores:
                all_scores.extend(scores.values())
        if all_scores:
            avg_confidence = sum(all_scores) / len(all_scores)
    
    return {
        "total_validations": total_validations,
        "total_fields_corrected": total_fields_corrected,
        "total_escalations": total_escalations,
        "pending_escalations": pending_escalations,
        "average_confidence_score": round(avg_confidence, 2)
    }


# Detailed Validation Endpoint
@app.get("/api/validation/{validation_id}")
def get_validation_detail(validation_id: int) -> dict:
    """
    Get detailed validation result by ID
    """
    history = fetch_validation_history(limit=1000)
    for item in history:
        if item['id'] == validation_id:
            escalations = fetch_escalations(validation_id=validation_id)
            return {
                "validation": item,
                "escalations": escalations
            }
    
    raise HTTPException(status_code=404, detail="Validation not found")


# Root endpoint
@app.get("/")
def root() -> dict:
    return {
        "name": "Autonomous Data Validation API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "validate": "/api/validate",
            "validate_file": "/api/validate-file (POST with file)",
            "history": "/api/history",
            "escalations": "/api/escalations",
            "stats": "/api/stats",
            "resolve_escalation": "/api/escalations/{escalation_id}/resolve",
            "docs": "/docs"
        }
    }
