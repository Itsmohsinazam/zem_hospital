"""
migrate_to_supabase.py — One-time MySQL → Supabase Data Migration
=================================================================
Run this script ONCE after setting up your Supabase project to copy
all existing patient records from your local MySQL database to Supabase.

Usage:
    python migrate_to_supabase.py

Requirements:
    pip install pymysql psycopg2-binary python-dotenv
    .env file must have SUPABASE_DB_URL filled in.
"""

import os
import sys
import pymysql
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# ── MySQL source (local) ──────────────────────────────────────────────────────
MYSQL_HOST = os.getenv('HMS_DB_HOST', 'localhost')
MYSQL_USER = os.getenv('HMS_DB_USER', 'root')
MYSQL_PASS = os.getenv('HMS_DB_PASS', '1234')
MYSQL_DB   = 'hms_data'     # primary database used by ZEM_HMS

# ── Supabase destination ──────────────────────────────────────────────────────
SUPABASE_URL = os.getenv('SUPABASE_DB_URL', '')


def connect_mysql():
    print("Connecting to local MySQL ...")
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASS, database=MYSQL_DB
        )
        print("  ✅ MySQL connected.")
        return conn
    except Exception as e:
        print(f"  ❌ MySQL connection failed: {e}")
        sys.exit(1)


def connect_supabase():
    print("Connecting to Supabase PostgreSQL ...")
    if not SUPABASE_URL or '[YOUR-' in SUPABASE_URL:
        print("  ❌ SUPABASE_DB_URL is not set in the .env file.")
        sys.exit(1)
    try:
        conn = psycopg2.connect(SUPABASE_URL, sslmode='require')
        conn.autocommit = False
        print("  ✅ Supabase connected.")
        return conn
    except Exception as e:
        print(f"  ❌ Supabase connection failed: {e}")
        sys.exit(1)


def migrate_patients(mysql_conn, pg_conn):
    """Copy pat_data rows from MySQL to Supabase, skipping duplicates."""
    cursor_m = mysql_conn.cursor()
    cursor_p = pg_conn.cursor()

    cursor_m.execute("SELECT * FROM pat_data ORDER BY Id ASC")
    rows = cursor_m.fetchall()
    print(f"\nMigrating {len(rows)} patient record(s) ...")

    inserted = skipped = errors = 0
    for row in rows:
        # MySQL: (Id, CNIC, Name, Phone, Age, City, Gender, Medicine)
        _, cnic, name, phone, age, city, gender, medicine = row
        try:
            # Check if already exists
            cursor_p.execute("SELECT 1 FROM pat_data WHERE cnic=%s AND name=%s", (cnic, name))
            if cursor_p.fetchone():
                skipped += 1
                continue
            cursor_p.execute(
                """
                INSERT INTO pat_data (cnic, name, phone, age, city, gender, medicine)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (cnic, name, phone, age, city, gender, medicine)
            )
            inserted += 1
        except Exception as e:
            print(f"    ⚠️  Row error (CNIC {cnic}): {e}")
            errors += 1

    pg_conn.commit()
    print(f"  ✅ Inserted: {inserted}  |  Skipped (already exist): {skipped}  |  Errors: {errors}")


def migrate_secondary_db(pg_conn):
    """Attempt to also migrate from the secondary 'patients_data' MySQL database if it exists."""
    print("\nChecking secondary MySQL database 'patients_data' ...")
    try:
        alt_conn = pymysql.connect(
            host=MYSQL_HOST, user=MYSQL_USER,
            password=MYSQL_PASS, database='patients_data'
        )
        cursor_m = alt_conn.cursor()
        cursor_p = pg_conn.cursor()
        cursor_m.execute("SELECT * FROM data ORDER BY Id ASC")
        rows = cursor_m.fetchall()
        print(f"  Found {len(rows)} record(s) in 'patients_data'.")

        inserted = skipped = 0
        for row in rows:
            id_, name, phone, age, gender, medicine = row
            # No CNIC or City in the old hms_db schema — use id as CNIC placeholder
            try:
                cursor_p.execute("SELECT 1 FROM pat_data WHERE cnic=%s", (str(id_),))
                if cursor_p.fetchone():
                    skipped += 1
                    continue
                cursor_p.execute(
                    """
                    INSERT INTO pat_data (cnic, name, phone, age, city, gender, medicine)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (str(id_), name, phone, age, '', gender, medicine)
                )
                inserted += 1
            except Exception as e:
                print(f"    ⚠️  Row error: {e}")

        pg_conn.commit()
        print(f"  ✅ Secondary DB — Inserted: {inserted}  |  Skipped: {skipped}")
        alt_conn.close()
    except pymysql.err.OperationalError:
        print("  ℹ️  'patients_data' database not found — skipping.")


def main():
    print("=" * 60)
    print("  ZEM HMS — MySQL → Supabase Migration Tool")
    print("=" * 60)

    mysql_conn = connect_mysql()
    pg_conn    = connect_supabase()

    migrate_patients(mysql_conn, pg_conn)
    migrate_secondary_db(pg_conn)

    mysql_conn.close()
    pg_conn.close()

    print("\n" + "=" * 60)
    print("  Migration complete! Open your Supabase Table Editor")
    print("  to verify the data at: https://app.supabase.com")
    print("=" * 60)


if __name__ == '__main__':
    main()
