"""
db.py

SQLite persistence for the Life Metrics Simulator.

This module stores every simulation run and every check-in made during
that run so that metric history survives across sessions, instead of
living only in the Flask session cookie. It uses the standard library
sqlite3 module directly (no ORM, no extra dependency) and opens a short
lived connection per call, which is appropriate for this app's simple,
low-concurrency development server usage.
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# Path to the SQLite database file, stored alongside the other source files.
DB_PATH = os.path.join(os.path.dirname(__file__), "life_metrics.db")


def _get_connection() -> sqlite3.Connection:
    """Open a new connection to the Life Metrics database."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """
    Create the runs and check_ins tables if they do not already exist.

    Returns:
        None
    """
    conn = _get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode TEXT NOT NULL,
                custom_metric_names TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS check_ins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                day INTEGER NOT NULL,
                moment_index INTEGER NOT NULL,
                time_label TEXT NOT NULL,
                action_id TEXT NOT NULL,
                action_label TEXT NOT NULL,
                note TEXT,
                metrics_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def create_run(mode: str, custom_metric_names: Optional[List[str]]) -> int:
    """
    Insert a new run row and return its generated id.

    Args:
        mode (str): Simulation mode ("student", "professional", or "custom").
        custom_metric_names (List[str] | None): Cleaned custom metric names
            for custom-mode runs, or None for built-in modes.

    Returns:
        int: The newly created run's id.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO runs (mode, custom_metric_names, created_at) "
            "VALUES (?, ?, ?)",
            (
                mode,
                json.dumps(custom_metric_names) if custom_metric_names else None,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def insert_check_in(run_id: int, action_id: str, entry: Dict[str, Any]) -> None:
    """
    Persist one check-in log entry for a run.

    Args:
        run_id (int): The id of the run this check-in belongs to.
        action_id (str): Identifier of the action the user selected.
        entry (Dict[str, Any]): A log entry dict as produced by
            simulation.log_check_in, containing "day", "moment",
            "time_label", "action_label", "snapshot", and "note".

    Returns:
        None
    """
    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO check_ins (
                run_id, day, moment_index, time_label,
                action_id, action_label, note, metrics_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                entry["day"],
                entry["moment"],
                entry["time_label"],
                action_id,
                entry.get("action_label", ""),
                entry.get("note", ""),
                json.dumps(entry["snapshot"]),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_check_ins_for_run(run_id: int) -> List[Dict[str, Any]]:
    """
    Fetch all check-ins recorded for a run, in the order they were logged.

    Args:
        run_id (int): The id of the run to fetch check-ins for.

    Returns:
        List[Dict[str, Any]]: One dict per check-in with keys "day",
        "moment_index", "time_label", "action_label", "note", and
        "metrics" (the decoded metric snapshot dict).
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            """
            SELECT day, moment_index, time_label, action_label, note, metrics_json
            FROM check_ins
            WHERE run_id = ?
            ORDER BY id ASC
            """,
            (run_id,),
        ).fetchall()
    finally:
        conn.close()

    return [
        {
            "day": day,
            "moment_index": moment_index,
            "time_label": time_label,
            "action_label": action_label,
            "note": note,
            "metrics": json.loads(metrics_json),
        }
        for day, moment_index, time_label, action_label, note, metrics_json in rows
    ]
