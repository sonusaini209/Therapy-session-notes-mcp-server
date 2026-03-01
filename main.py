import os
import sqlite3
import json
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("therapist-session-notes")


DB_PATH = os.path.join(os.path.dirname(__file__), "sessions.db")

# ── Database Setup ────────────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            date TEXT,
            notes TEXT,
            themes TEXT,
            sentiment_score REAL
        )
    """)
    conn.commit()
    return conn


def insert_session(patient_name, date, notes, themes, sentiment_score):
    conn = get_connection()
    conn.execute("""
        INSERT INTO sessions (patient_name, date, notes, themes, sentiment_score)
        VALUES (?, ?, ?, ?, ?)
    """, (patient_name, date, notes, json.dumps(themes), sentiment_score))
    conn.commit()
    conn.close()


def fetch_sessions(patient_name, limit=10):
    conn = get_connection()
    rows = conn.execute("""
        SELECT date, notes, themes, sentiment_score
        FROM sessions
        WHERE patient_name = ?
        ORDER BY date DESC
        LIMIT ?
    """, (patient_name, limit)).fetchall()
    conn.close()
    return [
        {
            "date": r[0],
            "notes": r[1],
            "themes": json.loads(r[2]),
            "sentiment_score": r[3]
        }
        for r in rows
    ]

def delete_patient(patient_name: str):
    conn = get_connection()
    conn.execute("DELETE FROM sessions WHERE patient_name = ?", (patient_name,))
    conn.commit()
    conn.close()

# ── Tools ─────────────────────────────────────────────────────────────

@mcp.tool()
def save_session(
    patient_name: str,
    notes: str,
    themes: list[str],
    sentiment_score: float,
    date: str = None
) -> str:
    """
    Save a therapy session to the database.
    themes: key topics from the session e.g. ["grief", "sleep", "work stress"]
    sentiment_score: float from -1.0 (crisis) to 1.0 (thriving)
    """
    session_date = date or datetime.today().strftime("%Y-%m-%d")
    insert_session(patient_name, session_date, notes, themes, sentiment_score)
    return f"Session saved for {patient_name} on {session_date}"


@mcp.tool()
def get_recent_sessions(patient_name: str, limit: int = 5) -> list:
    """
    Retrieve the most recent sessions for a patient by name.
    """
    return fetch_sessions(patient_name, limit) or []


@mcp.tool()
def get_sentiment_trend(patient_name: str) -> dict:
    """
    Returns sentiment scores over time for a patient so the LLM
    can detect if the patient is improving, stable, or declining.
    """
    sessions = fetch_sessions(patient_name, limit=10)
    if not sessions:
        return {"error": f"No sessions found for {patient_name}"}

    return {
        "patient_name": patient_name,
        "scores": [
            {"date": s["date"], "sentiment_score": s["sentiment_score"]}
            for s in sessions
        ]
    }


@mcp.tool()
def get_all_themes(patient_name: str) -> dict:
    """
    Returns all themes across every session for a patient so the LLM
    can identify recurring patterns and resolved issues.
    """
    sessions = fetch_sessions(patient_name, limit=50)
    if not sessions:
        return {"error": f"No sessions found for {patient_name}"}

    return {
        "patient_name": patient_name,
        "theme_history": [
            {"date": s["date"], "themes": s["themes"]}
            for s in sessions
        ]
    }


@mcp.tool()
def get_session_by_date(patient_name: str, date: str) -> dict:
    """
    Retrieve a specific session for a patient by date (YYYY-MM-DD).
    """
    sessions = fetch_sessions(patient_name, limit=100)
    match = next((s for s in sessions if s["date"] == date), None)
    if not match:
        return {"error": f"No session found for {patient_name} on {date}"}
    return match


@mcp.tool()
def delete_patient_data(patient_name: str) -> str:
    """
    Delete all session data for a patient by name.
    """
    delete_patient(patient_name)
    return f"All session data deleted for {patient_name}"


if __name__ == "__main__":
    mcp.run()
