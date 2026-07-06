"""
Database models and operations for the validation system
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import json

DB_PATH = Path(__file__).parent.parent / "database" / "validation.db"
DB_PATH.parent.mkdir(exist_ok=True)

SQLITE_TIMEOUT_SECONDS = 30


def get_connection():
    """Create a SQLite connection tuned for concurrent web requests."""
    conn = sqlite3.connect(DB_PATH, timeout=SQLITE_TIMEOUT_SECONDS)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def ensure_validation_history_schema(cursor):
    """Upgrade older validation_history tables in place."""
    cursor.execute("PRAGMA table_info(validation_history)")
    columns = {row[1] for row in cursor.fetchall()}

    if "raw_input" not in columns:
        cursor.execute(
            "ALTER TABLE validation_history ADD COLUMN raw_input TEXT DEFAULT ''"
        )
        if "original_data" in columns:
            cursor.execute(
                "UPDATE validation_history SET raw_input = COALESCE(raw_input, original_data, '')"
            )

    if "validation_errors" not in columns:
        cursor.execute(
            "ALTER TABLE validation_history ADD COLUMN validation_errors TEXT DEFAULT '{}'"
        )

    if "confidence_scores" not in columns:
        cursor.execute(
            "ALTER TABLE validation_history ADD COLUMN confidence_scores TEXT DEFAULT '{}'"
        )

    if "final_report" not in columns:
        cursor.execute(
            "ALTER TABLE validation_history ADD COLUMN final_report TEXT DEFAULT '{}'"
        )

    if "created_at" not in columns:
        cursor.execute(
            "ALTER TABLE validation_history ADD COLUMN created_at TIMESTAMP"
        )
        cursor.execute(
            "UPDATE validation_history SET created_at = COALESCE(created_at, CURRENT_TIMESTAMP)"
        )


def init_database():
    """Initialize the SQLite database with schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create validation history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS validation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_input TEXT NOT NULL,
            corrected_data TEXT NOT NULL,
            validation_errors TEXT NOT NULL,
            confidence_scores TEXT NOT NULL,
            final_report TEXT NOT NULL,
            status TEXT DEFAULT 'completed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    ensure_validation_history_schema(cursor)
    
    # Create user feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            user_correction TEXT,
            approved BOOLEAN DEFAULT 0,
            feedback_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (validation_id) REFERENCES validation_history(id)
        )
    ''')
    
    # Create escalation table for uncertain fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escalations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            validation_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            original_value TEXT,
            corrected_value TEXT,
            confidence_score REAL,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (validation_id) REFERENCES validation_history(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def save_validation_result(raw_input: str, corrected_data: Dict, validation_errors: Dict, 
                          confidence_scores: Dict, final_report: Dict) -> int:
    """Save validation result to database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(validation_history)")
    columns = {row[1] for row in cursor.fetchall()}

    insert_columns = []
    insert_values = []

    if "original_data" in columns:
        insert_columns.append("original_data")
        insert_values.append(raw_input)

    if "raw_input" in columns:
        insert_columns.append("raw_input")
        insert_values.append(raw_input)

    if "status" in columns:
        insert_columns.append("status")
        insert_values.append("completed")

    if "confidence" in columns:
        insert_columns.append("confidence")
        insert_values.append(final_report.get("average_confidence", 0.0))

    if "timestamp" in columns:
        insert_columns.append("timestamp")
        insert_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if "created_at" in columns:
        insert_columns.append("created_at")
        insert_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    insert_columns.extend([
        "corrected_data",
        "validation_errors",
        "confidence_scores",
        "final_report",
    ])
    insert_values.extend([
        json.dumps(corrected_data),
        json.dumps(validation_errors),
        json.dumps(confidence_scores),
        json.dumps(final_report),
    ])

    placeholders = ", ".join(["?"] * len(insert_values))
    column_sql = ", ".join(insert_columns)
    
    cursor.execute(
        f'''
        INSERT INTO validation_history
        ({column_sql})
        VALUES ({placeholders})
        ''',
        tuple(insert_values)
    )
    
    conn.commit()
    validation_id = cursor.lastrowid
    conn.close()
    
    return validation_id


def save_escalation(validation_id: int, field_name: str, original_value: str, 
                   corrected_value: str, confidence_score: float, reason: str):
    """Save an escalated field for human review"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO escalations 
        (validation_id, field_name, original_value, corrected_value, confidence_score, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (validation_id, field_name, original_value, corrected_value, confidence_score, reason))
    
    conn.commit()
    conn.close()


def fetch_validation_history(limit: int = 10) -> List[Dict]:
    """Fetch recent validation history"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(validation_history)")
    columns = {row[1] for row in cursor.fetchall()}

    raw_input_expr = None
    if "raw_input" in columns and "original_data" in columns:
        raw_input_expr = "COALESCE(NULLIF(raw_input, ''), original_data)"
    elif "raw_input" in columns:
        raw_input_expr = "raw_input"
    else:
        raw_input_expr = "original_data"
    validation_errors_column = "validation_errors" if "validation_errors" in columns else None
    confidence_scores_column = "confidence_scores" if "confidence_scores" in columns else None
    created_at_column = "created_at" if "created_at" in columns else ("timestamp" if "timestamp" in columns else None)

    select_columns = ["id", f"{raw_input_expr} AS raw_input", "corrected_data"]
    if validation_errors_column:
        select_columns.append(validation_errors_column)
    else:
        select_columns.append("'{}' AS validation_errors")
    if confidence_scores_column:
        select_columns.append(confidence_scores_column)
    else:
        select_columns.append("'{}' AS confidence_scores")
    if created_at_column:
        select_columns.append(created_at_column)
    else:
        select_columns.append("CURRENT_TIMESTAMP AS created_at")
    
    cursor.execute('''
        SELECT {} 
        FROM validation_history
        ORDER BY {} DESC
        LIMIT ?
    '''.format(
        ", ".join(select_columns),
        created_at_column or "id"
    ), (limit,))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'raw_input': row[1],
            'corrected_data': json.loads(row[2]),
            'validation_errors': json.loads(row[3]),
            'confidence_scores': json.loads(row[4]),
            'created_at': row[5]
        })
    
    conn.close()
    return results


def fetch_escalations(validation_id: int = None) -> List[Dict]:
    """Fetch escalated fields pending human review"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if validation_id:
        cursor.execute('''
            SELECT id, validation_id, field_name, original_value, corrected_value, 
                   confidence_score, reason, status, created_at
            FROM escalations
            WHERE validation_id = ?
            ORDER BY created_at DESC
        ''', (validation_id,))
    else:
        cursor.execute('''
            SELECT id, validation_id, field_name, original_value, corrected_value, 
                   confidence_score, reason, status, created_at
            FROM escalations
            WHERE status = 'pending'
            ORDER BY created_at DESC
        ''')
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'validation_id': row[1],
            'field_name': row[2],
            'original_value': row[3],
            'corrected_value': row[4],
            'confidence_score': row[5],
            'reason': row[6],
            'status': row[7],
            'created_at': row[8]
        })
    
    conn.close()
    return results


def resolve_escalation(escalation_id: int, approved: bool, user_correction: str = None):
    """Resolve an escalation with user feedback"""
    conn = get_connection()
    cursor = conn.cursor()
    
    status = 'approved' if approved else 'rejected'
    cursor.execute('''
        UPDATE escalations
        SET status = ?, resolved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (status, escalation_id))
    
    # Also save feedback
    escalation = conn.execute('SELECT validation_id, field_name FROM escalations WHERE id = ?', 
                             (escalation_id,)).fetchone()
    if escalation:
        cursor.execute('''
            INSERT INTO user_feedback (validation_id, field_name, user_correction, approved)
            VALUES (?, ?, ?, ?)
        ''', (escalation[0], escalation[1], user_correction, approved))
    
    conn.commit()
    conn.close()


# Initialize database on import
init_database()
