"""
models.py

SQLAlchemy models and persistence helpers for the Life Metrics Simulator.

Replaces the earlier raw sqlite3 module (db.py) so that data lives in
Postgres in production (via DATABASE_URL) and falls back to a local
SQLite file in development, with every run and check-in now tied to
the user who created it.
"""

import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """A registered Life Metrics account."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password: str) -> None:
        """Hash and store a plaintext password (never stored as-is)."""
        # pbkdf2:sha256 is used explicitly rather than Werkzeug's newer
        # scrypt default, since scrypt requires an OpenSSL build with
        # scrypt support that isn't guaranteed on every deployment target.
        self.password_hash = generate_password_hash(
            password, method="pbkdf2:sha256"
        )

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)


class Run(db.Model):
    """One simulation run (Student, Professional, or Custom) for a user."""

    __tablename__ = "runs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mode = db.Column(db.String(32), nullable=False)
    custom_metric_names = db.Column(db.Text, nullable=True)
    custom_actions = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    check_ins = db.relationship(
        "CheckIn", backref="run", order_by="CheckIn.id", lazy="select"
    )


class CheckIn(db.Model):
    """One logged check-in within a run."""

    __tablename__ = "check_ins"

    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("runs.id"), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    moment_index = db.Column(db.Integer, nullable=False)
    time_label = db.Column(db.String(32), nullable=False)
    action_id = db.Column(db.String(64), nullable=False)
    action_label = db.Column(db.String(255), nullable=False)
    note = db.Column(db.Text, nullable=True)
    metrics_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )


def create_run(
    user_id: int,
    mode: str,
    custom_metric_names: Optional[List[str]],
    custom_actions: Optional[List[Dict[str, str]]] = None,
) -> int:
    """
    Insert a new run row owned by the given user and return its id.

    Args:
        user_id (int): The owning user's id.
        mode (str): "student", "professional", or "custom".
        custom_metric_names (List[str] | None): Cleaned custom metric
            names for custom-mode runs, or None for built-in modes.
        custom_actions (List[Dict[str, str]] | None): The 3 custom
            action dicts ({"id", "label", "description"}) for custom-mode
            runs, or None for built-in modes. Persisted so a custom run
            can be fully reconstructed later (see app.py's dashboard
            "Continue" route).

    Returns:
        int: The newly created run's id.
    """
    run = Run(
        user_id=user_id,
        mode=mode,
        custom_metric_names=json.dumps(custom_metric_names)
        if custom_metric_names
        else None,
        custom_actions=json.dumps(custom_actions) if custom_actions else None,
    )
    db.session.add(run)
    db.session.commit()
    return run.id


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
    check_in = CheckIn(
        run_id=run_id,
        day=entry["day"],
        moment_index=entry["moment"],
        time_label=entry["time_label"],
        action_id=action_id,
        action_label=entry.get("action_label", ""),
        note=entry.get("note", ""),
        metrics_json=json.dumps(entry["snapshot"]),
    )
    db.session.add(check_in)
    db.session.commit()


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
    rows = (
        CheckIn.query.filter_by(run_id=run_id).order_by(CheckIn.id.asc()).all()
    )
    return [
        {
            "day": row.day,
            "moment_index": row.moment_index,
            "time_label": row.time_label,
            "action_label": row.action_label,
            "note": row.note,
            "metrics": json.loads(row.metrics_json),
        }
        for row in rows
    ]


def get_runs_for_user(user_id: int) -> List[Run]:
    """
    Fetch every run belonging to a user, most recently created first.

    Args:
        user_id (int): The id of the user whose runs to fetch.

    Returns:
        List[Run]: Run model instances, newest first.
    """
    return (
        Run.query.filter_by(user_id=user_id).order_by(Run.created_at.desc()).all()
    )


def get_owned_run(run_id: int, user_id: int) -> Optional[Run]:
    """
    Fetch a single run only if it belongs to the given user.

    Args:
        run_id (int): The id of the run to fetch.
        user_id (int): The id of the user who must own it.

    Returns:
        Run | None: The Run instance if found and owned by user_id,
        otherwise None.
    """
    return Run.query.filter_by(id=run_id, user_id=user_id).first()
