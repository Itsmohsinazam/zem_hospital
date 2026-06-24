"""
patient_db.py — Compatibility shim
===================================
All database operations now delegate to supabase_db.py (cloud PostgreSQL).
This file is kept so existing imports in ZEM_HMS.py, doctor_screen.py, etc.
continue to work without any changes.
"""
from supabase_db import (
    connt_db,
    insert,
    insert_token,
    admit_patient,
    insert_visitor,
    insert_suggestion,
    fetch_pat_data,
    fetch_patient_by_cnic,
    fetch_patient_by_id,
    update_db,
    del_db,
    search_db,
    validate_cnic,
    validate_phone,
    validate_age,
)

__all__ = [
    'connt_db', 'insert', 'insert_token', 'admit_patient',
    'insert_visitor', 'insert_suggestion',
    'fetch_pat_data', 'fetch_patient_by_cnic', 'fetch_patient_by_id',
    'update_db', 'del_db', 'search_db',
    'validate_cnic', 'validate_phone', 'validate_age',
]