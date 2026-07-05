import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "database" / "validation.db"


def init_db(db_path: Optional[Path] = None) -> Path:
    path = Path(db_path or DEFAULT_DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS validation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_data TEXT NOT NULL,
            corrected_data TEXT NOT NULL,
            status TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    return path


def save_validation_result(original_data, corrected_data, status, confidence, db_path: Optional[Path] = None) -> int:
    path = init_db(db_path)
    conn = sqlite3.connect(path)
    cursor = conn.execute(
        "INSERT INTO validation_history (original_data, corrected_data, status, confidence, timestamp) VALUES (?, ?, ?, ?, ?)",
        (
            original_data,
            json.dumps(corrected_data),
            status,
            float(confidence),
            datetime.utcnow().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def fetch_validation_history(db_path: Optional[Path] = None, limit: int = 10):
    path = init_db(db_path)
    conn = sqlite3.connect(path)
    rows = conn.execute(
        "SELECT original_data, corrected_data, status, confidence, timestamp FROM validation_history ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [
        {
            "original_data": row[0],
            "corrected_data": json.loads(row[1]),
            "status": row[2],
            "confidence": row[3],
            "timestamp": row[4],
        }
        for row in rows
    ]
