"""
supabase_db.py — ZEM HMS Unified Database Module
=================================================
Backend: Supabase (cloud-hosted PostgreSQL)
Driver:  psycopg2-binary

SETUP:
  1. Fill in your credentials in the .env file next to this script.
  2. Run supabase_schema.sql in the Supabase SQL Editor once to create tables.
  3. This module is imported by patient_db.py and adj_db.py so all screens
     work without any changes.

CONNECTION:
  Reads SUPABASE_DB_URL from .env  (or individual fields as fallback).
"""

import os
import re
import sys
import psycopg2
from dotenv import load_dotenv

# ── Load credentials from .env ────────────────────────────────────────────────
load_dotenv()

_DB_URL   = os.getenv('SUPABASE_DB_URL')
_DB_HOST  = os.getenv('SUPABASE_DB_HOST')
_DB_PORT  = os.getenv('SUPABASE_DB_PORT', '5432')
_DB_NAME  = os.getenv('SUPABASE_DB_NAME', 'postgres')
_DB_USER  = os.getenv('SUPABASE_DB_USER')
_DB_PASS  = os.getenv('SUPABASE_DB_PASS')

# Module-level connection & cursor (re-used across calls)
_conn   = None
_cursor = None

# ── Connection ────────────────────────────────────────────────────────────────

def _show_error(title, message):
    """
    QA-15 FIX: Never call messagebox at import time (before Tk root exists).
    Use print to stderr at import time; UI calls can use messagebox safely.
    """
    print(f"[{title}] {message}", file=sys.stderr)


def connt_db():
    """Open a connection to Supabase PostgreSQL and create tables if needed."""
    global _conn, _cursor
    try:
        if _DB_URL and '[YOUR-' not in _DB_URL:
            _conn = psycopg2.connect(_DB_URL, sslmode='require')
        elif _DB_HOST and _DB_USER and _DB_PASS:
            _conn = psycopg2.connect(
                host=_DB_HOST, port=_DB_PORT, dbname=_DB_NAME,
                user=_DB_USER, password=_DB_PASS, sslmode='require'
            )
        else:
            _show_error(
                "Configuration Error",
                "Supabase credentials not found.\n"
                "Open the .env file and paste your SUPABASE_DB_URL."
            )
            return False

        _conn.autocommit = False
        _cursor = _conn.cursor()
        _create_tables()
        return True

    except psycopg2.OperationalError as e:
        _show_error("Connection Failed", f"Could not connect to Supabase:\n{e}")
        return False
    except Exception as e:
        _show_error("Database Error", str(e))
        return False


def show_db_error(title, message):
    """
    Call this AFTER a Tk root exists (i.e., from within a screen function).
    Safe version that uses messagebox when a root window is present.
    """
    try:
        from tkinter import messagebox
        messagebox.showerror(title, message)
    except Exception:
        print(f"[{title}] {message}", file=sys.stderr)


def _create_tables():
    """Create all HMS tables if they do not already exist."""
    statements = [
        """
        CREATE TABLE IF NOT EXISTS pat_data (
            id          SERIAL PRIMARY KEY,
            cnic        VARCHAR(15)  NOT NULL,
            name        VARCHAR(100) NOT NULL,
            phone       VARCHAR(15),
            age         VARCHAR(10),
            city        VARCHAR(50),
            gender      VARCHAR(20),
            medicine    VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS emergency_tokens (
            token_id    SERIAL PRIMARY KEY,
            cnic        VARCHAR(15),
            patient_id  INTEGER REFERENCES pat_data(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS admited_patients (
            ward_id     SERIAL PRIMARY KEY,
            cnic        VARCHAR(15),
            patient_id  INTEGER REFERENCES pat_data(id) ON DELETE CASCADE,
            admitted_at TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS visitors (
            visitor_id      SERIAL PRIMARY KEY,
            visitor_name    VARCHAR(100),
            cnic            VARCHAR(15),
            contact_number  VARCHAR(15),
            patient_id      INTEGER,
            visited_at      TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS suggestions (
            suggestion_id   SERIAL PRIMARY KEY,
            suggestion_text VARCHAR(1000) NOT NULL,
            created_at      TIMESTAMP DEFAULT NOW()
        )
        """
    ]
    for stmt in statements:
        _cursor.execute(stmt)
    _conn.commit()


def _check_conn():
    """Ensure the connection is alive; attempt reconnect once if stale."""
    global _conn, _cursor
    if _conn is None:
        return connt_db()
    try:
        _cursor.execute("SELECT 1")
        return True
    except Exception:
        return connt_db()


# ── Input Validation ──────────────────────────────────────────────────────────

def validate_cnic(cnic: str) -> bool:
    """Pakistani CNIC: 13 digits, optionally formatted as XXXXX-XXXXXXX-X."""
    return bool(re.match(r'^\d{5}-?\d{7}-?\d$', cnic.strip()))


def validate_phone(phone: str) -> bool:
    """Pakistan mobile: 11 digits starting with 03, or international +92..."""
    p = phone.strip().replace(' ', '').replace('-', '')
    return bool(re.match(r'^(03\d{9}|\+92\d{10})$', p))


def validate_age(age: str) -> bool:
    """Age must be a positive integer between 1 and 150."""
    try:
        v = int(age.strip())
        return 0 < v <= 150
    except ValueError:
        return False


# ── Patient CRUD ──────────────────────────────────────────────────────────────

def insert(cnic, name, phone, age, city, gender, medicine) -> int | None:
    """
    Insert a new patient record.
    QA-31 FIX: Returns the new patient's ID (via RETURNING id), or None on failure.
    """
    if not _check_conn():
        return None
    try:
        _cursor.execute(
            """
            INSERT INTO pat_data (cnic, name, phone, age, city, gender, medicine)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (cnic, name, phone, age, city, gender, medicine)
        )
        new_id = _cursor.fetchone()[0]
        _conn.commit()
        return new_id
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to add patient:\n{e}")
        return None


def fetch_pat_data():
    """Return all patient records ordered by id."""
    if not _check_conn():
        return []
    try:
        _cursor.execute("SELECT * FROM pat_data ORDER BY id ASC")
        return _cursor.fetchall()
    except Exception as e:
        show_db_error("Database Error", f"Failed to fetch patients:\n{e}")
        return []


def fetch_patient_by_cnic(cnic):
    """Return the first patient record matching the given CNIC, or None."""
    if not _check_conn():
        return None
    try:
        _cursor.execute("SELECT * FROM pat_data WHERE cnic = %s LIMIT 1", (cnic,))
        return _cursor.fetchone()
    except Exception as e:
        show_db_error("Database Error", f"Failed to fetch patient:\n{e}")
        return None


def fetch_patient_by_id(patient_id):
    """Return a patient record by numeric ID."""
    if not _check_conn():
        return None
    try:
        _cursor.execute("SELECT * FROM pat_data WHERE id = %s", (patient_id,))
        return _cursor.fetchone()
    except Exception as e:
        show_db_error("Database Error", f"Failed to fetch patient:\n{e}")
        return None


def update_db(patient_id, cnic, name, phone, age, city, gender, medicine):
    """Update an existing patient record."""
    if not _check_conn():
        return
    try:
        _cursor.execute(
            """
            UPDATE pat_data
            SET cnic=%s, name=%s, phone=%s, age=%s, city=%s, gender=%s, medicine=%s
            WHERE id=%s
            """,
            (cnic, name, phone, age, city, gender, medicine, patient_id)
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to update patient:\n{e}")


def del_db(patient_id):
    """Delete a patient record by ID."""
    if not _check_conn():
        return
    try:
        _cursor.execute("DELETE FROM pat_data WHERE id = %s", (patient_id,))
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to delete patient:\n{e}")


def search_db(option, value):
    """Search patients by a whitelisted column name."""
    if not _check_conn():
        return []
    column_mapping = {
        "ID":    "id",
        "CNIC":  "cnic",
        "Name":  "name",
        "Phone": "phone",
        "City":  "city",
    }
    column = column_mapping.get(option)
    if not column:
        show_db_error("Error", f"Invalid search option: {option}")
        return []
    try:
        _cursor.execute(f"SELECT * FROM pat_data WHERE {column} = %s", (value,))
        return _cursor.fetchall()
    except Exception as e:
        show_db_error("Database Error", f"Search failed:\n{e}")
        return []


# ── Token & Admission Operations ──────────────────────────────────────────────

def insert_token(cnic, patient_id):
    """Record an emergency token for a patient."""
    if not _check_conn():
        return
    try:
        _cursor.execute(
            "INSERT INTO emergency_tokens (cnic, patient_id) VALUES (%s, %s)",
            (cnic, patient_id)
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to save token:\n{e}")


def admit_patient(cnic, patient_id):
    """Record a patient ward admission."""
    if not _check_conn():
        return
    try:
        _cursor.execute(
            "INSERT INTO admited_patients (cnic, patient_id) VALUES (%s, %s)",
            (cnic, patient_id)
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to admit patient:\n{e}")


# ── Visitor & Suggestion Operations ───────────────────────────────────────────

def insert_visitor(visitor_name, cnic, contact, patient_id):
    """Save a visitor record."""
    if not _check_conn():
        return
    try:
        pid = int(patient_id) if str(patient_id).strip().isdigit() else None
        _cursor.execute(
            """
            INSERT INTO visitors (visitor_name, cnic, contact_number, patient_id)
            VALUES (%s, %s, %s, %s)
            """,
            (visitor_name, cnic, contact, pid)
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to save visitor:\n{e}")


def insert_suggestion(text):
    """Save a suggestion to the database."""
    if not _check_conn():
        return
    try:
        _cursor.execute(
            "INSERT INTO suggestions (suggestion_text) VALUES (%s)",
            (text,)
        )
        _conn.commit()
    except Exception as e:
        _conn.rollback()
        show_db_error("Database Error", f"Failed to save suggestion:\n{e}")


# ── Module Init ───────────────────────────────────────────────────────────────

# QA-15 FIX: connt_db() uses print-to-stderr on failure, NOT messagebox,
# so it is safe to call at import time before any Tk root exists.
connt_db()


# ── Self-test when run directly ───────────────────────────────────────────────
if __name__ == '__main__':
    if _conn:
        print("✅  Connected to Supabase PostgreSQL successfully!")
        print(f"    Server version: {_conn.server_version}")
        rows = fetch_pat_data()
        print(f"    Patients in database: {len(rows)}")
        print("\nAll tables created/verified. Ready to use.")
    else:
        print("❌  Connection failed. Check your .env file.")
